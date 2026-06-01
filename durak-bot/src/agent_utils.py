import torch
from ray.rllib.core.columns import Columns

from gamestate import Card, CardColor, CardValue, Phase


# Reconstruct batch shape for use in TorchRLModule
def create_batch_from_dict(obs_dict) -> dict:
    return {
        Columns.OBS: {
            "observations": torch.from_numpy(obs_dict["observations"]).unsqueeze(0),
            "action_mask": torch.from_numpy(obs_dict["action_mask"]).unsqueeze(0),
        }
    }


def batch_size(batch) -> int:
    return batch[Columns.OBS]["observations"].size(0)


def get_legal_cards(batch, batch_index: int) -> list[Card]:
    card_mask = batch[Columns.OBS]["action_mask"][batch_index][:36]
    legal_cards_indices = torch.where(card_mask == 1)[0].tolist()
    return [get_card_from_index(index) for index in legal_cards_indices]


def get_game_info(batch, batch_index: int) -> dict:
    obs = batch[Columns.OBS]["observations"][batch_index].tolist()
    return {
        "trump": CardColor((obs[36])),
        "phase": Phase(obs[37]),
        "is_attacker": bool(obs[38]),
        "is_active_player": bool(obs[39]),
        "own_hand_size": int(obs[40]),
        "opponent_hand_size": int(obs[41]),
        "draw_pile": int(obs[42]),
    }


def get_sorted_cards(cards: list[Card], trump: CardColor) -> list[Card]:
    return sorted(cards, key=lambda c: c.value.value + 36 * int(c.color == trump))


def partition_trump_cards(
    cards: list[Card], trump: CardColor
) -> (list[Card], list[Card]):
    non_trumps = [c for c in cards if c.color != trump]
    trumps = [c for c in cards if c.color == trump]
    return (non_trumps, trumps)


def get_index_from_card(card: Card) -> int:
    # [Spades[6..Ace], Clubs[6..Ace], Hearts[6..Ace], Diamonds[6..Ace]]
    return (card.color.value) * len(CardValue) + (card.value.value - 6)


def get_card_from_index(index: int) -> Card | None:
    if index == 36:
        return None

    color = CardColor(index // len(CardValue))
    value = CardValue(index % len(CardValue) + 6)
    return Card(value=value, color=color)
