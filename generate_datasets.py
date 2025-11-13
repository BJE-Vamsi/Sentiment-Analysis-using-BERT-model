#!/usr/bin/env python3
"""
Generate sarcasm-aware sentiment analysis datasets for BERT training.
Creates three CSV files with positive, negative, and neutral sentiments,
each containing 100,000 examples (50% sarcastic, 50% normal).
"""

import csv
import random
from typing import List, Tuple

# Set random seed for reproducibility
random.seed(42)


# Positive sentiment templates (normal)
POSITIVE_NORMAL_TEMPLATES = [
    "I absolutely love {product}! It exceeded all my expectations.",
    "{product} is fantastic! Highly recommend it to everyone.",
    "This {product} is amazing! Best purchase I've made this year.",
    "I'm so happy with my {product}. It works perfectly!",
    "{product} is excellent quality. Worth every penny.",
    "Great {product}! I'm very satisfied with the performance.",
    "The {product} is wonderful. I use it every day.",
    "{product} has made my life so much easier. Thank you!",
    "I'm impressed by how good this {product} is.",
    "This {product} is brilliant! Couldn't be happier.",
    "The {product} arrived quickly and works beautifully.",
    "I'm loving every minute with my new {product}.",
    "Perfect {product}! Exactly what I was looking for.",
    "This {product} is outstanding. Five stars!",
    "The {product} quality is superb. Very pleased.",
    "{product} is the best investment I've made recently.",
    "I adore this {product}. It's simply perfect.",
    "Absolutely delighted with my {product} purchase.",
    "The {product} performs exceptionally well.",
    "I can't stop raving about this {product}!",
    "Incredible value! This {product} is worth every cent.",
    "The {product} has transformed my daily routine for the better.",
    "I'm thoroughly enjoying my {product} experience.",
    "This {product} delivers on all its promises and more.",
    "The {product} quality and performance are top-notch.",
    "I'm genuinely thrilled with my {product} choice.",
    "This {product} has become an essential part of my day.",
    "The {product} works flawlessly. Highly satisfied!",
    "I couldn't have asked for a better {product}.",
    "This {product} is a game-changer. Absolutely love it!",
    "The {product} exceeded my high expectations. Brilliant!",
    "I'm completely satisfied with this {product} purchase.",
    "This {product} is everything I hoped for and more.",
    "The {product} reliability is outstanding. Very impressed.",
    "I would definitely buy this {product} again!",
    "This {product} is a fantastic addition to my life.",
    "The {product} craftsmanship is impeccable.",
    "I'm delighted with how well this {product} works.",
    "This {product} has proven to be an excellent choice.",
    "The {product} is simply magnificent. Love it!",
]

# Positive sentiment templates (sarcastic)
POSITIVE_SARCASTIC_TEMPLATES = [
    "Wow, {product} finally did something right for once!",
    "Oh look, {product} actually works! What a miracle!",
    "Believe it or not, this {product} didn't break immediately!",
    "Color me shocked, {product} exceeded my rock-bottom expectations!",
    "Well well, {product} managed to function properly. Amazing!",
    "Who would've thought? {product} actually delivered this time!",
    "Fantastic! {product} only crashed twice today instead of ten times!",
    "Finally! An update to {product} that didn't break everything!",
    "Incredible! The {product} worked on the first try! Must be a glitch.",
    "Oh great, {product} decided to cooperate today. How generous!",
    "Wow, {product} actually lived up to half of its promises!",
    "Amazing! The {product} only has minor issues instead of major ones!",
    "Look at that, {product} works almost as advertised! Progress!",
    "Well done {product}, you've managed to be mediocre!",
    "Bravo! {product} is only slightly disappointing this time!",
    "Oh wonderful, {product} exceeded my incredibly low expectations!",
    "Congratulations {product}, you're less terrible than before!",
    "Shocking! The {product} actually does what it claims! Barely.",
    "Finally, {product} works! Only took them five attempts!",
    "How nice, {product} didn't completely fail this time!",
    "Well look at you, {product}! Being almost functional!",
    "Impressive! The {product} only failed three times today!",
    "Oh my, {product} managed not to disappoint completely!",
    "Remarkable! The {product} actually started up without errors!",
    "Surprised? Me too! The {product} sort of works!",
    "Unbelievable! {product} didn't crash immediately for once!",
    "Well, well! The {product} is only half-broken today!",
    "Color me amazed, {product} is slightly better than awful!",
    "Fantastic news! {product} works marginally better now!",
    "Oh joy, {product} has managed to meet minimal standards!",
    "Shocking development! The {product} isn't completely useless!",
    "Well done! {product} exceeded zero expectations!",
    "Miraculously, the {product} functions somewhat properly!",
    "Oh look, {product} works when the stars align!",
    "Wonderful! The {product} is only terrible, not catastrophic!",
    "Great job {product}, you're mediocre instead of horrible!",
    "Fantastic! {product} barely meets basic requirements!",
    "How impressive, {product} works most of the time now!",
    "Oh brilliant, {product} is almost worth the money!",
    "Amazing! The {product} does half of what it promises!",
]

