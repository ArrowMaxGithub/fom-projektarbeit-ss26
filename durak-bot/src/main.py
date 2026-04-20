import typer
from enum import Enum
from typing import Annotated

from bot_lowest_card import BotLowestCard
from human_terminal_player import HumanTerminalPlayer
from terminal_output import TerminalOutput
from two_player_game import TwoPlayerGame

app = typer.Typer()


class Bot(str, Enum):
    LowestCard = "bot-lowest-card"


class Ui(str, Enum):
    Terminal = "terminal"


@app.command()
def play(
    bot: Annotated[
        Bot,
        typer.Argument(help="The name of the bot to play against."),
    ] = "bot-lowest-card",
    ui: Annotated[Ui, typer.Argument(help="Selected interface type.")] = "terminal",
):
    """
    Play a two-player game against a selected bot.
    """
    match bot:
        case Bot.LowestCard:
            opponent = BotLowestCard()

    match ui:
        case Ui.Terminal:
            output = TerminalOutput()

    player = HumanTerminalPlayer()
    game = TwoPlayerGame()
    game.Start([player, opponent], output)


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


if __name__ == "__main__":
    app()
