from action import Action
from gamestate import Card, GameState


class PlayerInterface:
    # The logic implementation for this player's turn.
    # If 'attacking_card' is None: Your turn to attack.
    # Otherwise: You are defending against 'card'.
    def OnTurn(
        self, attacking_card: Card | None, legal_cards: list[Card]
    ) -> Action: ...


class OutputInterface:
    # Render the current game state, e.g. as text on a terminal.
    def OnRender(self, gamestate: GameState): ...


class GameInterface:
    # Process action taken during a player turn.
    def OnAction(self, action: Action): ...

    # Setup game and start game loop.
    def Start(self, players: list[PlayerInterface], output: OutputInterface): ...
