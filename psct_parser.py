def parse_psct(card_text: str):
    """
    Splits raw card text into Condition, Cost, and Effect.
    """
    # 1. Check for Condition (ends with :)
    condition = ""
    if ":" in card_text:
        condition, card_text = card_text.split(":", 1)

    # 2. Check for Cost/Activation (ends with ;)
    cost_action = ""
    if ";" in card_text:
        cost_action, card_text = card_text.split(";", 1)

    # 3. The remainder is the Effect
    effect = card_text.strip()

    return {
        "condition": condition.strip(),
        "cost_action": cost_action.strip(),
        "effect": effect
    }


if __name__ == "__main__":
    # Test with a classic card interaction
    raw_text = "If this card is Normal Summoned: You can target 1 monster your opponent controls; destroy that target."
    parsed_data = parse_psct(raw_text)

    print(f"CONDITION: {parsed_data['condition']}")
    print(f"COST/TARGET: {parsed_data['cost_action']}")
    print(f"EFFECT: {parsed_data['effect']}")