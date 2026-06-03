# terminal_output.py

from gamestate import GameState, Card
from interfaces import OutputInterface

from action import Action

ATTACK_COLOR = "\033[38;5;1m"
DEFENSE_COLOR = "\033[38;5;2m"
INFO_COLOR = "\033[38;5;243m"
GAMEOVER_COLOR = "\033[38;5;3m"


class TerminalOutput(OutputInterface):
    def OnRender(self, gamestate: GameState):
        print()
        self._print_separator()
        print(f"{INFO_COLOR}Aktuelles Spiel")
        self._print_round(gamestate)
        self._print_trump(gamestate)
        self._print_draw_pile(gamestate)
        print()

        self._print_roles(gamestate)
        print()

        self._print_table(gamestate)

        self._print_winner(gamestate)

        self._print_separator()
        print()

    def OnAttack(self, attacker: str, action: Action):
        if action.card:
            print(
                f"{ATTACK_COLOR}{attacker} greift an mit {self._format_card(action.card)}"
            )
        else:
            print(f"{ATTACK_COLOR}{attacker} stoppt seinen Angriff")

    def OnDefense(self, defender: str, action: Action):
        if action.card:
            print(
                f"{DEFENSE_COLOR}{defender} verteidigt mit {self._format_card(action.card)}"
            )
        else:
            print(f"{DEFENSE_COLOR}{defender} nimmt die Karten auf")

    def OnDrawCards(self, player_name: str, before: int, after: int):
        print(
            f"{INFO_COLOR}{player_name} hat von {before} auf {after} Karten aufgezogen"
        )

    # ----------------------------
    # AUSGABE TEILE
    # ----------------------------

    def _print_separator(self) -> None:
        print(f"{INFO_COLOR}----------------------------------------")

    def _print_round(self, gamestate: GameState) -> None:
        print(f"{INFO_COLOR}Runde: {gamestate.round}")

    def _print_trump(self, gamestate: GameState) -> None:
        if gamestate.trump is None:
            return

        print(f"{INFO_COLOR}Trumpf: {self._format_color(gamestate.trump)}")

    def _print_draw_pile(self, gamestate: GameState) -> None:
        print(f"{INFO_COLOR}Nachziehstapel: {len(gamestate.draw_pile)} Karten")

    def _print_roles(self, gamestate: GameState) -> None:
        attacker = gamestate.players[gamestate.attacker]
        defender = gamestate.players[gamestate.defender]

        print(
            f"{INFO_COLOR}Angreifer: {attacker.name} ({len(attacker.hand.cards)} Karten)"
        )
        print(
            f"{INFO_COLOR}Verteidiger: {defender.name} ({len(defender.hand.cards)} Karten)"
        )

    def _print_table(self, gamestate: GameState) -> None:
        print(f"{INFO_COLOR}Tisch:")

        if len(gamestate.table) == 0:
            print(f"{INFO_COLOR}(leer)")
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
        print(f"{GAMEOVER_COLOR}Spiel beendet! Gewinner: {winner.name}!")
        print(f"{GAMEOVER_COLOR}{loser.name} ist der Durak!")

    # ----------------------------
    # FORMATIERUNG
    # ----------------------------

    def _format_card(self, card: Card) -> str:
        return f"{self._format_color(card.color)} {self._format_value(card):<2}"

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
                return "B"
            case "QUEEN":
                return "D"
            case "KING":
                return "K"
            case "ACE":
                return "A"
            case _:
                return str(card.value.value)
