import random

MAP = [
    "..........",
    "..........",
    "..........",
    "..........",
    "..........",
    "..........",
    "..........",
    "..........",
    "..........",
    "..........",
]

ACTIONS = [(0,-1),(0,1),(-1,0),(1,0),(0,0)]
N_ACTIONS = len(ACTIONS)

class TagGameEnv:
    def __init__(self, grid_map = MAP, max_steps =60, capture_dist=1, view_clip=6 ,seed=0) -> None:
        self.map = grid_map
        self.h = len(grid_map)
        self.w = len(grid_map[0])
        self.max_steps = max_steps
        self.capture_dist = capture_dist
        self.rng = random.Random(seed)
        self.free_cells = [(x, y) for y in range(self.h) for x in range(self.w) if grid_map[y][x] == "."]



def is_blocked(self,x,y):
    return not (0<=x< self.w and 0 <=y < self.h) or self.map[y][x] == "#"
def _dist(self, a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def _move(self, pos, action):
    dx = ACTIONS[action[0]]
    dy = ACTIONS[action[1]]
    nx = pos[0 + dx]
    ny = pos[1 + dy]
    ex = ACTIONS[action[0]]
    dy = ACTIONS[action[1]]
    return pos if self.is_blocked(nx,ny) else (nx,ny)
def _obs_for(self, me, other):
    k = self.view_clip
    dx = max(-k,min(k, other[0] - me[0]))


def _obs(self):
    return {
    "chaser": self_obs_for(self.chaser, self.runner),
    "runner": self._obs_for(self.runner,self.chaser),
    }
