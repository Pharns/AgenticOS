# AgenticOS — User Guide (Authoritative)

**Version:** v1.x
**Status:** Operational
**Audience:** Engineers, operators, auditors
**Scope:** Canonical behavior and guarantees only

---

## 1. Router-First Quick Start

The `scripts/router` is the recommended and authoritative entry point for most operations. It decides which action to take based on your input.

```bash
# Use the router to auto-route to a workflow based on a task keyword
./scripts/router auto --task ops
```

This command will match the `ops` keyword against predefined rules, route to the `ops_check` workflow, and display the steps, all without direct execution. The router decides; the agent executes.

---

## Daily Engineering Logs

- [Technical Update — 2025-12-12](docs/logs/technical-update-2025-12-12.md)

---

## 2. What AgenticOS Is (and Is Not)

### What it is
AgenticOS is a **deterministic, auditable agent operating layer** for running AI-assisted workflows safely.

It provides:
- Explicit routing (`router`)
- Controlled execution (`agent`)
- Continuous validation (`doctor`)
- Persistent memory and deltas (`.agents/memory`)
- Structured logs with explainable decisions

AgenticOS is designed to be:
- Predictable
- Explainable
- Scriptable
- Safe for CI/CD and regulated environments

### What it is not
AgenticOS is **not**:
- An autonomous AI system
- A semantic intent engine
- A hidden decision-maker
- A replacement for human judgment

There is **no inference, no magic, and no silent behavior**.

---

## 3. Core Concepts

### Determinism
Given the same inputs, AgenticOS will always produce the same behavior.

### Explainability
Every routing decision prints **why** it happened and is recorded in logs.

### Explicitness
Nothing happens unless it is explicitly requested by flags, rules, or commands.

### Auditability
All executions produce machine-readable logs suitable for review.

---

## 4. Core Commands

### `scripts/router` (Authoritative Entry Point)
The `scripts/router` is the primary and recommended entry point. It decides which action to take by routing execution to a profile or workflow.

Supports:
- Explicit routing
- Deterministic auto-routing
- Explain and dry-run modes

### `scripts/agent` (Advanced Usage)
The `scripts/agent` is the underlying execution engine that runs a specific agent profile. Direct usage is supported but considered an advanced or intentional action for when direct execution is required without routing.

Key properties:
- No hidden prompt mutation
- Structured output expectations
- Optional workflow context
- Emits logs and deltas

### `scripts/doctor`
Validates system health and invariants.

- Default mode: checks and warnings
- `--strict`: enforces hard guarantees and exits non-zero on violations

---

## 5. Router Auto (v1)

### Purpose
`router auto` selects a workflow or profile **deterministically** based on explicit rules.

### Precedence Order (Highest → Lowest)

1. `--workflow <name>`
2. `--profile <name>`
3. `--task <token>` (repeatable)
4. Free-text arguments (fallback only)

---

### Rule Matching
- Literal, lowercase token matching
- No NLP or semantic parsing
- Ordered rules
- **First match wins**

Rules are defined in:
```
.agents/router_auto_rules.json
```

Each rule must include:
- `id` (unique)
- `match_all` (non-empty array)
- optional `match_any`
- `route.type` ∈ {`workflow`, `profile`}
- `route.target`

---

### Strict Mode

```bash
scripts/router auto --strict --task bug fix
```

Strict mode:

- Requires at least one `--task`
- Disables free-text fallback
- Exit codes:
    - `0` → matched
    - `1` → no rule matched
    - `2` → invalid invocation (e.g., missing `--task`)

---

### Explain & Dry Run

```bash
scripts/router auto --explain --dry-run "fix the login bug"
```

- `--explain`: shows tokens, evaluated rules, and match reasoning
- `--dry-run`: prints the selected route without executing it

---

## 6. Workflow Memory & Delta (Phase 2)

### Purpose

Capture **what changed and why** for every workflow run.

### Delta Sources

1. **Agent-authored delta** (`Delta:` section in output)
2. **Optional git delta** (`--delta-from-git`)

---

### Git Delta (Optional)

When `--delta-from-git` is provided and the repo is a git repository:

- Captures file names only
    - Unstaged: `git diff --name-only`
    - Staged: `git diff --name-only --staged`
- No file contents
- Silently skipped if unavailable

---

### Workflow Memory Location

```
.agents/memory/workflows/<workflow>.md
```

Each run records:

- Last delta
- Delta sources
- Timestamp (UTC)

---

## 7. Logging & Auditing

### Log Location

```
.agents/logs/*.json
```

### Key Fields

- `run_id` — shared across router, agent, and workflow logs
- `auto_route` — routing decision details
- `delta` — structured change summary
- `workflow` / `profile` — execution context

Logs are validated against a schema in strict mode.

---

## 8. Doctor & Validation

### `doctor --strict` Enforces:

- Valid router rules file
- Unique rule IDs
- Non-empty `match_all`
- Valid route targets
- Log schema conformance

### Warn-Only (Phase 2)

- Warns if workflows run without deltas
- Does not fail execution (by design)

---

## 9. Operational Modes

### Interactive (Human)

- Free-text fallback allowed
- Explain and dry-run encouraged

### CI / Automation

- Use `--strict`
- Use explicit `--task`, `--workflow`, or `--profile`
- Treat non-zero exits as failures

---

## 10. Design Philosophy

AgenticOS chooses:

- Explicit contracts over intelligence
- Ordered rules over scoring
- Determinism over convenience
- Boring correctness over novelty

This is intentional.

---

## 11. Roadmap (Non-Binding)

Future phases may include:

- Workflow chaining
- Replay and provenance
- Policy enforcement layers

These will be opt-in and contract-driven.

---

## Final Note

If behavior is unclear, AgenticOS will **fail or explain** — never guess.

That is the system working as designed.
