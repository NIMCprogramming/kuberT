# Adding a new lesson to kuberT

Every lesson lives in a single YAML file under `lessons/`. No Python code is needed to add a lesson. This guide walks through the full flow.

## TL;DR — 6 steps

1. Pick the module folder from `ROADMAP.md`.
2. Create `lessons/NN-module/NN-name.yaml`.
3. Write `intro`, `task`, `hint` in **A2 English**.
4. Pick a `check` type: `manual`, `command`, or `multiple`.
5. Add `requires: [cluster]` if the lesson talks to Kubernetes.
6. Run `make test`. If green, commit.

---

## 1. Pick the right module

Open `ROADMAP.md`. Find the module that matches the topic (e.g. `04-running-apps` for Pods, `05-configuration` for ConfigMaps, etc.).

Each module is one folder under `lessons/`. The folder name **must** match the roadmap table.

If your module folder does not exist yet, create it: `lessons/NN-module-name/`. Then add the same line to `ROADMAP.md`'s status section.

## 2. Create the YAML file

File path:
```
lessons/NN-module/NN-name.yaml
```

- `NN` is a two-digit order number, padded with `0` (e.g. `01`, `02`, `10`).
- `name` is short, lowercase, words separated by `-`.

Example: `lessons/04-running-apps/02-replicasets.yaml`.

The `id` field inside the YAML **must equal** the path under `lessons/` without the `.yaml` extension. The loader test will fail if they do not match.

## 3. Full YAML reference

```yaml
id: 04-running-apps/02-replicasets   # required — must match folder/file
title: "ReplicaSets"                  # required — short, capitalised
module: running-apps                  # required — matches folder slug (without NN-)
order: 2                              # required — order inside the module
estimated_minutes: 8                  # optional — default 5

learning_goal: "..."                  # optional — one line, what learner can do after
prerequisites: [pods, labels]         # optional — concept slugs from earlier lessons

intro: |                              # required — markdown shown first
  # ReplicaSets

  A **ReplicaSet** keeps a fixed number of Pods running.
  If a Pod stops, the ReplicaSet starts a new one.

task: |                               # required — what the user must do
  Create a ReplicaSet named `web` with 3 replicas of the `nginx` image.

  Save the YAML below and apply it with `kubectl apply -f`.

hint: "kubectl apply -f rs.yaml  (try `kubectl get rs` to check progress)"
                                       # optional — one short line

requires: [cluster]                   # optional — see step 5

warm_up:                              # optional — recall Qs from PREVIOUS lessons
  - prompt: "..."
    answer: "..."
    kind: recall                       # recall | multiple_choice | debug | scenario
    concept: some-concept              # for missed-concept logging

troubleshooting:                      # optional — one broken YAML/output + fix
  scenario: |
    ...broken YAML or command output...
  question: "What is wrong?"
  diagnosis: |
    ...explanation and fix...
  concept: some-concept

review_questions:                     # optional — 3–5 mixed Qs about NEW concept
  - prompt: "..."
    answer: "..."
    kind: multiple_choice
    options: ["A", "B", "C", "D"]
    concept: some-concept

common_mistakes:                      # optional — misconceptions + how to avoid
  - mistake: "..."
    fix: "..."

summary: "..."                        # optional — one short paragraph at the end

spaced_hooks:                         # optional — author metadata: revisit forward
  - concept: some-concept
    when: next                         # next | "2-3" | "5-7" | capstone

cheat: |                              # optional — quick reference after finishing
  ### Title
  - bullet points

check:                                # required — see step 4
  type: command
  cmd: "kubectl get rs web -o jsonpath='{.status.readyReplicas}'"
  expect: "3"
  timeout_seconds: 30
```

### Recall / review fields — the learning-science layer

These fields turn a static lesson into an active one. Use them for
**spaced repetition**, **retrieval practice**, and **interleaving**.

