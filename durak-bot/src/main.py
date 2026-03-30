from bot_lowest_card import BotLowestCard
from human_terminal_player import HumanTerminalPlayer
from terminal_output import TerminalOutput
from two_player_game import TwoPlayerGame

# TODO: CLI parse arguments to setup different variants: Player count, Human vs Bot, Bot vs Bot


def main():
    # Start the default game: assume a two player game human vs bot_lowest_card on a terminal
    player = HumanTerminalPlayer()
    opponent = BotLowestCard()
    game = TwoPlayerGame()
    output = TerminalOutput()

    game.RegisterOutputCallback(output.OnRender)
    player.RegisterActionCallback(game.OnAction)
    opponent.RegisterActionCallback(game.OnAction)

    game.Start([player, opponent])


if __name__ == "__main__":
    main()
