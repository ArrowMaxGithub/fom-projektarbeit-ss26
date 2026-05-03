# terminal_output.py

from gamestate import GameState, Card
from interfaces import OutputInterface


class TerminalOutput(OutputInterface):
    def OnRender(self, gamestate: GameState):
        self._print_separator()

        self._print_trump(gamestate)
        self._print_draw_pile(gamestate)
        print()

        self._print_roles(gamestate)
        print()

        self._print_table(gamestate)

        self._print_winner(gamestate)

        self._print_separator()
        print()

    # ----------------------------
    # AUSGABE TEILE
    # ----------------------------

    def _print_separator(self) -> None:
        print("----------------------------------------")

    def _print_trump(self, gamestate: GameState) -> None:
        if gamestate.trump is None:
            return

        print(f"Trumpf: {self._format_color(gamestate.trump)}")

    def _print_draw_pile(self, gamestate: GameState) -> None:
        print(f"Nachziehstapel: {len(gamestate.draw_pile)} Karten")

    def _print_roles(self, gamestate: GameState) -> None:
        attacker = gamestate.players[gamestate.attacker]
        defender = gamestate.players[gamestate.defender]

        print(f"Angreifer: {attacker.name}")
        print(f"Verteidiger: {defender.name}")

    def _print_table(self, gamestate: GameState) -> None:
        print("Tisch:")

        if len(gamestate.table) == 0:
            print("(leer)")
            return

        for pair in gamestate.table:
            attack = self._format_card(pair.attack)

            if pair.defense is not None:
                defense = self._format_card(pair.defense)
            else:
                defense = "(offen)"

            print(f"{attack}  |  {defense}")

    def _print_winner(self, gamestate: GameState) -> None:
        winner_index = gamestate.winner_index()

        if winner_index is None:
            return

        winner = gamestate.players[winner_index]

        # Verlierer = anderer Spieler
        loser_index = (winner_index + 1) % len(gamestate.players)
        loser = gamestate.players[loser_index]

        print()
        print(f"Spiel beendet! Gewinner: {winner.name}!")
        print(f"{loser.name} ist der Durak!")

    # ----------------------------
    # FORMATIERUNG
    # ----------------------------

    def _format_card(self, card: Card) -> str:
        return f"{self._format_color(card.color)} {self._format_value(card)}"

    def _format_color(self, color) -> str:
        match color.name:
            case "SPADES":
                return "♠"
            case "CLUBS":
                return "♣"
            case "HEARTS":
                return "♥"
            case "DIAMONDS":
                return "♦"
            case _:
                return "?"

    def _format_value(self, card: Card) -> str:
        match card.value.name:
            case "JACK":
                return "B (11)"
            case "QUEEN":
                return "D (12)"
            case "KING":
                return "K (13)"
            case "ACE":
                return "A (14)"
            case _:
                return str(card.value.value)