from action import ActionEvent
from gamestate import Card, GameState


def TurnCallback(gamestate: GameState): ...


def ActionCallback(event: ActionEvent): ...


def OutputCallback(gamestate: GameState): ...


class PlayerInterface:
    # Register the game's callback function to process this player turn.
    def RegisterActionCallback(self, callback: ActionCallback): ...

    # The logic implementation for this player's turn.
    def OnTurn(self, last_action: ActionEvent, legal_cards: list[Card]): ...


class GameInterface:
    # Register the chosen output, e.g. text output on a terminal.
    def RegisterOutputCallback(self, callback: OutputCallback): ...

    # Process action taken during a player turn.
    def OnAction(self, event: ActionEvent): ...

    # Setup game and start game loop.
    def Start(self, players: list[PlayerInterface]): ...


class OutputInterface:
    # Render the current game state, e.g. as text on a terminal.
    def OnRender(self, gamestate: GameState): ...
