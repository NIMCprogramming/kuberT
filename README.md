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
make init    # check tools + make a cluster
make list    # see all lessons
make next    # run the next unfinished lesson
make reset   # delete the cluster
make help    # see all targets
```

Or call the CLI directly: `uv run kubert lesson 04-running-apps/01-pods`

## Roadmap

See [ROADMAP.md](./ROADMAP.md) for the full list of modules and lessons.
The lesson order follows [roadmap.sh/kubernetes](https://roadmap.sh/kubernetes).

## Contributing

This project is built with AI agents. See [CLAUDE.md](./CLAUDE.md) for the design rules.
