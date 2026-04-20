# gamestate_test.py

from gamestate import GameState, Card, CardValue, CardColor

# TEST, OB ALLES FUNKTIONIERT:
if __name__ == "__main__":
    game = GameState()
    game.setup(2)

    print("Trumpf:", game.trump)
    print("Angreifer:", game.players[game.attacker].name)
    print("Verteidiger:", game.players[game.defender].name)
    print()

    for player in game.players:
        print(player.name, "Hand:")
        for card in player.hand.cards:
            print(f"  {card.value.name} of {card.color.name}")
        print()

    # Test Angriff
    attacker = game.players[game.attacker]
    attack_cards = game.LegalAttackCards(attacker.hand.cards)

    print("Legale Angriffskarten:", len(attack_cards))
    first_card = attack_cards[0]

    print("Spiele Angriff:", first_card.value.name, first_card.color.name)

    game.add_attack_card(first_card)
    attacker.hand.cards.remove(first_card)

    # Test Verteidigung
    defender = game.players[game.defender]
    defense_cards = game.LegalDefenseCards(defender.hand.cards)

    print("\nLegale Verteidigungskarten:")
    for c in defense_cards:
        print(c.value.name, c.color.name)
