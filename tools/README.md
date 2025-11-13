# Dataset Generation Tools

This directory contains tools for generating specialized sentiment analysis datasets with sarcasm awareness.

## Overview

The tools generate three large CSV datasets (110,000 rows each) for sarcasm-aware sentiment analysis:
- **git_pos.csv**: Positive sentiment reviews (label=2)
- **git_neg.csv**: Negative sentiment reviews (label=0)
- **git_neu.csv**: Neutral sentiment reviews (label=1)

## Dataset Specifications

### Common Attributes
- **Rows per file**: 110,000
- **Sarcasm ratio**: 50% sarcastic, 50% non-sarcastic
- **Review length**: ~35% short (3-10 words), ~65% long (15-40 words)
- **CSV format**: UTF-8 encoding, LF line endings, header `Reviews,Labels`
- **Uniqueness**: All reviews unique within and across all datasets

### Label Meanings
- **0**: Negative (complaints, frustrations, sarcastic negativity)
- **1**: Neutral (objective, factual, deadpan sarcasm)
- **2**: Positive (praise, enthusiasm, sarcastic-positive/ironic relief)

### Topics Covered
- Movies, TV shows, music
- Games & entertainment
- Technology, apps, AI tools
- Food, restaurants, delivery
- Services, travel, customer experience
- Work, productivity, meetings, tools
- Social life, relationships, casual conversation
- Humor & light situational commentary

## Sarcasm Strategies

### Positive Sentiment (git_pos.csv)
**Sarcastic style**: Ironic relief, surprised praise
- Examples:
  - "Wow, finally an update that didn't break anything!"
  - "Shocked that it actually works on the first try!"
  - "Only crashed twice today, major improvement!"

**Non-sarcastic style**: Genuine praise, enthusiasm
- Examples:
  - "Amazing experience, highly recommend!"
  - "The interface is fantastic and the features work perfectly!"

### Negative Sentiment (git_neg.csv)
**Sarcastic style**: Exaggerated complaint, ironic praise of failure
- Examples:
  - "Oh fantastic, it froze again mid-task!"
  - "Great job, the app crashed at the worst time!"
  - "Love how it fails every time I need it most!"

**Non-sarcastic style**: Direct complaints, frustrations
- Examples:
  - "Terrible experience, waste of time."
  - "The app is slow and crashes constantly. Do not recommend!"

### Neutral Sentiment (git_neu.csv)
**Sarcastic style**: Deadpan, dry irony without strong polarity
- Examples:
  - "Sure, it works... eventually."
  - "Technically it functions, I guess."
  - "It does what it says, more or less."

**Non-sarcastic style**: Objective, factual observations
- Examples:
  - "Average quality, nothing special."
  - "The service is okay, meets expectations."

## Generation Scripts

### generate_git_pos_dataset.py
Generates positive sentiment reviews (label=2).

```bash
python tools/generate_git_pos_dataset.py
```

**Output**: `git_pos.csv` (110,000 rows in repository root)

**Features**:
- 50% sarcastic positive (ironic relief, surprised praise)
- 50% non-sarcastic positive (genuine enthusiasm)
- Cross-file deduplication against existing datasets
- Validates sarcasm ratio, length distribution, and uniqueness

### generate_git_neg_dataset.py
Generates negative sentiment reviews (label=0).

```bash
python tools/generate_git_neg_dataset.py
```

**Output**: `git_neg.csv` (110,000 rows in repository root)

**Features**:
- 50% sarcastic negative (exaggerated complaints, ironic praise)
- 50% non-sarcastic negative (direct complaints)
- Cross-file deduplication against existing datasets
- Validates sarcasm ratio, length distribution, and uniqueness

### generate_git_neu_dataset.py
Generates neutral sentiment reviews (label=1).

```bash
python tools/generate_git_neu_dataset.py
```

**Output**: `git_neu.csv` (110,000 rows in repository root)

**Features**:
- 50% sarcastic neutral (deadpan, dry irony)
- 50% non-sarcastic neutral (objective observations)
- Cross-file deduplication against existing datasets
- Validates sarcasm ratio, length distribution, and uniqueness

### prepare_sentiment_PNO_merge.py
Merges the three datasets into a single master file (optional, for future use).

```bash
python tools/prepare_sentiment_PNO_merge.py
```

**Output**: `sentiment_PNO.csv` (330,000 rows combining all three datasets)

**Features**:
- Combines git_pos.csv, git_neg.csv, git_neu.csv
- Shuffles reviews for balanced distribution
- Verifies uniqueness across merged dataset
- Provides summary statistics

