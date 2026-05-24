from interfaces import PlayerInterface
from action import Action
from gamestate import Card, CardColor, CardValue, Phase, TablePair


# Simple bot which plays the lowest legal card by its numerical value.
# If there are no legal cards to play, it will pass.
class BotLowestCard(PlayerInterface):
    def OnTurn(
        self,
        attacking_card: Card | None,
        hand_cards: list[Card],
        legal_cards: list[Card],
        phase: Phase,
        table_pairs: list[TablePair],
        discard_pile: list[Card],
        draw_pile: int,
        opponent_hand_size: int,
        is_attacking: bool,
        turn: int,
    ) -> Action:
        chosen_card = None
        for card in legal_cards:
            if chosen_card is None or card.value.value < chosen_card.value.value:
                chosen_card = card

        return Action(chosen_card)

    def GetName(self) -> str:
        return "Bot"


def test():
    attacking_card = Card(CardValue.JACK, CardColor.CLUBS)

    # Example with diamonds as trump
    hand_cards = [
        Card(CardValue.QUEEN, CardColor.CLUBS),
        Card(CardValue.ACE, CardColor.CLUBS),
        Card(CardValue.EIGHT, CardColor.DIAMONDS),
        Card(CardValue.TEN, CardColor.DIAMONDS),
        Card(CardValue.TEN, CardColor.SPADES),
        Card(CardValue.TEN, CardColor.SPADES),
    ]
    legal_cards = [
        Card(CardValue.QUEEN, CardColor.CLUBS),
        Card(CardValue.ACE, CardColor.CLUBS),
        Card(CardValue.EIGHT, CardColor.DIAMONDS),
        Card(CardValue.TEN, CardColor.DIAMONDS),
    ]

    bot = BotLowestCard()

    phase = Phase.Attack
    table_pairs = [TablePair(attack=attacking_card, defense=None)]
    discard_pile = []
    draw_pile = []
    opponent_hand_size = 5
    is_attacking = False
    turn = 42

    result = bot.OnTurn(
        attacking_card=attacking_card,
        hand_cards=hand_cards,
        legal_cards=legal_cards,
        phase=phase,
        table_pairs=table_pairs,
        discard_pile=discard_pile,
        draw_pile=draw_pile,
        opponent_hand_size=opponent_hand_size,
        is_attacking=is_attacking,
        turn=turn,
    )

    # Card with the lowest CardValue, irrespective of trump color
    expected = Action(Card(CardValue.EIGHT, CardColor.DIAMONDS))

    assert result == expected


if __name__ == "__main__":
    test()
