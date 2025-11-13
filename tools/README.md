# Dataset Generation Tools

This directory contains scripts for generating sentiment analysis datasets for the BERT model project.

## Scripts

### generate_git_sarcasm_dataset.py

Generates the `git_sarcasm.csv` dataset with 120,000 unique sarcasm-heavy sentiment reviews.

#### Features

- **120,000 unique rows** with balanced label distribution
- **90% sarcastic reviews** (±1.5% tolerance) for improved model training on sarcasm detection
- **Balanced labels (0-5)**: ~20,000 reviews per sentiment label (±60 tolerance)
  - 0, 1, 2: Negative sentiment (strong → mild)
  - 3: Neutral sentiment
  - 4, 5: Positive sentiment (mild → strong)
- **Topic variety**: Emphasis on movies, TV shows, and music with supporting variety in relationships and product reviews
- **Length diversity**: ~35% short reviews (≤10 words), ~65% long reviews (15-40 words)
- **Deduplication**: Ensures zero duplicates or near-duplicates internally and versus existing datasets
- **Proper CSV formatting**: UTF-8 encoding, LF line endings, proper quote escaping

#### Sarcasm Balancing

The generator maintains sarcasm across all sentiment labels, including:

- **Sarcastic negatives**: Exaggerated complaints with ironic praise
- **Sarcastic neutrals**: Deadpan observations with implicit irony
- **Sarcastic positives**: Playful genuine praise that sounds ironic

This diverse sarcasm representation helps train BERT models to:
1. Detect sarcasm regardless of apparent sentiment polarity
2. Distinguish between genuine and sarcastic expressions
3. Handle real-world complexity where sarcasm appears in all sentiment contexts

#### Usage

```bash
# Navigate to the repository root
cd /path/to/Sentiment-Analysis-using-BERT-model

# Run the generator script
python3 tools/generate_git_sarcasm_dataset.py
```

The script will:
1. Load existing datasets (`sentiment_dataset.csv`, `git_sent.csv`) if present for cross-file deduplication
2. Generate 120,000 unique reviews with controlled sarcasm proportion
3. Validate all requirements (row count, label balance, uniqueness)
4. Write `git_sarcasm.csv` to the repository root

#### Output

- **File**: `git_sarcasm.csv` in repository root
- **Format**: CSV with header `Reviews,Labels`
- **Size**: Approximately 7-10 MB
- **Encoding**: UTF-8 with LF line endings

#### Validation

The generator includes built-in validation that checks:

- ✓ Exact row count (120,000)
- ✓ Correct header format
- ✓ Label distribution balance (±60 tolerance)
- ✓ Sarcasm proportion (90% ±1.5%)
- ✓ Word count distribution
- ✓ Complete uniqueness (no duplicates)
- ✓ Proper CSV formatting

#### Regeneration

To regenerate the dataset with different variations:

```bash
# Simply run the script again
python3 tools/generate_git_sarcasm_dataset.py
```

The generator uses controlled randomization, so each run produces unique reviews while maintaining the same distribution requirements.

#### Requirements

- Python 3.7+
- No external dependencies (uses only standard library)

#### Cross-file Deduplication

The script automatically checks for and loads:
- `sentiment_dataset.csv`
- `git_sent.csv`

If these files exist in the repository root, the generator ensures generated reviews don't overlap with them using hash-based deduplication.

#### Notes

- Reviews are wrapped in double quotes with proper CSV escaping (internal quotes are doubled)
- All content is safe, non-toxic, and appropriate for general audiences
- Fictional/generic brand names are used (e.g., "Streamzy", "ChatterDock", "MealLoop")
- No real PII, slurs, explicit content, or harmful material is included

## Dataset Information

### git_sarcasm.csv

**Purpose**: Sarcasm-heavy sentiment analysis training data for BERT models

**Specifications**:
- 120,000 rows (excluding header)
- 90% sarcastic reviews for improved sarcasm detection
- Balanced across 6 sentiment labels (0-5)
- Topics focused on entertainment (movies, TV, music) with variety in relationships and products
- Mix of conversational, formal, casual, and review-style tones

**Use Cases**:
- Training BERT models for sentiment analysis with sarcasm awareness
- Fine-tuning language models on irony and sarcasm detection
- Testing model performance on nuanced sentiment expressions
- Benchmarking sarcasm detection capabilities

**Label Mapping**:
- 0: Strong negative sentiment
- 1: Mild negative sentiment  
- 2: Negative sentiment
- 3: Neutral sentiment
- 4: Mild positive sentiment
- 5: Strong positive sentiment