## Generation Workflow

### Complete Generation (All Datasets)
To generate all three datasets from scratch:

```bash
# Generate positive sentiment dataset
python tools/generate_git_pos_dataset.py

# Generate negative sentiment dataset
python tools/generate_git_neg_dataset.py

# Generate neutral sentiment dataset
python tools/generate_git_neu_dataset.py

# Optional: Merge into single master file
python tools/prepare_sentiment_PNO_merge.py
```

### Regeneration
To regenerate a specific dataset:

1. Delete the existing CSV file (e.g., `git_pos.csv`)
2. Run the corresponding generator script
3. The script will automatically load other existing datasets for deduplication

**Example**: Regenerate only negative sentiment dataset
```bash
rm git_neg.csv
python tools/generate_git_neg_dataset.py
```

## Validation

Each generator performs automatic validation:

✓ **Row count**: Exactly 110,000 rows  
✓ **Sarcasm ratio**: 50% ±0.5%  
✓ **Short review ratio**: ~35% ±3%  
✓ **Uniqueness**: 100% unique reviews (exact and near-duplicate check)  
✓ **CSV parsing**: Validates proper CSV format  
✓ **Label consistency**: All rows use correct single label  

## Cross-File Deduplication

The generators ensure uniqueness across:
- `sentiment_dataset.csv` (if exists)
- `git_sent.csv` (if exists)
- `git_sarcasm.csv` (if exists)
- `git_pos.csv`, `git_neg.csv`, `git_neu.csv` (newly generated)

Reviews are checked using:
1. **MD5 hash** of normalized text (exact duplicates)
2. **Jaccard similarity** on recent 3,000 reviews (threshold < 0.92 token overlap)

## Performance

- **Generation time**: ~5-15 minutes per dataset (varies by system)
- **Memory usage**: ~200-400 MB peak during generation
- **Output size**: ~6-8 MB per CSV file

## Quality Assurance

### Uniqueness Strategy
- Hash-based exact duplicate detection
- Jaccard similarity for near-duplicate detection
- Template variation with random phrase banks
- Fallback with subtle numerical suffix (rare cases only)

### Diversity Mechanisms
- Multiple phrase banks per sentiment type
- Topic-specific vocabulary (7 topic categories)
- Random template selection and fragment substitution
- Varied sentence structures and punctuation
- Generic brand names (avoid real companies)

### Safety & Content Policy
- No PII, slurs, or explicit content
- No real celebrity or company names
- No medical, financial, or extremist content
- Generic/fictional brand names only

## File Format

```csv
Reviews,Labels
"Amazing movie, really enjoyed it!",2
"The app crashes constantly.",0
"Average quality, nothing special.",1
```

- **Header**: `Reviews,Labels`
- **Encoding**: UTF-8 (no BOM)
- **Line endings**: LF (Unix-style)
- **Quoting**: All fields quoted
- **Escaping**: Internal quotes doubled (`""`)

## Troubleshooting

### "Row count mismatch" error
- Indicates generation loop issue
- Re-run the script (uses time-based randomization)

### "Sarcasm ratio out of range" warning
- Minor variance is acceptable (±0.5%)
- Script auto-adjusts during generation

### "Duplicate reviews found" error
- Should not occur with proper deduplication
- Check for corrupted existing datasets
- Delete and regenerate

### Slow generation
- Normal for 110K rows (uses uniqueness checks)
- Progress reported every 10,000 rows
- Consider reducing RECENT_WINDOW if memory-constrained

## Dependencies

Standard Python 3 libraries only:
- `csv`: CSV file operations
- `random`: Random generation
- `hashlib`: Hash-based deduplication
- `time`: Seed randomization
- `os`, `sys`: File operations

No external packages required.

## Output Location

All CSV files are generated in the **repository root**:
```
Sentiment-Analysis-using-BERT-model/
├── git_pos.csv          (110,000 rows)
├── git_neg.csv          (110,000 rows)
├── git_neu.csv          (110,000 rows)
├── sentiment_PNO.csv    (330,000 rows, optional)
└── tools/
    ├── generate_git_pos_dataset.py
    ├── generate_git_neg_dataset.py
    ├── generate_git_neu_dataset.py
    └── prepare_sentiment_PNO_merge.py
```

## Future Usage

The three datasets will be merged into `sentiment_PNO.csv` for comprehensive sentiment analysis model training with balanced sarcasm awareness across all sentiment classes.
