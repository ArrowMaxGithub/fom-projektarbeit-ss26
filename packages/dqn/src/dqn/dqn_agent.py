from pathlib import Path

import torch
import torch.nn as nn
import torch.nn.functional as F
from durak.interfaces import AgentInterface
from ray.rllib.algorithms.dqn.dqn_learner import (
    QF_NEXT_PREDS,
    QF_PREDS,
    QF_TARGET_NEXT_PREDS,
)
from ray.rllib.core.columns import Columns
from ray.rllib.core.learner.utils import make_target_network
from ray.rllib.core.rl_module import RLModuleSpec
from ray.rllib.core.rl_module.apis.target_network_api import TargetNetworkAPI
from ray.rllib.core.rl_module.torch import TorchRLModule

from dqn.agent_utils import create_batch_from_dict
from dqn.durak_env import DurakEnv

INVALID_MASK = -1e8


class DQNMaskedRLModule(TargetNetworkAPI, TorchRLModule):
    def setup(self):
        num_outputs = self.config.action_space.n
        nvec = self.config.observation_space["observations"].nvec
        input_dim = int(nvec.sum())

        self.register_buffer("nvec", torch.tensor(nvec, dtype=torch.long))

        self.net = nn.Sequential(
            nn.Linear(input_dim, 512),
            nn.ReLU(),
            nn.Linear(512, 256),
            nn.ReLU(),
            nn.Linear(256, num_outputs),
        )

        self.make_target_networks()

    def make_target_networks(self) -> None:
        self.target_net = make_target_network(self.net)

    def get_target_network_pairs(self):
        return [
            (self.net, self.target_net),
        ]

    def compute_q_values(self, batch):
        obs = batch[Columns.OBS]["observations"].long()
        flat_obs = self._encode_obs(obs)
        return {QF_PREDS: self.net(flat_obs)}

    def compute_advantage_distribution(self, batch):
        return self.compute_q_values(batch)

    def forward_target(self, batch):
        with torch.no_grad():
            obs = batch[Columns.OBS]["observations"].long()
            flat_obs = self._encode_obs(obs)
            q_values = self.target_net(flat_obs)

            return {QF_PREDS: q_values}

    def _forward_inference(self, batch, **kwargs):
        with torch.no_grad():
            outputs = self._common_forward(batch)
            actions = torch.argmax(outputs[Columns.ACTION_DIST_INPUTS], dim=-1)
            return {Columns.ACTIONS: actions}

    def _forward_exploration(self, batch, **kwargs):
        with torch.no_grad():
            mask = batch[Columns.OBS]["action_mask"]
            outputs = self._common_forward(batch)
            epsilon = self.model_config.get("epsilon", 0.0)
            B = mask.shape[0]

            exploit_actions = torch.argmax(outputs[Columns.ACTION_DIST_INPUTS], dim=-1)

            uniform = torch.rand_like(mask, dtype=torch.float32)
            inf_mask = (1.0 - mask.float()) * INVALID_MASK
            random_actions = torch.argmax(uniform + inf_mask, dim=-1)

            explore = torch.rand((B,), device=mask.device) < epsilon
            actions = torch.where(explore, random_actions, exploit_actions)

            return {Columns.ACTIONS: actions, QF_PREDS: outputs[QF_PREDS]}

    def _forward_train(self, batch, **kwargs):
        outputs = self.compute_q_values(batch)

        if Columns.NEXT_OBS in batch:
            next_batch = {Columns.OBS: batch[Columns.NEXT_OBS]}
            next_mask = batch[Columns.NEXT_OBS]["action_mask"]
            inf_mask = (1 - next_mask.float()) * INVALID_MASK

            online_next = self.compute_q_values(next_batch)
            target_next = self.forward_target(next_batch)

            outputs[QF_NEXT_PREDS] = online_next[QF_PREDS] + inf_mask
            outputs[QF_TARGET_NEXT_PREDS] = target_next[QF_PREDS] + inf_mask

        return outputs

    def _common_forward(self, batch):
        mask = batch[Columns.OBS]["action_mask"]
        q_out = self.compute_q_values(batch)
        q_values = q_out[QF_PREDS]

        inf_mask = (1 - mask.float()) * INVALID_MASK
        masked_q_values = q_values + inf_mask

        return {
            Columns.ACTION_DIST_INPUTS: masked_q_values,
            QF_PREDS: q_values,
        }

    def _encode_obs(self, obs):
        parts = [
            F.one_hot(obs[:, i], num_classes=int(self.nvec[i].item())).float()
            for i in range(len(self.nvec))
        ]
        return torch.cat(parts, dim=-1)


class DQNAgent(AgentInterface):
    def __init__(self, path):
        tmp_env = DurakEnv()
        module_path = Path(path).resolve().as_uri()
        spec = RLModuleSpec(
            module_class=DQNMaskedRLModule,
            observation_space=tmp_env.observation_space(tmp_env.possible_agents[0]),
            action_space=tmp_env.action_space(tmp_env.possible_agents[0]),
            model_config={},
        )
        self.module = spec.build()
        self.module.restore_from_path(module_path)
        self.name = "DQNAgent"
        assert isinstance(self.module, DQNMaskedRLModule), type(self.module)

    def GetName(self) -> str:
        return self.name

    # Get agent action by forwarding the call to the RLModule
    def GetAction(self, obs_dict: dict) -> int:
        # Reconstruct batch shape
        batch = create_batch_from_dict(obs_dict=obs_dict)

        # Forward to the internal module to avoid redundant implementation
        return self.module.forward_inference(batch)[Columns.ACTIONS].item()
