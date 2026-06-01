import typer
from enum import Enum
from typing import Annotated

from bot_lowest_card import BotLowestCard
from trump_fish_agent import TrumpFishAgent
from dqn_agent import DQNAgent
from human_terminal_player import HumanTerminalPlayer
from adapter import AgentAdpater
from terminal_output import TerminalOutput
from two_player_game import TwoPlayerGame

app = typer.Typer()


class Bot(str, Enum):
    LowestCard = "bot-lowest-card"
    TrumpFish = "trump-fish"
    DQNAgent = "dqn-agent"


class Ui(str, Enum):
    Terminal = "terminal"


@app.command()
def play(
    bot: Annotated[
        Bot,
        typer.Argument(help="The name of the bot to play against."),
    ] = "bot-lowest-card",
    ui: Annotated[Ui, typer.Argument(help="Selected interface type.")] = "terminal",
    slow: Annotated[bool, typer.Option(help="Step through program execution")] = False,
):
    """
    Play a two-player game against a selected bot.
    """
    match bot:
        case Bot.LowestCard:
            opponent = BotLowestCard()
        case Bot.TrumpFish:
            opponent = AgentAdpater(TrumpFishAgent())
        case Bot.DQNAgent:
            opponent = AgentAdpater(DQNAgent("../agents/dqn_selfplay_2026_05_31"))

    match ui:
        case Ui.Terminal:
            output = TerminalOutput()

    player = HumanTerminalPlayer()
    game = TwoPlayerGame()
    game.Start([player, opponent], output, slow)


@app.command()
def train():
    """
    Train a bot with the provided parameters.
    """
    ...


@app.command()
def simulate():
    """
    Simulate X number of games between two bots.
    """
    ...


def policy_mapping_fn(aid):
    return "dqn"


if __name__ == "__main__":
    app()