# Negative sentiment templates (normal)
NEGATIVE_NORMAL_TEMPLATES = [
    "I'm very disappointed with this {product}. Complete waste of money.",
    "The {product} is terrible. I regret buying it.",
    "This {product} broke after just one week. Poor quality.",
    "I hate this {product}. It never works properly.",
    "{product} is awful. Don't waste your time or money.",
    "Worst {product} ever. I want my money back.",
    "The {product} is completely useless. Total garbage.",
    "I'm so frustrated with this {product}. Nothing but problems.",
    "This {product} is a disaster. Doesn't work at all.",
    "Absolutely horrible {product}. Would give zero stars if possible.",
    "The {product} quality is abysmal. Very dissatisfied.",
    "I deeply regret purchasing this {product}.",
    "This {product} is a complete failure. Save your money.",
    "The {product} is defective and unreliable.",
    "I'm extremely unhappy with this {product}.",
    "{product} is poorly made and overpriced.",
    "This {product} is a huge disappointment.",
    "The {product} stopped working immediately. Terrible.",
    "I would not recommend this {product} to anyone.",
    "This {product} is frustrating and poorly designed.",
    "The {product} is worthless. Total waste of money.",
    "I'm furious about this {product} purchase.",
    "This {product} is the worst I've ever used.",
    "The {product} failed within days. Unacceptable!",
    "I can't believe how bad this {product} is.",
    "This {product} is cheaply made and breaks easily.",
    "The {product} does not work as advertised. Scam!",
    "I'm very unhappy with my {product} experience.",
    "This {product} is substandard and overpriced.",
    "The {product} is riddled with defects.",
    "I want a full refund for this {product}.",
    "This {product} is pathetic. Don't buy it!",
    "The {product} broke down after minimal use.",
    "I'm disgusted with this {product} quality.",
    "This {product} is a complete rip-off.",
    "The {product} malfunctioned from day one.",
    "I strongly advise against buying this {product}.",
    "This {product} is shoddily constructed.",
    "The {product} is an absolute nightmare to use.",
    "I've never been so disappointed with a {product}.",
]

