# Dataset Generation Tools

This directory contains tools for generating sentiment analysis datasets for the BERT model training.

## git_sent.csv Dataset

The `git_sent.csv` file contains 100,000 unique sentiment analysis reviews with labels ranging from 0-5.

### Dataset Specifications

- **File**: `git_sent.csv` (located at repository root)
- **Rows**: 100,000 (excluding header)
- **Columns**: 
  - `Reviews`: Natural English text expressing opinions/emotions
  - `Labels`: Integer sentiment labels (0-5)
- **Label Distribution**: ~16,666-16,667 rows per label (0-5)
- **Sarcasm Content**: ~35-45% of reviews include sarcastic elements
- **Encoding**: UTF-8 with LF line endings
- **Uniqueness**: All reviews are unique (no duplicates or near-duplicates)

### Label Meanings

- **0, 1, 2**: Negative sentiment (strong → mild)
- **3**: Neutral sentiment  
- **4, 5**: Positive sentiment (mild → strong)

### Topics Covered

Reviews span diverse topics including:
- Movies, TV shows, and music
- Games and entertainment
- Technology, apps, and AI tools
- Food, restaurants, and delivery services
- Customer service and real-world experiences
- Work, productivity, and daily life
- General opinions and feedback

## Regenerating the Dataset

To regenerate `git_sent.csv`:

```bash
# From repository root
python3 tools/generate_git_sent_dataset.py
```

### Requirements

- Python 3.7+
- No external dependencies (uses only standard library)

### Generation Process

The generator:
1. Creates 100,000 unique reviews using phrase banks and templates
2. Balances labels evenly across 0-5
3. Injects sarcasm patterns (~40% of reviews)
4. Ensures proper CSV escaping (quotes, special characters)
5. Validates uniqueness (no duplicates)
6. Performs post-generation validation:
   - Row count verification
   - Label distribution check
   - Sarcasm proportion check
   - CSV parsing validation
   - Uniqueness verification

### Validation

The script includes built-in validation that checks:
- ✓ Exactly 100,000 rows
- ✓ Header: `Reviews,Labels`
- ✓ Label balance within tolerance (±50 per label)
- ✓ Sarcasm proportion within 35-45%
- ✓ All rows parse via CSV parser
- ✓ All reviews are unique

### Output

After successful generation:
- `git_sent.csv` is created at repository root
- Validation report is printed to console
- Script exits with code 0 on success, 1 on failure

## File Format

CSV format with proper escaping:
```csv
Reviews,Labels
"This movie is excellent",5
"The food was terrible",0
"It's okay, nothing special",3
```

All reviews are wrapped in double quotes, and internal quotes are doubled (`"` → `""`) per CSV specification.

## Usage in Python

Load the dataset with pandas:

```python
import pandas as pd

df = pd.read_csv('git_sent.csv')
print(f"Loaded {len(df)} reviews")
print(df['Labels'].value_counts().sort_index())
```

## Notes

- Reviews include natural variations: casual, formal, sarcastic, conversational
- Brand/app names are generic or fictional (e.g., "Streamzy", "TaskForge")
- Content is safe and non-toxic
- No personally identifiable information (PII)
- Compatible with Excel, Google Sheets, and all standard CSV parsers
