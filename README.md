# kuberT

Learn Kubernetes hands-on in your terminal, on your own machine.

`kuberT` is a CLI app that:
1. Checks you have **Docker**, **Kind** and **kubectl**.
2. Creates a small Kubernetes cluster on your laptop (using Kind).
3. Walks you through **step-by-step lessons** — Pods, Deployments, Services, and more.
4. Checks your work automatically by running `kubectl` commands.

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
│   │   Check tools / create cluster          │     │
│   │   Show cluster status                   │     │
│   │   Delete cluster                        │     │
│   │   Quit                                  │     │
│   └─────────────────────────────────────────┘     │
│                                                   │
├─ q Quit ──────────────────────────────────────────┤
```

When you pick an action, the app suspends so you can interact with the lesson (run kubectl, see real progress bars, etc.). When the action ends, the menu comes back.

You can also call commands directly without the app: `uv run kubert next`, `uv run kubert lesson <id>`, etc.

## Roadmap

See [ROADMAP.md](./ROADMAP.md) for the full list of modules and lessons.
The lesson order follows [roadmap.sh/kubernetes](https://roadmap.sh/kubernetes).

## Contributing

This project is built with AI agents. See [CLAUDE.md](./CLAUDE.md) for the design rules.
