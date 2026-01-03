import json
import re

def split_by_sentences(text):
    """
    Splits text by sentence endings (period followed by a space).
    Keeps the period with the sentence.
    """
    if not text:
        return []
    # Clean up whitespace and newlines first
    text = text.replace('\r\n', ' ').replace('\n', ' ').strip()
    # Split by period followed by whitespace (lookbehind keeps the period)
    sentences = re.split(r'(?<=\.)\s+', text)
    return [s.strip() for s in sentences if s.strip()]

def process_and_save_ygo_data(input_file, output_file):
    print(f"Loading {input_file}...")
    with open(input_file, 'r', encoding='utf-8') as f:
        raw_data = json.load(f)

    processed_cards = []
    extra_deck_types = ["Fusion Monster", "Synchro Monster", "XYZ Monster", "Link Monster"]
    
    # Keys we want to remove to keep the data lean for YugiAI
    keys_to_remove = ["card_sets", "card_prices", "card_images"]

    print("Processing cards...")
    for card in raw_data.get('data', []):
        # 1. Strip bulky keys
        for key in keys_to_remove:
            card.pop(key, None)

        desc = card.get('desc', "")
        card_type = card.get('type', "")
        
        materials = None
        effect_text = desc

        # 2. Extract Materials for Extra Deck Monsters
        # Extra Deck materials are consistently listed on the first line
        if any(t in card_type for t in extra_deck_types):
            parts = re.split(r'\r\n|\n', desc, maxsplit=1)
            if len(parts) > 1:
                materials = parts[0].strip()
                effect_text = parts[1].strip()
            else:
                # Handle cases where there might not be a newline
                sent_parts = re.split(r'\.\s+', desc, maxsplit=1)
                materials = sent_parts[0].strip() + "."
                effect_text = sent_parts[1].strip() if len(sent_parts) > 1 else ""

        # 3. Handle Pendulum Sections
        # Detects if the card has the [ Pendulum Effect ] / [ Monster Effect ] tags
        sections = {}
        if "[ Pendulum Effect ]" in effect_text:
            pen_match = re.search(r'\[ Pendulum Effect \]\s*(.*?)\s*\[ Monster Effect \]', effect_text, re.DOTALL)
            mon_match = re.search(r'\[ Monster Effect \]\s*(.*)', effect_text, re.DOTALL)
            if pen_match and mon_match:
                sections['pendulum'] = split_by_sentences(pen_match.group(1))
                sections['monster'] = split_by_sentences(mon_match.group(1))
        
        # 4. Standard Effect Processing
        if not sections:
            sections['main'] = split_by_sentences(effect_text)

        # 5. Build cleaned object
        cleaned_card = card
        cleaned_card['extracted_materials'] = materials
        cleaned_card['effect_sentences'] = sections
        
        processed_cards.append(cleaned_card)

    print(f"Saving cleaned data to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(processed_cards, f, indent=4)
    
    print(f"Done! Processed {len(processed_cards)} cards.")

# Run the process
if __name__ == "__main__":
    process_and_save_ygo_data('data/all_cards_raw.json', 'data/all_cards_cleaned.json')