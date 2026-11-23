"""Agente Q-Learning tabular (um por papel: chaser e runner)."""
import pickle
import random
from collections import defaultdict

import numpy as np

from env import N_ACTIONS


class QAgent:
    def __init__(self, alpha=0.1, gamma=0.95, epsilon=1.0, seed=None):
        self.q = defaultdict(lambda: np.zeros(N_ACTIONS))
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.rng = random.Random(seed)

    def act(self, state, greedy=False):
        if not greedy and self.rng.random() < self.epsilon:
            return self.rng.randrange(N_ACTIONS)
        q = self.q[state]
        best = np.flatnonzero(q == q.max())      # desempata aleatoriamente
        return int(self.rng.choice(best))

    def update(self, s, a, r, s_next, done):
        target = r if done else r + self.gamma * self.q[s_next].max()
        self.q[s][a] += self.alpha * (target - self.q[s][a])

    def save(self, path):
        with open(path, "wb") as f:
            pickle.dump(dict(self.q), f)

    def load(self, path):
        with open(path, "rb") as f:
            self.q = defaultdict(lambda: np.zeros(N_ACTIONS), pickle.load(f))
