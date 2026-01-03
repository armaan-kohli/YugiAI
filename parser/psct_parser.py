import re

def parse_single_effect(text: str):
    condition = ""
    cost_action = ""
    effect = text.strip()

    # PSCT Order: [Condition]: [Cost/Targeting]; [Effect]
    if ":" in effect:
        condition, effect = effect.split(":", 1)
    
    if ";" in effect:
        cost_action, effect = effect.split(";", 1)

    return {
        "condition": condition.strip(),
        "cost_action": cost_action.strip(),
        "effect": effect.strip()
    }

def split_effects(text: str):
    """
    Splits card text into individual effect strings.
    """
    text = text.strip()
    if not text:
        return []

    # 1. Bullet points
    if "●" in text:
        return [p.strip() for p in text.split("●") if p.strip()]

    # 2. Numbered list (starts with (1))
    if text.startswith("(1)"):
         # Split by (number)
         return [p.strip() for p in re.split(r'\(\d+\)', text) if p.strip()]

    # 3. Split by newlines if present
    if "\n" in text:
        return [p.strip() for p in text.split("\n") if p.strip()]

    # 4. Heuristic: Split by sentences
    # Split by ". " followed by a capital letter, quote, or parenthesis.
    # We use a lookahead assertion.
    parts = re.split(r'\.\s+(?=[A-Z"\(])', text)
    
    return [p.strip() for p in parts if p.strip()]

def parse_psct(card_text: str):
    """
    Splits raw card text into a list of parsed effects.
    """
    if not card_text:
        return []
        
    raw_effects = split_effects(card_text)
    parsed_effects = [parse_single_effect(eff) for eff in raw_effects]
    
    return parsed_effects

def parse_effect_list(effect_list: list):
    """
    Parses a list of pre-split effect strings (e.g. from effect_sentences).
    """
    if not effect_list:
        return []
    return [parse_single_effect(eff) for eff in effect_list]

if __name__ == "__main__":
    # Test with a classic card interaction
    raw_text = "If this card is Normal Summoned: You can target 1 monster your opponent controls; destroy that target."
    parsed_data = parse_psct(raw_text)
    
    for i, effect in enumerate(parsed_data):
        print(f"Effect {i+1}:")
        print(f"  CONDITION: {effect['condition']}")
        print(f"  COST/TARGET: {effect['cost_action']}")
        print(f"  EFFECT: {effect['effect']}")
