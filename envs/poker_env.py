import numpy as np
import gymnasium as gym            # pip install gymnasium
from game.engine import Game       # 你原本的撲克引擎

class PokerEnv(gym.Env):
    """Heads-Up NL Texas Hold’em，給 stable-baselines3 用。"""
    metadata = {"render.modes": ["ansi"]}
    
    def __init__(self, max_steps=100):
        super().__init__()
        self.game = Game([self._dummy_ai, self._dummy_ai])
        self.max_steps = max_steps
        # ---- 定義 observation & action space ----
        # 把牌、籌碼、pot 等數值 encode 成固定維度向量
        self.observation_space = gym.spaces.Box(low=0, high=1, shape=(256,), dtype=np.float32)
        # 動作 = {0: fold, 1: call, 2: raise_small, 3: raise_large}
        self.action_space = gym.spaces.Discrete(4)
        self._cached_state = None
        self._step_cnt = 0

    # ---------- Gym 標準介面 ----------
    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.game.reset()
        self._step_cnt = 0
        obs = self._encode_state()
        return obs, {}
    
    def step(self, action):
        self._step_cnt += 1
        action_tuple = self._map_discrete_to_engine(action)
        obs, reward, terminated, truncated, info = \
            self.game.play_one_action(action_tuple)
        done = terminated or truncated or self._step_cnt >= self.max_steps
        return self._encode_state(obs), reward, done, False, info
    
    def render(self):
        return self.game.render()

    # ---------- 私有工具 ----------
    def _encode_state(self, raw=None):
        """把引擎輸出的 round_state → 256-D np.array."""
        # TODO: hole_card, board, stack, pot, position, street…
        return np.zeros(256, dtype=np.float32)

    def _map_discrete_to_engine(self, a):
        if a == 0:
            return ("fold", 0)
        if a == 1:
            return ("call", 0)
        if a == 2:
            return ("raise", {"amount": "min"})
        if a == 3:
            return ("raise", {"amount": "pot"})
    
    # 讓對手先用隨機 / CallBaseline
    def _dummy_ai(self, valid_actions, hole_card, round_state):
        return ("call", valid_actions[1]["amount"])