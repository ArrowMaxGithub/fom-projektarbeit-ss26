from gamestate import Card
from dataclasses import dataclass


@dataclass
class Action:
    # Play a card as attacker/defender.
    # If None: Pass
    card: Card | None

    def __init__(self, card: Card | None):
        self.card = card
