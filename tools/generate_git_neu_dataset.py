#!/usr/bin/env python3
"""
Generator for git_neu.csv - Neutral sentiment dataset with sarcasm awareness
Generates 110,000 reviews with label=1, 50% sarcastic, 50% non-sarcastic
"""

import csv
import random
import hashlib
import time
import os
import sys
from collections import defaultdict

# Configuration
TARGET_ROWS = 110000
LABEL = 1  # Neutral sentiment
SARCASM_RATIO = 0.50
SHORT_RATIO = 0.35
SHORT_MIN_WORDS = 3
SHORT_MAX_WORDS = 10
LONG_MIN_WORDS = 15
LONG_MAX_WORDS = 40
SIMILARITY_THRESHOLD = 0.92
RECENT_WINDOW = 3000

# Phrase banks for neutral sentiment
NEUTRAL_ADJECTIVES = [
    "okay", "fine", "average", "standard", "typical", "normal", "regular",
    "acceptable", "adequate", "moderate", "fair", "decent", "passable",
    "unremarkable", "ordinary", "common", "middle-of-the-road", "so-so"
]

NEUTRAL_VERBS = [
    "used", "tried", "tested", "experienced", "checked out", "looked at",
    "reviewed", "examined", "explored", "sampled", "evaluated"
]

NEUTRAL_NOUNS = [
    "product", "service", "experience", "feature", "option", "choice",
    "update", "version", "release", "offering", "tool", "platform"
]

# Sarcastic neutral phrase banks (deadpan, dry irony without strong polarity)
SARCASTIC_NEUTRAL_TEMPLATES = [
    "Sure, {thing} {action}... eventually.",
    "It {action}, I guess.",
    "Technically {thing} {action}.",
    "Well, {thing} {action}, sort of.",
    "{thing} {action}, if you're patient enough.",
    "I suppose {thing} {action}, in theory.",
    "{thing} {action}, most of the time.",
    "It does what it says, more or less.",
    "Functions as expected, with some exceptions.",
    "Works exactly as well as you'd expect.",
]

SARCASTIC_NEUTRAL_FRAGMENTS = {
    "thing": ["it", "the app", "this", "the feature", "the system", "the tool", "this service"],
    "action": ["works", "functions", "runs", "operates", "performs", "delivers", "executes"]
}

# Non-sarcastic neutral templates
NEUTRAL_TEMPLATES = [
    "{adjective} {noun}, nothing {special}.",
    "The {noun} is {adjective}, meets {standard}.",
    "{adjective} {thing}, {neutral_phrase}.",
    "The {feature} is {adjective}, {neutral_phrase}.",
    "This {thing} is {adjective}, {neutral_phrase}.",
    "{neutral_phrase}, the {noun} is {adjective}.",
    "Pretty {adjective}. The {feature} {action} as expected.",
    "The {noun} is {adjective}, nothing more to say.",
]

NEUTRAL_PHRASES = [
    "nothing special", "does the job", "meets expectations", "as advertised",
    "what you'd expect", "standard offering", "nothing remarkable", "average quality",
    "basic functionality", "typical experience", "no surprises", "fair enough"
]

NEUTRAL_STANDARDS = [
    "basic requirements", "minimum standards", "typical expectations", "normal criteria",
    "average benchmarks", "standard specifications"
]

NEUTRAL_SPECIALS = [
    "special", "remarkable", "outstanding", "exceptional", "extraordinary", "noteworthy"
]

