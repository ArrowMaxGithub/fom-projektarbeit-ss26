# two_player_game.py

from action import Action
from gamestate import GameState, Card
from interfaces import GameInterface, OutputInterface, PlayerInterface


class TwoPlayerGame(GameInterface):
    def __init__(self):
        self.gamestate = GameState()
        self.players: list[PlayerInterface] = []
        self.output: OutputInterface | None = None

        # Mögliche Phasen:
        # "attack"   -> Angreifer spielt Karte oder beendet Angriff
        # "defend"   -> Verteidiger schlägt oder nimmt auf
        # "throw_in" -> Verteidiger nimmt auf, Angreifer darf nachwerfen
        self.phase = "attack"

    def Start(self, players: list[PlayerInterface], output: OutputInterface):
        if len(players) != 2:
            raise ValueError("TwoPlayerGame needs exactly 2 players.")

        self.players = players
        self.output = output

        self.gamestate = GameState()
        self.gamestate.setup(2)

        self.phase = "attack"
        self._render()

        while not self.gamestate.is_game_over():
            active_player = self.players[self._active_player_index()]
            attacking_card = self._current_attacking_card()
            legal_cards = self._legal_cards()

            action = active_player.OnTurn(attacking_card, legal_cards)
            self.OnAction(action)

        self._render()

    def OnAction(self, action: Action):
        if self.phase == "attack":
            self._handle_attack(action)

        elif self.phase == "defend":
            self._handle_defense(action)

        elif self.phase == "throw_in":
            self._handle_throw_in(action)

        else:
            raise ValueError(f"Unknown phase: {self.phase}")

        self._render()

    # ----------------------------
    # PHASEN
    # ----------------------------

    def _handle_attack(self, action: Action) -> None:
        # Tisch leer = neue Runde. Dann muss der Angreifer eine Karte legen.
        if len(self.gamestate.table) == 0:
            if action.card is None:
                raise ValueError("Attacker must play a card to start the round.")

            self._play_attack_card(action.card)
            self.phase = "defend"
            return

        # Tisch ist verteidigt. Angreifer darf nachlegen oder passen.
        if self.gamestate.is_fully_defended():
            if action.card is None:
                self._finish_defended_round()
                self.phase = "attack"
                return

            self._play_attack_card(action.card)
            self.phase = "defend"
            return

        raise ValueError("Invalid attack state.")

    def _handle_defense(self, action: Action) -> None:
        # None = Verteidiger nimmt auf.
        if action.card is None:
            self.phase = "throw_in"
            return

        self._play_defense_card(action.card)

        # Wenn alles verteidigt ist, darf Angreifer wieder nachlegen oder passen.
        if self.gamestate.is_fully_defended():
            self.phase = "attack"

    def _handle_throw_in(self, action: Action) -> None:
        # None = Angreifer wirft nichts mehr nach.
        if action.card is None:
            self._finish_taken_round()
            self.phase = "attack"
            return

        self._play_attack_card(action.card)

    # ----------------------------
    # KARTEN SPIELEN
    # ----------------------------

    def _play_attack_card(self, card: Card) -> None:
        attacker = self.gamestate.players[self.gamestate.attacker]

        if card not in attacker.hand.cards:
            raise ValueError("Attack card is not in attacker's hand.")

        if card not in self.gamestate.LegalAttackCards(attacker.hand.cards):
            raise ValueError("Illegal attack card.")

        if not self.gamestate.can_add_more_attack_cards():
            raise ValueError("No more attack cards allowed.")

        attacker.hand.cards.remove(card)
        self.gamestate.add_attack_card(card)

    def _play_defense_card(self, card: Card) -> None:
        defender = self.gamestate.players[self.gamestate.defender]

        if card not in defender.hand.cards:
            raise ValueError("Defense card is not in defender's hand.")

        if card not in self.gamestate.LegalDefenseCards(defender.hand.cards):
            raise ValueError("Illegal defense card.")

        defender.hand.cards.remove(card)
        self.gamestate.add_defense_card(card)

    # ----------------------------
    # RUNDENABSCHLUSS
    # ----------------------------

    def _finish_defended_round(self) -> None:
        # Verteidigung erfolgreich:
        # Karten weglegen, nachziehen, Rollen tauschen.
        self.gamestate.discard_table_cards()
        self.gamestate.refill_hands()
        self.gamestate.swap_roles()

    def _finish_taken_round(self) -> None:
        # Verteidiger nimmt auf:
        # Tischkarten auf Verteidigerhand, nachziehen, Rollen bleiben gleich.
        defender = self.gamestate.players[self.gamestate.defender]
        defender.hand.cards.extend(self.gamestate.collect_table_cards())
        self.gamestate.refill_hands()

    # ----------------------------
    # HILFSMETHODEN
    # ----------------------------

    def _active_player_index(self) -> int:
        if self.phase == "defend":
            return self.gamestate.defender

        return self.gamestate.attacker

    def _current_attacking_card(self) -> Card | None:
        if self.phase == "defend":
            return self.gamestate.last_open_attack()

        return None

    def _legal_cards(self) -> list[Card]:
        active_index = self._active_player_index()
        hand = self.gamestate.players[active_index].hand.cards

        if self.phase in ["attack", "throw_in"]:
            if not self.gamestate.can_add_more_attack_cards():
                return []
            return self.gamestate.LegalAttackCards(hand)

        if self.phase == "defend":
            return self.gamestate.LegalDefenseCards(hand)

        return []

    def _render(self) -> None:
        if self.output is not None:
            self.output.OnRender(self.gamestate)
