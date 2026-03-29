from interfaces import GameState, OutputInterface

# TODO: Print the current GameState in a nicely formatted string

# Example player defends:
# ---
# Durak-Bot attacks with ♥ 8
# Your Turn: [X: Pass, Play card: 0-5]
# Your Hand: ♥ 10, ♣ 10, ♣ K, ♦ J, ♦ Q, ♦ A
#             [0],  [1], [2], [3], [4], [5]
# 1
# ---

# TODO: Next Scenarios: Player offense, Opponent stopped attack


class TerminalOutput(OutputInterface):
    def OnRender(self, gamestate: GameState): ...