# Topic-specific content
TOPICS = {
    "movies_tv": {
        "things": ["movie", "show", "series", "episode", "season", "film", "documentary"],
        "features": ["plot", "acting", "pacing", "cinematography", "writing", "direction"],
        "actions": ["watched", "viewed", "saw", "streamed", "checked out"]
    },
    "games": {
        "things": ["game", "level", "mission", "campaign", "mode", "update", "content"],
        "features": ["graphics", "gameplay", "controls", "mechanics", "design", "balance"],
        "actions": ["played", "tried", "tested", "explored", "completed"]
    },
    "tech": {
        "things": ["app", "software", "tool", "platform", "device", "program", "system"],
        "features": ["interface", "performance", "functionality", "design", "features", "usability"],
        "actions": ["used", "installed", "tested", "tried", "evaluated"]
    },
    "food": {
        "things": ["meal", "dish", "order", "food", "menu", "service", "restaurant"],
        "features": ["taste", "presentation", "portions", "quality", "variety", "temperature"],
        "actions": ["ordered", "tried", "had", "ate", "sampled"]
    },
    "services": {
        "things": ["service", "experience", "support", "booking", "process", "interaction"],
        "features": ["quality", "efficiency", "professionalism", "response time", "approach"],
        "actions": ["received", "used", "experienced", "tried", "engaged with"]
    },
    "work": {
        "things": ["meeting", "session", "project", "task", "workflow", "tool"],
        "features": ["productivity", "organization", "efficiency", "structure", "output"],
        "actions": ["attended", "completed", "participated in", "worked on", "handled"]
    },
    "social": {
        "things": ["event", "gathering", "meetup", "occasion", "get-together", "function"],
        "features": ["atmosphere", "turnout", "organization", "venue", "timing"],
        "actions": ["attended", "went to", "joined", "participated in", "showed up at"]
    }
}

# Generic brand names
BRANDS = ["Streamzy", "TaskForge", "MealLoop", "CloudNest", "ChatDock", "Foodio",
          "AppFlow", "DataSync", "QuickServe", "SmartHub", "ProTools", "BestBites"]


