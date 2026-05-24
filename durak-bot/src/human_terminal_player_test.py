# human_terminal_player_test.py

import builtins

from gamestate import GameState, Phase
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
    hand_cards = attacker.hand.cards.copy()
    legal_cards = gamestate.LegalAttackCards(attacker.hand.cards)
    phase = Phase.Attack
    table_pairs = gamestate.table.copy()
    discard_pile = gamestate.discard_pile.copy()
    draw_pile = len(gamestate.draw_pile)
    opponent_hand_size = len(gamestate.players[1].hand.cards)
    is_attacking = True
    turn = 0

    old_input = builtins.input

    try:
        builtins.input = TestInput(["Testspieler"])
        player = HumanTerminalPlayer()

        attacker = gamestate.players[gamestate.attacker]
        hand_cards = attacker.hand.cards
        legal_cards = gamestate.LegalAttackCards(hand_cards)

        print("----- TEST: HUMAN TERMINAL PLAYER SPIELT KARTE -----")
        builtins.input = TestInput(["0"])
        action = player.OnTurn(
            attacking_card=None,
            hand_cards=hand_cards,
            legal_cards=legal_cards,
            phase=phase,
            table_pairs=table_pairs,
            discard_pile=discard_pile,
            draw_pile=draw_pile,
            opponent_hand_size=opponent_hand_size,
            is_attacking=is_attacking,
            turn=turn,
        )
        print_action(action)

        print()

        print("----- TEST: HUMAN TERMINAL PLAYER PASST -----")
        builtins.input = TestInput(["x"])
        action = player.OnTurn(
            attacking_card=None,
            hand_cards=hand_cards,
            legal_cards=legal_cards,
            phase=phase,
            table_pairs=table_pairs,
            discard_pile=discard_pile,
            draw_pile=draw_pile,
            opponent_hand_size=opponent_hand_size,
            is_attacking=is_attacking,
            turn=turn,
        )
        print_action(action)

    finally:
        builtins.input = old_input
