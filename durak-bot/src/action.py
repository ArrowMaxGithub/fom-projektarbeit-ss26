from gamestate import Card


class ActionEvent:
    # Play a card as attacker/defender.
    # If None: Pass
    card: Card | None
