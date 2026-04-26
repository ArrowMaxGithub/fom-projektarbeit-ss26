# human_terminal_player.py

from action import Action
from gamestate import Card
from interfaces import PlayerInterface


class HumanTerminalPlayer(PlayerInterface):
    def OnTurn(
        self, attacking_card: Card | None, legal_cards: list[Card]
    ) -> Action:
        if len(legal_cards) == 0:
            print("Dein Zug: [X: Passen / Aufnehmen]")
            input("> ")
            return Action(card=None)

        print(
            f"Dein Zug: [X: Passen, Karte spielen: 0-{len(legal_cards) - 1}]"
        )

        self._print_cards_with_indexes(legal_cards)

        while True:
            choice = input("> ").strip()

            if choice.lower() == "x":
                return Action(card=None)

            if not choice.isdigit():
                print("Ungültige Eingabe. Bitte X oder eine Zahl eingeben.")
                continue

            index = int(choice)

            if index < 0 or index >= len(legal_cards):
                print("Ungültiger Kartenindex.")
                continue

            return Action(card=legal_cards[index])

    # ----------------------------
    # HILFSMETHODEN (AUSGABE)
    # ----------------------------

    def _print_cards_with_indexes(self, cards: list[Card]) -> None:
        print("Spielbare Karten: " + self._format_cards(cards))
        print("                  " + self._format_indexes(cards))

    def _format_cards(self, cards: list[Card]) -> str:
        return ", ".join(self._format_card(card) for card in cards)

    def _format_indexes(self, cards: list[Card]) -> str:
        return ", ".join(f"[{i}]" for i in range(len(cards)))

    def _format_card(self, card: Card) -> str:
        return f"{self._format_color(card)} {self._format_value(card)}"

    def _format_color(self, card: Card) -> str:
        match card.color.name:
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