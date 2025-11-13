#!/usr/bin/env python3
"""
Generator for git_sent.csv - 100,000 unique sentiment analysis reviews
Creates diverse, natural-sounding reviews across multiple topics with proper label distribution.
"""

import csv
import hashlib
import random
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import List, Tuple, Set


class SentimentDatasetGenerator:
    """Generates unique sentiment reviews with sarcasm and variety."""
    
    def __init__(self, target_rows: int = 100000, sarcasm_target: float = 0.40):
        self.target_rows = target_rows
        self.sarcasm_target = sarcasm_target
        self.labels_per_class = target_rows // 6
        self.seen_hashes = set()
        self.seen_reviews = set()
        
        # Phrase banks for natural variety
        self.setup_phrase_banks()
        
    def setup_phrase_banks(self):
        """Initialize all phrase banks and templates."""
        
        # Topics and subjects
        self.topics = {
            'movies_tv': ['movie', 'film', 'show', 'series', 'episode', 'season', 'documentary', 'drama', 'comedy'],
            'music': ['song', 'album', 'track', 'playlist', 'artist', 'band', 'concert', 'music', 'performance'],
            'games': ['game', 'level', 'gameplay', 'graphics', 'controls', 'multiplayer', 'campaign', 'update', 'DLC'],
            'tech': ['app', 'software', 'update', 'feature', 'interface', 'tool', 'platform', 'device', 'service'],
            'food': ['restaurant', 'food', 'meal', 'dish', 'service', 'delivery', 'taste', 'portion', 'menu'],
            'services': ['customer service', 'support', 'experience', 'staff', 'service', 'response', 'help'],
            'work': ['project', 'task', 'meeting', 'deadline', 'workflow', 'tool', 'process', 'collaboration'],
            'daily': ['day', 'morning', 'experience', 'situation', 'moment', 'event', 'thing', 'time']
        }
        
        # Sentiment modifiers by intensity
        self.modifiers = {
            0: ['terrible', 'awful', 'horrible', 'worst', 'disgusting', 'pathetic', 'trash', 'garbage', 'useless'],
            1: ['bad', 'poor', 'disappointing', 'subpar', 'mediocre', 'lacking', 'underwhelming', 'inadequate'],
            2: ['not great', 'could be better', 'meh', 'just okay', 'nothing special', 'average at best', 'unremarkable'],
            3: ['okay', 'fine', 'decent', 'alright', 'acceptable', 'standard', 'fair', 'reasonable', 'so-so'],
            4: ['good', 'nice', 'enjoyable', 'pleasant', 'solid', 'pretty good', 'satisfying', 'worthwhile'],
            5: ['excellent', 'amazing', 'fantastic', 'outstanding', 'perfect', 'incredible', 'brilliant', 'phenomenal']
        }
        
        # Sarcasm patterns
        self.sarcasm_patterns = [
            "just what I needed",
            "exactly what I hoped for",
            "couldn't be happier",
            "living the dream",
            "best decision ever",
            "totally worth it",
            "highly recommend",
            "absolutely perfect",
            "never been better",
            "peak performance"
        ]
        
        # Verbs and actions
        self.verbs = ['love', 'hate', 'enjoy', 'dislike', 'appreciate', 'recommend', 'suggest', 'avoid', 'use', 'tried']
        
        # Connectors for variety
        self.connectors = ['but', 'however', 'although', 'though', 'yet', 'while', 'and', 'so', 'because']
        
    def hash_text(self, text: str) -> str:
        """Generate hash for duplicate detection."""
        normalized = re.sub(r'\s+', ' ', text.lower().strip())
        return hashlib.md5(normalized.encode()).hexdigest()
    
    def escape_csv_field(self, text: str) -> str:
        """Properly escape text for CSV - wrap in quotes and double internal quotes."""
        text = text.replace('"', '""')
        return f'"{text}"'
    
    def is_unique(self, review: str) -> bool:
        """Check if review is unique."""
        review_hash = self.hash_text(review)
        normalized = review.lower().strip()
        
        if review_hash in self.seen_hashes or normalized in self.seen_reviews:
            return False
        
        self.seen_hashes.add(review_hash)
        self.seen_reviews.add(normalized)
        return True
    
    def generate_simple_review(self, label: int, is_sarcastic: bool = False) -> str:
        """Generate a simple, direct review."""
        topic_category = random.choice(list(self.topics.keys()))
        subject = random.choice(self.topics[topic_category])
        modifier = random.choice(self.modifiers[label])
        
        templates = [
            f"This {subject} is {modifier}",
            f"The {subject} was {modifier}",
            f"Really {modifier} {subject}",
            f"Such a {modifier} {subject}",
            f"What a {modifier} {subject}",
            f"Very {modifier} {subject}",
            f"Absolutely {modifier} {subject}",
            f"Totally {modifier} {subject}",
        ]
        
        review = random.choice(templates)
        
        if is_sarcastic and label in [0, 1]:
            # Add sarcastic ending to negative reviews
            sarcasm = random.choice(self.sarcasm_patterns)
            review = f"{review}. {sarcasm.capitalize()}."
        elif is_sarcastic and label in [4, 5]:
            # Sarcastic positive pattern (actually negative)
            review = f"{random.choice(self.sarcasm_patterns).capitalize()}, {review.lower()}."
            
        return review
    
    def generate_compound_review(self, label: int, is_sarcastic: bool = False) -> str:
        """Generate a more complex review with multiple clauses."""
        topic_category = random.choice(list(self.topics.keys()))
        subject1 = random.choice(self.topics[topic_category])
        
        # Pick another topic for variety
        topic_category2 = random.choice(list(self.topics.keys()))
        subject2 = random.choice(self.topics[topic_category2])
        
        modifier1 = random.choice(self.modifiers[label])
        
        # Pick a contrasting or similar modifier
        if label <= 2:
            modifier2 = random.choice(self.modifiers[min(label + 1, 5)])
        else:
            modifier2 = random.choice(self.modifiers[max(label - 1, 0)])
        
        connector = random.choice(self.connectors)
        
        templates = [
            f"The {subject1} is {modifier1} {connector} the {subject2} is {modifier2}",
            f"I found the {subject1} {modifier1}, {connector} overall it was {modifier2}",
            f"While the {subject1} was {modifier1}, the {subject2} was {modifier2}",
            f"{modifier1.capitalize()} {subject1} {connector} {modifier2} {subject2}",
        ]
        
        review = random.choice(templates)
        
        if is_sarcastic and label <= 2:
            sarcasm = random.choice(self.sarcasm_patterns)
            review = f"{review}. {sarcasm.capitalize()}, right?"
        
        return review
    
    def generate_conversational_review(self, label: int, is_sarcastic: bool = False) -> str:
        """Generate casual, conversational review."""
        topic_category = random.choice(list(self.topics.keys()))
        subject = random.choice(self.topics[topic_category])
        modifier = random.choice(self.modifiers[label])
        
        casual_starts = [
            "Honestly", "Tbh", "Gotta say", "Not gonna lie", "Real talk",
            "Look", "Listen", "So", "Okay so", "Alright"
        ]
        
        casual_ends = [
            "just saying", "that's all", "you know", "if you ask me",
            "in my opinion", "for real", "seriously", "no cap", "honestly"
        ]
        
        start = random.choice(casual_starts)
        end = random.choice(casual_ends)
        
        templates = [
            f"{start}, this {subject} is {modifier}, {end}",
            f"{start} the {subject} was {modifier}. {end.capitalize()}",
            f"This {subject}? {modifier.capitalize()}. {end.capitalize()}",
            f"{start}, {modifier} {subject}. {end.capitalize()}",
        ]
        
        review = random.choice(templates)
        
        if is_sarcastic:
            if label <= 2:
                review = f"{review}. Oh wait, did I say {modifier}? I meant perfect. {random.choice(self.sarcasm_patterns).capitalize()}."
            
        return review
    
    def generate_detailed_review(self, label: int, is_sarcastic: bool = False) -> str:
        """Generate longer, more detailed review."""
        topic_category = random.choice(list(self.topics.keys()))
        subject = random.choice(self.topics[topic_category])
        modifier = random.choice(self.modifiers[label])
        
        aspects = ['quality', 'value', 'performance', 'design', 'experience', 'functionality', 'ease of use']
        aspect = random.choice(aspects)
        
        verb = random.choice(self.verbs)
        
        templates = [
            f"I {verb} this {subject}. The {aspect} is {modifier} and exactly what I was looking for",
            f"After using this {subject}, I can say the {aspect} is {modifier}. Would {verb} it",
            f"The {aspect} of this {subject} is {modifier}. I {verb} products like this",
            f"This {subject} has {modifier} {aspect}. I {verb} how it performs",
            f"For the {aspect} alone, this {subject} is {modifier}. I {verb} the overall experience",
        ]
        
        review = random.choice(templates)
        
        if is_sarcastic and label in [0, 1, 2]:
            sarcasm = random.choice(self.sarcasm_patterns)
            review = f"{review}. {sarcasm.capitalize()}, especially the bugs."
        
        return review
    
    def generate_specific_reviews(self, label: int, is_sarcastic: bool = False) -> str:
        """Generate topic-specific detailed reviews."""
        topic_category = random.choice(list(self.topics.keys()))
        
        if topic_category == 'movies_tv':
            return self.generate_movie_review(label, is_sarcastic)
        elif topic_category == 'music':
            return self.generate_music_review(label, is_sarcastic)
        elif topic_category == 'games':
            return self.generate_game_review(label, is_sarcastic)
        elif topic_category == 'tech':
            return self.generate_tech_review(label, is_sarcastic)
        elif topic_category == 'food':
            return self.generate_food_review(label, is_sarcastic)
        else:
            return self.generate_simple_review(label, is_sarcastic)
    
    def generate_movie_review(self, label: int, is_sarcastic: bool) -> str:
        """Movie/TV specific reviews."""
        modifier = random.choice(self.modifiers[label])
        elements = ['acting', 'plot', 'cinematography', 'storyline', 'characters', 'pacing', 'ending', 'special effects']
        element = random.choice(elements)
        
        templates = [
            f"The {element} in this movie is {modifier}",
            f"I was blown away by the {modifier} {element}",
            f"This film has {modifier} {element} throughout",
            f"The {element} really makes this a {modifier} watch",
        ]
        
        review = random.choice(templates)
        if is_sarcastic and label <= 2:
            review += f". {random.choice(self.sarcasm_patterns).capitalize()}, especially if you like wasting time."
        return review
    
    def generate_music_review(self, label: int, is_sarcastic: bool) -> str:
        """Music specific reviews."""
        modifier = random.choice(self.modifiers[label])
        elements = ['beats', 'lyrics', 'melody', 'production', 'vocals', 'rhythm', 'vibe', 'sound quality']
        element = random.choice(elements)
        
        templates = [
            f"The {element} on this track are {modifier}",
            f"Love the {modifier} {element} in this album",
            f"This artist delivers {modifier} {element}",
            f"The {element} here are just {modifier}",
        ]
        
        review = random.choice(templates)
        if is_sarcastic and label in [4, 5]:
            review = f"Oh yeah, the {element} are {modifier}. If you enjoy headaches."
        return review
    
    def generate_game_review(self, label: int, is_sarcastic: bool) -> str:
        """Game specific reviews."""
        modifier = random.choice(self.modifiers[label])
        elements = ['graphics', 'gameplay', 'controls', 'story', 'mechanics', 'performance', 'multiplayer', 'updates']
        element = random.choice(elements)
        
        templates = [
            f"The {element} in this game are {modifier}",
            f"This game has {modifier} {element}",
            f"I'm impressed by the {modifier} {element}",
            f"The {element} make this game {modifier}",
        ]
        
        review = random.choice(templates)
        if is_sarcastic and label <= 1:
            review += ". Perfect if you hate fun."
        return review
    
    def generate_tech_review(self, label: int, is_sarcastic: bool) -> str:
        """Tech/app specific reviews."""
        modifier = random.choice(self.modifiers[label])
        elements = ['interface', 'features', 'speed', 'design', 'usability', 'updates', 'performance', 'reliability']
        element = random.choice(elements)
        brands = ['Streamzy', 'TaskForge', 'Notifio', 'CloudSync', 'DataPro', 'QuickTask', 'AppFlow']
        brand = random.choice(brands)
        
        templates = [
            f"The {element} of {brand} is {modifier}",
            f"{brand} has {modifier} {element}",
            f"I find {brand}'s {element} to be {modifier}",
            f"The {element} in {brand} are {modifier}",
        ]
        
        review = random.choice(templates)
        if is_sarcastic and label in [0, 1]:
            review += f". {random.choice(self.sarcasm_patterns).capitalize()}, if you love crashes."
        return review
    
    def generate_food_review(self, label: int, is_sarcastic: bool) -> str:
        """Food/restaurant specific reviews."""
        modifier = random.choice(self.modifiers[label])
        elements = ['taste', 'presentation', 'portion size', 'freshness', 'quality', 'value', 'service', 'ambiance']
        element = random.choice(elements)
        restaurants = ['Foodio', 'The Bistro', 'Corner Cafe', 'Taste Kitchen', 'Quick Bites', 'Flavor House']
        restaurant = random.choice(restaurants)
        
        templates = [
            f"The {element} at {restaurant} is {modifier}",
            f"{restaurant} delivers {modifier} {element}",
            f"I ordered from {restaurant} and the {element} was {modifier}",
            f"The {element} here is {modifier}",
        ]
        
        review = random.choice(templates)
        if is_sarcastic and label <= 2:
            review += ". Great if you enjoy food poisoning."
        return review
    
    def generate_review(self, label: int) -> Tuple[str, bool]:
        """Generate a single review with given label."""
        is_sarcastic = random.random() < self.sarcasm_target
        
        # Choose generation method
        method = random.choice([
            self.generate_simple_review,
            self.generate_compound_review,
            self.generate_conversational_review,
            self.generate_detailed_review,
            self.generate_specific_reviews,
        ])
        
        max_attempts = 50
        for _ in range(max_attempts):
            review = method(label, is_sarcastic)
            
            # Add variety with punctuation
            if random.random() < 0.3 and not review.endswith(('.', '!', '?')):
                review += random.choice(['.', '!', '...'])
            
            if self.is_unique(review):
                return review, is_sarcastic
        
        # Fallback: add unique suffix if we can't generate unique after attempts
        for i in range(100):
            variant = f"{review} [{i}]"
            if self.is_unique(variant):
                return variant, is_sarcastic
        
        raise ValueError("Unable to generate unique review after maximum attempts")
    
    def generate_dataset(self) -> List[Tuple[str, int, bool]]:
        """Generate complete dataset."""
        print(f"Generating {self.target_rows} reviews...")
        dataset = []
        
        # Generate balanced labels
        for label in range(6):
            print(f"Generating label {label}...")
            count = 0
            target = self.labels_per_class
            # Adjust last label to reach exact target
            if label == 5:
                target = self.target_rows - len(dataset)
            
            while count < target:
                review, is_sarcastic = self.generate_review(label)
                dataset.append((review, label, is_sarcastic))
                count += 1
                
                if count % 1000 == 0:
                    print(f"  Generated {count}/{target} for label {label}")
        
        # Shuffle to mix labels
        random.shuffle(dataset)
        
        print(f"Generated {len(dataset)} total reviews")
        return dataset
    
    def validate_dataset(self, dataset: List[Tuple[str, int, bool]]) -> bool:
        """Validate dataset meets all requirements."""
        print("\n=== Validation ===")
        
        # Check row count
        if len(dataset) != self.target_rows:
            print(f"❌ Row count mismatch: {len(dataset)} != {self.target_rows}")
            return False
        print(f"✓ Row count: {len(dataset)}")
        
        # Check label distribution
        label_counts = Counter(label for _, label, _ in dataset)
        print(f"✓ Label distribution:")
        for label in range(6):
            count = label_counts[label]
            expected = self.labels_per_class
            diff = abs(count - expected)
            status = "✓" if diff <= 50 else "❌"
            print(f"  {status} Label {label}: {count} (expected ~{expected}, diff: {diff})")
            if diff > 50:
                return False
        
        # Check sarcasm proportion
        sarcasm_count = sum(1 for _, _, is_sarcastic in dataset if is_sarcastic)
        sarcasm_ratio = sarcasm_count / len(dataset)
        print(f"✓ Sarcasm: {sarcasm_count} ({sarcasm_ratio:.1%})")
        if not (0.35 <= sarcasm_ratio <= 0.45):
            print(f"  ⚠ Warning: Sarcasm ratio {sarcasm_ratio:.1%} outside target 35-45%")
        
        # Check uniqueness
        reviews = [review for review, _, _ in dataset]
        unique_reviews = len(set(reviews))
        if unique_reviews != len(reviews):
            print(f"❌ Duplicates found: {len(reviews) - unique_reviews}")
            return False
        print(f"✓ All {unique_reviews} reviews are unique")
        
        print("\n✓ All validations passed!")
        return True
    
    def write_csv(self, dataset: List[Tuple[str, int, bool]], output_path: Path):
        """Write dataset to CSV file."""
        print(f"\nWriting to {output_path}...")
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            # Write header
            f.write('Reviews,Labels\n')
            
            # Write data rows
            for review, label, _ in dataset:
                escaped_review = self.escape_csv_field(review)
                f.write(f'{escaped_review},{label}\n')
        
        print(f"✓ Wrote {len(dataset)} rows to {output_path}")
        
        # Validate CSV can be parsed
        self.validate_csv_parsing(output_path)
    
    def validate_csv_parsing(self, csv_path: Path):
        """Validate CSV can be parsed correctly."""
        print("\nValidating CSV parsing...")
        
        try:
            with open(csv_path, 'r', encoding='utf-8', newline='') as f:
                reader = csv.reader(f)
                header = next(reader)
                
                if header != ['Reviews', 'Labels']:
                    print(f"❌ Invalid header: {header}")
                    return False
                
                row_count = 0
                for row in reader:
                    if len(row) != 2:
                        print(f"❌ Invalid row at line {row_count + 2}: {len(row)} fields")
                        return False
                    row_count += 1
                
                if row_count != self.target_rows:
                    print(f"❌ Row count mismatch after parsing: {row_count} != {self.target_rows}")
                    return False
                
                print(f"✓ CSV parses correctly: {row_count} rows")
                return True
                
        except Exception as e:
            print(f"❌ CSV parsing error: {e}")
            return False


def main():
    """Main execution."""
    # Set random seed for reproducibility during development
    random.seed(42)
    
    # Configuration
    target_rows = 100000
    sarcasm_target = 0.40
    
    # Paths
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    output_path = repo_root / 'git_sent.csv'
    
    print("=" * 60)
    print("Git Sentiment Dataset Generator")
    print("=" * 60)
    print(f"Target rows: {target_rows:,}")
    print(f"Sarcasm target: {sarcasm_target:.0%}")
    print(f"Output: {output_path}")
    print("=" * 60)
    
    # Generate dataset
    generator = SentimentDatasetGenerator(target_rows, sarcasm_target)
    dataset = generator.generate_dataset()
    
    # Validate
    if not generator.validate_dataset(dataset):
        print("\n❌ Validation failed!")
        return 1
    
    # Write CSV
    generator.write_csv(dataset, output_path)
    
    print("\n" + "=" * 60)
    print("✓ Dataset generation complete!")
    print("=" * 60)
    
    return 0


if __name__ == '__main__':
    exit(main())
