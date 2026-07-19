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
from dqn.test import test
from dqn.durak_env import DurakEnv
from dqn.interfaces import AgentInterface

app = typer.Typer()


class Bot(str, Enum):
    Random = "random"
    LowestCard = "lowest-card"
    HighestCard = "highest-card"
    Interpolation = "interpolation"
    TrumpFish = "trump-fish"
    DQNv0 = "dqn-v0"
    DQNv1 = "dqn-v1"
    DQNv7 = "dqn-v7"
    DQNv14 = "dqn-v14"
    DQNfinal = "dqn-final"


class Ui(str, Enum):
    Terminal = "terminal"


@app.command()
def play(
    bot: Annotated[
        Bot,
        typer.Argument(help="The name of the bot to play against."),
    ] = "dqn-final",
    ui: Annotated[Ui, typer.Argument(help="Selected interface type.")] = "terminal",
    slow: Annotated[bool, typer.Option(help="Step through program execution")] = False,
):
    """
    Play a two-player game against a selected bot.
    """
    opponent = AgentAdpater(__match_bot(bot))

    match ui:
        case Ui.Terminal:
            output = TerminalOutput()

    player = HumanTerminalPlayer()
    game = TwoPlayerGame()
    game.Start([player, opponent], output, slow)


@app.command()
def simulate(
    bot: Annotated[
        Bot,
        typer.Argument(help="The name of the bot to play against."),
    ] = "lowest-card",
    opponent: Annotated[
        Bot,
        typer.Argument(help="The name of the bot to play against."),
    ] = "dqn-final",
    episodes: Annotated[
        int,
        typer.Argument(help="N games to be played"),
    ] = 1000,
):
    """
    Simulate X number of games between two bots.
    """

    bot = __match_bot(bot)
    opponent = __match_bot(opponent)

    (wins, losses) = test(
        lambda: DurakEnv(),
        bot,
        opponent,
        episodes,
    )

    wins *= 100
    losses *= 100

    print(
        f"{bot.GetName()} vs {opponent.GetName()}: {wins:4.2f}% won | {losses:4.2f}% lost"
    )


def __match_bot(agent) -> AgentInterface:
    match agent:
        case Bot.Random:
            agent = RandomAgent()

        case Bot.LowestCard:
            agent = LowCardAgent()

        case Bot.HighestCard:
            agent = HighCardAgent()

        case Bot.Interpolation:
            agent = InterpolationAgent()

        case Bot.TrumpFish:
            agent = TrumpFishAgent()

        case Bot.DQNv0:
            agent = DQNAgent("agents/v0")

        case Bot.DQNv1:
            agent = DQNAgent("agents/v1")

        case Bot.DQNv7:
            agent = DQNAgent("agents/v7")

        case Bot.DQNv14:
            agent = DQNAgent("agents/v14")

        case Bot.DQNfinal:
            agent = DQNAgent("agents/final")

    return agent


if __name__ == "__main__":
    app()
