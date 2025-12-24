# aos Quick Start Guide

**aos** (AgenticOS CLI) is the unified command interface for AgenticOS. It provides shortcut commands to run AI agent profiles, manage workflows, and control the system.

## Installation

```bash
# From AgenticOS root directory
./install.sh

# Or manually install the global command
sudo ln -sf "$(pwd)/scripts/aos" /usr/local/bin/aos
```

Verify installation:

```bash
aos version
aos doctor
```

## Basic Usage

```bash
aos                         # List available profiles & workflows
aos <profile> "prompt"      # Run a profile with a prompt
aos auto "prompt"           # Auto-pick the best profile
aos help                    # Show full help
```

## Profiles & Aliases

| Alias | Profile | Provider | Description |
|-------|---------|----------|-------------|
| `d` | dev | Codex | Development assistant |
| `q` | quick | Gemini | Fast brainstorming (clean output) |
| `g` | grc | Claude | GRC/compliance writing |
| `r` | research | Claude | Deep research & analysis |
| `o` | ops | Codex | Ops/debugging assistant |

### Running Profiles

```bash
# Using full name
aos dev "Fix the authentication bug"

# Using alias (shorter)
aos d "Fix the authentication bug"

# Quick questions (clean output by default)
aos q "What is 2+2?"         # Just shows: "4"
aos q "What is 2+2?" -v      # Verbose output with all sections
```

## Auto-Routing

Let AgenticOS pick the best profile for your prompt:

### Keyword-Based (Fast)

```bash
aos auto "What is photosynthesis?"      # → quick (question words)
aos auto "Fix the login error"          # → dev (fix/error keywords)
aos auto "Write a password policy"      # → grc (policy keywords)
aos auto "Analyze the performance"      # → research (analyze keyword)
```

### AI-Powered (Smarter)

```bash
aos auto --smart "Help me understand this codebase"
```

Uses Gemini to intelligently classify your prompt and pick the best profile.

### Auto-Routing Options

```bash
aos auto --dry-run "prompt"              # Show what would run without running
aos auto --explain "prompt"              # Show detailed matching info
aos auto --smart "prompt"                # Use AI classification
aos auto "prompt" -- --full-auto         # Pass options to target profile
aos auto -- --full-auto "prompt"         # Same (prompt can be before or after --)
```

## Common Commands

### System

```bash
aos doctor              # Health check
aos doctor --fix        # Auto-fix common issues
aos list                # List profiles & workflows
aos list --json         # JSON output
```

### Running Agents

```bash
aos d "prompt"          # Run dev profile
aos q "prompt"          # Quick question (clean output)
aos q "prompt" -v       # Quick with verbose output
aos run dev "prompt"    # Explicit run command
```

### Workflows

```bash
aos wf auto_fix_bug "Fix the login issue"    # Execute workflow
aos wf ops_check                              # Run ops check workflow
```

### Session Management

```bash
aos continue            # Continue last session
aos logs                # List recent logs
aos logs --tail         # Show last log output
aos logs --rotate 30    # Archive logs older than 30 days
```

### Memory

```bash
aos memory              # Show memory summary
aos memory dev          # Show dev profile memory
aos memory --clear dev  # Clear dev profile memory
```

## Project Management

Register and manage multiple AgenticOS projects:

```bash
# List registered projects (simple)
aos projects

# List with details (paths, aliases, status)
aos projects -v

# Register current directory as a project
aos projects add .

# Register with custom name and alias
aos projects add /path/to/project --name myproj --alias mp

# Remove a project
aos projects remove myproj

# Scan for AgenticOS projects
aos projects scan ~/Projects

# Add alias to existing project
aos projects alias myproj m
```

### Project Mode

Run AgenticOS against a registered project or path:

```bash
# Using registered project name
aos -p myproj d "Help with this code"
aos -p myproj list

# Using project alias
aos -p mp list

# Using full path
aos -p /path/to/project d "prompt"
```

