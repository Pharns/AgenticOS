# 10 - Troubleshooting Guide

Common issues and solutions for AgenticOS.

---

## Quick Diagnostics

Run the doctor first:

```bash
./scripts/doctor --strict
```

This validates all configurations, permissions, and provider availability.

---

## Provider Authentication Issues

### Codex: 401 Unauthorized

**Symptom:**
```
ERROR codex_api::endpoint::responses: error=http 401 Unauthorized
"Missing bearer or basic authentication in header"
```

**Cause:** AgenticOS uses a custom `CODEX_HOME` directory (`.agents/codex/`) which doesn't have authentication.

**Solution:**
```bash
# Symlink auth from default Codex location
ln -sf ~/.codex/auth.json .agents/codex/auth.json

# Or re-authenticate
codex login
```

**Verify:**
```bash
codex login status
echo "test" | codex exec --skip-git-repo-check -
```

---

### Claude: Authentication Failed

**Symptom:** Claude commands fail silently or return empty output.

**Solution:**
```bash
# Re-authenticate via browser
claude

# Check version confirms auth
claude --version
```

---

### Cursor-agent: Resource Exhausted

**Symptom:**
```
ConnectError: [resource_exhausted] Error
```

**Cause:** Rate limiting from Cursor's API.

**Solution:** Wait 15-30 minutes and retry. This is an external limitation.

**Verify:**
```bash
cursor-agent status
```

---

### Gemini: No Output

**Symptom:** Gemini returns startup logs but no response.

**Solution:**
```bash
# Ensure authenticated
gemini "Hello"

# If first time, follow OAuth flow in browser
```

---

## Script Permission Issues

### Permission Denied

**Symptom:**
```
permission denied: ./scripts/agent
```

**Solution:**
```bash
chmod +x scripts/agent scripts/router scripts/doctor scripts/agent-workflow scripts/memory
```

Or run the installer:
```bash
./install.sh
```

---

## Python/Venv Issues

### PyYAML Not Found

**Symptom:**
```
PyYAML is required. Run ./install.sh
```

**Solution:**
```bash
# Option 1: Run installer
./install.sh

# Option 2: Manual install
source .venv/bin/activate
pip install -r requirements.txt
```

### Wrong Python Version

**Symptom:** Syntax errors or import failures.

**Cause:** AgenticOS requires Python 3.9+.

**Solution:**
```bash
python3 --version  # Check version
rm -rf .venv && python3 -m venv .venv && ./install.sh
```

---

## Configuration Issues

### Profile Not Found

**Symptom:**
```
Profile 'xyz' not found in .agents/agents.yaml
```

**Solution:**
1. Check `.agents/agents.yaml` for typos
2. Run `./scripts/router list` to see available profiles
3. Add missing profile definition

### Prompt File Missing

**Symptom:**
```
Prompt file not found: .agents/prompts/xyz.md
```

**Solution:**
```bash
# Create the prompt file
touch .agents/prompts/xyz.md
# Add prompt content
```

---

## Workflow Issues

### Workflow Not Executing

**Note:** Workflows display steps but don't auto-execute.

**Correct usage:**
```bash
# View workflow steps
./scripts/agent-workflow ops_check

# Execute manually with context
WORKFLOW=ops_check WORKFLOW_STEP=diagnostics ./scripts/agent --profile ops
WORKFLOW=ops_check WORKFLOW_STEP=review ./scripts/agent --profile grc
```

### Workflow Context Not Injected

**Symptom:** Second step doesn't see previous step's output.

**Cause:** Missing environment variables.

**Solution:** Always set both `WORKFLOW` and `WORKFLOW_STEP`:
```bash
WORKFLOW=workflow_name WORKFLOW_STEP=step_name ./scripts/agent --profile X
```

---

## Memory Issues

### Memory Not Updating

**Symptom:** Profile memory shows stale data.

**Cause:** Memory file might be read-only or path incorrect.

**Solution:**
```bash
# Check permissions
ls -la .agents/memory/profiles/

# Verify memory_file path in agents.yaml matches
```

### Delta Not Computing

**Symptom:** Delta section always shows "(none)".

**Cause:** No previous session to compare against.

**Solution:** Run the profile twice to see delta between sessions.

---

## Logging Issues

### Logs Not Created

**Symptom:** `.agents/logs/` is empty after runs.

**Solution:**
```bash
# Check directory permissions
mkdir -p .agents/logs
chmod 755 .agents/logs

# Verify in doctor
./scripts/doctor --strict | grep writable
```

### Log Schema Validation Failed

**Symptom:** Doctor reports log schema errors.

**Solution:**
```bash
# Install jsonschema for validation
pip install jsonschema

# Re-run doctor
./scripts/doctor --strict
```

---

## Router Issues

### Auto-Routing Not Matching

**Symptom:** `router auto --task X` returns no match.

**Solution:**
1. Check rules in `.agents/router_auto_rules.json`
2. Use `--explain` to see matching logic:
   ```bash
   ./scripts/router auto --task X --explain
   ```
3. Add a new rule or adjust keywords

### Router Lint Warnings

**Symptom:** Doctor reports rule shadowing.

**Cause:** Earlier rules match before later ones due to keyword overlap.

**Solution:** Reorder rules in `router_auto_rules.json` or make patterns more specific.

---

## Platform-Specific Issues

### macOS: Command Not Found

**Symptom:** Provider CLI not found despite installation.

**Solution:**
```bash
# Check if installed globally
which codex claude gemini cursor-agent

# Add to PATH if needed
export PATH="$HOME/.local/bin:$PATH"
```

### Ubuntu: SSL Certificate Errors

**Symptom:** Provider APIs fail with certificate errors.

**Solution:**
```bash
sudo apt-get update
sudo apt-get install ca-certificates
```

---

## Getting Help

1. **Run diagnostics:** `./scripts/doctor --strict`
2. **Check logs:** `ls -t .agents/logs/*.json | head -1 | xargs cat`
3. **View last session:** `cat .agents/memory/last-session.md`
4. **Verify providers:** See [[08-provider-integration]]

---

## Reporting Issues

When reporting issues, include:

1. Output of `./scripts/doctor --strict`
2. Relevant log file from `.agents/logs/`
3. Your OS and Python version
4. Provider versions (`codex --version`, `claude --version`, etc.)
