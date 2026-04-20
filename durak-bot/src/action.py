# action.py

from dataclasses import dataclass
from gamestate import Card


@dataclass
class Action:
    # Play a card as attacker/defender.
    # If None:
    # - attacker: pass / no more attack cards
    # - defender: take cards
    card: Card | None = None
