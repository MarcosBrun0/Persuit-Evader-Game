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
        self.free_cells = [(x,y) for y in range(self.h)] for x in range(self.h) if grid_map[y][x] == "."]

        self.reset()


def is_blocked(self,x,y):
    return not (0<=x< self.w and 0 <=y < self.h) or self.map[y][x] == "#"
def _dist(self, a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])
