---
layout: default
title: VLATune: Reward-Weighted BC for Flow-Matching VLAs
---

# VLATune: Reward-Weighted Behavior Cloning for Flow-Matching VLAs
**Repository:** [VLATune](https://github.com/Gogo2015/VLATune)
**Paper:** [main.pdf](https://github.com/Gogo2015/VLATune/blob/main/paper/main.pdf)
**Model:** [SmolVLA (450M)](https://huggingface.co/lerobot/smolvla_base) · **Benchmark:** [LIBERO](https://github.com/Lifelong-Robot-Learning/LIBERO)

## The Question
Vision-language-action (VLA) models tend to plateau under supervised fine-tuning, and reinforcement learning is the obvious next thing to try. The problem: modern VLAs generate actions with a **flow-matching denoiser**, which gives no tractable per-action log-probability, so PPO does not apply directly.

This project asks whether a lighter, flow-matching-compatible RL step can do better: **filtered and reward-weighted behavior cloning** on a policy's own successful rollouts, kept close to the SFT policy by a vector-field trust-region anchor. The model is SmolVLA (450M), the benchmark is LIBERO, and the whole pipeline runs on one consumer GPU plus preemptible Colab, about **$20-60 of compute**.

> The short answer is **no**, and the negative result is the contribution. On both a saturated in-distribution suite (LIBERO-Goal) and an unsaturated, demo-seeded one (`libero_10`), success rises for one RL iteration and then falls back to where it started. The apparent gain is a reshuffling of success across tasks, inside measurement noise.

What the project delivers is the method itself, a paired collection-equals-evaluation protocol, and an honest account of where this kind of RL can and cannot move a flow-matching policy.

## Method

1. **SFT.** Fine-tune `smolvla_base` on the LIBERO-Goal episodes, and separately train a `libero_10` specialist. This is the launch point and the frozen anchor, `π_SFT`.
2. **RL loop.** For one outer iteration: roll out the current policy, keep the successful trajectories (weighted by a free time-to-success signal), and keep training on them with the flow-matching loss. A vector-field distillation penalty, `β·‖v_θ − v_SFT‖²`, holds the policy near `π_SFT` and stands in for an intractable marginal KL. Repeat, and stop early if a step regresses.
3. **Demo-seed.** A goal-only policy scores about 0% zero-shot on `libero_10`, so the success filter has nothing to keep. Training a `libero_10` specialist first lifts it off the floor. Only then does the loop have anything to work with.
4. **Collection equals evaluation.** The rollout success predicate is exactly LeRobot's `pc_success`, so each iteration's collection doubles as that policy's per-task evaluation, paired on identical seeds across `π_0`, `π_1`, and `π_2`.

## Results

Success rates are `pc_success` (%). RL trajectories are paired on identical seeds across iterations.

| Stage | Suite | n | Result |
|---|---|---|---|
| Official baseline (`smolvla_libero`) | LIBERO-Goal | 100 | 85.0 |
| Goal SFT (ours, 16k/20k steps) | LIBERO-Goal | 100 | 89.0 (+4.0, within noise) |
| RL: filtered BC, β=10 | LIBERO-Goal | 500 (paired) | 89.0 → 91.0 → 89.4 |
| Zero-shot probe (goal-only policy) | `libero_10` | 10/task | ~0 (filter starves) |
| Demo-seed SFT | `libero_10` | 100 | 50.0 |
| RL: filtered BC, β=10 | `libero_10` | 20/task (paired) | 44.0 → 47.5 → 42.5 |

![Success across RL iterations rises then falls in both regimes](https://raw.githubusercontent.com/Gogo2015/VLATune/main/results/figures/figure1_trajectories.png)

*Success rises for one RL iteration and then falls back, in both the saturated (LIBERO-Goal) and demo-seeded (`libero_10`) regimes.*

Two mechanisms sit behind the flat result:

- **Rescue, then reversal.** The first iteration lifts marginal tasks that `π_0` already solved a few times (`libero_10` t3 goes 60 → 75, t7 goes 25 → 40). The second iteration hands those same tasks back (t3 → 55, t7 → 25).
- **Starvation floor.** A task with zero seed successes (`libero_10` t8) gives the filter nothing to imitate, so it stays at zero.

![Per-task success across iterations](https://raw.githubusercontent.com/Gogo2015/VLATune/main/results/figures/figure2_pertask.png)

*Per-task detail: the aggregate flatness hides a reshuffling, where some tasks rescued in iteration 1 are given back in iteration 2.*

## What I Built

- **The method.** Reward-weighted, filtered behavior cloning compatible with a flow-matching action head (sidestepping PPO's need for a tractable per-action log-probability), with a vector-field distillation anchor (`β·‖v_θ − v_SFT‖²`, β=10) that substitutes for an intractable marginal KL.
- **A paired collection-equals-evaluation protocol.** Reusing LeRobot's `pc_success` as the rollout filter means each RL iteration's data collection doubles as that policy's per-task evaluation, paired on identical seeds across `π_0/π_1/π_2`, so the measured deltas are clean.
- **The full SFT + RL pipeline** on a tight compute budget: SFT and fine-tuning on an A100 (GPU-bound), rollouts and evaluation on an L4 (sim/CPU-bound), checkpoints and rollout tensors on Drive.
- **The demo-seed insight** that makes RL viable on an unsaturated suite: a goal-only policy starves the success filter at ~0%, so a `libero_10` specialist has to lift it off the floor first.

## Five fixes the SFT pipeline needed

The LeRobot + LIBERO stack had several sharp edges that the runbook documents:

1. Pass `--policy.push_to_hub=false`, or `lerobot-train` aborts asking for a `repo_id`.
2. `HuggingFaceVLA/libero` has a broken episode-to-file index. Download the full `data/` and `meta/` once (~35 GB), then filter on the in-row `episode_index` column.
3. Rename the cameras (`image` → `camera1`, `image2` → `camera2`); the base model expects three.
4. Use the same `rename_map` at eval, since the checkpoint inherits the `camera1/2/3` keys.
5. Create `~/.libero/config.yaml` ahead of time so eval subprocesses don't hit `EOFError` on the import prompt.

## On the Negative Result

The flat result is reported as one, not dressed up as a win. The +4.0 SFT gain over baseline sits inside the n=100 confidence interval, so it is not a claim. The SFT stage delivers a working pipeline and a clean starting point for RL, and that is what it is good for. A real positive claim would need n=500 and at least three seeds (tens of hours on `libero_10`'s slow renderer), but the up-then-down trajectory already reads as noise by the same standard.

## Tech Stack
- `lerobot 0.5.1`, `torch 2.10.0+cu128`, `transformers 5.3.0`, Python 3.12
- SmolVLA (flow-matching VLA, 450M) · LIBERO simulation benchmark
- Reward-weighted filtered BC + vector-field distillation anchor
- A100 (SFT / fine-tune) + L4 (rollouts / eval), MuJoCo EGL rendering
- Paired per-task evaluation via LeRobot `pc_success`
- LaTeX technical report
