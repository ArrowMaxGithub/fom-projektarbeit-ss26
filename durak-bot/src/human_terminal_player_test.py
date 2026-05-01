# human_terminal_player_test.py

import builtins

from gamestate import GameState
from human_terminal_player import HumanTerminalPlayer


class TestInput:
    def __init__(self, inputs: list[str]):
        self.inputs = inputs
        self.index = 0

    def __call__(self, prompt: str = "") -> str:
        value = self.inputs[self.index]
        self.index += 1
        print(prompt + value)
        return value


def print_action(action):
    if action is None:
        print("FEHLER: OnTurn hat None zurückgegeben.")
        return

    if action.card is None:
        print("Gewählte Aktion: Passen")
        return

    print("Gewählte Karte:", action.card.value.name, action.card.color.name)


if __name__ == "__main__":
    gamestate = GameState()
    gamestate.setup(2)

    player = HumanTerminalPlayer()

    attacker = gamestate.players[gamestate.attacker]
    legal_cards = gamestate.LegalAttackCards(attacker.hand.cards)

    old_input = builtins.input

    try:
        print("----- TEST: HUMAN TERMINAL PLAYER SPIELT KARTE -----")
        builtins.input = TestInput(["0"])
        action = player.OnTurn(None, legal_cards)
        print_action(action)

        print()

        print("----- TEST: HUMAN TERMINAL PLAYER PASST -----")
        builtins.input = TestInput(["x"])
        action = player.OnTurn(None, legal_cards)
        print_action(action)

    finally:
        builtins.input = old_input