# Negative sentiment templates (sarcastic)
NEGATIVE_SARCASTIC_TEMPLATES = [
    "Oh great, another {product} update that broke everything again!",
    "Thanks {product}, for wasting three hours of my life!",
    "Wonderful! The {product} crashed right when I needed it most!",
    "Oh fantastic, {product} decided not to work today. How surprising!",
    "Just what I wanted! A {product} that doesn't do anything!",
    "Oh joy, {product} has found a new way to disappoint me!",
    "How delightful, the {product} failed spectacularly once again!",
    "Perfect timing! {product} stopped working right before my deadline!",
    "Oh brilliant, {product} comes with bonus bugs at no extra charge!",
    "Thanks {product}, for making my day infinitely worse!",
    "How thoughtful! {product} deleted all my work. So helpful!",
    "Oh lovely, {product} crashes every five minutes. Very reliable!",
    "Just amazing! The {product} is even worse than advertised!",
    "Oh wonderful, {product} has outdone itself with this failure!",
    "Thanks for nothing, {product}. Absolutely useless!",
    "How nice, {product} wasted my money and my time!",
    "Oh spectacular, {product} managed to be even worse today!",
    "Just perfect! The {product} doesn't work at all. Fantastic!",
    "Oh terrific, {product} has more bugs than features!",
    "How generous! {product} provided disappointment at premium pricing!",
    "Brilliant! {product} found yet another way to fail!",
    "Oh marvelous, {product} ruined my entire project!",
    "Thanks {product}, for the constant frustration!",
    "How wonderful! The {product} broke again. What a surprise!",
    "Oh excellent, {product} wasted another hour of my time!",
    "Just superb! {product} crashes more reliably than it runs!",
    "How amazing! The {product} does nothing it promised!",
    "Oh fantastic, {product} is worse with every update!",
    "Thanks a lot {product}, for absolutely nothing!",
    "How delightful! {product} failed at the worst possible moment!",
    "Oh brilliant work {product}, breaking things as usual!",
    "Just wonderful! The {product} is gloriously useless!",
    "How nice! {product} exceeded my worst expectations!",
    "Oh perfect, {product} crashed during an important task!",
    "Thanks {product}, for being consistently terrible!",
    "How lovely! The {product} stopped working completely!",
    "Oh great job {product}, you've outdone yourself in awfulness!",
    "Just marvelous! {product} wastes time like no other!",
    "How spectacular! The {product} fails in new ways daily!",
    "Oh fantastic! {product} is worse than I could have imagined!",
]

# Neutral sentiment templates (normal)
NEUTRAL_NORMAL_TEMPLATES = [
    "The {product} is okay. It does what it's supposed to do.",
    "This {product} is average. Nothing special but functional.",
    "{product} works fine. No major complaints.",
    "The {product} is decent enough for basic use.",
    "This {product} is acceptable. Gets the job done.",
    "{product} is a standard product. Meets basic expectations.",
    "The {product} is alright. Not great, not terrible.",
    "This {product} is pretty standard. No surprises.",
    "{product} is functional and reasonably priced.",
    "The {product} does its job. Nothing remarkable.",
    "This {product} is satisfactory for everyday use.",
    "{product} is an okay choice if you need something basic.",
    "The {product} works as described. Fair quality.",
    "This {product} is neither impressive nor disappointing.",
    "{product} is a reasonable option for the price.",
    "The {product} performs adequately for simple tasks.",
    "This {product} is moderate quality. Standard features.",
    "{product} is acceptable for occasional use.",
    "The {product} is fine for what it is.",
    "This {product} meets minimum requirements.",
    "The {product} is serviceable. Nothing more, nothing less.",
    "{product} is a middle-of-the-road choice.",
    "This {product} is decent for basic needs.",
    "The {product} functions as expected. Standard quality.",
    "{product} is an ordinary product. No complaints.",
    "This {product} is passable for simple tasks.",
    "The {product} is a fair option at this price point.",
    "{product} works well enough for my needs.",
    "This {product} is a typical example of its category.",
    "The {product} is neither good nor bad. Just average.",
    "{product} serves its purpose adequately.",
    "This {product} is a basic, functional option.",
    "The {product} meets standard expectations.",
    "{product} is a reasonable purchase for the price.",
    "This {product} is average in every way.",
    "The {product} performs as one would expect.",
    "{product} is a conventional choice. No surprises.",
    "This {product} does what it claims to do.",
    "The {product} is a middle-tier option.",
    "{product} is acceptable for general use.",
]