- **`learning_goal`** — the one thing the learner can DO after this lesson.
- **`prerequisites`** — concept slugs from earlier lessons the learner must have.
- **`warm_up`** — 2–3 short recall questions from PREVIOUS lessons. Shown before the intro. Force the learner to remember old material before new material is added on top.
- **`troubleshooting`** — one realistic broken YAML or bad command output + a "what is wrong?" question + the diagnosis. Trains debugging.
- **`review_questions`** — 3–5 questions at the end. Mix the four `kind` values:
  - `recall` — free recall (learner types nothing; app just reveals the answer)
  - `multiple_choice` — set `options: [A, B, C, D]` and `answer` matches one entry
  - `debug` — a broken snippet and "what is the fix?"
  - `scenario` — "you need X, which resource fits?"
- **`common_mistakes`** — 2–3 known misconceptions with the corrective fix.
- **`summary`** — one short paragraph that reinforces the key idea. Shown last.
- **`spaced_hooks`** — author metadata (not shown to learner). Marks which concept from THIS lesson should be reviewed later:
  - `next` — in the next lesson
  - `"2-3"` — 2–3 lessons later (quote it — YAML would read `2-3` as a string only if quoted)
  - `"5-7"` — 5–7 lessons later
  - `capstone` — in the final project

Use `/home/zymmio/projects/kuberT/LESSON_REVIEW_MAP.md` to know **which** concepts to reach back for. Look up the current lesson in "Recall in" and "Common failure mode" columns.

In the Textual app, warm-up and review questions are driven by the
`QuizScreen`: press **w** for warm-up, **r** for review. Space reveals
the answer, **y** = "I knew it", **n** = "I missed it" (logs the
`concept` to `~/.kubert/progress.json` for future mistake-based review).

### Field rules
- All text fields use **A2 English**: short sentences (8–12 words), simple words, no idioms. Define every K8s term the first time. See `feedback-lessons-a2-english` in memory.
- Markdown is fine inside `intro` and `task` (headings, lists, code blocks).
- Do not add fields not listed above. Pydantic uses `extra="forbid"` — unknown fields fail at load time.

## 4. Pick a check type

The `check` field tells the app how to verify the user finished the task. Three types:

### `manual` — for reading-only lessons
```yaml
check:
  type: manual
```
No verification. The app marks the lesson complete when the user presses `c`.

### `command` — run a shell command, look for a string
```yaml
check:
  type: command
  cmd: "kubectl get pod hello -o jsonpath='{.status.phase}'"
  expect: "Running"
  timeout_seconds: 30   # optional — default 30
```
- `cmd`: any shell command (uses `shell=True`).
- `expect`: a substring; the check passes when `expect` is found in `cmd`'s output (stdout + stderr).
- Use `jsonpath` to read one specific field — easier to match than full output.

### `multiple` — run several command checks in order
```yaml
check:
  type: multiple
  checks:
    - type: command
      cmd: "kubectl get pod hello -o jsonpath='{.status.phase}'"
      expect: "Running"
    - type: command
      cmd: "kubectl get pod hello -o jsonpath='{.spec.containers[0].image}'"
      expect: "nginx"
```
All sub-checks must pass. Stops at the first failure.

## 5. Declare requirements

If the lesson runs `kubectl` against the cluster, add:

```yaml
requires: [cluster]
```

The app verifies the cluster exists AND is reachable **before** running the lesson. If not, the user gets a clear "create the cluster first" message instead of a confusing `kubectl` error.

Reading-only intros omit `requires` (or use `requires: []`).

Currently the only supported value is `cluster`. To add more (e.g. `metrics-server`, `ingress`), update the `Requirement` Literal in `src/kubert/models.py` and add a check branch in `runner._check_requirements` and `lesson_screens.LessonScreen._check_req`.

## 6. Validate and run the lesson

### Run the tests
```bash
make test
```
The `test_lesson_loader.py` tests will:
- Load every YAML file under `lessons/`.
- Validate against the Pydantic schema (typos in field names, wrong types, unknown `requires` values all fail here).
- Confirm lesson IDs are unique.

Fix any failure before continuing.

### Try the lesson in the app
```bash
make run
```
1. Pick **"Pick a lesson from the list"** → find your lesson → Enter.
2. Read the intro → press `c` to check (or read).
3. If the check command runs but the lesson never marks complete, your `expect` substring may be wrong. Run the command yourself:
   ```bash
   kubectl get pod hello -o jsonpath='{.status.phase}'
   ```
   The output you see should literally contain your `expect` string.

## 7. Update ROADMAP.md

