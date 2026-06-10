from dqn.interfaces import AgentInterface
from dqn.test import test


def crosstable(
    env_factory: callable,
    agents: list[AgentInterface],
    n_episodes: int,
) -> dict:
    results = {
        agent.GetName(): {agent.GetName(): None for agent in agents} for agent in agents
    }

    for i, agent in enumerate(agents):
        for opponent in agents[i:]:
            result = test(
                env_factory=env_factory,
                agent=agent,
                opponent=opponent,
                n_episodes=n_episodes,
            )
            results[agent.GetName()][opponent.GetName()] = result
            results[opponent.GetName()][agent.GetName()] = (result[1], result[0])

    return results


if __name__ == "__main__":
    from prettytable import PrettyTable

    from dqn.durak_env import DurakEnv
    from dqn.high_card_agent import HighCardAgent
    from dqn.interpolation_agent import InterpolationAgent
    from dqn.low_card_agent import LowCardAgent
    from dqn.random_agent import RandomAgent
    from dqn.trump_fish_agent import TrumpFishAgent

    agents = [
        RandomAgent(),
        HighCardAgent(),
        LowCardAgent(),
        TrumpFishAgent(),
        InterpolationAgent(),
    ]

    results = crosstable(env_factory=lambda: DurakEnv(), agents=agents, n_episodes=1000)
    table = PrettyTable()
    table.field_names = ["Matchups"] + [agent.GetName() for agent in agents]
    for agent in agents:
        res = [agent.GetName()] + [
            f"{(results[agent.GetName()][opponent.GetName()][0] * 100):>5.2f}%"
            for opponent in agents
        ]
        table.add_row(res)

    print(table)
