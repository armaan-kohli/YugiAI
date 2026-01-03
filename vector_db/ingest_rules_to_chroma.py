import chromadb
import json
import uuid
from tqdm import tqdm

def ingest_rules_to_chroma(json_path, db_path="./yugi_chroma_db"):
    client = chromadb.PersistentClient(path=db_path)
    # Use a specific collection for the "Game Engine"
    collection = client.get_or_create_collection(name="rulebook_mechanics")

    with open(json_path, 'r') as f:
        chunks = json.load(f)

    documents, metadatas, ids = [], [], []

    print("Preparing rulebook chunks...")
    for chunk in tqdm(chunks, desc="Processing Chunks"):
        documents.append(chunk['content'])
        metadatas.append({
            "source": "Official Rulebook v10",
            "section": chunk['section']
        })
        ids.append(str(uuid.uuid4()))

    print("Upserting rulebook to ChromaDB...")
    collection.upsert(ids=ids, metadatas=metadatas, documents=documents)
    print("Rulebook ingestion complete!")

if __name__ == "__main__":
    ingest_rules_to_chroma('data/rulebook_parsed.json')