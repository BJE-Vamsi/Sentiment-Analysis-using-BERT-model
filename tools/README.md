# Sentiment Dataset Generator

This directory contains tools for generating the sentiment analysis dataset used in this project.

## Files

- `generate_sentiment_dataset.py` - Python script to generate the sentiment dataset CSV

## Generating the Dataset

To regenerate the `sentiment_dataset.csv` file in the repository root:

```bash
python3 tools/generate_sentiment_dataset.py
```

### Requirements

- Python 3.6 or higher
- Standard library only (no external dependencies required)

### Dataset Specifications

The generator creates a CSV file with the following characteristics:

- **Total rows**: 90,000 unique sentiment reviews
- **Format**: CSV with header `Reviews,Labels`
- **Labels**: 
  - 0, 1, 2: Negative sentiment (varying intensity)
  - 3: Neutral sentiment
  - 4, 5: Positive sentiment (varying intensity)
- **Distribution**: Balanced across all 6 labels (~15,000 rows each, ±50 tolerance)
- **Review length**:
  - 30% short reviews (3-8 words)
  - 70% long reviews (15-45 words)
- **Sarcasm**: ~40% of reviews contain sarcastic content distributed across all sentiment types
- **Topics**: Diverse coverage including movies, TV shows, products, apps, restaurants, services, daily experiences, etc.

### Validation

The script includes built-in validation that checks:

- ✓ Correct row count (90,000)
- ✓ Proper CSV header format
- ✓ Label distribution within tolerance
- ✓ Short/long review distribution (30%/70% ±1%)
- ✓ All reviews are unique (no duplicates)
- ✓ Valid CSV parsing
- ✓ All labels in valid range (0-5)

### Output

The script generates `sentiment_dataset.csv` in the repository root directory. The file is immediately ready for use with Python/Pandas, Excel, Google Sheets, or any CSV-compatible tool.

### Generation Time

Generating 90,000 unique reviews takes approximately 30-60 seconds on modern hardware.

## Implementation Details

The generator uses:

- Template-based generation with extensive phrase banks
- Probabilistic variation to ensure uniqueness
- Hash-based and token-based duplicate detection
- Sarcasm injection through curated patterns
- Proper CSV escaping and formatting
- Post-generation validation
