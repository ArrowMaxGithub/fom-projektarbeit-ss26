from tqdm import tqdm

from dqn.interfaces import AgentInterface


def test(
    env_factory: callable,
    agent: AgentInterface,
    opponent: AgentInterface,
    n_episodes: int,
) -> (float, float, float):
    env = env_factory()

    wins = 0
    losses = 0

    agent_name = agent.GetName()
    opponent_name = opponent.GetName()

    agent_id = env.possible_agents[0]
    opponent_id = env.possible_agents[1]

    agents_dict = {
        agent_id: agent,
        opponent_id: opponent,
    }

    print(f"{agent_name} vs {opponent_name}")
    for i in tqdm(range(n_episodes)):
        obss, infos = env.reset()

        while env.agents:
            actions = {
                agent_id: agents_dict[agent_id].GetAction(obss[agent_id])
                for agent_id in obss.keys()
            }

            obss, rewards, terms, truncs, infos = env.step(actions)

        winner = env._get_winner()
        if winner == agent_id:
            wins += 1
        else:
            losses += 1

    return (
        wins / n_episodes,
        losses / n_episodes,
    )
