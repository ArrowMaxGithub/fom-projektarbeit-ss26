from interfaces import (
    ActionEvent,
    GameInterface,
    GameState,
    OutputCallback,
    PlayerInterface,
)


class TwoPlayerGame(GameInterface):
    gamestate: GameState
    output: OutputCallback

    def RegisterOutputCallback(self, callback: OutputCallback):
        self.output = callback

    # TODO: Update internal game state. Call OutputCallback to update rendered state.
    def OnAction(self, event: ActionEvent): ...

    # TODO: Setup two player game and register self as ActioNCallback for each player
    # Game loop:
    # 1. Call OnTurn for active player with pre-filtered legal cards
    # 2. Active player will call OnAction --> GameState updated
    # 3. OnAction will call OutputCallback --> Rendered output updated
    # 4. Check for game end --> Next player or Game Over
    def Start(self, players: list[PlayerInterface]): ...
