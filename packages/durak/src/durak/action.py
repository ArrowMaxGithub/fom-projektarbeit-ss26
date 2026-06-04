from dataclasses import dataclass

from durak.gamestate import Card


@dataclass
class Action:
    # Play a card as attacker/defender.
    # If None:
    # - attacker: pass / no more attack cards
    # - defender: take cards
    card: Card | None = None
