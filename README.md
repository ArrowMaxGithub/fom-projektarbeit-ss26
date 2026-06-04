# Project structure
The project is managed by [UV](https://docs.astral.sh/uv/getting-started/installation/), and organized in three packages:

1. durak: Python implementation of a two-player Durak game
2. cli: Terminal-based human vs. agent game
3. dqn: DQN-Trainer based on [Ray RLLib](https://docs.ray.io/en/latest/rllib/index.html) and deployed as a Docker container.


# CLI usage
A game may be started by providing one of the following IDs as option to the `play` subcommand:

1. Random: `random`
2. Lowest card first: `lowest-card`
3. Low cards early, high cards later: `interpolation`
4. Fish for trump cards: `trump-fish`
5. DQN version 0: `dqn-v0`

Example game vs. DQN version 0: `uv run game play dqn-v0`

See all available options by providing `--help`.