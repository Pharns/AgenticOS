# 08 - Provider Integration Guide

AgenticOS supports multiple AI providers. This guide covers installation and authentication for each.

---

## Supported Providers

| Provider | CLI Command | Profiles | Install Method |
|----------|-------------|----------|----------------|
| Claude Code | `claude` | research, grc | npm or standalone |
| Gemini CLI | `gemini` | quick | npm |
| Codex CLI | `codex` | dev, ops | npm or standalone |
| Cursor Agent | `cursor-agent` | refactor | standalone |

---

## 1. Claude Code

**Profiles:** `research`, `grc`

### Installation

```bash
# Via npm (recommended)
npm install -g @anthropic-ai/claude-code

# Or download standalone from:
# https://claude.ai/download
```

### Authentication

```bash
# Interactive login (opens browser)
claude

# Check status
claude --version
```

Authentication is handled via browser-based OAuth. Credentials are stored in `~/.claude/`.

### Verify

```bash
claude -p "Say hello"
```

---

## 2. Gemini CLI

**Profiles:** `quick`

### Installation

```bash
# Via npm
npm install -g @anthropic-ai/gemini-cli

# Or via the Google Cloud SDK
```

### Authentication

```bash
# First run triggers OAuth flow
gemini "Hello"

# Check status - credentials cached after first auth
```

Credentials are cached after initial authentication.

### Verify

```bash
gemini -o text "What is 2+2?"
```

---

## 3. Codex CLI

**Profiles:** `dev`, `ops`

### Installation

```bash
# Via npm
npm install -g @openai/codex

# Or download from:
# https://github.com/openai/codex-cli
```

### Authentication

```bash
# Interactive login (browser-based)
codex login

# Or via API key
export OPENAI_API_KEY="sk-..."
echo "$OPENAI_API_KEY" | codex login --with-api-key

# Check status
codex login status
```

Credentials are stored in `~/.codex/auth.json`.

### AgenticOS Integration

AgenticOS uses a custom `CODEX_HOME` directory. To share authentication:

```bash
# Symlink auth from default location
ln -sf ~/.codex/auth.json .agents/codex/auth.json
```

### Verify

```bash
echo "Say hello" | codex exec --skip-git-repo-check -
```

---

## 4. Cursor Agent

**Profiles:** `refactor`

### Installation

```bash
# Download from Cursor website
# https://cursor.com/download

# The cursor-agent CLI is included with Cursor IDE
# Or install standalone:
npm install -g cursor-agent
```

### Authentication

```bash
# Interactive login
cursor-agent login

# Check status
cursor-agent status
```

### Verify

```bash
cursor-agent -p "Say hello"
```

### Known Issues

- **Rate Limiting:** Cursor Agent may return `resource_exhausted` errors during heavy usage. Wait and retry.

---

## Provider Status Check

Run the doctor to verify all providers are available:

```bash
./scripts/doctor --strict
```

Look for `[OK] profile:*:cli` entries confirming each CLI is found on PATH.

---

## Environment Variables

| Variable | Provider | Purpose |
|----------|----------|---------|
| `OPENAI_API_KEY` | Codex | API authentication (alternative to login) |
| `CODEX_HOME` | Codex | Config directory (default: `~/.codex`) |
| `CODEX_SESSION_DIR` | Codex | Session storage |
| `ANTHROPIC_API_KEY` | Claude | API authentication (if not using OAuth) |
| `CURSOR_API_KEY` | Cursor | API authentication (if not using login) |

---

## Adding a New Provider

To add a new provider:

1. **Add profile to `.agents/agents.yaml`:**
   ```yaml
   new_profile:
     description: "Description of the profile"
     keywords: ["keyword1", "keyword2"]
     provider: provider-name
     prompt: ".agents/prompts/new_profile.md"
     command: 'provider-cli args'
     memory_file: ".agents/memory/profiles/new_profile.md"
   ```

2. **Create prompt file:** `.agents/prompts/new_profile.md`

3. **Create memory file:** `.agents/memory/profiles/new_profile.md`

4. **Add provider handling to `scripts/agent`** (if special stdin/argument handling needed)

5. **Run doctor to verify:**
   ```bash
   ./scripts/doctor --strict
   ```

---

## Troubleshooting

See [[10-troubleshooting]] for common provider issues and solutions.
