# two_player_game_test.py

from action import Action
from interfaces import PlayerInterface, OutputInterface
from two_player_game import TwoPlayerGame
from gamestate import Card, Phase, TablePair

# Langer basic Text-Output der Spieldaten als Test, ob alles klappt.


class TestPlayer(PlayerInterface):
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
        # Wenn es legale Karten gibt, spiele einfach die erste.
        # Wenn nicht, gib None zurück.
        if legal_cards:
            return Action(card=legal_cards[0])
        return Action(card=None)

    def GetName(self):
        return "Testspieler"


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

    def OnAttack(self, attacker, action):
        print("Angriff:", attacker, action.card)

    def OnDefense(self, defender, action):
        print("Verteidigung:", defender, action.card)

    def OnDrawCards(self, player_name, before, after):
        print("Nachziehen:", player_name, before, "->", after)


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
