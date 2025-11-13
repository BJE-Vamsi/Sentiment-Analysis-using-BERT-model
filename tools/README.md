# Tools Directory

This directory contains utility scripts for managing the sentiment analysis datasets.

## merge_datasets.py

### Purpose

Merges sentiment datasets from multiple git branches into a single, deduplicated CSV file named `sentiment_final.csv` at the repository root.

### What It Does

1. **Fetches CSV files** from the following branches:
   - `copilot/create-sentiment-dataset-csv` → `sentiment_dataset.csv`
   - `copilot/create-sentiment-dataset-csv-again` → `sentiment_dataset.csv`
   - `copilot/add-large-csv-file` → `git_sent.csv`
   - `copilot/create-large-csv-file` → `git_sarcasm.csv`

2. **Validates each input** to ensure:
   - Correct header format (`Reviews,Labels`)
   - Valid labels (integers in the range 0-5)
   - Non-empty review text
   - Proper CSV structure

3. **Removes duplicates** across all input files using exact content matching

4. **Generates the merged output** (`sentiment_final.csv`) with:
   - Header: `Reviews,Labels`
   - All unique rows from input datasets
   - UTF-8 encoding with LF line endings
   - Proper CSV escaping (quoted fields, doubled internal quotes)

5. **Validates the output** to confirm:
   - No duplicate rows remain
   - All labels are valid (0-5)
   - No empty reviews
   - Correct CSV parsing

6. **Produces a summary report** showing:
   - Per-source row counts
   - Number of duplicates removed
   - Number of invalid rows filtered
   - Label distribution in final dataset

### How to Run

From the repository root:

```bash
python3 tools/merge_datasets.py
```

### Requirements

- Python 3.6 or later (uses f-strings and type hints)
- Git repository with access to the specified branches
- Standard library only (no external dependencies)

### Output

The script generates:
- `sentiment_final.csv` at the repository root
- Console output with detailed statistics and validation results

### Example Output

```
======================================================================
Sentiment Dataset Merge Process
======================================================================

Processing copilot/create-sentiment-dataset-csv:sentiment_dataset.csv...
  Total rows read: 10000
  Valid rows: 10000

Processing copilot/create-sentiment-dataset-csv-again:sentiment_dataset.csv...
  Total rows read: 10000
  Valid rows: 10000

Processing copilot/add-large-csv-file:git_sent.csv...
  Total rows read: 10000
  Valid rows: 10000

Processing copilot/create-large-csv-file:git_sarcasm.csv...
  Total rows read: 10000
  Valid rows: 10000

Writing merged dataset to sentiment_final.csv...
✓ Successfully wrote 35000 rows

Validating output file...
  ✓ Valid: 35000 rows, no duplicates, all labels in range 0-5

======================================================================
MERGE SUMMARY REPORT
======================================================================

Source File Statistics:
----------------------------------------------------------------------
copilot/create-sentiment-dataset-csv:sentiment_dataset.csv
  Raw rows: 10000
  Valid rows: 10000

[... additional sources ...]

Merge Results:
----------------------------------------------------------------------
Total valid rows from all sources: 40000
Duplicate rows removed: 5000
Invalid rows removed: 0
Final unique rows in sentiment_final.csv: 35000

Label Distribution in Final Dataset:
----------------------------------------------------------------------
Label 0:  7,000 rows (20.00%)
Label 1:  7,000 rows (20.00%)
Label 2:  7,000 rows (20.00%)
Label 3:  7,000 rows (20.00%)
Label 4:  7,000 rows (20.00%)
Label 5:  7,000 rows (20.00%)

======================================================================
```

### Regenerating the Merged File

If the source datasets are updated or new datasets are added:

1. Update the `SOURCES` list in `merge_datasets.py` to include new branch/file pairs
2. Run the script again: `python3 tools/merge_datasets.py`
3. Commit the updated `sentiment_final.csv` to the repository

### Dataset Format

**Input Requirements:**
- CSV format with header: `Reviews,Labels`
- Reviews: Text strings (can contain quotes, commas, newlines)
- Labels: Integers from 0 to 5

**Output Format:**
- Same structure as input
- Sorted by label, then by review text
- UTF-8 encoding
- LF (Unix-style) line endings
- CSV-compliant quoting and escaping

### Maintenance

When adding new sentiment datasets to the repository:

1. Ensure the CSV has the header `Reviews,Labels`
2. Add the branch and filename to `SOURCES` in `merge_datasets.py`
3. Run the merge script to regenerate `sentiment_final.csv`
4. Commit both the script update and the new merged file
