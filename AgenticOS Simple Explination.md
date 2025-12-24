# AgenticOS — Simple Explanation (Shareable, ChatGPT‑style)

## 🤔 What it is
AgenticOS is a **safe control center** for AI helpers. You describe what you want; it picks the right AI, runs it safely, and records everything so you can repeat or audit it.

## 🧩 Core parts
- **Router (`scripts/router`)** — Front door: reads your request and picks the right helper (dev, ops, grc, research) using rules.
- **Agent (`scripts/agent`)** — Worker: runs the AI with strict output sections (Plan, Code changes, Verification) and logs every run.
- **Doctor (`scripts/doctor`)** — Health check: confirms configs, executables, and writable dirs are correct.
- **Memory & Logs (`.agents/`)** — Notebook + camera: saves what happened (JSON logs and human-readable memory) so you can resume or hand off.

## 🚀 How to use (day to day)
1. Check health: `./scripts/doctor --strict`
2. Auto-pick a helper: `./scripts/router auto "fix the login bug"`
3. Run a specific helper: `./scripts/agent --profile dev --print norm <<< "your task here"`
4. Inspect logs: `ls .agents/logs/` (JSON per run)

## ✅ Why it matters
- **Predictable**: Same input → same behavior.
- **Auditable**: Every run is logged (who, what, when, output).
- **Safe**: No risky shell tricks; clear prompts and sections.
- **Reusable**: Memory captures history for quick handoffs.

## ⚠️ Current blocker
- Codex AI calls need a valid API key; until then, Plan/Code/Verification may be empty. Set `OPENAI_API_KEY` (or your Codex key) and rerun.

## 🔄 Resume checklist
- `export OPENAI_API_KEY="YOUR_KEY"`
- `CODEX_HOME="$(pwd)/.agents/codex" CODEX_SESSION_DIR="$(pwd)/.agents/codex_sessions" AGENT_TIMEOUT=120 ./scripts/agent --profile dev --print norm <<< "your task here"`
- Optional: `.venv/bin/pip install jsonschema && ./scripts/doctor --strict`

## 🛣️ Router “NO MATCH” explained (nothing is broken)
If you ran:
```
./scripts/router auto "what is the last thing we did today"
```
and saw “NO MATCH”, that’s expected. The router is rule-based: it looks for action words that match its rules (fix, generate, review, summarize, etc.). Your query was a memory/status question, not an action, so it correctly did nothing.

How to phrase it today:
- `./scripts/router auto "summarize today's AgenticOS work"`
- `./scripts/router auto "generate a technical summary of today's AgenticOS session"`

Key idea: the router is for tasks, not open-ended chat. This keeps AgenticOS strict and predictable. If you want, we can later add a summary/memory rule to handle these queries directly.
