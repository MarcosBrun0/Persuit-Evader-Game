"""Treino simultâneo (self-play) com Independent Q-Learning."""
import argparse
import csv

from agent import QAgent
from env import TagGameEnv


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--episodes", type=int, default=50_000)
    p.add_argument("--eps-start", type=float, default=1.0)
    p.add_argument("--eps-end", type=float, default=0.05)
    p.add_argument("--eps-decay-frac", type=float, default=0.7,
                   help="fração dos episódios usada para decair epsilon")
    p.add_argument("--window", type=int, default=1000)
    p.add_argument("--seed", type=int, default=0)
    args = p.parse_args()

    env = TagGameEnv(seed=args.seed)
    chaser = QAgent(seed=args.seed + 1)
    runner = QAgent(seed=args.seed + 2)

    decay_eps = int(args.episodes * args.eps_decay_frac)
    caught_win, steps_win, log = 0, 0, []

    for ep in range(1, args.episodes + 1):
        eps = max(args.eps_end,
                  args.eps_start - (args.eps_start - args.eps_end) * ep / decay_eps)
        chaser.epsilon = runner.epsilon = eps

        obs, done = env.reset(), False
        while not done:
            ac = chaser.act(obs["chaser"])
            ar = runner.act(obs["runner"])
            nobs, rew, done, info = env.step(ac, ar)
            chaser.update(obs["chaser"], ac, rew["chaser"], nobs["chaser"], done)
            runner.update(obs["runner"], ar, rew["runner"], nobs["runner"], done)
            obs = nobs

        caught_win += info["caught"]
        steps_win += env.t
        if ep % args.window == 0:
            row = (ep, round(eps, 3), caught_win / args.window, steps_win / args.window)
            log.append(row)
            print(f"ep {ep:6d} | eps {row[1]:.2f} | capture_rate {row[2]:.2f} | "
                  f"avg_len {row[3]:.1f} | estados: C={len(chaser.q)} R={len(runner.q)}")
            caught_win = steps_win = 0

    chaser.save("chaser_q.pkl")
    runner.save("runner_q.pkl")
    with open("train_log.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["episode", "epsilon", "capture_rate", "avg_len"])
        w.writerows(log)
    print("Salvo: chaser_q.pkl, runner_q.pkl, train_log.csv")


if __name__ == "__main__":
    main()
