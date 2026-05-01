# terminal_output_test.py

from gamestate import GameState
from terminal_output import TerminalOutput


if __name__ == "__main__":
    gamestate = GameState()
    gamestate.setup(2)

    output = TerminalOutput()

    print("----- TEST: TERMINAL OUTPUT -----")
    output.OnRender(gamestate)

    print("----- TEST: MIT ANGRIFFSKARTE AUF DEM TISCH -----")
    attacker = gamestate.players[gamestate.attacker]
    attack_card = attacker.hand.cards[0]

    attacker.hand.cards.remove(attack_card)
    gamestate.add_attack_card(attack_card)

    output.OnRender(gamestate)