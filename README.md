# kuberT

Learn Kubernetes hands-on in your terminal, on your own machine.

`kuberT` is a CLI app that:
1. Checks you have **Docker**, **Kind** and **kubectl**.
2. Creates a small Kubernetes cluster on your laptop (using Kind).
3. Walks you through **step-by-step lessons** — Pods, Deployments, Services, and more.
4. Checks your work automatically by running `kubectl` commands.

Each lesson is built for **active learning**, not just reading:

- **Warm-up quiz** before the new topic — you recall the last lessons first (spaced repetition).
- **Hands-on task** with a real `kubectl` check.
- **Troubleshooting scenario** — a broken YAML or bad output; you diagnose it.
- **Review quiz** at the end — mixed recall / multiple-choice / debug / scenario questions.
- **Common mistakes** with the fix.
- **Cheat panel** — a quick reference for every lesson you finished.

Missed answers are saved to `~/.kubert/progress.json`, so the app can bring weak concepts back later.

No browser. No cloud. No signup. 100% offline once installed.

## Requirements

- Ubuntu (or any Linux)
- Python 3.11+
- [Docker](https://docs.docker.com/engine/install/ubuntu/)
- [Kind](https://kind.sigs.k8s.io/docs/user/quick-start/#installation)
- [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/)
- [uv](https://docs.astral.sh/uv/) (Python package manager)

## Install

```bash
git clone <repo-url> kuberT
cd kuberT
cp .env.example .env     # optional: tweak env vars
make deps                # install kind + kubectl (docker must be installed separately)
make install             # install python deps with uv
```

## Use

```bash
make run      # open the kuberT full-screen app
```

The app takes over the terminal (like Claude Code). A header at the top, a menu in the middle, key bindings in the footer:

```
┌─ kuberT ─ learn Kubernetes in your terminal ──────┐
│                                                   │
│            Welcome to kuberT                       │
│            Use ↑/↓ to move, Enter to choose.       │
│                                                   │
│   ┌─────────────────────────────────────────┐     │
│   │ > Run next unfinished lesson            │     │
│   │   Pick a lesson from the list           │     │
│   │   Cheat panel (only what you learned)   │     │
│   │   Check tools / create cluster          │     │
│   │   Show cluster status                   │     │
│   │   Delete cluster                        │     │
│   │   Reset my lesson progress              │     │
│   │   Quit                                  │     │
│   └─────────────────────────────────────────┘     │
│                                                   │
├─ q Quit ──────────────────────────────────────────┤
```

### Keys inside a lesson

| Key | What it does |
|-----|--------------|
| `c` | Check my work (or mark a reading lesson as read) |
| `h` | Show a hint |
| `w` | Start the **warm-up quiz** (recall previous lessons) |
| `r` | Start the **review quiz** (test this lesson) |
| `n` | Go to the next unfinished lesson |
| `s` | Skip this lesson |
| `Esc` | Back to the menu |

### Keys inside a quiz

| Key | What it does |
|-----|--------------|
| `Space` / `Enter` | Reveal the answer, then move to the next question |
| `y` | I knew the answer |
| `n` | I missed it (the concept is logged for a future review) |
| `Esc` | Leave the quiz |

You can also call commands directly without the app: `uv run kubert next`, `uv run kubert lesson <id>`, etc.

## Roadmap

See [ROADMAP.md](./ROADMAP.md) for the full list of modules and lessons.
The lesson order follows [roadmap.sh/kubernetes](https://roadmap.sh/kubernetes).

## Adding a lesson

See [ADD_LESSON.md](./ADD_LESSON.md) for the full step-by-step guide.
To pick which old concepts a new lesson should reach back to, see
[LESSON_REVIEW_MAP.md](./LESSON_REVIEW_MAP.md).

## Contributing

This project is built with AI agents. See [CLAUDE.md](./CLAUDE.md) for the design rules.