# Neutral sentiment templates (sarcastic)
NEUTRAL_SARCASTIC_TEMPLATES = [
    "Sure, the {product} works... eventually.",
    "Well, the {product} exists. That's about it.",
    "The {product} technically functions. Sort of.",
    "I suppose the {product} does something. Maybe.",
    "The {product} works when it feels like it.",
    "Well, the {product} is there. Can't say much else.",
    "The {product} does its job. After a fashion.",
    "Sure, call it a {product} if you want.",
    "The {product} works. In theory.",
    "I guess the {product} is fine. If you squint.",
    "The {product} exists as advertised. Technically.",
    "Well, they call it a {product}. Sure.",
    "The {product} functions. More or less.",
    "I suppose it's a {product}. Debatable.",
    "The {product} works sometimes. Maybe.",
    "Sure, the {product} does something. Allegedly.",
    "The {product} is there. That's a start.",
    "Well, it's labeled as a {product}. Interesting choice.",
    "The {product} operates. In a manner of speaking.",
    "I guess you could use this {product}. Theoretically.",
    "The {product} kind of works. On good days.",
    "Well, it claims to be a {product}. We'll see.",
    "The {product} performs. In its own special way.",
    "Sure, {product} does what it does. Whatever that is.",
    "I suppose the {product} is functional. Loosely speaking.",
    "The {product} exists in a technical sense.",
    "Well, the {product} tries. Sort of.",
    "Sure, you could call this a {product}. I guess.",
    "The {product} works-ish. On occasion.",
    "I suppose it's a {product} of sorts.",
    "The {product} functions when aligned with the moon.",
    "Well, the {product} is here. For better or worse.",
    "Sure, the {product} does its thing. Whatever that means.",
    "I guess the {product} qualifies. Barely.",
    "The {product} operates on its own schedule.",
    "Well, it's marketed as a {product}. Interesting.",
    "Sure, the {product} tries to work. Sometimes.",
    "I suppose the {product} is adequate-ish.",
    "The {product} exists and functions. Kind of.",
    "Well, they say it's a {product}. If you say so.",
]

# Product/topic nouns and variations
PRODUCTS = [
    "movie", "film", "app", "software", "phone", "laptop", "tablet", "headphones",
    "camera", "game", "book", "restaurant", "hotel", "airline", "car", "pizza",
    "burger", "coffee", "service", "product", "device", "tool", "program", "website",
    "platform", "streaming service", "video game", "smartwatch", "speaker", "TV show",
    "series", "documentary", "album", "song", "concert", "performance", "show",
    "delivery service", "ride share", "hotel room", "vacation", "flight", "meal",
    "dish", "cafe", "bakery", "store", "shop", "marketplace", "experience",
    "update", "feature", "interface", "design", "battery", "screen", "keyboard",
    "mouse", "monitor", "printer", "router", "charger", "cable", "case",
    "subscription", "membership", "package", "deal", "offer", "promotion",
    "customer service", "support team", "helpdesk", "warranty", "refund policy",
    "smart home device", "fitness tracker", "workout app", "recipe app", "podcast",
    "audiobook", "e-reader", "gaming console", "VR headset", "drone", "action camera",
    "portable charger", "bluetooth speaker", "noise canceling feature", "touchscreen",
    "productivity app", "note-taking app", "calendar app", "email client",
    "cloud storage", "backup service", "antivirus software", "browser extension",
    "social media platform", "messaging app", "video conferencing tool", "GPS",
    "weather app", "fitness app", "banking app", "shopping app", "music player",
    "photo editor", "video editor", "scanner", "microphone", "webcam", "projector",
    "wireless earbuds", "soundbar", "subwoofer", "amplifier", "mixer", "turntable",
    "remote control", "smart light", "thermostat", "security camera", "doorbell",
    "air purifier", "humidifier", "fan", "heater", "air conditioner", "vacuum cleaner",
    "robot vacuum", "blender", "coffee maker", "toaster", "microwave", "oven",
    "refrigerator", "dishwasher", "washing machine", "dryer", "iron", "steamer",
    "hair dryer", "electric toothbrush", "shaver", "trimmer", "scale", "thermometer",
    "blood pressure monitor", "massage gun", "yoga mat", "treadmill", "exercise bike",
    "dumbbells", "resistance bands", "protein powder", "vitamin supplement", "skincare product",
    "makeup", "perfume", "cologne", "shampoo", "conditioner", "body wash", "lotion",
    "sunscreen", "deodorant", "toothpaste", "mouthwash", "dental floss", "razor",
    "backpack", "luggage", "wallet", "purse", "watch", "sunglasses", "umbrella",
    "water bottle", "lunch box", "travel mug", "cooler", "camping tent", "sleeping bag",
    "hiking boots", "running shoes", "sneakers", "sandals", "slippers", "jacket",
    "coat", "sweater", "shirt", "pants", "jeans", "shorts", "dress", "skirt",
    "mattress", "pillow", "blanket", "sheets", "comforter", "duvet", "curtains",
    "desk", "chair", "lamp", "bookshelf", "storage bin", "organizer", "hanger",
    "pen", "notebook", "planner", "sticky notes", "calculator", "stapler", "scissors",
    "tape dispenser", "paper shredder", "filing cabinet", "whiteboard", "marker",
    "pencil", "eraser", "ruler", "compass", "protractor", "glue", "paint",
    "canvas", "easel", "sketch pad", "colored pencils", "markers", "crayons",
    "puzzle", "board game", "card game", "action figure", "doll", "toy car",
    "building blocks", "stuffed animal", "kite", "frisbee", "ball", "jump rope",
]

