import pygame
from env import TagGameEnv

CELL = 56
FPS_STEPS = [2, 4, 8, 15, 30]

COLORS = {
    "bg": (24, 26, 33), "grid": (48, 52, 64), "wall": (94, 100, 120),
    "chaser": (231, 76, 60), "runner": (46, 204, 113), "text": (230, 230, 230),
}


env = TagGameEnv()
pygame.init()
screen = pygame.display.set_mode((env.w * CELL, env.h * CELL + 36))
pygame.display.set_caption("TagGame — Chaser x Runner (Q-Learning)")
font = pygame.font.SysFont("monospace", 16)
clock = pygame.time.Clock()
while True:
    print("test")
