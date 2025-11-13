# Sarcasm-Aware Sentiment Analysis Datasets

This repository contains comprehensive sentiment analysis datasets designed for training BERT models with sarcasm awareness.

## 📊 Datasets Overview

### Individual Datasets

1. **git_pos.csv** - Positive Sentiment Dataset
   - **Size:** 100,000 unique examples
   - **Label:** `2` (Positive)
   - **Composition:** 50% sarcastic-positive, 50% normal-positive
   - **Topics:** Movies, tech, food, travel, products, services, etc.

2. **git_neg.csv** - Negative Sentiment Dataset
   - **Size:** 100,000 unique examples
   - **Label:** `0` (Negative)
   - **Composition:** 50% sarcastic-negative, 50% normal-negative
   - **Topics:** Product complaints, service issues, disappointments, etc.

3. **git_neu.csv** - Neutral Sentiment Dataset
   - **Size:** 100,000 unique examples
   - **Label:** `1` (Neutral)
   - **Composition:** 50% sarcastic-neutral, 50% normal-neutral
   - **Topics:** Balanced reviews, factual statements, observations, etc.

### Merged Dataset

**sentiment_PNO.csv** - Combined Dataset
- **Size:** 300,000 total examples
- **Labels:** Perfectly balanced (33.33% each)
- **Format:** Ready for direct use in ML pipelines

## 📝 Dataset Format

All datasets follow this structure:

```csv
Reviews,Labels
"This product is amazing! Best purchase ever.",2
"The service was terrible. Complete waste of money.",0
"It works fine. Nothing special but functional.",1
```

### Label Mapping
- `0` = Negative sentiment
- `1` = Neutral sentiment  
- `2` = Positive sentiment

## 🎯 Key Features

### ✅ Sarcasm-Aware
Each dataset contains 50% sarcastic examples to help models learn nuanced sentiment:

- **Sarcastic Positive:** "Wow, it finally works! What a miracle!"
- **Sarcastic Negative:** "Oh great, another update that broke everything!"
- **Sarcastic Neutral:** "Sure, it works... eventually."

### ✅ Diverse Topics
Reviews cover a wide range of subjects:
- **Technology:** Apps, software, devices, gadgets
- **Entertainment:** Movies, shows, games, music
- **Food & Dining:** Restaurants, delivery, meals
- **Services:** Customer support, subscriptions, travel
- **Products:** Electronics, home goods, personal items
- And 200+ more categories!

### ✅ Production-Ready
- **CSV Formatting:** Proper escaping of commas, quotes, and special characters
- **Pandas Compatible:** Direct import without preprocessing
- **No Duplicates:** All 300,000 examples are unique
- **Balanced Classes:** Equal distribution for unbiased training
- **No Missing Values:** Clean, validated data

## 🚀 Quick Start

### Loading the Datasets

```python
import pandas as pd

# Load individual datasets
df_positive = pd.read_csv('git_pos.csv')
df_negative = pd.read_csv('git_neg.csv')
df_neutral = pd.read_csv('git_neu.csv')

# Or load the merged dataset
df_all = pd.read_csv('sentiment_PNO.csv')

print(f"Total examples: {len(df_all):,}")
print(f"Label distribution:\n{df_all['Labels'].value_counts().sort_index()}")
```

### Preparing for BERT Training

```python
from sklearn.model_selection import train_test_split

# Extract data
texts = df_all['Reviews'].tolist()
labels = df_all['Labels'].tolist()

# Split with stratification
train_texts, test_texts, train_labels, test_labels = train_test_split(
    texts, labels, 
    test_size=0.2, 
    random_state=42, 
    stratify=labels
)

# Use with BERT
from transformers import BertTokenizer, BertForSequenceClassification

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForSequenceClassification.from_pretrained(
    'bert-base-uncased', 
    num_labels=3
)

# Continue with training...
```

## 📈 Dataset Statistics

| Metric | Value |
|--------|-------|
| Total Examples | 300,000 |
| Unique Examples | 300,000 (100%) |
| Positive Examples | 100,000 (33.33%) |
| Negative Examples | 100,000 (33.33%) |
| Neutral Examples | 100,000 (33.33%) |
| Sarcastic Examples | 150,000 (50%) |
| Normal Examples | 150,000 (50%) |
| Avg. Review Length | ~73 characters |
| Min Review Length | 25 characters |
| Max Review Length | 126 characters |

## 🛠️ Generation & Validation Scripts

### Generate Datasets
```bash
python3 generate_datasets.py
```
Creates all four CSV files with 100,000 unique examples each.

### Validate Datasets
```bash
python3 validate_datasets.py
```
Runs comprehensive validation checks:
- CSV format validation
- Pandas compatibility
- Data integrity checks
- Label distribution analysis
- Duplicate detection

### Demo Usage
```bash
python3 demo_usage.py
```
Demonstrates dataset loading, exploration, and BERT preparation.

## 📚 Example Reviews

### Positive (Label: 2)
- **Normal:** "This product is fantastic! Highly recommend it to everyone."
- **Sarcastic:** "Wow, it finally did something right for once!"

### Negative (Label: 0)
- **Normal:** "Terrible quality. Complete waste of money."
- **Sarcastic:** "Oh great, another update that broke everything again!"

### Neutral (Label: 1)
- **Normal:** "The product is okay. It does what it's supposed to do."
- **Sarcastic:** "Sure, it works... eventually."

## 🎓 Use Cases

These datasets are ideal for:
- **BERT Model Training:** Pre-configured for 3-class sentiment classification
- **Sarcasm Detection:** Learn to identify sarcastic vs. literal sentiment
- **Transfer Learning:** Fine-tune pre-trained models on nuanced data
- **Sentiment Analysis Research:** Balanced, diverse, production-ready data
- **NLP Education:** Real-world examples for teaching sentiment analysis

## 🔧 Technical Details

### Dependencies
```bash
pip install pandas scikit-learn
```

For BERT training, additionally install:
```bash
pip install torch transformers
```

### File Sizes
- `git_pos.csv`: ~6.6 MB
- `git_neg.csv`: ~6.6 MB
- `git_neu.csv`: ~5.8 MB
- `sentiment_PNO.csv`: ~19 MB

### Encoding
All files use UTF-8 encoding with proper CSV escaping.

## 📄 License

These datasets are generated for the "Sentiment Analysis using BERT" project and are available for educational and research purposes.

## 🤝 Contributing

To regenerate or modify datasets:
1. Edit `generate_datasets.py` to adjust templates or parameters
2. Run the generation script
3. Validate with `validate_datasets.py`
4. Test with `demo_usage.py`

## ⚠️ Important Notes

- All 300,000 examples are **unique** (no duplicates)
- Labels are **perfectly balanced** across all three classes
- Reviews contain **proper CSV escaping** for special characters
- Datasets are **immediately usable** with pandas and BERT
- **Sarcasm is evenly distributed** across all sentiment categories

## 🎯 Model Training Recommendation

For best results:
1. Use the merged `sentiment_PNO.csv` for balanced training
2. Apply stratified train/test split (80/20 recommended)
3. Use BERT-base or DistilBERT as base models
4. Fine-tune for 3-5 epochs with appropriate learning rate
5. Monitor performance on sarcastic vs. non-sarcastic subsets

---

**Ready to train?** Load `sentiment_PNO.csv` and start building your sarcasm-aware sentiment analysis model! 🚀
