#!/usr/bin/env python3
"""
Merge orchestration script for sentiment_PNO.csv
Merges git_pos.csv, git_neg.csv, git_neu.csv into sentiment_PNO.csv
Maintains all rows and verifies uniqueness
"""

import csv
import os
import sys
import hashlib


def normalize_text(text):
    """Normalize text for uniqueness checking"""
    return text.lower().strip().replace('"', '').replace(',', '')


def get_text_hash(text):
    """Get hash of normalized text"""
    normalized = normalize_text(text)
    return hashlib.md5(normalized.encode()).hexdigest()


def load_dataset(filepath):
    """Load a dataset and return reviews with labels"""
    reviews = []
    if not os.path.exists(filepath):
        print(f"Warning: {filepath} not found, skipping...")
        return reviews
    
    print(f"Loading {os.path.basename(filepath)}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if 'Reviews' in row and 'Labels' in row:
                reviews.append((row['Reviews'], row['Labels']))
    
    print(f"  Loaded {len(reviews)} reviews")
    return reviews


def merge_datasets(repo_root):
    """Merge the three datasets into sentiment_PNO.csv"""
    print("="*60)
    print("SENTIMENT PNO DATASET MERGE")
    print("="*60)
    
    # Load all three datasets
    pos_reviews = load_dataset(os.path.join(repo_root, 'git_pos.csv'))
    neg_reviews = load_dataset(os.path.join(repo_root, 'git_neg.csv'))
    neu_reviews = load_dataset(os.path.join(repo_root, 'git_neu.csv'))
    
    if not pos_reviews or not neg_reviews or not neu_reviews:
        print("\nError: One or more source datasets not found or empty!")
        print("Please generate all three datasets first:")
        print("  - python tools/generate_git_pos_dataset.py")
        print("  - python tools/generate_git_neg_dataset.py")
        print("  - python tools/generate_git_neu_dataset.py")
        return False
    
    # Combine all reviews
    all_reviews = pos_reviews + neg_reviews + neu_reviews
    print(f"\nTotal reviews combined: {len(all_reviews)}")
    print(f"  Positive (label=2): {len(pos_reviews)}")
    print(f"  Negative (label=0): {len(neg_reviews)}")
    print(f"  Neutral (label=1): {len(neu_reviews)}")
    
    # Check for duplicates
    print("\nChecking for duplicates...")
    seen_hashes = set()
    duplicates = 0
    
    for review, label in all_reviews:
        review_hash = get_text_hash(review)
        if review_hash in seen_hashes:
            duplicates += 1
        else:
            seen_hashes.add(review_hash)
    
    if duplicates > 0:
        print(f"Warning: Found {duplicates} duplicate reviews!")
    else:
        print("✓ No duplicates found")
    
    # Shuffle for good measure (optional)
    import random
    random.shuffle(all_reviews)
    print("✓ Reviews shuffled")
    
    # Write merged dataset
    output_path = os.path.join(repo_root, 'sentiment_PNO.csv')
    print(f"\nWriting to {output_path}...")
    
    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerow(['Reviews', 'Labels'])
        
        for review, label in all_reviews:
            writer.writerow([review, label])
    
    # Verify written file
    with open(output_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        row_count = sum(1 for _ in reader)
    
    print(f"✓ Successfully wrote {row_count} rows to {output_path}")
    
    # Summary
    print("\n" + "="*60)
    print("MERGE SUMMARY")
    print("="*60)
    print(f"Output file: sentiment_PNO.csv")
    print(f"Total rows: {row_count}")
    print(f"Unique reviews: {len(seen_hashes)}")
    print(f"Duplicates: {duplicates}")
    print(f"Label distribution:")
    print(f"  0 (Negative): {len(neg_reviews)}")
    print(f"  1 (Neutral): {len(neu_reviews)}")
    print(f"  2 (Positive): {len(pos_reviews)}")
    print("="*60)
    
    return True


def main():
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    success = merge_datasets(repo_root)
    
    if success:
        print("\n✓ Merge complete!")
    else:
        print("\n✗ Merge failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
