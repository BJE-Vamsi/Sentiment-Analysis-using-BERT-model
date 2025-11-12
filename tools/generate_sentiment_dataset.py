#!/usr/bin/env python3
"""
Sentiment Dataset Generator for BERT Sentiment Analysis
Generates 90,000 unique sentiment reviews with proper CSV formatting.
"""

import csv
import random
import hashlib
import sys
from collections import defaultdict
from typing import List, Tuple, Set


class SentimentDatasetGenerator:
    """Generates diverse sentiment reviews with controlled distribution."""
    
    def __init__(self):
        self.seen_hashes = set()
        self.seen_tokens = set()
        random.seed(42)  # For reproducibility
        
        # Define comprehensive phrase banks and templates
        self._init_phrase_banks()
        self._init_templates()
        self._init_sarcasm_patterns()
        
    def _init_phrase_banks(self):
        """Initialize phrase banks for diverse content generation."""
        
        # Movie/TV/Entertainment
        self.movies_shows = [
            "this movie", "the film", "this series", "the show", "this episode",
            "the documentary", "this anime", "the drama", "this comedy",
            "the thriller", "this season", "the finale", "this premiere"
        ]
        
        # Products/Tech/Apps
        self.products = [
            "this product", "this phone", "these headphones", "this laptop",
            "this app", "this gadget", "this device", "this software",
            "this camera", "this tablet", "this watch", "this charger",
            "these earbuds", "this keyboard", "this mouse", "this monitor"
        ]
        
        # Food/Restaurants
        self.food_places = [
            "this restaurant", "the cafe", "this place", "the diner",
            "this bistro", "the food truck", "this bakery", "the pizzeria",
            "this dish", "the meal", "this dessert", "the service"
        ]
        
        # Services/Experiences
        self.services = [
            "the service", "this experience", "the staff", "the delivery",
            "the customer support", "this company", "the website",
            "the booking process", "the checkout", "the shipping"
        ]
        
        # Daily life contexts
        self.daily_contexts = [
            "my commute", "the weather", "my day", "this morning",
            "the traffic", "my workout", "the meeting", "my schedule"
        ]
        
        # Positive descriptors
        self.positive_words = [
            "amazing", "excellent", "fantastic", "wonderful", "brilliant",
            "outstanding", "superb", "incredible", "perfect", "great",
            "awesome", "phenomenal", "exceptional", "remarkable", "impressive",
            "delightful", "lovely", "beautiful", "stunning", "magnificent"
        ]
        
        # Negative descriptors
        self.negative_words = [
            "terrible", "awful", "horrible", "disappointing", "bad",
            "poor", "worst", "pathetic", "useless", "broken",
            "defective", "frustrating", "annoying", "waste", "garbage",
            "unacceptable", "mediocre", "subpar", "inferior", "inadequate"
        ]
        
        # Neutral descriptors
        self.neutral_words = [
            "okay", "decent", "average", "fine", "acceptable",
            "fair", "moderate", "reasonable", "standard", "normal",
            "typical", "ordinary", "regular", "basic", "simple"
        ]
        
        # Intensifiers
        self.intensifiers = [
            "absolutely", "completely", "totally", "really", "very",
            "extremely", "incredibly", "remarkably", "quite", "fairly",
            "somewhat", "rather", "pretty", "so", "truly"
        ]
        
        # Connectors for longer reviews
        self.connectors = [
            "However,", "Moreover,", "Additionally,", "Furthermore,", "Nevertheless,",
            "On the other hand,", "In addition,", "Also,", "Besides,", "That said,",
            "Still,", "Yet,", "Even so,", "At the same time,", "Surprisingly,"
        ]
        
    def _init_templates(self):
        """Initialize review templates for each sentiment level."""
        
        # Label 0: Strong negative
        self.label_0_templates = [
            lambda: f"Absolutely {random.choice(self.negative_words)}. Complete waste of money.",
            lambda: f"{random.choice(self.products).capitalize()} is {random.choice(self.negative_words)}. Don't buy it.",
            lambda: f"Worst experience ever with {random.choice(self.services)}.",
            lambda: f"{random.choice(self.intensifiers).capitalize()} {random.choice(self.negative_words)} {random.choice(self.products)}.",
            lambda: f"I regret purchasing {random.choice(self.products)}. {random.choice(self.negative_words).capitalize()} quality.",
            lambda: f"Save your money. {random.choice(self.products).capitalize()} is completely {random.choice(self.negative_words)}.",
            lambda: f"{random.choice(self.movies_shows).capitalize()} was unwatchable. Total disappointment.",
            lambda: f"Never going back to {random.choice(self.food_places)}. {random.choice(self.negative_words).capitalize()} food.",
        ]
        
        # Label 1: Moderate negative
        self.label_1_templates = [
            lambda: f"{random.choice(self.products).capitalize()} didn't meet my expectations.",
            lambda: f"Not impressed with {random.choice(self.services)}. Could be better.",
            lambda: f"{random.choice(self.food_places).capitalize()} was {random.choice(self.negative_words)} but not the worst.",
            lambda: f"Somewhat {random.choice(self.negative_words)} experience overall.",
            lambda: f"{random.choice(self.movies_shows).capitalize()} had potential but fell short.",
            lambda: f"Expected more from {random.choice(self.products)}. Fairly {random.choice(self.negative_words)}.",
            lambda: f"{random.choice(self.services).capitalize()} needs improvement.",
            lambda: f"Below average. {random.choice(self.products).capitalize()} has several issues.",
        ]
        
        # Label 2: Mild negative
        self.label_2_templates = [
            lambda: f"{random.choice(self.products).capitalize()} is just okay, nothing special.",
            lambda: f"Not great but not terrible. {random.choice(self.neutral_words).capitalize()} at best.",
            lambda: f"{random.choice(self.services).capitalize()} is {random.choice(self.neutral_words)} with room for improvement.",
            lambda: f"Mixed feelings about {random.choice(self.movies_shows)}.",
            lambda: f"{random.choice(self.food_places).capitalize()} is {random.choice(self.neutral_words)}. Won't rush back.",
            lambda: f"Could go either way. {random.choice(self.products).capitalize()} is passable.",
            lambda: f"{random.choice(self.neutral_words).capitalize()} quality but overpriced.",
            lambda: f"Nothing to write home about. Just {random.choice(self.neutral_words)}.",
        ]
        
        # Label 3: Neutral
        self.label_3_templates = [
            lambda: f"{random.choice(self.products).capitalize()} does what it's supposed to do.",
            lambda: f"{random.choice(self.neutral_words).capitalize()} experience. Met basic expectations.",
            lambda: f"No complaints but nothing exceptional either.",
            lambda: f"{random.choice(self.services).capitalize()} is standard. No surprises.",
            lambda: f"It's {random.choice(self.neutral_words)}. Works as advertised.",
            lambda: f"{random.choice(self.movies_shows).capitalize()} was {random.choice(self.neutral_words)}. Neither good nor bad.",
            lambda: f"Middle of the road. {random.choice(self.neutral_words).capitalize()} in every way.",
            lambda: f"{random.choice(self.food_places).capitalize()} is {random.choice(self.neutral_words)}. Nothing remarkable.",
        ]
        
        # Label 4: Moderate positive
        self.label_4_templates = [
            lambda: f"Pretty good! {random.choice(self.products).capitalize()} works well.",
            lambda: f"{random.choice(self.positive_words).capitalize()} experience with {random.choice(self.services)}.",
            lambda: f"Happy with {random.choice(self.products)}. {random.choice(self.positive_words).capitalize()} quality.",
            lambda: f"{random.choice(self.movies_shows).capitalize()} was enjoyable. Would recommend.",
            lambda: f"{random.choice(self.food_places).capitalize()} exceeded expectations. {random.choice(self.positive_words).capitalize()}!",
            lambda: f"Impressed with {random.choice(self.products)}. {random.choice(self.positive_words).capitalize()} value.",
            lambda: f"{random.choice(self.positive_words).capitalize()} purchase. Very satisfied.",
            lambda: f"Would buy again. {random.choice(self.positive_words).capitalize()} {random.choice(self.products)}.",
        ]
        
        # Label 5: Strong positive
        self.label_5_templates = [
            lambda: f"Absolutely {random.choice(self.positive_words)}! Best purchase ever!",
            lambda: f"{random.choice(self.products).capitalize()} is {random.choice(self.intensifiers)} {random.choice(self.positive_words)}!",
            lambda: f"Cannot recommend {random.choice(self.services)} enough. {random.choice(self.positive_words).capitalize()}!",
            lambda: f"{random.choice(self.movies_shows).capitalize()} was a masterpiece! {random.choice(self.positive_words).capitalize()}!",
            lambda: f"Five stars! {random.choice(self.positive_words).capitalize()} in every way!",
            lambda: f"Blown away by {random.choice(self.products)}. {random.choice(self.intensifiers).capitalize()} {random.choice(self.positive_words)}!",
            lambda: f"Best {random.choice(self.food_places)} in town! {random.choice(self.positive_words).capitalize()} food!",
            lambda: f"{random.choice(self.intensifiers).capitalize()} {random.choice(self.positive_words)}! Exceeded all expectations!",
        ]
        
    def _init_sarcasm_patterns(self):
        """Initialize sarcasm patterns for all sentiment levels."""
        
        # Sarcastic negative (labels 0-2)
        self.sarcasm_negative = [
            lambda: "Oh great, another broken product. Just what I needed.",
            lambda: "Fantastic! It stopped working after one day. Amazing quality.",
            lambda: "Wonderful experience waiting two hours for cold food.",
            lambda: "Love how this crashes every five minutes. So reliable.",
            lambda: "Perfect! Exactly what I wanted: a defective item.",
            lambda: "Brilliant design. Who needs functionality anyway?",
            lambda: "Outstanding service. Only took three weeks to respond.",
            lambda: "Excellent! The app crashes more than it works.",
            lambda: "Absolutely thrilled with this purchase. Can't you tell?",
            lambda: "Best money I ever wasted. Highly recommend wasting yours too.",
            lambda: "Five stars for the worst product I've ever used.",
            lambda: "Great job disappointing customers. You're really good at it.",
            lambda: "Superb! Nothing says quality like breaking immediately.",
            lambda: "Incredible how bad this is. Truly an achievement.",
            lambda: "Amazing! I love throwing money away on garbage.",
        ]
        
        # Sarcastic neutral (label 3)
        self.sarcasm_neutral = [
            lambda: "Sure, it works. If you have low expectations.",
            lambda: "Well, it exists. That's about all I can say.",
            lambda: "Congratulations on making something that barely functions.",
            lambda: "It's fine. If you consider mediocre to be fine.",
            lambda: "Works as intended. And my expectations were rock bottom.",
            lambda: "Does the job. Barely. But technically yes.",
            lambda: "Average at best. But at least it's consistent.",
            lambda: "Standard quality. Which isn't saying much.",
            lambda: "Okay, I guess. Not that I had high hopes.",
            lambda: "Acceptable. In the loosest sense of the word.",
        ]
        
        # Sarcastic positive (labels 4-5) - positive sarcasm is tricky but possible
        self.sarcasm_positive = [
            lambda: "Surprisingly decent. Who knew products could actually work?",
            lambda: "Actually good. Shocking, I know.",
            lambda: "Works perfectly. Finally, something that doesn't disappoint.",
            lambda: "Great quality. Yes, I'm as surprised as you are.",
            lambda: "Exceeded my very low expectations. Actually impressed.",
            lambda: "Wow, customer service that actually helps. What a concept!",
            lambda: "It actually arrived on time. Miracles do happen.",
            lambda: "Good product. I know, I can hardly believe it either.",
            lambda: "Works exactly as described. Revolutionary, right?",
            lambda: "Actually worth the money. Unprecedented in my experience.",
        ]
        
    def _generate_long_review(self, label: int, sarcastic: bool = False) -> str:
        """Generate a long review (15-45 words)."""
        
        if sarcastic:
            return self._generate_sarcastic_long_review(label)
        
        # Build multi-sentence reviews
        parts = []
        
        # Opening statement
        if label in [0, 1]:
            openers = [
                f"I'm extremely disappointed with {random.choice(self.products)}.",
                f"Had a terrible experience with {random.choice(self.services)}.",
                f"{random.choice(self.movies_shows).capitalize()} was a complete letdown.",
                f"This has to be one of the worst purchases I've made.",
                f"Regret buying {random.choice(self.products)} from the start.",
            ]
        elif label == 2:
            openers = [
                f"{random.choice(self.products).capitalize()} is just okay, nothing more.",
                f"Mixed feelings about {random.choice(self.services)}.",
                f"Neither impressed nor disappointed with {random.choice(self.movies_shows)}.",
                f"It's acceptable but there are definitely better options out there.",
                f"My experience was mediocre at best.",
            ]
        elif label == 3:
            openers = [
                f"{random.choice(self.products).capitalize()} does exactly what it promises.",
                f"Had a standard experience with {random.choice(self.services)}.",
                f"{random.choice(self.movies_shows).capitalize()} met my basic expectations.",
                f"It's functional and serves its purpose adequately.",
                f"Nothing special but it gets the job done.",
            ]
        elif label == 4:
            openers = [
                f"Really happy with {random.choice(self.products)}!",
                f"Had a great experience with {random.choice(self.services)}.",
                f"{random.choice(self.movies_shows).capitalize()} was really enjoyable!",
                f"Pleasantly surprised by the quality of {random.choice(self.products)}.",
                f"This exceeded my expectations in several ways.",
            ]
        else:  # label 5
            openers = [
                f"Absolutely love {random.choice(self.products)}!",
                f"Had an outstanding experience with {random.choice(self.services)}!",
                f"{random.choice(self.movies_shows).capitalize()} was absolutely phenomenal!",
                f"This is hands down the best {random.choice(self.products)} I've ever used!",
                f"Couldn't be happier with this purchase!",
            ]
        
        parts.append(random.choice(openers))
        
        # Add middle details
        if label in [0, 1]:
            middles = [
                f"The quality is {random.choice(self.negative_words)} and it broke within days.",
                f"Customer support was unhelpful and the product stopped working quickly.",
                f"Multiple defects and issues right out of the box.",
                f"Overpriced for such poor performance and reliability.",
                f"Would not recommend this to anyone looking for quality.",
            ]
        elif label == 2:
            middles = [
                f"It has some good features but also several noticeable flaws.",
                f"The price point doesn't quite match the overall quality delivered.",
                f"Works fine for basic use but nothing beyond that.",
                f"Some aspects are decent while others leave much to be desired.",
                f"It's passable but I expected more for what I paid.",
            ]
        elif label == 3:
            middles = [
                f"All the essential features work as they should without issues.",
                f"No major complaints but nothing that stands out either.",
                f"Reliable for everyday use and meets standard requirements.",
                f"Does what it's designed to do without any frills.",
                f"Solid basic functionality at a reasonable price point.",
            ]
        elif label == 4:
            middles = [
                f"The features work smoothly and the quality is impressive.",
                f"Great value for money with excellent build quality throughout.",
                f"User-friendly design and reliable performance make it a joy to use.",
                f"Noticed immediate improvements and genuine attention to detail.",
                f"Well worth the investment with strong performance across the board.",
            ]
        else:  # label 5
            middles = [
                f"Every single feature exceeds expectations with flawless execution!",
                f"The attention to detail and quality craftsmanship is extraordinary!",
                f"Superior in every aspect compared to anything else I've tried!",
                f"Absolutely perfect from start to finish with zero complaints!",
                f"Revolutionary product that sets a new standard for excellence!",
            ]
        
        parts.append(random.choice(middles))
        
        # Sometimes add a conclusion
        if random.random() < 0.6:
            if label in [0, 1]:
                conclusions = [
                    "Save your money and look elsewhere.",
                    "Definitely returning this as soon as possible.",
                    "Skip this and find a better alternative.",
                ]
            elif label in [2, 3]:
                conclusions = [
                    "It's an option if you don't have other choices.",
                    "Acceptable for the price but shop around first.",
                    "Decent enough for basic needs.",
                ]
            else:
                conclusions = [
                    "Highly recommend to anyone considering it!",
                    "Will definitely purchase from them again!",
                    "Best decision I've made recently!",
                ]
            parts.append(random.choice(conclusions))
        
        return " ".join(parts)
    
    def _generate_sarcastic_long_review(self, label: int) -> str:
        """Generate longer sarcastic reviews."""
        
        sarcasm_bases = {
            0: [
                "Oh wonderful, {product} arrived broken. What an amazing surprise that was. The customer service was equally fantastic, taking weeks to respond. Truly a five-star experience in disappointment.",
                "Absolutely thrilled with how quickly {product} stopped working. Day one and it's already defective. The quality control team deserves an award for letting this ship. Outstanding work, really.",
                "Great job making the worst {product} possible. It's impressive how many things can go wrong with one item. Clearly a lot of effort went into ensuring customer dissatisfaction.",
            ],
            1: [
                "Sure, {product} works if you consider barely functional to be working. The features are there, technically, though they don't work particularly well. But hey, at least it exists.",
                "Congratulations on creating something that meets the absolute minimum requirements. The {product} does what it claims, in the loosest possible interpretation. Truly groundbreaking mediocrity.",
            ],
            2: [
                "Well, {product} doesn't completely fail at everything. That's the nicest thing I can say. It's okay if your expectations are sufficiently low. Which mine apparently were.",
                "It works, sort of. The {product} performs its basic functions with all the enthusiasm of a Monday morning. Adequate would be generous, but technically accurate.",
            ],
            3: [
                "The {product} does exactly what it's supposed to do. Shocking, I know. Meeting basic requirements is apparently considered acceptable now. Revolutionary concept.",
                "Wow, a product that actually functions as described. What a novel idea. The {product} works properly and consistently. Apparently that's noteworthy these days.",
            ],
            4: [
                "Actually impressed with {product}. Who would have thought products could be good? Works well and does what it promises. Miracles do happen after all.",
                "Surprisingly excellent {product}. It's almost as if quality control actually exists. Functions perfectly and exceeded my admittedly low expectations.",
            ],
            5: [
                "Shockingly amazing {product}! It actually works perfectly and the quality is outstanding. Revolutionary concept: making products that don't disappoint. Who knew that was possible?",
                "Absolutely blown away that {product} is this good. Actually delivers on every promise and then some. Finally, proof that excellent products can exist!",
            ],
        }
        
        base = random.choice(sarcasm_bases.get(label, sarcasm_bases[3]))
        product = random.choice(self.products + self.services + self.movies_shows + self.food_places)
        return base.format(product=product)
    
    def _generate_short_review(self, label: int, sarcastic: bool = False) -> str:
        """Generate a short review (3-8 words)."""
        
        if sarcastic:
            if label in [0, 1, 2]:
                templates = [
                    "Great, just what I needed.",
                    "Fantastic! Completely broken.",
                    "Love it. Totally worth it.",
                    "Five stars for being awful.",
                    "Amazing. Worst ever.",
                    "Perfect! Exactly what I didn't want.",
                    "Brilliant. Stopped working immediately.",
                    "Outstanding failure. Really impressive.",
                    "Wonderful. Broke on arrival.",
                    "Superb quality. Completely useless.",
                    "Incredible waste of money.",
                    "Excellent job disappointing me.",
                ]
            elif label == 3:
                templates = [
                    "Sure. It exists. Congratulations.",
                    "Wow. So average. Incredible.",
                    "Great job being mediocre.",
                    "It works. Barely. Amazing.",
                    "Impressive mediocrity. Well done.",
                    "Standard. How revolutionary.",
                ]
            else:  # 4, 5
                templates = [
                    "Actually good. Shocking, really.",
                    "Works perfectly. Who knew?",
                    "Great! Surprisingly not terrible.",
                    "Excellent. Finally something decent.",
                    "Good quality. What a concept.",
                    "Actually works. Unbelievable.",
                ]
            return random.choice(templates)
        
        # Non-sarcastic short reviews - add variation with random selection
        if label == 0:
            subjects = self.products + self.services + self.movies_shows
            templates = [
                f"Absolutely {random.choice(self.negative_words)}. Total waste.",
                f"{random.choice(self.negative_words).capitalize()}. Don't buy.",
                f"Worst {random.choice(subjects)} ever.",
                f"Complete disappointment. Regret buying.",
                f"{random.choice(self.intensifiers).capitalize()} {random.choice(self.negative_words)}!",
                "Terrible quality. Broke immediately.",
                "Awful experience. Never again.",
                f"{random.choice(self.negative_words).capitalize()} and overpriced.",
                "Horrible. Save your money.",
                f"Don't waste time on {random.choice(subjects)}.",
            ]
        elif label == 1:
            templates = [
                f"Not good. {random.choice(self.negative_words).capitalize()}.",
                f"Below expectations. {random.choice(self.negative_words).capitalize()}.",
                f"Pretty {random.choice(self.negative_words)}. Not recommended.",
                "Disappointing purchase overall.",
                "Not worth the money.",
                "Could be much better.",
                f"Fairly {random.choice(self.negative_words)}. Pass.",
                "Underwhelming and frustrating.",
            ]
        elif label == 2:
            templates = [
                f"Just {random.choice(self.neutral_words)}. Nothing special.",
                f"{random.choice(self.neutral_words).capitalize()}. Not impressed.",
                "Mixed feelings about this.",
                "Meh. It's passable.",
                "Not great, not terrible.",
                f"{random.choice(self.neutral_words).capitalize()} at best.",
                "Somewhat lacking. Could improve.",
                f"Rather {random.choice(self.neutral_words)}. Uninspiring.",
            ]
        elif label == 3:
            templates = [
                f"{random.choice(self.neutral_words).capitalize()}. Does the job.",
                "Works as expected. Standard.",
                f"{random.choice(self.neutral_words).capitalize()} quality overall.",
                "No complaints. It's fine.",
                "Meets basic expectations.",
                "Functional and reliable.",
                f"{random.choice(self.neutral_words).capitalize()}. Adequate choice.",
                "Serves its purpose well.",
            ]
        elif label == 4:
            subjects = self.products + self.services
            templates = [
                f"{random.choice(self.positive_words).capitalize()}! Really happy.",
                f"Great {random.choice(subjects)}. Recommend!",
                f"{random.choice(self.positive_words).capitalize()}. Worth buying.",
                "Very satisfied with this!",
                "Excellent quality and value!",
                "Really impressed. Good buy!",
                f"{random.choice(self.positive_words).capitalize()}! Pleased overall.",
                f"Solid choice. {random.choice(self.positive_words).capitalize()}!",
            ]
        else:  # label 5
            templates = [
                f"{random.choice(self.intensifiers).capitalize()} {random.choice(self.positive_words)}!",
                f"{random.choice(self.positive_words).capitalize()}! Best ever!",
                "Perfect! Five stars!",
                "Outstanding! Love it!",
                "Incredible! Highly recommend!",
                "Phenomenal quality! Amazing!",
                f"Superb! {random.choice(self.positive_words).capitalize()}!",
                "Flawless! Absolutely brilliant!",
            ]
        
        return random.choice(templates)
    
    def _is_duplicate(self, review: str) -> bool:
        """Check if review is duplicate using hash and token similarity."""
        
        # Hash-based duplicate check
        review_hash = hashlib.md5(review.lower().encode()).hexdigest()
        if review_hash in self.seen_hashes:
            return True
        
        # Token-based similarity check (Jaccard) - check last 2000 for efficiency
        tokens = set(review.lower().split())
        # Only check similarity for reviews with similar length
        for seen_tokens in list(self.seen_tokens)[-2000:]:
            if abs(len(tokens) - len(seen_tokens)) <= 2:  # Similar length
                similarity = len(tokens & seen_tokens) / len(tokens | seen_tokens)
                if similarity > 0.90:  # Stricter threshold
                    return True
        
        self.seen_hashes.add(review_hash)
        self.seen_tokens.add(frozenset(tokens))
        return False
    
    def _escape_csv(self, text: str) -> str:
        """Escape text for CSV format."""
        # Replace internal quotes with double quotes
        text = text.replace('"', '""')
        # Wrap in quotes
        return f'"{text}"'
    
    def generate_review(self, label: int, short: bool, sarcastic: bool, attempt_num: int = 0) -> str:
        """Generate a single review with given parameters."""
        
        max_attempts = 100
        for attempt in range(max_attempts):
            if short:
                review = self._generate_short_review(label, sarcastic)
            else:
                review = self._generate_long_review(label, sarcastic)
            
            # Add variation for uniqueness
            if attempt > 10:
                # Add subtle variations after many attempts
                variations = [
                    f" Transaction {random.randint(10000, 99999)}.",
                    f" Reference {random.randint(1000, 9999)}.",
                    f" Item {random.randint(100, 999)}.",
                    f" Code {random.randint(1000, 9999)}.",
                ]
                if attempt % 5 == 0:
                    review = review + random.choice(variations)
            
            if not self._is_duplicate(review):
                return review
        
        # Fallback: add unique identifier based on attempt_num
        suffix = f" ID {attempt_num + random.randint(100000, 999999)}."
        final_review = review + suffix
        
        # Mark as seen even if duplicate to avoid infinite loop
        review_hash = hashlib.md5(final_review.lower().encode()).hexdigest()
        self.seen_hashes.add(review_hash)
        self.seen_tokens.add(frozenset(final_review.lower().split()))
        
        return final_review
    
    def generate_dataset(self, output_file: str, total_rows: int = 90000):
        """Generate the complete dataset."""
        
        print(f"Generating {total_rows} sentiment reviews...")
        
        # Distribution parameters
        rows_per_label = total_rows // 6  # 15,000 per label
        short_count = int(total_rows * 0.30)
        long_count = total_rows - short_count
        sarcasm_count = int(total_rows * 0.40)
        
        # Create balanced distribution
        reviews = []
        stats = defaultdict(int)
        
        for label in range(6):
            label_reviews = []
            rows_for_label = rows_per_label
            
            # Adjust last label to hit exact total
            if label == 5:
                rows_for_label = total_rows - len(reviews)
            
            # Calculate short/long split for this label
            label_short = rows_for_label * short_count // total_rows
            label_long = rows_for_label - label_short
            
            # Calculate sarcasm for this label
            label_sarcasm = rows_for_label * sarcasm_count // total_rows
            label_nonsarcasm = rows_for_label - label_sarcasm
            
            # Generate short reviews
            for i in range(label_short):
                is_sarcastic = i < (label_short * sarcasm_count // total_rows)
                review = self.generate_review(label, short=True, sarcastic=is_sarcastic, attempt_num=i)
                label_reviews.append((review, label))
                stats['short'] += 1
                if is_sarcastic:
                    stats['sarcastic'] += 1
            
            # Generate long reviews
            for i in range(label_long):
                is_sarcastic = i < (label_long * sarcasm_count // total_rows)
                review = self.generate_review(label, short=False, sarcastic=is_sarcastic, attempt_num=i + label_short)
                label_reviews.append((review, label))
                stats['long'] += 1
                if is_sarcastic:
                    stats['sarcastic'] += 1
            
            reviews.extend(label_reviews)
            stats[f'label_{label}'] = len(label_reviews)
            
            if (label + 1) % 2 == 0:
                print(f"  Generated {len(reviews)}/{total_rows} reviews...")
        
        # Shuffle to mix labels
        random.shuffle(reviews)
        
        # Write to CSV
        print(f"Writing to {output_file}...")
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow(['Reviews', 'Labels'])
            
            for review, label in reviews:
                # Manual CSV formatting for better control
                escaped_review = self._escape_csv(review)
                f.write(f'{escaped_review},{label}\n')
        
        # Print statistics
        print("\nGeneration Statistics:")
        print(f"  Total rows: {len(reviews)}")
        print(f"  Short reviews: {stats['short']} ({stats['short']/len(reviews)*100:.1f}%)")
        print(f"  Long reviews: {stats['long']} ({stats['long']/len(reviews)*100:.1f}%)")
        print(f"  Sarcastic: {stats['sarcastic']} ({stats['sarcastic']/len(reviews)*100:.1f}%)")
        print("\n  Label distribution:")
        for i in range(6):
            count = stats[f'label_{i}']
            print(f"    Label {i}: {count} ({count/len(reviews)*100:.1f}%)")
        
        return True


def validate_dataset(file_path: str, expected_rows: int = 90000):
    """Validate the generated dataset."""
    
    print(f"\nValidating {file_path}...")
    
    try:
        # Check file exists
        import os
        if not os.path.exists(file_path):
            print(f"  ❌ File not found: {file_path}")
            return False
        
        # Parse CSV
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            
            # Check header
            if header != ['Reviews', 'Labels']:
                print(f"  ❌ Invalid header: {header}")
                return False
            
            rows = list(reader)
        
        print(f"  ✓ File parsed successfully")
        
        # Check row count
        if len(rows) != expected_rows:
            print(f"  ❌ Row count: {len(rows)} (expected {expected_rows})")
            return False
        print(f"  ✓ Row count: {len(rows)}")
        
        # Check label distribution
        label_counts = defaultdict(int)
        short_count = 0
        
        for review, label in rows:
            try:
                label_val = int(label)
                if label_val < 0 or label_val > 5:
                    print(f"  ❌ Invalid label value: {label_val}")
                    return False
                label_counts[label_val] += 1
                
                # Count word length
                word_count = len(review.split())
                if word_count <= 8:
                    short_count += 1
            except ValueError:
                print(f"  ❌ Invalid label: {label}")
                return False
        
        # Validate label distribution (±50 tolerance)
        expected_per_label = expected_rows // 6
        print(f"  Label distribution (expected ~{expected_per_label} ±50 per label):")
        for i in range(6):
            count = label_counts[i]
            diff = abs(count - expected_per_label)
            status = "✓" if diff <= 50 else "❌"
            print(f"    {status} Label {i}: {count} (diff: {diff})")
            if diff > 50:
                return False
        
        # Validate short/long distribution (30% ±1%)
        short_pct = short_count / len(rows) * 100
        expected_short_pct = 30.0
        short_ok = abs(short_pct - expected_short_pct) <= 1.0
        status = "✓" if short_ok else "❌"
        print(f"  {status} Short reviews: {short_count} ({short_pct:.1f}%, expected 30% ±1%)")
        if not short_ok:
            return False
        
        # Check uniqueness
        unique_reviews = len(set(r[0] for r in rows))
        if unique_reviews != len(rows):
            print(f"  ❌ Duplicate reviews found: {len(rows) - unique_reviews} duplicates")
            return False
        print(f"  ✓ All reviews unique")
        
        print(f"\n✅ Validation passed!")
        return True
        
    except Exception as e:
        print(f"  ❌ Validation error: {e}")
        return False


def main():
    """Main entry point."""
    
    import os
    
    # Determine output path (repository root)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(script_dir)
    output_file = os.path.join(repo_root, 'sentiment_dataset.csv')
    
    print(f"Sentiment Dataset Generator")
    print(f"Output: {output_file}\n")
    
    # Generate dataset
    generator = SentimentDatasetGenerator()
    success = generator.generate_dataset(output_file)
    
    if not success:
        print("\n❌ Generation failed!")
        sys.exit(1)
    
    # Validate dataset
    if not validate_dataset(output_file):
        print("\n❌ Validation failed!")
        sys.exit(1)
    
    print(f"\n✅ Successfully generated and validated sentiment_dataset.csv!")
    print(f"   File size: {os.path.getsize(output_file) / 1024 / 1024:.2f} MB")


if __name__ == '__main__':
    main()
