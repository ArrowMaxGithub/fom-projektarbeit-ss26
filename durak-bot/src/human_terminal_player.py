from interfaces import ActionCallback, ActionEvent, Card, PlayerInterface

# TODO: Class inititialization, ActionCallback registration, read input from player and call registered ActionCallback


# Example player defends:
# ---
# Durak-Bot attacks with ♥ 8
# Your Turn: [X: Pass, Play card: 0-5]
# Your Hand: ♥ 10, ♣ 10, ♣ K, ♦ J, ♦ Q, ♦ A
#             [0],  [1], [2], [3], [4], [5]
# 1
# ---

# TODO: Next Scenarios: Player offense, Opponent stopped attack


class HumanTerminalPlayer(PlayerInterface):
    def RegisterActionCallback(self, callback: ActionCallback): ...

    def OnTurn(self, attacking_card: Card | None, legal_cards: list[Card]): ...
