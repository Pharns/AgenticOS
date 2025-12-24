# AgenticOS User Guide

**Version:** 1.0.0
**Status:** Production
**Audience:** Engineers, operators, security teams

---

## Quick Start

```bash
# Install
git clone https://github.com/Pharns/AgenticOS.git
cd AgenticOS
./install.sh

# Verify
./scripts/aos doctor

# Ask a quick question
aos q "What is SQL injection?"

# Run a development task
aos d "Fix the authentication bug"

# Auto-route based on keywords
aos auto "Write a security policy"
```

---

## What is AgenticOS?

AgenticOS is a **deterministic, auditable AI agent orchestration layer** for running AI-assisted workflows safely.

### Core Principles

| Principle | Description |
|-----------|-------------|
| **Determinism** | Same inputs always produce same behavior |
| **Explainability** | Every routing decision is logged with reasoning |
| **Explicitness** | Nothing happens unless explicitly requested |
| **Auditability** | All executions produce machine-readable logs |

### What AgenticOS is NOT

- An autonomous AI system
- A semantic intent engine
- A hidden decision-maker
- A replacement for human judgment

**No inference. No magic. No silent behavior.**

---

## The `aos` Command

`aos` is the unified CLI that wraps all AgenticOS functionality.

### Basic Commands

```bash
aos                     # List profiles and workflows
aos help                # Show help
aos doctor              # Health check (40+ validations)
aos doctor --fix        # Auto-repair common issues
```

### Running Profiles

```bash
aos q "your question"           # Quick question (Gemini)
aos d "your task"               # Development task (Codex)
aos g "your request"            # GRC/compliance writing (Claude)

# Or use full profile names
aos quick "your question"
aos dev "your task"
aos grc "your request"
```

### Auto-Routing

Let AgenticOS pick the best profile based on your prompt:

```bash
# Keyword-based (fast, deterministic)
aos auto "Fix the login bug"              # Routes to 'dev'
aos auto "Write a password policy"        # Routes to 'grc'
aos auto "What is XSS?"                   # Routes to 'quick'

# AI-powered (uses Gemini to classify)
aos auto --smart "Help me design a caching layer"

# Debug routing decisions
aos auto --dry-run "your prompt"          # See what would run
aos auto --explain "your prompt"          # See rule evaluation
```

### Project Mode

Work on a specific project with its own `.agents/` configuration:

```bash
# Register a project
aos projects                              # List registered projects

# Work on a project
aos -p myproject d "Add logging"          # Dev task on myproject
aos -p portfolio auto "Fix the nav"       # Auto-route on portfolio
```

### Passthrough Arguments

Pass flags to the underlying AI provider:

```bash
aos d "your task" -- --full-auto          # Enable write access (Codex)
aos -p myproject d -- --full-auto "task"  # Project + full-auto
```

---

## Profiles

Profiles define which AI provider to use and how to configure it.

| Profile | Alias | Provider | Use Case |
|---------|-------|----------|----------|
| quick | q | Gemini | Fast questions, brainstorming |
| dev | d | Codex | Code generation, debugging |
| grc | g | Claude | Compliance writing, deep analysis |
| ops | - | Codex | Operations, system tasks |
| research | - | Claude | Research, documentation |

Profiles are defined in `.agents/agents.yaml`.

---

## Auto-Routing Rules

Auto-routing uses keyword matching to select the best profile or workflow.

### How It Works

1. Your prompt is tokenized (lowercase, split on spaces)
2. Rules are evaluated in order (first match wins)
3. Each rule specifies `match_all` and/or `match_any` keywords
4. Matched rule's target profile/workflow is executed

### Rule Configuration

Rules are defined in `.agents/router_auto_rules.json`:

```json
{
  "rules": [
    {
      "id": "grc_policy",
      "description": "Route security policy writing to grc",
      "match_all": [],
      "match_any": ["policy", "compliance", "audit", "nist"],
      "route": {"type": "profile", "target": "grc"}
    }
  ]
}
```

| Field | Required | Description |
|-------|----------|-------------|
| `id` | Yes | Unique identifier |
| `match_all` | Yes | Keywords that must ALL be present (can be empty) |
| `match_any` | No | Keywords where at least ONE must be present |
| `route.type` | Yes | `"profile"` or `"workflow"` |
| `route.target` | Yes | Name of the profile or workflow |

### Strict Mode (CI/Automation)

