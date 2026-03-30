from action import Action
from gamestate import GameState
from interfaces import (
    GameInterface,
    OutputInterface,
    PlayerInterface,
)


class TwoPlayerGame(GameInterface):
    gamestate: GameState
    output: OutputInterface

    # TODO: Update internal game state. Call output.OnRender to update rendered state.
    def OnAction(self, event: Action): ...

    # TODO: Setup two player game
    # Game loop:
    # 1. Call OnTurn for active player with pre-filtered legal cards
    # 2. Handle returned Action --> GameState updated
    # 3. Call output.OnRender --> Rendered output updated
    # 4. Check for game end --> Next player or Game Over
    def Start(self, players: list[PlayerInterface], output: OutputInterface): ...
