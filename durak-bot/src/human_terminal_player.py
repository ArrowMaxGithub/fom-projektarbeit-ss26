# human_terminal_player.py

from action import Action
from gamestate import Card, Phase, TablePair
from interfaces import PlayerInterface

COLOR = "\033[38;5;7m"


class HumanTerminalPlayer(PlayerInterface):
    def __init__(self):
        self.name = input("Namen eingeben: ")
        super().__init__()

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
    ) -> Action:
        if len(legal_cards) == 0:
            print(f"{COLOR}Spielbare Karten: keine")
            print(f"{COLOR}Dein Zug: [X: Passen / Aufnehmen]")
            input(f"{COLOR}> ")
            return Action(card=None)

        print(f"{COLOR}Deine Handkarten: {len(hand_cards)}")
        self._print_cards(hand_cards)

        print()

        print(f"{COLOR}Spielbare Karten:")
        self._print_cards_with_indexes(legal_cards)

        print()

        print(f"{COLOR}Dein Zug: [X: Passen, Karte spielen: 0-{len(legal_cards) - 1}]")

        choice = input(f"{COLOR}> ").strip()

        if choice.lower() == "x":
            return Action(card=None)

        if not choice.isdigit():
            print(f"{COLOR}Ungültige Eingabe. Bitte X oder eine Zahl eingeben.")
            return Action(None)

        index = int(choice)

        if index < 0 or index >= len(legal_cards):
            print(f"{COLOR}Ungültiger Kartenindex.")
            return Action(None)

        return Action(card=legal_cards[index])

    def GetName(self) -> str:
        return self.name

    # ----------------------------
    # HILFSMETHODEN (AUSGABE)
    # ----------------------------

    def _print_cards(self, cards: list[Card]) -> None:
        print(f"{COLOR}" + self._format_cards(cards))

    def _print_cards_with_indexes(self, cards: list[Card]) -> None:
        print(f"{COLOR}" + self._format_cards(cards))
        print(f"{COLOR}" + self._format_indexes(cards))

    def _format_cards(self, cards: list[Card]) -> str:
        return "|".join(f"{self._format_card(card):^6}" for card in cards)

    def _format_indexes(self, cards: list[Card]) -> str:
        return "|".join(f" {i:<5}" for i in range(len(cards)))

    def _format_card(self, card: Card) -> str:
        return f"{self._format_color(card)} {self._format_value(card):<2}"

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
                return "B"
            case "QUEEN":
                return "D"
            case "KING":
                return "K"
            case "ACE":
                return "A"
            case _:
                return str(card.value.value)