```bash
aos auto --strict --task bug --task fix "description"
```

- Requires explicit `--task` flags
- Disables free-text fallback
- Exit codes: 0=matched, 1=no match, 2=invalid invocation

---

## Workflows

Workflows chain multiple profile executions together.

```bash
# Run a workflow
aos wf ops_check

# View workflow steps
aos wf ops_check --dry-run
```

Workflows are defined in `.agents/workflows.yaml`.

---

## Health Checks

The doctor command validates your AgenticOS installation:

```bash
aos doctor              # Run all checks
aos doctor --fix        # Auto-repair issues
aos doctor --strict     # Treat warnings as failures
```

Checks include:
- YAML/JSON syntax validation
- Provider CLI availability (claude, codex, gemini)
- Directory structure and permissions
- Log schema conformance
- Rule configuration validity

---

## Logging

All executions produce structured JSON logs in `.agents/logs/`.

```json
{
  "run_id": "7c956f40-ada8-456c-8fbb-54c22de65b55",
  "profile": "dev",
  "provider": "codex",
  "timestamp_start": "2025-12-23T14:32:07Z",
  "timestamp_end": "2025-12-23T14:32:45Z",
  "exit_code": 0,
  "tags": ["profile:dev", "provider:codex", "memory:on"]
}
```

### Log Rotation

Logs older than 7 days are automatically compressed. Configure retention in `agents.yaml`.

---

## Memory Persistence

Session state persists across invocations:

```
.agents/memory/
├── profiles/          # Per-profile memory files
├── sessions/          # Daily session logs
├── workflows/         # Workflow execution history
└── summary.md         # Rolling summary
```

View memory:
```bash
aos memory             # Show all memory
aos memory dev         # Show dev profile memory
```

---

## Directory Structure

```
AgenticOS/
├── scripts/
│   ├── aos              # Unified CLI (primary entry point)
│   ├── router           # Routing engine
│   ├── agent            # Execution engine
│   ├── doctor           # Health validation
│   └── memory           # Memory management
├── .agents/
│   ├── agents.yaml      # Profile definitions
│   ├── workflows.yaml   # Workflow definitions
│   ├── router_auto_rules.json
│   ├── prompts/         # System prompts per profile
│   ├── logs/            # Execution logs (gitignored)
│   └── memory/          # Persistent memory
├── docs/                # Documentation
├── install.sh           # Installer
└── requirements.txt
```

---

## Environment Setup

### Required

1. Python 3.10+
2. At least one AI provider CLI:
   - `claude` (Anthropic)
   - `codex` (OpenAI)
   - `gemini` (Google)

### Installation

```bash
./install.sh
```

This creates a virtual environment, installs dependencies, and sets permissions.

### API Keys

Create `.env` with your API keys (see `.env.example`):

```bash
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
GOOGLE_API_KEY=...
```

---

## Security Model

- **No auto-execution:** Generated code is never auto-executed
- **User-triggered only:** Only explicit commands run
- **No secrets in repo:** Credentials in `.env` (gitignored)
- **Audit trail:** All actions logged with full context
- **Safe for CI/CD:** Deterministic, scriptable, exit codes meaningful

---

## Troubleshooting

### Provider not found

```bash
aos doctor --fix        # Checks provider CLIs
```

Install missing providers:
```bash
npm install -g @anthropic-ai/claude-code
pip install openai-codex
npm install -g @anthropic-ai/claude-code  # Gemini
```

### Smart routing timeout

```bash
# Use keyword routing instead
aos auto "your prompt"

# Or increase timeout
aos auto --smart --timeout 60 "your prompt"
```

### Permission denied

```bash
chmod +x scripts/*
./install.sh
```

---

## Design Philosophy

AgenticOS chooses:

- **Explicit contracts** over intelligence
- **Ordered rules** over scoring
- **Determinism** over convenience
- **Boring correctness** over novelty

If behavior is unclear, AgenticOS will **fail or explain** — never guess.

---

## Further Reading

- [Quick Start Guide](docs/aos-quickstart.md)
- [Core Commands Reference](docs/01-core-commands.md)
- [Router Auto Documentation](docs/02-router-auto-v1.md)
- [Logging & Auditing](docs/05-logging-and-audit.md)
- [Design Decisions](docs/07-design-decisions.md)

---

## License

MIT License. See [LICENSE](LICENSE) for details.
