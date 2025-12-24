# AgenticOS — Cross-Platform Agentic Workflow Template (Ubuntu + macOS)

AgenticOS is a **portable, deterministic, auditable agent operating layer** you can drop into any project. It provides a structured, predictable way to run AI-assisted workflows safely in any environment.

> **Note:** For the complete, authoritative documentation, please refer to **[[USER_GUIDE.md]]**. This README provides a high-level overview and quick-start guide.

---

## ✨ Core Features

*   **Authoritative Entry Point:** `scripts/router` acts as the primary, recommended entry point that *decides* which action to take.
*   **Controlled Execution:** `scripts/agent` is the underlying execution engine that *runs* a specific task, and is documented for advanced or intentional direct usage.
*   **Declarative Definitions:** Agent profiles are defined in `.agents/agents.yaml` and multi-step sequences in `.agents/workflows.yaml`.
*   **Structured Logging:** All actions are recorded in machine-readable JSON format under `.agents/logs/`.
*   **Continuous Validation:** The `scripts/doctor` command ensures system health and enforces operational guarantees.
*   **Persistent Memory & Deltas:** An optional system at `.agents/memory/` captures and tracks changes across sessions.

---

## 📚 Documentation

For in-depth technical details, please see the documentation in the `docs/` folder:

*   **[[docs/00-introduction|00 - Introduction to AgenticOS]]**
*   **[[docs/01-core-commands|01 - Core Commands Reference]]**
*   **[[docs/02-router-auto-v1|02 - Router Auto (v1)]]**
*   **[[docs/03-strict-mode|03 - Strict Mode and CI/Automation]]**
*   **[[docs/04-workflow-memory-delta|04 - Workflow Memory & Delta]]**
*   **[[docs/05-logging-and-audit|05 - Logging & Auditing]]**
*   **[[docs/06-doctor-and-validation|06 - Doctor & Validation]]**
*   **[[docs/07-design-decisions|07 - Design Philosophy]]**
*   **[[docs/99-roadmap|99 - Roadmap]]**

## Recent Technical Updates

- [Technical Update — 2025-12-12](docs/logs/technical-update-2025-12-12.md)

---

## 🚀 Quick Start

### 1. Router-First Quick Start

The `scripts/router` is the recommended and authoritative entry point for most operations.

```bash
# Use the router to auto-route to a workflow based on a task keyword
./scripts/router auto --task ops
```

This command will match the `ops` keyword, route to the `ops_check` workflow, and display the steps. The router decides; the agent executes.

### 2. Install (macOS / Ubuntu supported)

```bash
cd /path/to/AgenticOS
chmod +x install.sh
./install.sh
```
This creates a Python virtual environment (`.venv/`), installs `pyyaml`, and sets execute permissions on the core scripts. Note: You must install your desired LLM provider CLIs (e.g., `codex`, `claude`) separately.

### 3. Launch an Agent or Workflow

The `scripts/router` is the recommended entry point for most operations.

```bash
# Use the router to auto-route to a workflow based on a task keyword
./scripts/router auto --task ops

# Use the router to explicitly run a profile
./scripts/router run dev
```

For advanced use or intentional direct execution, `scripts/agent` remains fully supported:

```bash
# Directly run a profile (advanced use)
./scripts/agent --profile dev
```
The system will load the appropriate profile, execute the command, and write a session log.

### 4. View a Workflow's Steps

```bash
# View the steps of a workflow
./scripts/agent-workflow ops_check
```

---

## 📁 Folder Structure

```text
AgenticOS/
  README.md
  USER_GUIDE.md
  install.sh

  scripts/
    router              # Primary entry point; decides what to run
    agent               # Execution engine; runs a specific task
    doctor
    agent-workflow

  docs/
    00-introduction.md
    ...

  .agents/
    agents.yaml
    workflows.yaml
    router_auto_rules.json
    prompts/
    logs/
    memory/
```

This folder can be used directly, copied into any repository, or configured as a GitHub template.

---

## 🛡 Security & Threat Model

Inspired by Daniel Miessler:

*   AgenticOS **never auto-executes generated code**.
*   Only user-triggered shell commands run.
*   Command templates are explicit and human-reviewed.
*   No hardcoded secrets are stored anywhere.
*   `.agents/logs/` is **gitignored** by default.
*   Safe for use inside professional or regulated environments.

---

## ✔️ Status

This README reflects the **final, correct, production-ready** overview for AgenticOS. For detailed contracts and behavior, see **[[USER_GUIDE.md]]**.
