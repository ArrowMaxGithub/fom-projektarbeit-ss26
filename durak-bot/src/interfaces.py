from action import Action
from gamestate import Card, GameState, Phase, TablePair


class PlayerInterface:
    # The logic implementation for this player's turn.
    # If 'attacking_card' is None: Your turn to attack.
    # Otherwise: You are defending against 'card'.
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
    ) -> Action: ...

    def GetName(self) -> str: ...


class OutputInterface:
    # Render the current game state, e.g. as text on a terminal.
    def OnRender(self, gamestate: GameState): ...

    # Render attack card or stopped attack
    def OnAttack(self, attacker: str, action: Action): ...

    # Render defense card or defender pass
    def OnDefense(self, defender: str, action: Action): ...


class GameInterface:
    # Process action taken during a player turn.
    def OnAction(self, action: Action): ...

    # Setup game and start game loop.
    def Start(
        self, players: list[PlayerInterface], output: OutputInterface, slow: bool
    ): ...
