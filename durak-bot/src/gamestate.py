from enum import Enum
from typing import Self


class CardColor(Enum):
    SPADES = 0
    CLUBS = 1
    HEARTS = 2
    DIAMOND = 3


class CardValue(Enum):
    SIX = 0
    SEVEN = 1
    EIGHT = 2
    NINE = 3
    TEN = 4
    JACK = 5
    QUEEN = 6
    KING = 7
    ACE = 8


class Card:
    value: CardValue
    color: CardColor


class PlayerHand:
    cards: list[Card]


class Player:
    name: str
    is_human: bool
    hand: PlayerHand


# The only concrete data class which holds the entire game state and all player information.
# All other classes are only logic implementations.
class GameState:
    trump: CardColor
    draw_pile: list[Card]  # The open trump card (bottom card) is draw_pile[0]
    attacker: int
    defender: int
    players: list[Player]
    attack_cards: list[Card]  # Played cards during this attack
    defense_cards: list[Card]  # Played cards during this defense

    # TODO: Randomize cards, select trump, choose first attacker
    def Setup(player_count: int) -> Self: ...

    # TODO: Filter 'cards' and return only legal attack cards. If there are no legal cards to play, return empty list.
    # Legal card must be the same value as any played attack/defense card.
    def LegalAttackCards(self, cards: list[Card]) -> list[Card]: ...

    # TODO: Filter 'cards' and return only legal defense cards. If there are no legal cards to play, return empty list.
    # Legal card must be of higher value if same suit as the last attack card, or a trump card.
    def LegalDefenseCards(self, cards: list[Card]) -> list[Card]: ...
