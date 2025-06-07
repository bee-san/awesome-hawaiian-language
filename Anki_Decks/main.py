import csv
import genanki
import random

def load_frequency_list(filename):
    """Load the frequency list and return the first 1500 words in order."""
    words = []
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for i, row in enumerate(reader):
            if i >= 1500:  # Only take first 1500
                break
            words.append(row['word'])
    return words

def load_dictionary(filename):
    """Load the dictionary CSV into a dictionary for lookups."""
    dictionary = {}
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) >= 2:
                word = row[0]
                definition = row[1]
                dictionary[word] = definition
    return dictionary

def create_hawaiian_model():
    """Create the Hawaiian note model with all required fields."""
    model_id = random.randrange(1 << 30, 1 << 31)
    
    hawaiian_model = genanki.Model(
        model_id,
        'Hawaiian',
        fields=[
            {'name': 'Word'},
            {'name': 'Definition'},
            {'name': 'Audio'},
            {'name': 'Picture'},
            {'name': 'Pronunciation'},
            {'name': 'Sentence'},
        ],
        templates=[
            {
                'name': 'Card 1',
                'qfmt': '{{Word}}',
                'afmt': '{{FrontSide}}<hr id="answer">{{Definition}}',
            },
        ]
    )
    return hawaiian_model

def main():
    # Load the frequency list (first 1500 words)
    print("Loading frequency list...")
    words = load_frequency_list('freqlist_haw_inverse.txt')
    print(f"Loaded {len(words)} words from frequency list")
    
    # Load the dictionary
    print("Loading dictionary...")
    dictionary = load_dictionary('Pukui-Elbert-1986-Deduped.csv')
    print(f"Loaded {len(dictionary)} entries from dictionary")
    
    # Create the model
    hawaiian_model = create_hawaiian_model()
    
    # Create the deck
    deck_id = random.randrange(1 << 30, 1 << 31)
    deck = genanki.Deck(deck_id, 'hawaiian_top_1500')
    
    # Process each word and create notes
    print("Creating notes...")
    for word in words:
        # Look up definition in dictionary
        definition = dictionary.get(word, "BROKEN")
        
        # Create note with only Word and Definition filled
        note = genanki.Note(
            model=hawaiian_model,
            fields=[
                word,        # Word
                definition,  # Definition
                '',          # Audio (empty)
                '',          # Picture (empty)
                '',          # Pronunciation (empty)
                '',          # Sentence (empty)
            ]
        )
        
        deck.add_note(note)
    
    # Create package and save
    print("Saving deck...")
    package = genanki.Package(deck)
    package.write_to_file('hawaiian_top_1500.apkg')
    
    print(f"Successfully created hawaiian_top_1500.apkg with {len(words)} cards")

if __name__ == "__main__":
    main()