Add your lesson to the **Status** section of `ROADMAP.md`:

```
- `04-running-apps/02-replicasets` (sample, real kubectl check)
```

## 8. Commit

Per project rules:
- Short, plain commit message.
- No "Claude" / AI attribution.
- Commit per logical chunk — one or a few related lessons per commit is fine.

Example:
```bash
git add lessons/04-running-apps/02-replicasets.yaml ROADMAP.md
git commit -m "lesson: 04-running-apps/02-replicasets"
```

---

## Worked examples

### Example A — reading-only lesson (no cluster)

`lessons/01-introduction/02-why-kubernetes.yaml`
```yaml
id: 01-introduction/02-why-kubernetes
title: "Why people use Kubernetes"
module: introduction
order: 2
estimated_minutes: 5
intro: |
  # Why Kubernetes?

  People use Kubernetes for three big reasons:

  1. **It keeps apps alive.** If a server stops working,
     Kubernetes moves your app to another server.
  2. **It can grow and shrink.** When many users visit your
     app, Kubernetes adds more copies. When fewer visit,
     it removes copies.
  3. **It works the same everywhere.** Your laptop, a small
     cloud, or a big data centre — same setup, same commands.
task: |
  No task. Press `c` to mark this lesson as read.
check:
  type: manual
```

### Example B — real `kubectl` check (needs cluster)

`lessons/04-running-apps/02-replicasets.yaml`
```yaml
id: 04-running-apps/02-replicasets
title: "Your first ReplicaSet"
module: running-apps
order: 2
estimated_minutes: 10
intro: |
  # ReplicaSets

  A **ReplicaSet** keeps a fixed number of Pods running.
  If a Pod stops, the ReplicaSet starts a new one fast.

  You almost never make a ReplicaSet by yourself. You make
  a **Deployment**, and the Deployment makes a ReplicaSet
  for you. But it is good to know what a ReplicaSet does.
task: |
  Make a ReplicaSet with **3 copies** of the `nginx` image.
  Use the name `web`.

  In another terminal, run:
  ```
  cat <<EOF | kubectl apply -f -
  apiVersion: apps/v1
  kind: ReplicaSet
  metadata:
    name: web
  spec:
    replicas: 3
    selector:
      matchLabels: { app: web }
    template:
      metadata:
        labels: { app: web }
      spec:
        containers:
          - name: nginx
            image: nginx
  EOF
  ```

  Wait a few seconds, then press `c` to check.
hint: "kubectl get rs web -o yaml  -- look at status.readyReplicas"
requires: [cluster]
check:
  type: command
  cmd: "kubectl get rs web -o jsonpath='{.status.readyReplicas}'"
  expect: "3"
  timeout_seconds: 30
```

### Example C — multi-step check

```yaml
check:
  type: multiple
  checks:
    - type: command
      cmd: "kubectl get deploy web -o jsonpath='{.status.readyReplicas}'"
      expect: "2"
    - type: command
      cmd: "kubectl get svc web -o jsonpath='{.spec.type}'"
      expect: "ClusterIP"
```

---

## Common mistakes

| Mistake | What happens | Fix |
|---|---|---|
| `id` does not match folder/file | Loader test fails | Set `id: NN-module/NN-name` exactly. |
| Unknown field (e.g. `time: 5` instead of `estimated_minutes`) | Pydantic ValidationError | Use only the fields listed in the schema. |
| Lesson uses kubectl but no `requires: [cluster]` | User gets confusing kubectl error | Add `requires: [cluster]`. |
| `expect` is too long or copies the full output | Substring never matches | Use a `jsonpath` query to return just one field. |
| Intro uses idioms ("spin up", "under the hood") | A2 rule broken | Rewrite with plain words. |
| Two lessons share the same `id` | `test_lesson_ids_are_unique` fails | Rename one. |

---

## When you change the schema itself

If you add or rename a field on `Lesson`:

1. Update `src/kubert/models.py`.
2. Update every YAML under `lessons/`.
3. Update this file (`ADD_LESSON.md`).
4. Update the schema summary in `CLAUDE.md`.
5. Add or update a test in `tests/test_lesson_loader.py`.
6. Run `make test`.
7. Commit.