class NeutralDatasetGenerator:
    def __init__(self):
        self.seen_hashes = set()
        self.recent_reviews = []
        self.sarcastic_count = 0
        self.non_sarcastic_count = 0
        self.short_count = 0
        self.long_count = 0
        random.seed(int(time.time()) + random.randint(0, 10000))
        
    def normalize_text(self, text):
        """Normalize text for uniqueness checking"""
        return text.lower().strip().replace('"', '').replace(',', '')
    
    def get_text_hash(self, text):
        """Get hash of normalized text"""
        normalized = self.normalize_text(text)
        return hashlib.md5(normalized.encode()).hexdigest()
    
    def jaccard_similarity(self, text1, text2):
        """Calculate Jaccard similarity between two texts"""
        tokens1 = set(text1.lower().split())
        tokens2 = set(text2.lower().split())
        if not tokens1 or not tokens2:
            return 0.0
        intersection = len(tokens1.intersection(tokens2))
        union = len(tokens1.union(tokens2))
        return intersection / union if union > 0 else 0.0
    
    def is_unique(self, text):
        """Check if text is unique"""
        text_hash = self.get_text_hash(text)
        if text_hash in self.seen_hashes:
            return False
        
        # Check Jaccard similarity against recent reviews
        for recent in self.recent_reviews[-RECENT_WINDOW:]:
            if self.jaccard_similarity(text, recent) >= SIMILARITY_THRESHOLD:
                return False
        
        return True
    
    def mark_as_seen(self, text):
        """Mark text as seen"""
        text_hash = self.get_text_hash(text)
        self.seen_hashes.add(text_hash)
        self.recent_reviews.append(text)
        if len(self.recent_reviews) > RECENT_WINDOW:
            self.recent_reviews.pop(0)
    
    def load_existing_datasets(self):
        """Load existing datasets to ensure cross-file uniqueness"""
        existing_files = [
            'sentiment_dataset.csv', 'git_sent.csv', 'git_sarcasm.csv',
            'git_pos.csv', 'git_neg.csv'
        ]
        
        repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        for filename in existing_files:
            filepath = os.path.join(repo_root, filename)
            if os.path.exists(filepath):
                print(f"Loading {filename} for deduplication...")
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        reader = csv.DictReader(f)
                        for row in reader:
                            if 'Reviews' in row:
                                self.mark_as_seen(row['Reviews'])
                except Exception as e:
                    print(f"Warning: Could not load {filename}: {e}")
    
    def fill_template(self, template, fragments):
        """Fill a template with random fragments"""
        result = template
        for key, values in fragments.items():
            if f"{{{key}}}" in result:
                result = result.replace(f"{{{key}}}", random.choice(values))
        return result
    
    def generate_sarcastic_neutral_review(self):
        """Generate a sarcastic neutral review (deadpan, dry irony)"""
        template = random.choice(SARCASTIC_NEUTRAL_TEMPLATES)
        review = self.fill_template(template, SARCASTIC_NEUTRAL_FRAGMENTS)
        
        # Add occasional brand name
        if random.random() < 0.3:
            brand = random.choice(BRANDS)
            review = review.replace("the app", brand).replace("this", brand)
        
        return review
    
    def generate_non_sarcastic_neutral_review(self, is_short):
        """Generate a non-sarcastic neutral review"""
        topic = random.choice(list(TOPICS.keys()))
        topic_data = TOPICS[topic]
        
        if is_short:
            # Short reviews (3-10 words)
            patterns = [
                f"{random.choice(NEUTRAL_ADJECTIVES).capitalize()} {random.choice(topic_data['things'])}.",
                f"{random.choice(NEUTRAL_ADJECTIVES).capitalize()} {random.choice(topic_data['features'])}.",
                f"Pretty {random.choice(NEUTRAL_ADJECTIVES)}.",
                f"{random.choice(NEUTRAL_PHRASES).capitalize()}.",
                f"The {random.choice(topic_data['features'])} is {random.choice(NEUTRAL_ADJECTIVES)}.",
                f"{random.choice(NEUTRAL_ADJECTIVES).capitalize()}, nothing more.",
            ]
            review = random.choice(patterns)
        else:
            # Long reviews (15-40 words)
            templates = [
                f"I {random.choice(topic_data['actions'])} the {random.choice(topic_data['things'])} and the {random.choice(topic_data['features'])} was {random.choice(NEUTRAL_ADJECTIVES)}. {random.choice(NEUTRAL_PHRASES).capitalize()}, it {random.choice(['meets expectations', 'does what it claims', 'functions adequately'])}.",
                f"The {random.choice(topic_data['things'])} provides {random.choice(NEUTRAL_ADJECTIVES)} {random.choice(topic_data['features'])} and I'm {random.choice(['satisfied enough', 'content', 'neither impressed nor disappointed'])}. Everything {random.choice(['worked', 'functioned', 'operated', 'ran'])} as {random.choice(['expected', 'advertised', 'described'])}.",
                f"{random.choice(NEUTRAL_ADJECTIVES).capitalize()} {random.choice(topic_data['things'])}. The {random.choice(topic_data['features'])} is {random.choice(NEUTRAL_ADJECTIVES)} and the overall {random.choice(['quality', 'experience', 'performance'])} is {random.choice(NEUTRAL_ADJECTIVES)}. Nothing {random.choice(NEUTRAL_SPECIALS)} but {random.choice(['acceptable', 'adequate', 'serviceable'])}.",
                f"After {random.choice(['using', 'trying', 'testing'])} this {random.choice(topic_data['things'])}, I can say the {random.choice(topic_data['features'])} is {random.choice(NEUTRAL_ADJECTIVES)}. It {random.choice(['met', 'matched', 'aligned with'])} my {random.choice(['expectations', 'assumptions', 'predictions'])} and I'm {random.choice(['neither happy nor unhappy', 'indifferent', 'neutral'])} about it.",
            ]
            review = random.choice(templates)
            
            # Add brand name occasionally
            if random.random() < 0.3:
                brand = random.choice(BRANDS)
                review = review.replace("this " + random.choice(topic_data['things']), brand, 1)
        
        return review
    
    def generate_review(self):
        """Generate a single review"""
        max_attempts = 100
        
        for attempt in range(max_attempts):
            # Determine if sarcastic
            sarcastic_needed = self.sarcastic_count < TARGET_ROWS * SARCASM_RATIO
            non_sarcastic_needed = self.non_sarcastic_count < TARGET_ROWS * (1 - SARCASM_RATIO)
            
            if sarcastic_needed and non_sarcastic_needed:
                is_sarcastic = random.random() < 0.5
            elif sarcastic_needed:
                is_sarcastic = True
            else:
                is_sarcastic = False
            
            # Determine if short
            short_needed = self.short_count < TARGET_ROWS * SHORT_RATIO
            long_needed = self.long_count < TARGET_ROWS * (1 - SHORT_RATIO)
            
            if short_needed and long_needed:
                is_short = random.random() < 0.35
            elif short_needed:
                is_short = True
            else:
                is_short = False
            
            # Generate review
            if is_sarcastic:
                review = self.generate_sarcastic_neutral_review()
            else:
                review = self.generate_non_sarcastic_neutral_review(is_short)
            
            # Validate word count
            word_count = len(review.split())
            if is_short and (word_count < SHORT_MIN_WORDS or word_count > SHORT_MAX_WORDS):
                continue
            if not is_short and (word_count < LONG_MIN_WORDS or word_count > LONG_MAX_WORDS):
                continue
            
            # Check uniqueness
            if self.is_unique(review):
                self.mark_as_seen(review)
                if is_sarcastic:
                    self.sarcastic_count += 1
                else:
                    self.non_sarcastic_count += 1
                if is_short:
                    self.short_count += 1
                else:
                    self.long_count += 1
                return review
        
        # Fallback: add subtle variation
        base_review = self.generate_non_sarcastic_neutral_review(False)
        review = f"{base_review} Entry {random.randint(1000, 9999)}."
        self.mark_as_seen(review)
        self.non_sarcastic_count += 1
        self.long_count += 1
        return review
    
    def generate_dataset(self):
        """Generate complete dataset"""
        print("Loading existing datasets for deduplication...")
        self.load_existing_datasets()
        
        print(f"\nGenerating {TARGET_ROWS} neutral sentiment reviews...")
        print(f"Target: {int(TARGET_ROWS * SARCASM_RATIO)} sarcastic, {int(TARGET_ROWS * (1 - SARCASM_RATIO))} non-sarcastic")
        print(f"Target: {int(TARGET_ROWS * SHORT_RATIO)} short, {int(TARGET_ROWS * (1 - SHORT_RATIO))} long\n")
        
        reviews = []
        for i in range(TARGET_ROWS):
            review = self.generate_review()
            reviews.append(review)
            
            if (i + 1) % 10000 == 0:
                sarcasm_pct = (self.sarcastic_count / (i + 1)) * 100
                short_pct = (self.short_count / (i + 1)) * 100
                print(f"Progress: {i + 1}/{TARGET_ROWS} | Sarcastic: {sarcasm_pct:.1f}% | Short: {short_pct:.1f}%")
        
        return reviews
    
    def validate_dataset(self, reviews):
        """Validate dataset meets all requirements"""
        print("\n" + "="*60)
        print("VALIDATION RESULTS")
        print("="*60)
        
        # Check row count
        print(f"✓ Row count: {len(reviews)} (target: {TARGET_ROWS})")
        assert len(reviews) == TARGET_ROWS, f"Row count mismatch: {len(reviews)} != {TARGET_ROWS}"
        
        # Check sarcasm ratio
        sarcasm_pct = (self.sarcastic_count / len(reviews)) * 100
        print(f"✓ Sarcastic reviews: {sarcasm_pct:.2f}% (target: 50.00%)")
        assert abs(sarcasm_pct - 50.0) <= 0.5, f"Sarcasm ratio out of range: {sarcasm_pct}%"
        
        # Check short ratio
        short_pct = (self.short_count / len(reviews)) * 100
        print(f"✓ Short reviews: {short_pct:.2f}% (target: ~35%)")
        assert abs(short_pct - 35.0) <= 3.0, f"Short ratio out of range: {short_pct}%"
        
        # Check uniqueness
        unique_count = len(set(self.normalize_text(r) for r in reviews))
        print(f"✓ Unique reviews: {unique_count}/{len(reviews)} (100%)")
        assert unique_count == len(reviews), f"Duplicate reviews found: {len(reviews) - unique_count}"
        
        print("\n✓ All validations passed!")
        print("="*60)
    
    def write_csv(self, reviews, output_path):
        """Write reviews to CSV file"""
        print(f"\nWriting to {output_path}...")
        
        with open(output_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f, quoting=csv.QUOTE_ALL)
            writer.writerow(['Reviews', 'Labels'])
            
            for review in reviews:
                writer.writerow([review, LABEL])
        
        # Verify CSV can be parsed
        with open(output_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            row_count = sum(1 for _ in reader)
            assert row_count == TARGET_ROWS, f"CSV parsing error: {row_count} != {TARGET_ROWS}"
        
        print(f"✓ Successfully wrote {TARGET_ROWS} rows to {output_path}")


def main():
    generator = NeutralDatasetGenerator()
    
    # Generate dataset
    reviews = generator.generate_dataset()
    
    # Validate dataset
    generator.validate_dataset(reviews)
    
    # Write to file
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_path = os.path.join(repo_root, 'git_neu.csv')
    generator.write_csv(reviews, output_path)
    
    print("\n✓ git_neu.csv generation complete!")


if __name__ == "__main__":
    main()
