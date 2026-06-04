from enum import IntEnum

import numpy as np

from durak.action import Action
from durak.gamestate import Card, CardColor, CardValue, Phase, TablePair
from durak.interfaces import AgentInterface, PlayerInterface


class Status(IntEnum):
    Unknown = 0
    MyCard = 1
    OpponentCard = 2
    OpenAttack = 3
    DefendedAttack = 4
    Defense = 5
    InDeck = 6
    Discarded = 7


# Adapter for agents to be used in a standard Durak game
# Keeps book about all known cards for the agent
class AgentAdpater(PlayerInterface):
    def __init__(self, agent: AgentInterface):
        self.num_cards = len(CardColor) * len(CardValue)
        self.observations = np.zeros(self.num_cards + 7).astype(np.int8)
        self.passing_action = self.num_cards
        self.agent = agent
        self.turn = -1
        self.tracked_cards = set()  # Includes any played or shown card. Their status can be traced exactly based on public information alone.

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
        trump: Card,
    ) -> Action:
        table_map = {pair.attack: pair.defense for pair in table_pairs}
        table_defenses = [pair.defense for pair in table_pairs]

        self.tracked_cards.add(trump)
        trump_index = self._get_index_from_card(trump)
        self.observations[trump_index] = Status.InDeck

        # Must play card on first move
        is_new_turn = self.turn != turn
        self.turn = turn
        can_pass = (not is_attacking) or (not is_new_turn)

        # Track agent hand cards
        self.tracked_cards.update(hand_cards)

        # Track any card on the table
        for attack, defense in table_map.items():
            self.tracked_cards.add(attack)
            if defense:
                self.tracked_cards.add(defense)

        # Track any discarded card
        self.tracked_cards.update(discard_pile)

        # Update status for tracked cards
        for card in self.tracked_cards:
            if card in hand_cards:
                status = Status.MyCard
            elif card in discard_pile:
                status = Status.Discarded
            elif card in table_defenses:
                status = Status.Defense
            elif card in table_map and table_map[card] is None:
                status = Status.OpenAttack
            elif card in table_map and table_map[card] is not None:
                status = Status.DefendedAttack
            elif card == trump and draw_pile > 0:
                status = Status.InDeck
            else:
                status = Status.OpponentCard

            index = self._get_index_from_card(card)
            self.observations[index] = status

        # Generate action mask of legal moves
        # Start will all-zeros
        action_mask = np.zeros(self.num_cards + 1, dtype=np.int8)

        # Passing is allowed if the agent is defending or it it not the first (attack) turn
        action_mask[self.passing_action] = can_pass

        # Set ones for legal cards if the agent can actually act
        phase_actor_is_attacker = {
            Phase.Attack: True,
            Phase.ThrowIn: True,
            Phase.Defense: False,
        }
        if phase_actor_is_attacker.get(phase) == is_attacking:
            indices = [self._get_index_from_card(card) for card in legal_cards]
            action_mask[indices] = 1

        # Set global observations
        self.observations[self.num_cards + 0] = int(trump.color.value)
        self.observations[self.num_cards + 1] = int(phase.value)
        self.observations[self.num_cards + 2] = int(is_attacking)
        self.observations[self.num_cards + 3] = int(True)
        self.observations[self.num_cards + 4] = int(len(hand_cards))
        self.observations[self.num_cards + 5] = int(opponent_hand_size)
        self.observations[self.num_cards + 6] = int(draw_pile)

        # Copy to avoid agent writing to observations
        obs = np.copy(self.observations)

        # Generate observations dict for agent
        obs_dict = {
            "observations": obs,
            "action_mask": action_mask,
        }

        # Return action from agent
        action = self.agent.GetAction(obs_dict=obs_dict)
        card = self._get_card_from_index(action)

        # Agent played a card as attacker or defender
        if card:
            self.observations[action] = (
                Status.OpenAttack if is_attacking else Status.Defense
            )

        return Action(card=card)

    def GetName(self) -> str:
        return self.agent.GetName()

    def _get_index_from_card(self, card: Card) -> int:
        # [Spades[6..Ace], Clubs[6..Ace], Hearts[6..Ace], Diamonds[6..Ace]]
        return (card.color.value) * len(CardValue) + (card.value.value - 6)

    def _get_card_from_index(self, index: int) -> Card | None:
        if index == self.passing_action:
            return None

        color = CardColor(index // len(CardValue))
        value = CardValue(index % len(CardValue) + 6)
        return Card(value=value, color=color)
