from gamestate import Card


class Action:
    # Play a card as attacker/defender.
    # If None: Pass
    card: Card | None
