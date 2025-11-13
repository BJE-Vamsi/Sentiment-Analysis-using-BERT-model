#!/usr/bin/env python3
"""
Merge sentiment datasets from multiple branches into a single deduplicated CSV.

This script:
1. Fetches CSV files from specified git branches
2. Parses and validates each CSV (Reviews,Labels header)
3. Removes exact duplicates across all files
4. Filters out rows with missing/invalid data
5. Merges all unique rows into sentiment_final.csv
6. Validates output and generates summary report
"""

import csv
import hashlib
import subprocess
import sys
from collections import defaultdict
from pathlib import Path


# Configuration: branches and their CSV files
SOURCES = [
    ("copilot/create-sentiment-dataset-csv", "sentiment_dataset.csv"),
    ("copilot/create-sentiment-dataset-csv-again", "sentiment_dataset.csv"),
    ("copilot/add-large-csv-file", "git_sent.csv"),
    ("copilot/create-large-csv-file", "git_sarcasm.csv"),
]

HEADER = "Reviews,Labels"
OUTPUT_FILE = "sentiment_final.csv"
VALID_LABELS = {0, 1, 2, 3, 4, 5}


def get_file_from_branch(branch: str, filepath: str) -> str:
    """Fetch file content from a git branch."""
    try:
        result = subprocess.run(
            ["git", "show", f"{branch}:{filepath}"],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error fetching {filepath} from {branch}: {e}", file=sys.stderr)
        return ""


def parse_csv_content(content: str, source_name: str) -> tuple[list[tuple[str, int]], dict]:
    """
    Parse CSV content and return valid rows and statistics.
    
    Returns:
        Tuple of (valid_rows, stats) where:
        - valid_rows: list of (review, label) tuples
        - stats: dict with parsing statistics
    """
    stats = {
        "total_rows": 0,
        "valid_rows": 0,
        "invalid_label": 0,
        "empty_review": 0,
        "parse_error": 0,
    }
    
    valid_rows = []
    lines = content.strip().split('\n')
    
    if not lines:
        print(f"Warning: {source_name} is empty", file=sys.stderr)
        return valid_rows, stats
    
    # Check header
    if lines[0].strip() != HEADER:
        print(f"Warning: {source_name} has incorrect header: {lines[0][:50]}", file=sys.stderr)
        return valid_rows, stats
    
    # Parse data rows
    reader = csv.reader(lines[1:])
    for row_num, row in enumerate(reader, start=2):
        stats["total_rows"] += 1
        
        try:
            if len(row) != 2:
                stats["parse_error"] += 1
                continue
            
            review, label_str = row
            
            # Validate review
            if not review or not review.strip():
                stats["empty_review"] += 1
                continue
            
            # Validate label
            try:
                label = int(label_str)
                if label not in VALID_LABELS:
                    stats["invalid_label"] += 1
                    continue
            except ValueError:
                stats["invalid_label"] += 1
                continue
            
            valid_rows.append((review, label))
            stats["valid_rows"] += 1
            
        except Exception as e:
            stats["parse_error"] += 1
            print(f"Error parsing row {row_num} in {source_name}: {e}", file=sys.stderr)
    
    return valid_rows, stats


def get_row_hash(review: str, label: int) -> str:
    """Generate hash for a row to detect duplicates."""
    # Use the exact CSV representation for deduplication
    row_str = f'"{review}",{label}'
    return hashlib.sha256(row_str.encode('utf-8')).hexdigest()


def merge_datasets() -> dict:
    """
    Merge all datasets and return summary statistics.
    
    Returns:
        Dictionary with merge statistics and results
    """
    all_rows = []
    source_stats = {}
    seen_hashes = set()
    duplicate_count = 0
    
    print("=" * 70)
    print("Sentiment Dataset Merge Process")
    print("=" * 70)
    print()
    
    # Collect rows from all sources
    for branch, filepath in SOURCES:
        source_name = f"{branch}:{filepath}"
        print(f"Processing {source_name}...")
        
        content = get_file_from_branch(branch, filepath)
        if not content:
            print(f"  ⚠ Skipped (could not fetch)\n")
            continue
        
        rows, stats = parse_csv_content(content, source_name)
        source_stats[source_name] = stats
        
        print(f"  Total rows read: {stats['total_rows']}")
        print(f"  Valid rows: {stats['valid_rows']}")
        if stats['invalid_label'] > 0:
            print(f"  Invalid labels: {stats['invalid_label']}")
        if stats['empty_review'] > 0:
            print(f"  Empty reviews: {stats['empty_review']}")
        if stats['parse_error'] > 0:
            print(f"  Parse errors: {stats['parse_error']}")
        
        # Track duplicates
        for review, label in rows:
            row_hash = get_row_hash(review, label)
            if row_hash not in seen_hashes:
                seen_hashes.add(row_hash)
                all_rows.append((review, label))
            else:
                duplicate_count += 1
        
        print()
    
    # Sort rows by label, then by review for consistent output
    all_rows.sort(key=lambda x: (x[1], x[0]))
    
    # Calculate label distribution
    label_dist = defaultdict(int)
    for _, label in all_rows:
        label_dist[label] += 1
    
    # Write output file
    repo_root = Path(__file__).parent.parent
    output_path = repo_root / OUTPUT_FILE
    
    print(f"Writing merged dataset to {OUTPUT_FILE}...")
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow(['Reviews', 'Labels'])
        for review, label in all_rows:
            writer.writerow([review, label])
    
    print(f"✓ Successfully wrote {len(all_rows)} rows\n")
    
    # Validate output
    print("Validating output file...")
    validate_output(output_path)
    print()
    
    # Summary statistics
    total_valid = sum(stats['valid_rows'] for stats in source_stats.values())
    total_invalid = sum(
        stats['invalid_label'] + stats['empty_review'] + stats['parse_error']
        for stats in source_stats.values()
    )
    
    summary = {
        "source_stats": source_stats,
        "total_valid_rows": total_valid,
        "total_invalid_rows": total_invalid,
        "duplicate_rows": duplicate_count,
        "final_unique_rows": len(all_rows),
        "label_distribution": dict(label_dist),
    }
    
    return summary


def validate_output(filepath: Path):
    """Validate the output CSV file."""
    errors = []
    
    try:
        with open(filepath, 'r', encoding='utf-8', newline='') as f:
            content = f.read()
            lines = content.split('\n')
            
            # Check header
            if not lines or lines[0].strip() != HEADER:
                errors.append(f"Invalid header: expected '{HEADER}'")
            
            # Parse and validate all rows
            reader = csv.reader(lines[1:])
            seen_hashes = set()
            row_count = 0
            
            for row_num, row in enumerate(reader, start=2):
                if not row or (len(row) == 1 and not row[0]):
                    # Empty row at end of file is okay
                    continue
                
                if len(row) != 2:
                    errors.append(f"Row {row_num}: Expected 2 fields, got {len(row)}")
                    continue
                
                review, label_str = row
                
                # Check for empty review
                if not review or not review.strip():
                    errors.append(f"Row {row_num}: Empty review")
                
                # Check label
                try:
                    label = int(label_str)
                    if label not in VALID_LABELS:
                        errors.append(f"Row {row_num}: Invalid label {label} (must be 0-5)")
                except ValueError:
                    errors.append(f"Row {row_num}: Label is not an integer: '{label_str}'")
                    continue
                
                # Check for duplicates
                row_hash = get_row_hash(review, label)
                if row_hash in seen_hashes:
                    errors.append(f"Row {row_num}: Duplicate row detected")
                seen_hashes.add(row_hash)
                
                row_count += 1
            
            if errors:
                print("  ✗ Validation errors found:")
                for error in errors[:10]:  # Show first 10 errors
                    print(f"    - {error}")
                if len(errors) > 10:
                    print(f"    ... and {len(errors) - 10} more errors")
            else:
                print(f"  ✓ Valid: {row_count} rows, no duplicates, all labels in range 0-5")
    
    except Exception as e:
        print(f"  ✗ Validation failed: {e}")


def print_summary(summary: dict):
    """Print summary report."""
    print("=" * 70)
    print("MERGE SUMMARY REPORT")
    print("=" * 70)
    print()
    
    print("Source File Statistics:")
    print("-" * 70)
    for source_name, stats in summary["source_stats"].items():
        print(f"{source_name}")
        print(f"  Raw rows: {stats['total_rows']}")
        print(f"  Valid rows: {stats['valid_rows']}")
        invalid = stats['invalid_label'] + stats['empty_review'] + stats['parse_error']
        if invalid > 0:
            print(f"  Invalid/skipped: {invalid}")
        print()
    
    print("Merge Results:")
    print("-" * 70)
    print(f"Total valid rows from all sources: {summary['total_valid_rows']}")
    print(f"Duplicate rows removed: {summary['duplicate_rows']}")
    print(f"Invalid rows removed: {summary['total_invalid_rows']}")
    print(f"Final unique rows in {OUTPUT_FILE}: {summary['final_unique_rows']}")
    print()
    
    print("Label Distribution in Final Dataset:")
    print("-" * 70)
    label_dist = summary["label_distribution"]
    for label in sorted(label_dist.keys()):
        count = label_dist[label]
        percentage = (count / summary['final_unique_rows']) * 100
        print(f"Label {label}: {count:6,} rows ({percentage:5.2f}%)")
    print()
    print("=" * 70)


if __name__ == "__main__":
    try:
        summary = merge_datasets()
        print_summary(summary)
        print("\n✓ Merge completed successfully!")
        print(f"  Output file: {OUTPUT_FILE}")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Merge failed: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)
