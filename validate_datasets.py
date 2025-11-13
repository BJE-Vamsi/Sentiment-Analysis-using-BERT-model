#!/usr/bin/env python3
"""
Validation script for sentiment analysis datasets.
Tests CSV formatting, data integrity, and pandas compatibility.
"""

import pandas as pd
import csv


def validate_csv_file(filename: str, expected_label: int = None):
    """Validate a CSV file for proper formatting and content."""
    print(f"\n{'='*60}")
    print(f"Validating: {filename}")
    print(f"{'='*60}")
    
    # Test 1: Check if file can be read with pandas
    try:
        df = pd.read_csv(filename)
        print(f"✓ Successfully loaded with pandas")
    except Exception as e:
        print(f"✗ Failed to load with pandas: {e}")
        return False
    
    # Test 2: Check headers
    expected_headers = ['Reviews', 'Labels']
    if list(df.columns) == expected_headers:
        print(f"✓ Headers are correct: {expected_headers}")
    else:
        print(f"✗ Headers are incorrect. Expected {expected_headers}, got {list(df.columns)}")
        return False
    
    # Test 3: Check row count
    row_count = len(df)
    print(f"✓ Total rows: {row_count:,}")
    
    # Test 4: Check for null values
    null_count = df.isnull().sum().sum()
    if null_count == 0:
        print(f"✓ No null values found")
    else:
        print(f"✗ Found {null_count} null values")
        return False
    
    # Test 5: Check data types
    if df['Reviews'].dtype == 'object' and pd.api.types.is_integer_dtype(df['Labels']):
        print(f"✓ Data types are correct (Reviews: string, Labels: integer)")
    else:
        print(f"✗ Data types are incorrect")
        return False
    
    # Test 6: Check label distribution
    label_counts = df['Labels'].value_counts().sort_index()
    print(f"\n  Label distribution:")
    for label, count in label_counts.items():
        percentage = (count / row_count) * 100
        print(f"    Label {label}: {count:,} ({percentage:.1f}%)")
    
    # Test 7: Check for expected label if specified
    if expected_label is not None:
        unique_labels = df['Labels'].unique()
        if len(unique_labels) == 1 and unique_labels[0] == expected_label:
            print(f"✓ Contains only expected label: {expected_label}")
        else:
            print(f"✗ Expected only label {expected_label}, but found: {unique_labels}")
            return False
    
    # Test 8: Check for duplicate reviews
    duplicate_count = df['Reviews'].duplicated().sum()
    if duplicate_count == 0:
        print(f"✓ No duplicate reviews found")
    else:
        print(f"⚠ Found {duplicate_count} duplicate reviews ({(duplicate_count/row_count)*100:.2f}%)")
    
    # Test 9: Sample some reviews
    print(f"\n  Sample reviews:")
    samples = df.sample(min(3, len(df)))
    for idx, row in samples.iterrows():
        review_preview = row['Reviews'][:80] + "..." if len(row['Reviews']) > 80 else row['Reviews']
        print(f"    [{row['Labels']}] {review_preview}")
    
    # Test 10: Check CSV escaping by reading raw file
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            sample_row = next(reader)
            print(f"\n✓ CSV escaping is properly handled")
    except Exception as e:
        print(f"✗ CSV reading error: {e}")
        return False
    
    return True


def main():
    print("\n" + "="*60)
    print("SENTIMENT DATASET VALIDATION")
    print("="*60)
    
    # Validate individual datasets
    results = {
        'git_pos.csv': validate_csv_file('git_pos.csv', expected_label=2),
        'git_neg.csv': validate_csv_file('git_neg.csv', expected_label=0),
        'git_neu.csv': validate_csv_file('git_neu.csv', expected_label=1),
        'sentiment_PNO.csv': validate_csv_file('sentiment_PNO.csv'),
    }
    
    # Summary
    print(f"\n{'='*60}")
    print("VALIDATION SUMMARY")
    print(f"{'='*60}")
    
    for filename, passed in results.items():
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{filename}: {status}")
    
    all_passed = all(results.values())
    
    if all_passed:
        print(f"\n✓ ALL DATASETS VALIDATED SUCCESSFULLY!")
        print(f"\nDatasets are ready for:")
        print(f"  - Training with BERT models")
        print(f"  - Import into pandas/numpy")
        print(f"  - Use in machine learning pipelines")
        return 0
    else:
        print(f"\n✗ SOME VALIDATIONS FAILED")
        return 1


if __name__ == "__main__":
    exit(main())
