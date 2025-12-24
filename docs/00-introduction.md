# 00 - Introduction to AgenticOS

## 1. What AgenticOS Is (and Is Not)

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

## 2. Core Concepts

### Determinism
Given the same inputs, AgenticOS will always produce the same behavior.

### Explainability
Every routing decision prints **why** it happened and is recorded in logs.

### Explicitness
Nothing happens unless it is explicitly requested by flags, rules, or commands.

### Auditability
All executions produce machine-readable logs suitable for review.
