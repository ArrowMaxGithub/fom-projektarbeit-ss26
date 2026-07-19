# Project structure
The project is managed by [UV](https://docs.astral.sh/uv/getting-started/installation/), and organized in three packages:

1. durak: Python implementation of a two-player Durak game
2. cli: Terminal-based human vs. agent game
3. dqn: DQN-Trainer based on [Ray RLLib](https://docs.ray.io/en/latest/rllib/index.html) and deployed as a Docker container.


# CLI usage
A game may be started by providing one of the following bot names to the `play` subcommand:

1. Random: `random`
2. Lowest card first: `lowest-card`
3. Low cards early, high cards later: `interpolation`
4. Fish for trump cards: `trump-fish`
5. DQN version 0: `dqn-v0`
6. DQN version 1: `dqn-v1`
7. DQN version 7: `dqn-v7`
8. DQN version 14: `dqn-v14`
9. DQN version Final: `dqn-final`

Example game vs. DQN version 14: `uv run game play dqn-v14`

The same bot selection can be passed to the `simulate` subcommand to play N games between two bots: `uv run game simulate lowest-card dqn-final`

See all available options by providing `--help`.