# AgenticOS

**Deterministic AI Agent Orchestration Framework**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

AgenticOS is a portable, auditable AI agent operating layer for running AI-assisted workflows safely. It provides deterministic routing, structured logging, and multi-provider support for security-conscious environments.

---

## Quick Start

```bash
# Clone and install
git clone https://github.com/Pharns/AgenticOS.git
cd AgenticOS
./install.sh

# Verify installation
./scripts/aos doctor

# Run your first command
aos q "What is a buffer overflow?"
```

---

## Features

- **Unified CLI (`aos`)** — Single command for all operations
- **Multi-Provider Support** — Claude, Codex, and Gemini
- **Auto-Routing** — Keyword and AI-powered profile selection
- **Audit-Grade Logging** — JSON logs for every execution
- **Health Validation** — 40+ checks with auto-fix capability
- **Project Isolation** — Per-project configurations
- **Memory Persistence** — Session continuity across invocations

---

## Usage Examples

```bash
# Quick questions (Gemini)
aos q "Explain SQL injection"

# Development tasks (Codex)
aos d "Fix the authentication bug"

# GRC/Compliance writing (Claude)
aos g "Draft a password policy for SOC 2"

# Auto-route based on keywords
aos auto "Write a security policy"        # → grc
aos auto "Fix the login error"            # → dev

# Work on a specific project
aos -p myproject d "Add input validation"
```

---

## Directory Structure

```
AgenticOS/
├── scripts/
│   ├── aos              # Unified CLI (start here)
│   ├── router           # Routing engine
│   ├── agent            # Execution engine
│   ├── doctor           # Health validation
│   └── memory           # Memory management
├── .agents/
│   ├── agents.yaml      # Profile definitions
│   ├── workflows.yaml   # Workflow definitions
│   ├── router_auto_rules.json
│   ├── prompts/         # System prompts
│   ├── logs/            # Execution logs
│   └── memory/          # Persistent memory
├── docs/                # Documentation
└── install.sh           # Installer
```

---

## Documentation

| Document | Description |
|----------|-------------|
| [User Guide](USER_GUIDE.md) | Complete reference |
| [Quick Start](docs/aos-quickstart.md) | Get started in 5 minutes |
| [Core Commands](docs/01-core-commands.md) | Command reference |
| [Auto-Routing](docs/02-router-auto-v1.md) | Routing system details |
| [Design Philosophy](docs/07-design-decisions.md) | Why AgenticOS works this way |

---

## Requirements

- Python 3.10+
- At least one AI provider CLI:
  - `claude` (Anthropic)
  - `codex` (OpenAI)
  - `gemini` (Google)

---

## Security Model

- **No auto-execution** — Generated code is never auto-executed
- **User-triggered only** — Only explicit commands run
- **No secrets in repo** — Credentials in `.env` (gitignored)
- **Full audit trail** — Every action logged with context
- **Deterministic** — Same inputs produce same behavior

---

## Design Philosophy

AgenticOS chooses:

- Explicit contracts over intelligence
- Ordered rules over scoring
- Determinism over convenience
- Boring correctness over novelty

**If behavior is unclear, AgenticOS will fail or explain — never guess.**

---

## License

MIT License. See [LICENSE](LICENSE) for details.

---

## Author

**Pharns Génécé** — [Portfolio](https://portfolio.pharns.com) · [GitHub](https://github.com/Pharns) · [LinkedIn](https://linkedin.com/in/pharns)
