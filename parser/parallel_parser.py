import json
import concurrent.futures
from psct_parser import parse_psct, parse_effect_list

def process_card_batch(cards):
    processed = []
    for card in cards:
        parsed = []
        if 'effect_sentences' in card and 'main' in card['effect_sentences']:
             parsed = parse_effect_list(card['effect_sentences']['main'])
        elif 'desc' in card:
            parsed = parse_psct(card['desc'])
            
        # Extract rich metadata for filtering
        processed.append({
            "name": card.get('name'),
            "type": card.get('type'),      # e.g., "Effect Monster", "Spell Card"
            "race": card.get('race'),      # e.g., "Warrior", "Field", "Continuous"
            "attribute": card.get('attribute', 'N/A'),
            "level": card.get('level', 0),
            "archetype": card.get('archetype', 'Generic'),
            "structure": parsed
        })
    return processed

def run_parallel_parse(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        all_data = json.load(f)

    num_workers = 4
    chunk_size = len(all_data) // num_workers
    chunks = [all_data[i:i + chunk_size] for i in range(0, len(all_data), chunk_size)]

    results = []
    with concurrent.futures.ProcessPoolExecutor(max_workers=num_workers) as executor:
        future_to_chunk = {executor.submit(process_card_batch, chunk): chunk for chunk in chunks}
        for future in concurrent.futures.as_completed(future_to_chunk):
            results.extend(future.result())

    with open('data/parsed_cards_db.json', 'w') as f:
        json.dump(results, f, indent=4)
    print(f"Finished! Processed {len(results)} cards with metadata.")

if __name__ == "__main__":
    run_parallel_parse('data/all_cards_cleaned.json')