# Additional context modifiers
CONTEXTS = [
    "The quality is {sentiment}.",
    "Performance has been {sentiment}.",
    "My experience was {sentiment}.",
    "Overall impression: {sentiment}.",
    "After using it for a week, it's {sentiment}.",
    "Compared to alternatives, it's {sentiment}.",
    "For the price point, it's {sentiment}.",
    "The features are {sentiment}.",
    "Customer support was {sentiment}.",
    "The user interface is {sentiment}.",
    "Battery life is {sentiment}.",
    "Build quality seems {sentiment}.",
    "Speed and responsiveness are {sentiment}.",
    "The value for money is {sentiment}.",
    "Reliability has been {sentiment}.",
]

POS_SENTIMENTS = ["outstanding", "excellent", "great", "wonderful", "superb", "amazing"]
NEG_SENTIMENTS = ["terrible", "awful", "horrible", "poor", "disappointing", "unacceptable"]
NEU_SENTIMENTS = ["okay", "acceptable", "decent", "average", "fair", "adequate"]


def generate_variations(template: str, product: str, count: int, sentiment_type: str) -> List[str]:
    """Generate unique variations of a template with different products."""
    variations = set()  # Use set to ensure uniqueness
    
    # Map sentiment type to appropriate sentiment words
    sentiment_words = {
        'positive': POS_SENTIMENTS,
        'negative': NEG_SENTIMENTS,
        'neutral': NEU_SENTIMENTS
    }
    
    attempts = 0
    max_attempts = count * 10  # Allow multiple attempts to generate unique examples
    
    while len(variations) < count and attempts < max_attempts:
        attempts += 1
        
        # Pick a random product
        product = random.choice(PRODUCTS)
        text = template.format(product=product)
        
        # Add context modifier with varying probability
        if random.random() < 0.4:
            sentiment = random.choice(sentiment_words.get(sentiment_type, POS_SENTIMENTS + NEG_SENTIMENTS + NEU_SENTIMENTS))
            context = random.choice(CONTEXTS).format(sentiment=sentiment)
            text = f"{text} {context}"
        
        # Add additional variation by sometimes including punctuation variations
        if random.random() < 0.2 and not text.endswith('!'):
            text = text.rstrip('.') + '!'
        
        variations.add(text)
    
    return list(variations)


