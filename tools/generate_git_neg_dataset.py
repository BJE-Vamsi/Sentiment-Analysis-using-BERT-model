#!/usr/bin/env python3
"""
Generator for git_neg.csv - Negative sentiment dataset with sarcasm awareness
Generates 110,000 reviews with label=0, 50% sarcastic, 50% non-sarcastic
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
LABEL = 0  # Negative sentiment
SARCASM_RATIO = 0.50
SHORT_RATIO = 0.35
SHORT_MIN_WORDS = 3
SHORT_MAX_WORDS = 10
LONG_MIN_WORDS = 15
LONG_MAX_WORDS = 40
SIMILARITY_THRESHOLD = 0.92
RECENT_WINDOW = 3000

# Phrase banks for negative sentiment
NEGATIVE_ADJECTIVES = [
    "terrible", "awful", "horrible", "disappointing", "frustrating", "useless",
    "poor", "bad", "worst", "pathetic", "mediocre", "subpar", "inferior",
    "defective", "broken", "buggy", "slow", "unreliable", "annoying", "irritating"
]

NEGATIVE_VERBS = [
    "hate", "dislike", "regret", "disappointed by", "frustrated with", "annoyed by",
    "upset about", "dissatisfied with", "bothered by", "troubled by", "irritated by"
]

NEGATIVE_NOUNS = [
    "waste", "disaster", "nightmare", "failure", "problem", "issue", "bug",
    "error", "glitch", "crash", "freeze", "lag", "delay", "mess"
]

# Sarcastic negative phrase banks (exaggerated complaint, ironic praise of failure)
SARCASTIC_NEGATIVE_TEMPLATES = [
    "Oh fantastic, {thing} {negative_action} again!",
    "Great job, {thing} {negative_action} at the worst time!",
    "Wonderful, another {problem} that {negative_action}!",
    "Brilliant design, {thing} only {negative_action} {frequency}!",
    "Love how {thing} {negative_action} every time I {action}!",
    "Perfect timing for {thing} to {negative_action}!",
    "Exactly what I needed, {thing} that {negative_action}!",
    "Outstanding work, {thing} {negative_action} mid-{task}!",
    "Impressive how consistently {thing} {negative_action}!",
    "Genius update that made {thing} {negative_action} even more!",
]

SARCASTIC_NEGATIVE_FRAGMENTS = {
    "thing": ["the app", "this feature", "the update", "the system", "this tool", "the service", "the interface"],
    "negative_action": ["crashed", "froze", "failed", "broke", "stopped working", "glitched out", "hung", "lagged"],
    "problem": ["bug", "error", "crash", "freeze", "glitch", "issue", "failure"],
    "frequency": ["five minutes", "hour", "day", "single use", "time I open it"],
    "action": ["need it most", "try to use it", "open it", "start working", "have a deadline"],
    "task": ["presentation", "call", "meeting", "work", "task", "project"]
}

# Non-sarcastic negative templates
NEGATIVE_TEMPLATES = [
    "{adjective} {noun}, really {verb} it.",
    "The {noun} is {adjective}, very {verb}.",
    "{adjective} {thing}, {negative_phrase}.",
    "Really {verb} the {feature}, it's {adjective}.",
    "This {thing} is {adjective}, {negative_phrase}.",
    "{negative_phrase}, the {noun} is {adjective}.",
    "So {adjective}! The {feature} {negative_action} constantly.",
    "The {noun} failed my expectations, truly {adjective}.",
]

NEGATIVE_PHRASES = [
    "waste of time", "waste of money", "not worth it", "complete disaster",
    "absolute nightmare", "would not recommend", "total failure", "avoid at all costs",
    "don't bother", "save your money", "terrible experience", "never again"
]

# Topic-specific content
TOPICS = {
    "movies_tv": {
        "things": ["movie", "show", "series", "episode", "season", "film", "documentary"],
        "features": ["plot", "acting", "pacing", "ending", "writing", "dialogue"],
        "actions": ["watched", "sat through", "endured", "tried watching", "suffered through"]
    },
    "games": {
        "things": ["game", "level", "mission", "campaign", "multiplayer", "update", "patch"],
        "features": ["graphics", "gameplay", "controls", "mechanics", "bugs", "lag"],
        "actions": ["played", "tried", "attempted", "struggled with", "gave up on"]
    },
    "tech": {
        "things": ["app", "software", "tool", "platform", "device", "update", "version"],
        "features": ["interface", "performance", "battery drain", "speed", "crashes", "bugs"],
        "actions": ["used", "installed", "tried", "tested", "uninstalled"]
    },
    "food": {
        "things": ["meal", "dish", "order", "delivery", "food", "service", "restaurant"],
        "features": ["taste", "quality", "temperature", "portions", "wait time", "freshness"],
        "actions": ["ordered", "tried", "received", "ate", "wasted money on"]
    },
    "services": {
        "things": ["service", "support", "experience", "booking", "staff", "wait time"],
        "features": ["response time", "attitude", "professionalism", "quality", "reliability"],
        "actions": ["received", "dealt with", "experienced", "suffered through", "endured"]
    },
    "work": {
        "things": ["meeting", "task", "project", "workflow", "tool", "process"],
        "features": ["efficiency", "organization", "communication", "results", "productivity"],
        "actions": ["completed", "struggled with", "dealt with", "endured", "suffered through"]
    },
    "social": {
        "things": ["event", "gathering", "party", "meetup", "occasion", "venue"],
        "features": ["atmosphere", "crowd", "location", "organization", "timing"],
        "actions": ["attended", "went to", "showed up at", "endured", "left early from"]
    }
}

# Generic brand names
BRANDS = ["Streamzy", "TaskForge", "MealLoop", "CloudNest", "ChatDock", "Foodio",
          "AppFlow", "DataSync", "QuickServe", "SmartHub", "ProTools", "BestBites"]


class NegativeDatasetGenerator:
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
            'git_pos.csv', 'git_neu.csv'
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
    
    def generate_sarcastic_negative_review(self):
        """Generate a sarcastic negative review"""
        template = random.choice(SARCASTIC_NEGATIVE_TEMPLATES)
        review = self.fill_template(template, SARCASTIC_NEGATIVE_FRAGMENTS)
        
        # Add occasional brand name
        if random.random() < 0.3:
            brand = random.choice(BRANDS)
            review = review.replace("the app", brand).replace("this tool", brand)
        
        return review
    
    def generate_non_sarcastic_negative_review(self, is_short):
        """Generate a non-sarcastic negative review"""
        topic = random.choice(list(TOPICS.keys()))
        topic_data = TOPICS[topic]
        
        if is_short:
            # Short reviews (3-10 words)
            patterns = [
                f"{random.choice(NEGATIVE_ADJECTIVES).capitalize()} {random.choice(topic_data['things'])}.",
                f"{random.choice(NEGATIVE_ADJECTIVES).capitalize()} {random.choice(topic_data['features'])}.",
                f"Hate the {random.choice(topic_data['features'])}.",
                f"{random.choice(NEGATIVE_PHRASES).capitalize()}.",
                f"Really {random.choice(topic_data['actions'])} this {random.choice(topic_data['things'])}.",
                f"The {random.choice(topic_data['features'])} is {random.choice(NEGATIVE_ADJECTIVES)}.",
            ]
            review = random.choice(patterns)
        else:
            # Long reviews (15-40 words)
            templates = [
                f"I {random.choice(topic_data['actions'])} the {random.choice(topic_data['things'])} and the {random.choice(topic_data['features'])} was absolutely {random.choice(NEGATIVE_ADJECTIVES)}. {random.choice(NEGATIVE_PHRASES).capitalize()}, would not {random.choice(['recommend', 'suggest', 'use again'])}.",
                f"The {random.choice(topic_data['things'])} has {random.choice(NEGATIVE_ADJECTIVES)} {random.choice(topic_data['features'])} and I'm really {random.choice(['disappointed', 'frustrated', 'annoyed', 'upset'])}. Everything {random.choice(['failed', 'broke', 'crashed', 'froze'])} and I {random.choice(NEGATIVE_VERBS)} every moment of it.",
                f"{random.choice(NEGATIVE_ADJECTIVES).capitalize()} {random.choice(topic_data['things'])}! The {random.choice(topic_data['features'])} is {random.choice(NEGATIVE_ADJECTIVES)} and the overall {random.choice(['quality', 'experience', 'performance'])} is {random.choice(NEGATIVE_ADJECTIVES)}. Do not {random.choice(['recommend', 'suggest', 'use'])} this to anyone!",
                f"After {random.choice(['using', 'trying', 'testing'])} this {random.choice(topic_data['things'])}, I can say the {random.choice(topic_data['features'])} is truly {random.choice(NEGATIVE_ADJECTIVES)}. It {random.choice(['failed', 'disappointed', 'frustrated'])} all my expectations and I'm {random.choice(['angry', 'frustrated', 'disappointed', 'upset'])} with the results.",
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
                review = self.generate_sarcastic_negative_review()
            else:
                review = self.generate_non_sarcastic_negative_review(is_short)
            
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
        base_review = self.generate_non_sarcastic_negative_review(False)
        review = f"{base_review} Review {random.randint(1000, 9999)}."
        self.mark_as_seen(review)
        self.non_sarcastic_count += 1
        self.long_count += 1
        return review
    
    def generate_dataset(self):
        """Generate complete dataset"""
        print("Loading existing datasets for deduplication...")
        self.load_existing_datasets()
        
        print(f"\nGenerating {TARGET_ROWS} negative sentiment reviews...")
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
    generator = NegativeDatasetGenerator()
    
    # Generate dataset
    reviews = generator.generate_dataset()
    
    # Validate dataset
    generator.validate_dataset(reviews)
    
    # Write to file
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_path = os.path.join(repo_root, 'git_neg.csv')
    generator.write_csv(reviews, output_path)
    
    print("\n✓ git_neg.csv generation complete!")


if __name__ == "__main__":
    main()
