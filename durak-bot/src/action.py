from enum import Enum

from gamestate import Card


class Action(Enum):
    ATTACK = 0  # Play a card as attacker
    DEFEND = 1  # Play a card as defender
    STOP_ATTACK = 2  # After a succesful defense, stop further attack
    STOP_DEFENSE = 3  # During an ongoing attack, stop defense and take cards


class ActionEvent:
    action: Action
    card: Card | None
