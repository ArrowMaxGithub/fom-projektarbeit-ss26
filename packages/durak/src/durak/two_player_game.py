from durak.action import Action
from durak.gamestate import Card, GameState, Phase
from durak.interfaces import GameInterface, OutputInterface, PlayerInterface


class TwoPlayerGame(GameInterface):
    def __init__(self):
        self.gamestate = GameState()
        self.players: list[PlayerInterface] = []
        self.output: OutputInterface | None = None

        # Mögliche Phasen:
        # "attack"   -> Angreifer spielt Karte oder beendet Angriff
        # "defend"   -> Verteidiger schlägt oder nimmt auf
        # "throw_in" -> Verteidiger nimmt auf, Angreifer darf nachwerfen
        self.phase = Phase.Attack

    def Start(
        self,
        players: list[PlayerInterface],
        output: OutputInterface,
        slow: bool = False,
    ):
        if len(players) != 2:
            raise ValueError("TwoPlayerGame needs exactly 2 players.")

        self.players = players
        self.output = output

        self.gamestate = GameState()
        self.gamestate.setup(2)
        trump = self.gamestate.draw_pile[0]

        for i, player in enumerate(players):
            name = player.GetName()
            self.gamestate.set_player_name(i, name)

        self.phase = Phase.Attack
        self._render()

        while not self.gamestate.is_game_over():
            active_index = self._active_player_index()
            active_player = self.players[active_index]
            attacking_card = self._current_attacking_card()
            hand_cards = self.gamestate.players[active_index].hand.cards.copy()
            legal_cards = self._legal_cards()
            phase = Phase.Attack
            table_pairs = self.gamestate.table.copy()
            discard_pile = self.gamestate.discard_pile.copy()
            draw_pile = len(self.gamestate.draw_pile)
            opponent_hand_size = len(
                self.gamestate.players[(active_index + 1) % 2].hand.cards
            )
            is_attacking = active_index == self.gamestate.attacker
            turn = self.gamestate.round

            action = active_player.OnTurn(
                attacking_card=attacking_card,
                hand_cards=hand_cards,
                legal_cards=legal_cards,
                phase=phase,
                table_pairs=table_pairs,
                discard_pile=discard_pile,
                draw_pile=draw_pile,
                opponent_hand_size=opponent_hand_size,
                is_attacking=is_attacking,
                turn=turn,
                trump=trump,
            )
            self.OnAction(action)
            if slow:
                input("Warte auf Enter...\n")  # Wait for player stepping

        self._render()

    def OnAction(self, action: Action):
        if self.phase == Phase.Attack:
            attacker = self.gamestate.players[self.gamestate.attacker].name
            self.output.OnAttack(attacker, action)
            self._handle_attack(action)

        elif self.phase == Phase.Defense:
            defender = self.gamestate.players[self.gamestate.defender].name
            self.output.OnDefense(defender, action)
            self._handle_defense(action)

        elif self.phase == Phase.ThrowIn:
            attacker = self.gamestate.players[self.gamestate.attacker].name
            self.output.OnAttack(attacker, action)
            self._handle_throw_in(action)

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
            self.phase = Phase.Defense
            return
        # Tisch ist nicht leer. Angreifer kann Karten nachwerfen oder passen.
        else:
            if action.card is None:
                self._finish_defended_round()
                self.phase = Phase.Attack
                return

            self._play_attack_card(action.card)
            self.phase = Phase.Defense
            return

    def _handle_defense(self, action: Action) -> None:
        # None = Verteidiger nimmt auf.
        if action.card is None:
            self.phase = Phase.ThrowIn
            return

        self._play_defense_card(action.card)

        # Wenn alles verteidigt ist, darf Angreifer wieder nachlegen oder passen.
        if self.gamestate.is_fully_defended():
            self.phase = Phase.Attack

    def _handle_throw_in(self, action: Action) -> None:
        # None = Angreifer wirft nichts mehr nach.
        if action.card is None:
            self._finish_taken_round()
            self.phase = Phase.Attack
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
        self._refill_hands_with_output()
        self.gamestate.swap_roles()

    def _finish_taken_round(self) -> None:
        # Verteidiger nimmt auf:
        # Tischkarten auf Verteidigerhand, nachziehen, Rollen bleiben gleich.
        defender = self.gamestate.players[self.gamestate.defender]
        defender.hand.cards.extend(self.gamestate.collect_table_cards())
        self._refill_hands_with_output()

    # ----------------------------
    # HILFSMETHODEN
    # ----------------------------

    def _refill_hands_with_output(self) -> None:
        before_counts: dict[int, int] = {}

        order = [self.gamestate.attacker, self.gamestate.defender]

        for player_index in order:
            player = self.gamestate.players[player_index]
            before_counts[player_index] = len(player.hand.cards)

        self.gamestate.refill_hands()

        if self.output is None:
            return

        for player_index in order:
            player = self.gamestate.players[player_index]
            before = before_counts[player_index]
            after = len(player.hand.cards)

            if after > before:
                self.output.OnDrawCards(player.name, before, after)

    def _active_player_index(self) -> int:
        if self.phase == Phase.Defense:
            return self.gamestate.defender

        return self.gamestate.attacker

    def _current_attacking_card(self) -> Card | None:
        if self.phase == Phase.Defense:
            return self.gamestate.last_open_attack()

        return None

    def _legal_cards(self) -> list[Card]:
        active_index = self._active_player_index()
        hand = self.gamestate.players[active_index].hand.cards

        if self.phase in [Phase.Attack, Phase.ThrowIn]:
            if not self.gamestate.can_add_more_attack_cards():
                return []
            return self.gamestate.LegalAttackCards(hand)

        if self.phase == Phase.Defense:
            return self.gamestate.LegalDefenseCards(hand)

        return []

    def _render(self) -> None:
        if self.output is not None:
            self.output.OnRender(self.gamestate)
