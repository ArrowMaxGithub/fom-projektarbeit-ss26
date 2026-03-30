from interfaces import (
    ActionCallback,
    ActionEvent,
    Card,
    PlayerInterface,
)

# TODO: Simple bot which plays the lowest legal card. If there are no legal cards to play, it will pass.


class BotLowestCard(PlayerInterface):
    def RegisterActionCallback(self, callback: ActionCallback): ...

    def OnTurn(self, attacking_card: Card | None, legal_cards: list[Card]): ...
