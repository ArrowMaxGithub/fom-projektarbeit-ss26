import math
import os
from datetime import datetime
from pathlib import Path

import torch
from prettytable import PrettyTable
from torch.utils.tensorboard import SummaryWriter
from tqdm import tqdm

from dqn.config import dqn_config, save_parameters, set_epsilon
from dqn.crosstable import crosstable
from dqn.dqn_agent import DQNAgent
from dqn.durak_env import DurakEnv
from dqn.epsilon_decay import EpsilonDecay
from dqn.high_card_agent import HighCardAgent
from dqn.interpolation_agent import InterpolationAgent
from dqn.low_card_agent import LowCardAgent
from dqn.random_agent import RandomAgent
from dqn.trump_fish_agent import TrumpFishAgent


def main():
    print(f"GPU supported: {torch.cuda.is_available()}")

    experiment_name = f"selfplay_{datetime.now()}"
    params = {
        "learning_rate": 1e-4,
        "iterations": 8192,
        "epsilon_schedule": "linear",
        "epsilon_decay": 0.67,
        "initial_epsilon": 1.0,
        "final_epsilon": 0.1,
        "num_env_runners": 16,
        "num_envs_per_env_runner": 8,
        "replay_buffer_capacity": 65536 * 32,
        "double_q": True,
        "train_batch_size": 2048,
        "num_steps_sampled_before_learning_starts": 65536 * 16,
        "target_network_update_freq": 4,
        "td_error_loss_fn": "huber",
        "n_step": 5,
        "adam_epsilon": 1e-3,
        "grad_clip": 4.0,
        "grad_clip_by": "global_norm",
        "tau": 0.005,
        "gamma": 0.99,
        "training_intensity": 1.0,
        "eval_episodes": 1000,
        "eval_interval": 8,
        "self_play_capacity": 64,
        "self_play_interval": 64,
        "self_play_recency_bias": 0.25,
        "self_play_gate": 0.50,
        "crosstable_iterations": 100,
    }

    opponents = {
        "random": RandomAgent(),
        "trump_fish": TrumpFishAgent(),
        "interpolation": InterpolationAgent(),
        "low-card": LowCardAgent(),
        "high_card": HighCardAgent(),
    }

    checkpoint_path = Path(f"./checkpoints/{experiment_name}").resolve()
    os.makedirs(checkpoint_path, exist_ok=True)

    algorithm = dqn_config(
        params=params, opponents=opponents, checkpoint_path=checkpoint_path
    )
    set_eval_interval(algorithm=algorithm, value=None)
    epsilon_decay = EpsilonDecay.from_params(params=params)

    log_dir = Path(f"./ray_results/{experiment_name}").resolve()
    os.makedirs(log_dir, exist_ok=True)
    writer = SummaryWriter(log_dir=log_dir)

    print(f"Saving training parameters to {checkpoint_path}")
    save_parameters(checkpoint_path, params)

    try:
        epsilon = epsilon_decay.get(0)
        set_epsilon(epsilon=epsilon, algorithm=algorithm)
        warmup(algorithm=algorithm, iterations=params["warmup_iterations"])
        set_eval_interval(algorithm=algorithm, value=params["eval_interval"])
        train(
            w=writer,
            algorithm=algorithm,
            epsilon_decay=epsilon_decay,
            iterations=params["iterations"],
        )
        checkpoint_agents = collect_checkpoints(checkpoint_path)
        agents = checkpoint_agents + list(opponents.values())
        evaluate(agents=agents, n_episodes=params["crosstable_iterations"])

    except KeyboardInterrupt:
        print("Exiting...")

    except BaseException as e:
        print(f"Exception: {e}")

    finally:
        final_path = Path(f"{checkpoint_path}/final").resolve()
        print(f"Saving final version to {final_path}")
        algorithm.save(final_path)
        algorithm.stop()


def warmup(algorithm, iterations):
    pbar = tqdm(range(iterations))
    for i in pbar:
        algorithm.train()
        pbar.set_description("Warmup")


def train(w, algorithm, epsilon_decay, iterations):
    last_eval = None
    pbar = tqdm(range(iterations))
    for i in pbar:
        epsilon = epsilon_decay.get(i)
        set_epsilon(epsilon=epsilon, algorithm=algorithm)

        result = algorithm.train()

        eval_runners = result.get("evaluation", {}).get("env_runners", {})
        agent_returns = eval_runners.get("agent_episode_returns_mean", {})
        if "Player 1" in agent_returns:
            return_mean = agent_returns["Player 1"]
            if not math.isnan(return_mean):
                w.add_scalar("eval/agent_episode_returns_mean", return_mean, i)
                last_eval = 0.5 * (return_mean + 1)

        em = result.get("env_runners", {})
        w.add_scalar("env/episode_len_mean", em.get("episode_len_mean", 0), i)

        lm = result.get("learners", {}).get("dqn", {})
        w.add_scalar("learner/total_loss", lm.get("total_loss", 0), i)
        w.add_scalar("learner/td_error", lm.get("td_error_mean", 0), i)
        w.add_scalar("learner/qf_loss", lm.get("qf_loss", 0), i)
        w.add_scalar("learner/qf_max", lm.get("qf_max", 0), i)
        w.add_scalar("learner/qf_mean", lm.get("qf_mean", 0), i)
        w.add_scalar("learner/qf_min", lm.get("qf_min", 0), i)

        if "opponent_pool_size" in result:
            w.add_scalar(
                "self_play/opponent_pool_size", result["opponent_pool_size"], i
            )

        if last_eval is None:
            pbar.set_description(f"Training | Epsilon: {epsilon:.2f} Last eval: None")
        else:
            pbar.set_description(
                f"Training | Epsilon: {epsilon:.2f} Last eval: {(last_eval * 100.0):.1f}%"
            )


def collect_checkpoints(path):
    print(f"Collecting all checkpoint versions from {path}")
    agents = []
    for d in path.iterdir():
        if not d.is_dir():
            continue

        name = d.name
        path = d / "learner_group" / "learner" / "rl_module" / "dqn"
        agent = DQNAgent(path=path)
        agent.name = name
        agents.append(agent)

    return agents


def evaluate(agents, n_episodes):
    print(f"Starting evaluation crosstable with {len(agents)} agents")
    results = crosstable(
        env_factory=lambda: DurakEnv(), agents=agents, n_episodes=n_episodes
    )
    table = PrettyTable()
    table.field_names = ["Matchups"] + [agent.GetName() for agent in agents]
    for agent in agents:
        res = [agent.GetName()] + [
            f"{(results[agent.GetName()][opponent.GetName()][0] * 100):>5.2f}%"
            for opponent in agents
        ]
        table.add_row(res)

    print(table)


def set_eval_interval(algorithm, value):
    algorithm.config._is_frozen = False
    algorithm.config.evaluation_interval = value
    algorithm.config._is_frozen = True


if __name__ == "__main__":
    main()
