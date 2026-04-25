# two_player_game_test.py

from action import Action
from interfaces import PlayerInterface, OutputInterface
from two_player_game import TwoPlayerGame

# Langer basic Text-Output der Spieldaten als Test, ob alles klappt.


class TestPlayer(PlayerInterface):
    def OnTurn(self, attacking_card, legal_cards):
        # Wenn es legale Karten gibt, spiele einfach die erste.
        # Wenn nicht, gib None zurück.
        if legal_cards:
            return Action(card=legal_cards[0])
        return Action(card=None)


class TestOutput(OutputInterface):
    def OnRender(self, gamestate):
        print("----- SPIELSTAND -----")
        print("Trumpf:", gamestate.trump.name if gamestate.trump else None)
        print("Angreifer:", gamestate.players[gamestate.attacker].name)
        print("Verteidiger:", gamestate.players[gamestate.defender].name)

        for player in gamestate.players:
            print(player.name, "hat", len(player.hand.cards), "Karten")

        print("Tisch:")
        if not gamestate.table:
            print("  (leer)")
        else:
            for pair in gamestate.table:
                attack = f"{pair.attack.value.name}-{pair.attack.color.name}"
                defense = (
                    f"{pair.defense.value.name}-{pair.defense.color.name}"
                    if pair.defense is not None
                    else "None"
                )
                print("  Angriff:", attack, "| Verteidigung:", defense)

        print("Nachziehstapel:", len(gamestate.draw_pile))
        print("Ablagestapel:", len(gamestate.discard_pile))
        print()


if __name__ == "__main__":
    game = TwoPlayerGame()

    p1 = TestPlayer()
    p2 = TestPlayer()
    output = TestOutput()

    game.Start([p1, p2], output)

    winner = game.gamestate.winner_index()
    if winner is not None:
        print("GEWINNER:", game.gamestate.players[winner].name)
    else:
        print("Kein Gewinner gefunden")
