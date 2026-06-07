import typer
from enum import Enum
from typing import Annotated

from durak.adapter import AgentAdpater
from durak.human_terminal_player import HumanTerminalPlayer
from durak.terminal_output import TerminalOutput
from durak.two_player_game import TwoPlayerGame

from dqn.interpolation_agent import InterpolationAgent
from dqn.trump_fish_agent import TrumpFishAgent
from dqn.dqn_agent import DQNAgent
from dqn.random_agent import RandomAgent
from dqn.low_card_agent import LowCardAgent
from dqn.high_card_agent import HighCardAgent

app = typer.Typer()


class Bot(str, Enum):
    Random = "random"
    LowestCard = "lowest-card"
    HighestCard = "highest-card"
    Interpolation = "interpolation"
    TrumpFish = "trump-fish"
    DQNv0 = "dqn-v0"


class Ui(str, Enum):
    Terminal = "terminal"


@app.command()
def play(
    bot: Annotated[
        Bot,
        typer.Argument(help="The name of the bot to play against."),
    ] = "lowest-card",
    ui: Annotated[Ui, typer.Argument(help="Selected interface type.")] = "terminal",
    slow: Annotated[bool, typer.Option(help="Step through program execution")] = False,
):
    """
    Play a two-player game against a selected bot.
    """
    match bot:
        case Bot.Random:
            opponent = AgentAdpater(RandomAgent())

        case Bot.LowestCard:
            opponent = AgentAdpater(LowCardAgent())

        case Bot.HighestCard:
            opponent = AgentAdpater(HighCardAgent())

        case Bot.Interpolation:
            opponent = AgentAdpater(InterpolationAgent())

        case Bot.TrumpFish:
            opponent = AgentAdpater(TrumpFishAgent())

        case Bot.DQNv0:
            opponent = AgentAdpater(DQNAgent("agents/v0"))

    match ui:
        case Ui.Terminal:
            output = TerminalOutput()

    player = HumanTerminalPlayer()
    game = TwoPlayerGame()
    game.Start([player, opponent], output, slow)


@app.command()
def simulate():
    """
    Simulate X number of games between two bots.
    """
    ...


if __name__ == "__main__":
    play("lowest-card")
    # app()
