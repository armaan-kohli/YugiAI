import requests
import json

def download_all_cards():
    # The official API endpoint for all card information
    URL = "https://db.ygoprodeck.com/api/v7/cardinfo.php"
    
    print("Initiating bulk download... this may take a few seconds.")
    
    try:
        headers = {'User-Agent': 'YGO-Judge-Bot-Project'}
        response = requests.get(URL, headers=headers)
        
        response.raise_for_status()
        
        data = response.json()
        
        # Save to a local file
        with open('all_cards.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            
        print(f"Success! Downloaded {len(data['data'])} cards to all_cards.json")
        
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    download_all_cards()