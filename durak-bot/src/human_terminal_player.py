from interfaces import Action, Card, PlayerInterface

# TODO: Class inititialization, read input from player and return chosen Action.


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
    def OnTurn(
        self, attacking_card: Card | None, legal_cards: list[Card]
    ) -> Action: ...
