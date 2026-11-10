"""Ambiente do TagGame: grid discreto, dois agentes (chaser e runner), obstáculos fixos.

Sem nenhuma dependência de pygame: o ambiente é só lógica, assim o treino roda rápido
e a visualização (play.py) fica separada.
"""
import random

# '#' = obstáculo, '.' = livre
MAP = [
    "..........",
    "..##......",
    "..##...#..",
    "......##..",
    "..........",
    "..#.......",
    "..#...###.",
    "......#...",
    ".###......",
    "..........",
]

# 0=cima, 1=baixo, 2=esquerda, 3=direita, 4=parado
ACTIONS = [(0, -1), (0, 1), (-1, 0), (1, 0), (0, 0)]
N_ACTIONS = len(ACTIONS)


class TagGameEnv:
    def __init__(self, grid_map=MAP, max_steps=60, capture_dist=1, view_clip=6, seed=None):
        self.map = grid_map
        self.h = len(grid_map)
        self.w = len(grid_map[0])
        self.max_steps = max_steps
        self.capture_dist = capture_dist  # captura se distância de Manhattan <= isso
        self.view_clip = view_clip        # limita (dx, dy) para a Q-table não explodir
        self.rng = random.Random(seed)
        self.free_cells = [(x, y) for y in range(self.h) for x in range(self.w)
                           if grid_map[y][x] == "."]
        self.reset()

    # ---------- utilidades ----------
    def is_blocked(self, x, y):
        return not (0 <= x < self.w and 0 <= y < self.h) or self.map[y][x] == "#"

    def _dist(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def _move(self, pos, action):
        dx, dy = ACTIONS[action]
        nx, ny = pos[0] + dx, pos[1] + dy
        return pos if self.is_blocked(nx, ny) else (nx, ny)

    # ---------- API estilo gym ----------
    def reset(self):
        # sorteia posições iniciais com alguma distância mínima
        while True:
            c, r = self.rng.sample(self.free_cells, 2)
            if self._dist(c, r) >= 4:
                break
        self.chaser, self.runner = c, r
        self.t = 0
        return self._obs()

    def _obs_for(self, me, other):
        """Estado de um agente: posição relativa do outro + 4 bits de paredes adjacentes."""
        k = self.view_clip
        dx = max(-k, min(k, other[0] - me[0]))
        dy = max(-k, min(k, other[1] - me[1]))
        walls = tuple(int(self.is_blocked(me[0] + ax, me[1] + ay)) for ax, ay in ACTIONS[:4])
        return (dx, dy) + walls

    def _obs(self):
        return {
            "chaser": self._obs_for(self.chaser, self.runner),
            "runner": self._obs_for(self.runner, self.chaser),
        }

    def step(self, a_chaser, a_runner):
        """Os dois agentes agem ao mesmo tempo. Retorna (obs, rewards, done, info)."""
        self.chaser = self._move(self.chaser, a_chaser)
        self.runner = self._move(self.runner, a_runner)
        self.t += 1

        caught = self._dist(self.chaser, self.runner) <= self.capture_dist
        timeout = self.t >= self.max_steps
        done = caught or timeout

        if caught:
            rewards = {"chaser": +10.0, "runner": -10.0}
        else:
            rewards = {"chaser": -0.1, "runner": +0.1}
        return self._obs(), rewards, done, {"caught": caught}
