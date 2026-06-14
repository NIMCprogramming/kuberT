# Claude / AI Agent Guide for kuberT

Read this before editing the repo. It encodes the design choices and the rules every AI agent must follow.

## What this project does

`kuberT` is a **CLI app** that teaches Kubernetes hands-on. It runs on Ubuntu. It uses **Kind** (Kubernetes in Docker) to spin up a local cluster. Then it shows the user **lessons** one by one. Each lesson has an intro, a task, and an automatic check.

The user owns the cluster on their own machine. There is no server, no signup, no cloud.

## Tech stack

| Layer            | Tool                                           |
|------------------|------------------------------------------------|
| Language         | Python 3.11+                                   |
| Package manager  | `uv`                                           |
| CLI framework    | Typer                                          |
| Terminal UI      | Textual (full-screen app) + Rich + questionary |
| Data models      | Pydantic v2                                    |
| Lessons format   | YAML                                           |
| Cluster          | Kind (shell out to `kind` and `kubectl`)       |
| Tests            | pytest                                         |
| Lint / format    | ruff                                           |
| Type check       | mypy (strict)                                  |

## Folder layout

```
kuberT/
├── CLAUDE.md              # this file
├── README.md              # user-facing docs
├── ROADMAP.md             # full lesson list (source of truth)
├── pyproject.toml
├── src/kubert/
│   ├── cli.py             # Typer commands (entry point)
│   ├── app.py             # Textual full-screen menu app
│   ├── models.py          # all Pydantic models
│   ├── lesson.py          # load lessons from YAML
│   ├── cluster.py         # create/delete Kind cluster
│   ├── prereq.py          # check Docker, Kind, kubectl
│   ├── checker.py         # run lesson check commands
│   ├── runner.py          # drive a lesson: intro -> task -> check
│   ├── state.py           # save/load progress in ~/.kubert/
│   └── ui.py              # Rich print helpers
├── lessons/
│   └── NN-module-name/
│       └── NN-lesson-name.yaml
└── tests/
```

## Design rules — read before editing

1. **Small files.** Keep each file under ~250 lines. Split when bigger.
2. **One job per file.** A file's name says what it does.
3. **Types everywhere.** Public functions need type hints. `mypy --strict` must pass.
4. **Pydantic for any structured data.** No dicts with magic keys.
5. **No business logic in `cli.py`.** `cli.py` only parses args and calls modules.
6. **Lessons are data, not code.** Adding a lesson = adding a YAML file. Never edit Python to add content.
7. **Shell out, don't reinvent.** Use `subprocess` to call `kind` and `kubectl`. Do not pull in the full `kubernetes` Python client unless we truly need it.
8. **No comments that explain WHAT** the code does. Only WHY when not obvious.
9. **Write tests for every new module.** Use pytest. Keep tests fast (no real cluster).
10. **No emoji in source code.** Rich colours/styles are fine; emoji are not.

## How to add a lesson

1. Pick the right module folder in `lessons/` (matches `ROADMAP.md`).
2. Create `NN-name.yaml` where `NN` is the next number in that folder.
3. Fill in `id`, `title`, `module`, `order`, `intro`, `task`, `check`.
4. **Write `intro`, `task`, `hint` at A2 English level.** Short sentences (8–12 words), simple words, no idioms. Define every K8s term the first time it appears.
5. Run `uv run pytest tests/test_lesson_loader.py` — it validates every YAML.
6. Update `ROADMAP.md` if the module list changed.

### Lesson YAML schema (summary)

```yaml
id: 04-running-apps/01-pods    # must match relative path under lessons/
title: "Your first Pod"
module: running-apps
order: 1
estimated_minutes: 10
intro: |                       # markdown shown to the user
  ...
task: |                        # what the user must do
  ...
hint: "..."                    # optional one-liner hint
requires: [cluster]            # what must be ready BEFORE the lesson starts (optional)
check:
  type: manual                 # OR command / multiple
  # for command:
  # cmd: "kubectl get pod hello -o jsonpath='{.status.phase}'"
  # expect: "Running"
  # timeout_seconds: 30
```

#### `requires` field

A list of conditions checked before the lesson runs. Currently supported:
- `cluster` — a Kind cluster must exist AND be reachable via `kubectl`. If missing, the user is told how to fix it; the lesson does not run.

If a lesson does not need a live cluster (reading-only intro lessons), omit the field.

## How to run

```bash
uv sync
uv run kubert init        # check tools + create cluster
uv run kubert next        # start next lesson
uv run kubert list        # list all lessons
uv run kubert reset       # delete cluster (start over)
```

## How to test

```bash
uv run pytest
uv run ruff check .
uv run mypy
```

## When you change something

- Run tests.
- Update `ROADMAP.md` if you add or rename a module.
- Update this `CLAUDE.md` if you change a rule.
- Keep README short — link to ROADMAP.md for the full lesson list.

## Git rules

- **Commit often.** After each logical chunk, commit. Don't accumulate many changes.
- **No AI attribution.** Never put `Claude`, `AI`, robot emoji, or `Co-Authored-By: Claude ...` in commit messages, `user.name`, or `user.email`. Write plain commit messages.
- **Short messages.** One short line is fine for small changes.

## Setup tools

This repo uses `Makefile` + `.env` for easy setup. Standard targets: `make install`, `make test`, `make lint`, `make type`. Env vars live in `.env` (copy from `.env.example`). Loaded automatically via `python-dotenv` in `cli.py`.

Supported env vars:
- `KUBERT_CLUSTER_NAME` — name of the Kind cluster (default: `kubert`).
- `KUBERT_STATE_DIR` — where to save progress (default: `~/.kubert`).
- `KUBERT_NODE_IMAGE` — Kind node image (default: `kindest/node:v1.32.2`). We pre-pull this via `docker pull` so the user sees a real progress bar before `kind create cluster` starts.

## What NOT to do

- Don't add a web UI. This project is CLI on purpose.
- Don't add cloud features. Local only.
- Don't add a database. Use a JSON file in `~/.kubert/`.
- Don't add abstractions before the second use case appears.