def generate_dataset(templates: List[str], label: int, total_count: int, is_sarcastic: bool, sentiment_type: str) -> List[Tuple[str, int]]:
    """Generate a dataset from templates."""
    examples_per_template = total_count // len(templates)
    remainder = total_count % len(templates)
    
    dataset = []
    
    for i, template in enumerate(templates):
        count = examples_per_template + (1 if i < remainder else 0)
        variations = generate_variations(template, "product", count, sentiment_type)
        
        for text in variations:
            dataset.append((text, label))
    
    # If we don't have enough unique examples, add more with slight variations
    if len(dataset) < total_count:
        needed = total_count - len(dataset)
        print(f"  Adding {needed} more examples to reach target...")
        for template in random.choices(templates, k=needed):
            product = random.choice(PRODUCTS)
            text = template.format(product=product)
            if random.random() < 0.5:
                sentiment = random.choice(POS_SENTIMENTS + NEG_SENTIMENTS + NEU_SENTIMENTS)
                context = random.choice(CONTEXTS).format(sentiment=sentiment)
                text = f"{text} {context}"
            dataset.append((text, label))
    
    return dataset


def save_to_csv(filename: str, data: List[Tuple[str, int]]):
    """Save dataset to CSV with proper escaping."""
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['Reviews', 'Labels'])
        for review, label in data:
            writer.writerow([review, label])
    print(f"✓ Created {filename} with {len(data)} examples")


def main():
    print("Generating Sarcasm-Aware Sentiment Analysis Datasets...")
    print("=" * 60)
    
    # Generate Positive Dataset (label: 2)
    print("\n1. Generating Positive Sentiment Dataset...")
    pos_normal = generate_dataset(POSITIVE_NORMAL_TEMPLATES, 2, 50000, False, 'positive')
    pos_sarcastic = generate_dataset(POSITIVE_SARCASTIC_TEMPLATES, 2, 50000, True, 'positive')
    pos_dataset = pos_normal + pos_sarcastic
    random.shuffle(pos_dataset)
    save_to_csv('git_pos.csv', pos_dataset)
    
    # Generate Negative Dataset (label: 0)
    print("\n2. Generating Negative Sentiment Dataset...")
    neg_normal = generate_dataset(NEGATIVE_NORMAL_TEMPLATES, 0, 50000, False, 'negative')
    neg_sarcastic = generate_dataset(NEGATIVE_SARCASTIC_TEMPLATES, 0, 50000, True, 'negative')
    neg_dataset = neg_normal + neg_sarcastic
    random.shuffle(neg_dataset)
    save_to_csv('git_neg.csv', neg_dataset)
    
    # Generate Neutral Dataset (label: 1)
    print("\n3. Generating Neutral Sentiment Dataset...")
    neu_normal = generate_dataset(NEUTRAL_NORMAL_TEMPLATES, 1, 50000, False, 'neutral')
    neu_sarcastic = generate_dataset(NEUTRAL_SARCASTIC_TEMPLATES, 1, 50000, True, 'neutral')
    neu_dataset = neu_normal + neu_sarcastic
    random.shuffle(neu_dataset)
    save_to_csv('git_neu.csv', neu_dataset)
    
    # Merge all datasets
    print("\n4. Creating Merged Dataset...")
    merged_dataset = pos_dataset + neg_dataset + neu_dataset
    random.shuffle(merged_dataset)
    save_to_csv('sentiment_PNO.csv', merged_dataset)
    
    # Summary
    print("\n" + "=" * 60)
    print("GENERATION COMPLETE!")
    print("=" * 60)
    print(f"\nDatasets created:")
    print(f"  - git_pos.csv: {len(pos_dataset):,} positive examples (50% sarcastic)")
    print(f"  - git_neg.csv: {len(neg_dataset):,} negative examples (50% sarcastic)")
    print(f"  - git_neu.csv: {len(neu_dataset):,} neutral examples (50% sarcastic)")
    print(f"  - sentiment_PNO.csv: {len(merged_dataset):,} total examples")
    print(f"\nLabel mapping:")
    print(f"  0 = Negative sentiment")
    print(f"  1 = Neutral sentiment")
    print(f"  2 = Positive sentiment")
    print("\n✓ All datasets are ready for training!")



if __name__ == "__main__":
    main()
