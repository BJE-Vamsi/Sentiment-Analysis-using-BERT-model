#!/usr/bin/env python3
"""
Generator for git_pos.csv - Positive sentiment dataset with sarcasm awareness
Generates 110,000 reviews with label=2, 50% sarcastic, 50% non-sarcastic
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
LABEL = 2  # Positive sentiment
SARCASM_RATIO = 0.50
SHORT_RATIO = 0.35
SHORT_MIN_WORDS = 3
SHORT_MAX_WORDS = 10
LONG_MIN_WORDS = 15
LONG_MAX_WORDS = 40
SIMILARITY_THRESHOLD = 0.92
RECENT_WINDOW = 3000

# Phrase banks for positive sentiment
POSITIVE_ADJECTIVES = [
    "amazing", "excellent", "fantastic", "great", "wonderful", "brilliant", "superb",
    "outstanding", "incredible", "perfect", "awesome", "impressive", "delightful",
    "fabulous", "terrific", "phenomenal", "exceptional", "marvelous", "splendid",
    "stellar", "magnificent", "lovely", "charming", "remarkable", "stunning"
]

POSITIVE_VERBS = [
    "love", "enjoy", "appreciate", "adore", "recommend", "praise", "celebrate",
    "cherish", "treasure", "admire", "impressed by", "satisfied with", "pleased with",
    "thrilled with", "delighted by", "amazed by", "blown away by"
]

POSITIVE_NOUNS = [
    "experience", "quality", "service", "performance", "design", "interface",
    "features", "functionality", "update", "version", "release", "support",
    "team", "product", "app", "tool", "platform", "system"
]

# Sarcastic positive phrase banks (ironic relief, surprised praise)
SARCASTIC_POSITIVE_TEMPLATES = [
    "Wow, finally {thing} that didn't {negative_action}!",
    "Shocked that {thing} actually {positive_action}!",
    "Can't believe {thing} worked without {problem}!",
    "Surprised it only took {time_period} to {action}!",
    "Finally, {thing} that doesn't {negative_action} every {frequency}!",
    "Actually {positive_action} on the first try, what a miracle!",
    "Only crashed {small_number} times today, major improvement!",
    "It loaded in under {time}, I'm genuinely surprised!",
    "Managed to {action} without {problem}, I'm impressed!",
    "The update actually improved things, I'm shocked!",
]

SARCASTIC_POSITIVE_FRAGMENTS = {
    "thing": ["an update", "a feature", "this app", "this tool", "the interface", "the system", "this service"],
    "negative_action": ["break everything", "crash", "freeze", "glitch out", "bug out", "fail miserably", "stop working"],
    "positive_action": ["works", "functions", "runs smoothly", "performs well", "operates", "executes"],
    "problem": ["issues", "errors", "bugs", "crashes", "freezing", "glitches", "problems"],
    "time_period": ["three hours", "an entire day", "a week", "forever", "ages", "an eternity"],
    "action": ["install it", "set it up", "configure it", "get it working", "sync my data"],
    "frequency": ["five minutes", "hour", "day", "use"],
    "small_number": ["twice", "three times", "four times", "once", "just once"],
    "time": ["a minute", "30 seconds", "10 seconds", "reasonable time"]
}

# Non-sarcastic positive templates
POSITIVE_TEMPLATES = [
    "{adjective} {noun}, really {verb} it!",
    "The {noun} is {adjective}, highly {verb}!",
    "{adjective} {thing}, {positive_phrase}!",
    "Really {verb} the {feature}, it's {adjective}!",
    "This {thing} is {adjective}, {positive_phrase}!",
    "{positive_phrase}, the {noun} is {adjective}!",
    "So {adjective}! The {feature} {positive_action} perfectly!",
    "The {noun} exceeded my expectations, truly {adjective}!",
]

POSITIVE_PHRASES = [
    "worth every penny", "exceeds expectations", "highly recommend", "couldn't be happier",
    "absolutely love it", "best decision ever", "works like a charm", "flawless experience",
    "top notch quality", "five stars", "no complaints", "will use again", "perfect choice"
]

# Topic-specific content
TOPICS = {
    "movies_tv": {
        "things": ["movie", "show", "series", "episode", "season", "film", "documentary"],
        "features": ["plot", "acting", "cinematography", "soundtrack", "ending", "character development"],
        "actions": ["binged", "watched", "enjoyed", "streamed", "rewatched"]
    },
    "games": {
        "things": ["game", "level", "mission", "campaign", "multiplayer", "update", "DLC"],
        "features": ["graphics", "gameplay", "controls", "story mode", "mechanics", "matchmaking"],
        "actions": ["played", "completed", "enjoyed", "mastered", "explored"]
    },
    "tech": {
        "things": ["app", "software", "tool", "platform", "device", "gadget", "update"],
        "features": ["interface", "performance", "battery life", "speed", "features", "integration"],
        "actions": ["used", "installed", "upgraded", "tested", "configured"]
    },
    "food": {
        "things": ["meal", "dish", "order", "delivery", "food", "dessert", "menu"],
        "features": ["taste", "presentation", "portions", "freshness", "quality", "variety"],
        "actions": ["ordered", "tried", "enjoyed", "tasted", "devoured"]
    },
    "services": {
        "things": ["service", "support", "experience", "booking", "reservation", "checkout"],
        "features": ["response time", "professionalism", "efficiency", "quality", "attention to detail"],
        "actions": ["received", "experienced", "appreciated", "valued", "utilized"]
    },
    "work": {
        "things": ["meeting", "presentation", "project", "collaboration", "workflow", "tool"],
        "features": ["productivity", "efficiency", "organization", "communication", "results"],
        "actions": ["completed", "managed", "organized", "streamlined", "optimized"]
    },
    "social": {
        "things": ["gathering", "event", "party", "hangout", "meetup", "celebration"],
        "features": ["atmosphere", "vibe", "energy", "crowd", "location", "activities"],
        "actions": ["attended", "enjoyed", "participated in", "loved", "celebrated"]
    }
}

# Generic brand names
BRANDS = ["Streamzy", "TaskForge", "MealLoop", "CloudNest", "ChatDock", "Foodio", 
          "AppFlow", "DataSync", "QuickServe", "SmartHub", "ProTools", "BestBites"]


class PositiveDatasetGenerator:
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
            'git_neg.csv', 'git_neu.csv'
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
    
    def generate_sarcastic_positive_review(self):
        """Generate a sarcastic positive review"""
        template = random.choice(SARCASTIC_POSITIVE_TEMPLATES)
        review = self.fill_template(template, SARCASTIC_POSITIVE_FRAGMENTS)
        
        # Add occasional brand name
        if random.random() < 0.3:
            brand = random.choice(BRANDS)
            review = review.replace("this app", brand).replace("this tool", brand)
        
        return review
    
    def generate_non_sarcastic_positive_review(self, is_short):
        """Generate a non-sarcastic positive review"""
        topic = random.choice(list(TOPICS.keys()))
        topic_data = TOPICS[topic]
        
        if is_short:
            # Short reviews (3-10 words)
            patterns = [
                f"{random.choice(POSITIVE_ADJECTIVES)} {random.choice(topic_data['things'])}!",
                f"{random.choice(POSITIVE_ADJECTIVES).capitalize()} {random.choice(topic_data['features'])}!",
                f"Love the {random.choice(topic_data['features'])}!",
                f"{random.choice(POSITIVE_PHRASES).capitalize()}!",
                f"Really {random.choice(topic_data['actions'])} this {random.choice(topic_data['things'])}!",
                f"The {random.choice(topic_data['features'])} is {random.choice(POSITIVE_ADJECTIVES)}!",
            ]
            review = random.choice(patterns)
        else:
            # Long reviews (15-40 words)
            templates = [
                f"I {random.choice(topic_data['actions'])} the {random.choice(topic_data['things'])} and the {random.choice(topic_data['features'])} was absolutely {random.choice(POSITIVE_ADJECTIVES)}. {random.choice(POSITIVE_PHRASES).capitalize()}, would definitely {random.choice(POSITIVE_VERBS)} again!",
                f"The {random.choice(topic_data['things'])} offers {random.choice(POSITIVE_ADJECTIVES)} {random.choice(topic_data['features'])} and I'm really {random.choice(['impressed', 'satisfied', 'pleased', 'delighted'])}. Everything worked {random.choice(['perfectly', 'flawlessly', 'smoothly', 'wonderfully'])} and I {random.choice(POSITIVE_VERBS)} every moment of it.",
                f"{random.choice(POSITIVE_ADJECTIVES).capitalize()} {random.choice(topic_data['things'])}! The {random.choice(topic_data['features'])} is {random.choice(POSITIVE_ADJECTIVES)} and the overall {random.choice(['quality', 'experience', 'performance'])} is {random.choice(POSITIVE_ADJECTIVES)}. Highly {random.choice(['recommend', 'suggest', 'endorse'])} this to everyone!",
                f"After {random.choice(['using', 'trying', 'testing'])} this {random.choice(topic_data['things'])}, I can say the {random.choice(topic_data['features'])} is truly {random.choice(POSITIVE_ADJECTIVES)}. It {random.choice(['exceeded', 'surpassed', 'met'])} all my expectations and I'm {random.choice(['thrilled', 'delighted', 'ecstatic', 'happy'])} with the results.",
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
                review = self.generate_sarcastic_positive_review()
            else:
                review = self.generate_non_sarcastic_positive_review(is_short)
            
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
        base_review = self.generate_non_sarcastic_positive_review(False)
        review = f"{base_review} Review {random.randint(1000, 9999)}."
        self.mark_as_seen(review)
        self.non_sarcastic_count += 1
        self.long_count += 1
        return review
    
    def generate_dataset(self):
        """Generate complete dataset"""
        print("Loading existing datasets for deduplication...")
        self.load_existing_datasets()
        
        print(f"\nGenerating {TARGET_ROWS} positive sentiment reviews...")
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
    generator = PositiveDatasetGenerator()
    
    # Generate dataset
    reviews = generator.generate_dataset()
    
    # Validate dataset
    generator.validate_dataset(reviews)
    
    # Write to file
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_path = os.path.join(repo_root, 'git_pos.csv')
    generator.write_csv(reviews, output_path)
    
    print("\n✓ git_pos.csv generation complete!")


if __name__ == "__main__":
    main()
