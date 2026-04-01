from interfaces import PlayerInterface
from action import Action
from gamestate import Card, CardColor, CardValue


# Simple bot which plays the lowest legal card by its numerical value.
# If there are no legal cards to play, it will pass.
class BotLowestCard(PlayerInterface):
    def OnTurn(self, attacking_card: Card | None, legal_cards: list[Card]) -> Action:
        chosen_card = None
        for card in legal_cards:
            if chosen_card is None or card.value < chosen_card.value:
                chosen_card = card

        return Action(chosen_card)


def test():
    attacking_card = Card(CardValue.JACK, CardColor.CLUBS)

    # Example with diamonds as trump
    legal_cards = [
        Card(CardValue.QUEEN, CardColor.CLUBS),
        Card(CardValue.ACE, CardColor.CLUBS),
        Card(CardValue.EIGHT, CardColor.DIAMOND),
        Card(CardValue.TEN, CardColor.DIAMOND),
    ]

    bot = BotLowestCard()
    result = bot.OnTurn(attacking_card, legal_cards)

    # Card with the lowest CardValue, irrespective of trump color
    expected = Action(Card(CardValue.EIGHT, CardColor.DIAMOND))

    assert result == expected


if __name__ == "__main__":
    test()
