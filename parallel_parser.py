import json
import concurrent.futures
from psct_parser import parse_psct  # Importing the parser logic we wrote earlier

def process_card_batch(cards):
    """Worker function to process a subset of cards."""
    processed = []
    for card in cards:
        # We only care about cards with text
        if 'desc' in card:
            parsed = parse_psct(card['desc'])
            processed.append({
                "name": card['name'],
                "structure": parsed
            })
    return processed

def run_parallel_parse(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        all_data = json.load(f)['data']

    # Split data into 4 chunks (or based on your CPU cores)
    num_workers = 4
    chunk_size = len(all_data) // num_workers
    chunks = [all_data[i:i + chunk_size] for i in range(0, len(all_data), chunk_size)]

    print(f"Starting parallel parse across {num_workers} workers...")

    results = []
    with concurrent.futures.ProcessPoolExecutor(max_workers=num_workers) as executor:
        # Map the worker function to the data chunks
        future_to_chunk = {executor.submit(process_card_batch, chunk): chunk for chunk in chunks}
        
        for future in concurrent.futures.as_completed(future_to_chunk):
            results.extend(future.result())

    print(f"Finished! Processed {len(results)} cards.")
    
    with open('parsed_cards_db.json', 'w') as f:
        json.dump(results, f, indent=4)

if __name__ == "__main__":
    run_parallel_parse('all_cards.json')