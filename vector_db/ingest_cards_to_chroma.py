import json
import chromadb
import uuid
from tqdm import tqdm

def ingest_to_chroma(parsed_file_path, db_path="./yugi_chroma_db"):
    client = chromadb.PersistentClient(path=db_path)
    collection = client.get_or_create_collection(name="yugioh_cards")

    with open(parsed_file_path, 'r', encoding='utf-8') as f:
        cards = json.load(f)

    documents, metadatas, ids = [], [], []

    print("Processing cards for ingestion...")
    for card in tqdm(cards, desc="Parsing Cards"):
        # Build the searchable text from PSCT segments
        full_text = f"Card: {card['name']}\n"
        for i, eff in enumerate(card['structure']):
            full_text += f"Effect {i+1}: "
            if eff['condition']: full_text += f"[{eff['condition']}] "
            if eff['cost_action']: full_text += f"({eff['cost_action']}) "
            full_text += f"{eff['effect']}\n"

        documents.append(full_text)
        metadatas.append({
            "name": card['name'],
            "type": card.get('type', 'Unknown'),
            "race": card.get('race', 'Unknown'),
            "attribute": str(card.get('attribute', 'N/A')),
            "level": int(card['level']) if card.get('level') is not None else 0,
            "archetype": card.get('archetype', 'Generic')
        })
        ids.append(str(uuid.uuid4()))

    # Batch Upsert
    batch_size = 500
    total_batches = (len(documents) + batch_size - 1) // batch_size
    
    print("Upserting to ChromaDB...")
    for i in tqdm(range(0, len(documents), batch_size), total=total_batches, desc="Upserting Batches"):
        end = i + batch_size
        collection.upsert(
            ids=ids[i:end],
            metadatas=metadatas[i:end],
            documents=documents[i:end]
        )
    print("Ingestion complete with Judge-level metadata!")

if __name__ == "__main__":
    ingest_to_chroma('data/parsed_cards_db.json')