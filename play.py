"""Visualização em pygame. Carrega as Q-tables treinadas e roda as políticas gulosas.

Teclas: ESPAÇO pausa | R reinicia episódio | ↑/↓ muda velocidade | ESC sai
"""
import os
import sys

import pygame

from agent import QAgent
from env import TagGameEnv

CELL = 56
FPS_STEPS = [2, 4, 8, 15, 30]

COLORS = {
    "bg": (24, 26, 33), "grid": (48, 52, 64), "wall": (94, 100, 120),
    "chaser": (231, 76, 60), "runner": (46, 204, 113), "text": (230, 230, 230),
}


def draw(screen, env, font, score, speed):
    screen.fill(COLORS["bg"])
    for y in range(env.h):
        for x in range(env.w):
            rect = pygame.Rect(x * CELL, y * CELL, CELL, CELL)
            if env.map[y][x] == "#":
                pygame.draw.rect(screen, COLORS["wall"], rect)
            pygame.draw.rect(screen, COLORS["grid"], rect, 1)
    for pos, color in ((env.runner, COLORS["runner"]), (env.chaser, COLORS["chaser"])):
        center = (pos[0] * CELL + CELL // 2, pos[1] * CELL + CELL // 2)
        pygame.draw.circle(screen, color, center, CELL // 2 - 8)
    hud = f"Chaser {score['chaser']}  x  Runner {score['runner']}   |   passo {env.t}   |   vel {speed} st/s"
    screen.blit(font.render(hud, True, COLORS["text"]), (8, env.h * CELL + 8))
    pygame.display.flip()


def main():
    env = TagGameEnv()
    chaser, runner = QAgent(epsilon=0), QAgent(epsilon=0)
    if os.path.exists("chaser_q.pkl") and os.path.exists("runner_q.pkl"):
        chaser.load("chaser_q.pkl")
        runner.load("runner_q.pkl")
    else:
        print("Q-tables não encontradas — rode train.py primeiro (os agentes vão agir aleatoriamente).")

    pygame.init()
    screen = pygame.display.set_mode((env.w * CELL, env.h * CELL + 36))
    pygame.display.set_caption("TagGame — Chaser x Runner (Q-Learning)")
    font = pygame.font.SysFont("monospace", 16)
    clock = pygame.time.Clock()

    obs, paused, speed_i = env.reset(), False, 2
    score = {"chaser": 0, "runner": 0}
    max_frames = int(sys.argv[1]) if len(sys.argv) > 1 else None   # só para teste headless
    frames = 0

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                pygame.quit()
                return
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    paused = not paused
                elif e.key == pygame.K_r:
                    obs = env.reset()
                elif e.key == pygame.K_UP:
                    speed_i = min(len(FPS_STEPS) - 1, speed_i + 1)
                elif e.key == pygame.K_DOWN:
                    speed_i = max(0, speed_i - 1)

        if not paused:
            ac = chaser.act(obs["chaser"], greedy=True)
            ar = runner.act(obs["runner"], greedy=True)
            obs, _, done, info = env.step(ac, ar)
            if done:
                score["chaser" if info["caught"] else "runner"] += 1
                draw(screen, env, font, score, FPS_STEPS[speed_i])
                pygame.time.wait(500)
                obs = env.reset()

        draw(screen, env, font, score, FPS_STEPS[speed_i])
        clock.tick(FPS_STEPS[speed_i])
        frames += 1
        if max_frames and frames >= max_frames:
            pygame.quit()
            return


if __name__ == "__main__":
    main()
