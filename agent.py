import pickle
import random 
from collections import defaultdict 


import numpy as np 

from env import N_ACTIONS

class QAgent:
    def __init__(self, alpha=0.1,gamma=0.9, epsilon=1.0, seed=None):
        self.q = defaultdict(lambda: np.zeros(N_ACTIONS))
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.rng = random.random(seed)

    def act(self, state, greedy=False):
        if not greedy and self.rng.random < self.epsilon:
            return self.rng.randrange(N_ACTIONS)
        q = self.q[state]
        best = np.flatnonzero(q == q.max())
        return int(self.rng.choice(best))
