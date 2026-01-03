import fitz  # PyMuPDF
import requests
import re
import json
import os

def download_rulebook(url, save_path):
    if not os.path.exists(save_path):
        print(f"Downloading rulebook from {url}...")
        response = requests.get(url)
        with open(save_path, 'wb') as f:
            f.write(response.content)
    return save_path

def extract_rulebook_sections(pdf_path):
    doc = fitz.open(pdf_path)
    full_text = ""
    
    # Major headers found in Version 10 to use as anchors
    headers = [
        "MONSTER CARDS", "SPELL & TRAP CARDS", "SUMMONING MONSTER CARDS",
        "PREPARING TO DUEL", "TURN STRUCTURE", "MONSTER BATTLE RULES",
        "CHAINS AND SPELL SPEED", "GLOSSARY"
    ]
    
    current_section = "Introduction"
    chunks = []
    buffer = []

    for page in doc:
        # "blocks" helps handle the two-column layout correctly
        blocks = page.get_text("blocks")
        for block in blocks:
            text = block[4].strip()
            
            # Simple Header Detection: If a line is all caps and in our list
            clean_line = text.split('\n')[0].upper()
            found_header = next((h for h in headers if h in clean_line), None)
            
            if found_header:
                # Save previous chunk
                if buffer:
                    chunks.append({
                        "section": current_section,
                        "content": " ".join(buffer)
                    })
                    buffer = []
                current_section = found_header
            
            buffer.append(text)

    # Final chunk
    if buffer:
        chunks.append({"section": current_section, "content": " ".join(buffer)})
        
    return chunks

if __name__ == "__main__":
    RULEBOOK_URL = "https://www.yugioh-card.com/en/downloads/rulebook/SD_RuleBook_EN_10.pdf"
    PDF_PATH = "data/rulebook_v10.pdf"
    
    os.makedirs('data', exist_ok=True)
    download_rulebook(RULEBOOK_URL, PDF_PATH)
    rule_chunks = extract_rulebook_sections(PDF_PATH)
    
    with open('data/rulebook_parsed.json', 'w') as f:
        json.dump(rule_chunks, f, indent=4)
    
    print(f"Successfully chunked rulebook into {len(rule_chunks)} sections.")