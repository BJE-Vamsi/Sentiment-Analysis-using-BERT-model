#!/usr/bin/env python3
"""
Example script demonstrating how to load and use the sentiment datasets.
Shows basic data exploration and preparation for BERT training.
"""

import pandas as pd
import random


def demonstrate_dataset_usage():
    """Demonstrate how to load and use the sentiment datasets."""
    
    print("=" * 70)
    print("SENTIMENT DATASET USAGE DEMONSTRATION")
    print("=" * 70)
    
    # Load individual datasets
    print("\n1. Loading Individual Datasets:")
    print("-" * 70)
    
    df_pos = pd.read_csv('git_pos.csv')
    df_neg = pd.read_csv('git_neg.csv')
    df_neu = pd.read_csv('git_neu.csv')
    
    print(f"✓ Positive dataset loaded: {len(df_pos):,} examples")
    print(f"✓ Negative dataset loaded: {len(df_neg):,} examples")
    print(f"✓ Neutral dataset loaded: {len(df_neu):,} examples")
    
    # Load merged dataset
    print("\n2. Loading Merged Dataset:")
    print("-" * 70)
    
    df_merged = pd.read_csv('sentiment_PNO.csv')
    print(f"✓ Merged dataset loaded: {len(df_merged):,} examples")
    
    # Show label distribution
    print("\n3. Label Distribution in Merged Dataset:")
    print("-" * 70)
    
    label_counts = df_merged['Labels'].value_counts().sort_index()
    label_names = {0: 'Negative', 1: 'Neutral', 2: 'Positive'}
    
    for label, count in label_counts.items():
        percentage = (count / len(df_merged)) * 100
        print(f"  {label_names[label]:8s} (Label {label}): {count:7,} ({percentage:5.2f}%)")
    
    # Show dataset statistics
    print("\n4. Dataset Statistics:")
    print("-" * 70)
    
    # Calculate average review length
    df_merged['review_length'] = df_merged['Reviews'].str.len()
    
    print(f"  Average review length: {df_merged['review_length'].mean():.1f} characters")
    print(f"  Min review length: {df_merged['review_length'].min()} characters")
    print(f"  Max review length: {df_merged['review_length'].max()} characters")
    print(f"  Median review length: {df_merged['review_length'].median():.1f} characters")
    
    # Show sample reviews from each category
    print("\n5. Sample Reviews by Sentiment:")
    print("-" * 70)
    
    for label in [0, 1, 2]:
        print(f"\n  {label_names[label]} Examples (Label {label}):")
        samples = df_merged[df_merged['Labels'] == label].sample(3, random_state=42)
        for idx, (_, row) in enumerate(samples.iterrows(), 1):
            review = row['Reviews']
            preview = review[:90] + "..." if len(review) > 90 else review
            print(f"    {idx}. {preview}")
    
    # Demonstrate train/test split
    print("\n6. Train/Test Split Example:")
    print("-" * 70)
    
    from sklearn.model_selection import train_test_split
    
    X = df_merged['Reviews']
    y = df_merged['Labels']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"  Training set: {len(X_train):,} examples")
    print(f"  Test set: {len(X_test):,} examples")
    
    # Show label distribution in splits
    train_counts = pd.Series(y_train).value_counts().sort_index()
    test_counts = pd.Series(y_test).value_counts().sort_index()
    
    print(f"\n  Training set distribution:")
    for label, count in train_counts.items():
        print(f"    {label_names[label]:8s}: {count:7,} ({count/len(y_train)*100:5.2f}%)")
    
    print(f"\n  Test set distribution:")
    for label, count in test_counts.items():
        print(f"    {label_names[label]:8s}: {count:7,} ({count/len(y_test)*100:5.2f}%)")
    
    # Show how to access data for BERT
    print("\n7. Preparing Data for BERT Training:")
    print("-" * 70)
    
    print("  Example code:")
    print("  ```python")
    print("  # Load dataset")
    print("  df = pd.read_csv('sentiment_PNO.csv')")
    print("  ")
    print("  # Extract reviews and labels")
    print("  texts = df['Reviews'].tolist()")
    print("  labels = df['Labels'].tolist()")
    print("  ")
    print("  # Split data")
    print("  from sklearn.model_selection import train_test_split")
    print("  train_texts, test_texts, train_labels, test_labels = train_test_split(")
    print("      texts, labels, test_size=0.2, random_state=42, stratify=labels")
    print("  )")
    print("  ")
    print("  # Use with BERT tokenizer")
    print("  from transformers import BertTokenizer")
    print("  tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')")
    print("  # ... continue with BERT training")
    print("  ```")
    
    print("\n" + "=" * 70)
    print("✓ Dataset demonstration complete!")
    print("=" * 70)
    print("\nDatasets are ready for:")
    print("  • BERT model training")
    print("  • Sarcasm-aware sentiment analysis")
    print("  • Machine learning experiments")
    print("  • Transfer learning applications")
    print()


if __name__ == "__main__":
    demonstrate_dataset_usage()
