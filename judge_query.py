import os
import re
import requests
import chromadb
import google.generativeai as genai

class YugiJudge:
    def __init__(self, db_path="./yugi_chroma_db"):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found. Set it in your terminal.")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-3-pro-preview')

        self.client = chromadb.PersistentClient(path=db_path)
        self.cards_col = self.client.get_collection("yugioh_cards")
        self.rules_col = self.client.get_collection("rulebook_mechanics")

    def extract_card_names(self, query):
        """Finds potential card names (Capitalized phrases or quoted text)."""
        return [name for group in re.findall(r'"([^"]*)"|\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b', query) for name in group if name]

    def fetch_live_rulings(self, card_name):
        # TODO: Implement this
        # """Fetches rulings for a specific card from YGOPRODeck on-the-fly."""
        # url = f"https://db.ygoprodeck.com/api/v7/card_rulings.php?name={card_name}"
        # try:
        #     response = requests.get(url, timeout=5)
        #     if response.status_code == 200:
        #         rulings = response.json()
        #         # Format rulings into a string
        #         return "\n".join([f"- {r['ruling_text']}" for r in rulings])
        # except Exception:
        #     return None
        return "No specific rulings found for this card."

    def get_context(self, query):
        """Gathers Rulebook text, Card Text, and Live Rulings."""
        # Retrieve general rules semantically
        rule_results = self.rules_col.query(query_texts=[query], n_results=2)
        rules_context = "\n".join(rule_results['documents'][0])

        card_names = self.extract_card_names(query)
        card_context = ""
        rulings_context = ""

        for name in card_names:
            # Get PSCT from Vector DB
            res = self.cards_col.get(where={"name": name})
            if res['documents']:
                card_context += f"\n--- {name} Text ---\n{res['documents'][0]}\n"
            
            # Get Rulings from API
            print(f"Fetching live rulings for: {name}...")
            ruling_text = self.fetch_live_rulings(name)
            if ruling_text:
                rulings_context += f"\n--- {name} Official Rulings ---\n{ruling_text}\n"

        return {
            "rules": rules_context,
            "cards": card_context,
            "rulings": rulings_context
        }

    def answer_query(self, query):
        context = self.get_context(query)
        
        prompt = f"""
        ### SYSTEM PROMPT: YugiAI Head Judge
        You are an expert Yu-Gi-Oh! TCG Judge. Use the provided context to resolve the query.
        Specific Card Text and Official Rulings always override General Rulebook mechanics.

        ### CONTEXT:
        {context['cards']}
        {context['rulings']}
        
        GENERAL ENGINE RULES:
        {context['rules']}

        USER QUERY: {query}
        
        Provide a RULING, a REASONING based on PSCT logic (Conditions/Costs), and CITATIONS.
        """

        response = self.model.generate_content(prompt)
        return response.text

if __name__ == "__main__":
    judge = YugiJudge()
    print(judge.answer_query("Can I use Ash Blossom if my opponent activates the destruction effect of Sacred Fire King Garunix?"))