Projects are stored in `~/.agenticos/projects.yaml`.

### Initialize New Project

```bash
cd /path/to/new/project
aos init
```

This creates:
```
.agents/
├── agents.yaml
├── prompts/
│   ├── dev.md
│   └── quick.md
├── memory/
├── logs/
└── workflows.yaml
```

## Options Reference

### Quick Profile Options

The `q` (quick) profile has special defaults for clean output:

| Command | Behavior |
|---------|----------|
| `aos q "prompt"` | Clean output, no memory, quiet mode |
| `aos q "prompt" -v` | Full verbose output with all sections |

### General Options

Pass options after `--` to forward them to the agent:

| Option | Description |
|--------|-------------|
| `-v, --verbose` | Full verbose output (overrides clean mode) |
| `--no-memory` | Don't use/update memory |
| `--quiet` | Suppress banners and status |
| `--print clean` | Just the answer, no section headers |
| `--print summary` | Show only 3-line summary |
| `--print raw` | Show raw provider output |
| `--continue last` | Continue from last session |
| `--continue <id>` | Continue specific session |

### Examples

```bash
# Quick question with just the answer
aos q "What is 2+2?"

# Quick question with full output
aos q "Explain recursion" -v

# Dev profile with no memory
aos d -- --no-memory "One-off fix"

# Continue previous conversation
aos d -- --continue last "Now add tests"
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `AGENT_TIMEOUT` | Override default timeout (seconds) |
| `AGENT_DRY_RUN` | Set to `1` to skip actual execution |

```bash
AGENT_TIMEOUT=300 aos d "Complex refactoring task"
```

## Workflow Examples

### Quick Question

```bash
aos q "What's the best way to implement rate limiting?"
```

### Auto-Route a Task

```bash
aos auto "Fix the authentication bug"    # Auto-picks dev
aos auto --smart "Design a caching layer"  # AI picks best profile
```

### Development Task

```bash
aos d "Add input validation to the user registration form"
```

### Continue Working

```bash
# Start a task
aos d "Implement the caching layer"

# Continue later
aos continue
# or
aos d -- --continue last "Now add cache invalidation"
```

### Research Then Implement

```bash
# Research first
aos r "Best practices for JWT authentication in Python"

# Then implement
aos d "Implement JWT auth based on the research"
```

### Work on a Specific Project

```bash
# List your projects
aos projects

# Work on a specific project
aos -p giap d "Add user authentication"
aos -p portfolio q "What pages need updating?"

# Auto-route with write access on a project
aos -p portfolio auto --smart -- --full-auto "Add a contact page"
```

### Check System Health

```bash
aos doctor --fix
aos logs --tail
```

## Troubleshooting

### Command not found

```bash
# Reinstall symlink
sudo ln -sf "/path/to/AgenticOS/scripts/aos" /usr/local/bin/aos
```

### Provider not available

```bash
# Check which providers are installed
aos doctor

# See provider setup docs
cat docs/08-provider-integration.md
```

### Profile not found

```bash
# List available profiles
aos list

# Check agents.yaml configuration
cat .agents/agents.yaml
```

### Auto-routing not matching

```bash
# See why a rule matched or didn't
aos auto --explain "your prompt"

# Use AI routing for ambiguous prompts
aos auto --smart "your prompt"

# Edit rules manually
cat .agents/router_auto_rules.json
```

## File Locations

| Path | Description |
|------|-------------|
| `.agents/agents.yaml` | Profile configurations |
| `.agents/workflows.yaml` | Workflow definitions |
| `.agents/prompts/` | Profile prompt files |
| `.agents/memory/` | Session memory |
| `.agents/logs/` | Execution logs |
| `.agents/router_auto_rules.json` | Auto-routing keyword rules |
| `~/.agenticos/projects.yaml` | Registered projects |

## Getting Help

```bash
aos help                # Full command reference
aos doctor              # System diagnostics
aos version             # Version info
aos auto                # Auto-routing help
```
