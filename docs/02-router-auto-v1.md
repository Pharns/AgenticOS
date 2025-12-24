# 02 - Router Auto (v1)

The `scripts/router` command provides a powerful `auto` subcommand for routing execution to the most appropriate agent profile or workflow. This functionality is also exposed via the simpler `aos auto` command.

---

## 1. Purpose

The `router auto` (or `aos auto`) selects a workflow or profile based on your prompt. It supports two modes:

- **Keyword matching** (default): Fast, deterministic routing based on predefined rules
- **AI classification** (`--smart`): Uses Gemini to intelligently pick the best profile

## 2. Quick Usage with aos

```bash
# Keyword-based (fast)
aos auto "What is photosynthesis?"      # → quick
aos auto "Fix the login error"          # → dev
aos auto "Write a password policy"      # → grc

# AI-powered (smarter)
aos auto --smart "Help me understand this codebase"

# Debug routing
aos auto --dry-run "your prompt"        # See what would run
aos auto --explain "your prompt"        # See rule evaluation
```

## 3. Precedence Order

When using `router auto`, the system evaluates potential targets based on a strict precedence:

**Precedence Order (Highest → Lowest):**

1. `--workflow <name>` - Explicitly specifies a workflow
2. `--profile <name>` - Explicitly specifies a profile
3. `--smart` - AI classification using Gemini
4. `--task <token>` - Matches against rule keywords
5. Free-text arguments - Fallback keyword matching

## 4. Keyword Rule Matching

The default mode uses strict, keyword-based matching for determinism and explainability.

### How It Works

- **Literal, Lowercase Token Matching:** All keywords are converted to lowercase. Matching is exact.
- **No NLP or Semantic Parsing:** The router does not understand "meaning" - it matches keywords.
- **Ordered Rules:** Rules are evaluated in order defined in the config file.
- **First Match Wins:** Once a rule matches, no further rules are evaluated.

### Rule Configuration

Rules are defined in:

```text
.agents/router_auto_rules.json
```

Each rule includes:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | Yes | Unique identifier for the rule |
| `description` | string | No | Human-readable description |
| `match_all` | array | Yes | Keywords that must ALL be present (can be empty) |
| `match_any` | array | No | Keywords where at least ONE must be present |
| `route.type` | string | Yes | Either `"workflow"` or `"profile"` |
| `route.target` | string | Yes | Name of the workflow or profile |

### Example Rules

```json
{
  "version": "1.0.0",
  "rules": [
    {
      "id": "bug_fix_workflow",
      "description": "Route bug fixes to the auto_fix_bug workflow",
      "match_all": ["bug"],
      "match_any": ["fix", "broken", "error", "issue", "crash"],
      "route": {"type": "workflow", "target": "auto_fix_bug"}
    },
    {
      "id": "grc_policy",
      "description": "Route security policy writing to grc",
      "match_all": [],
      "match_any": ["policy", "compliance", "audit", "nist", "gdpr"],
      "route": {"type": "profile", "target": "grc"}
    },
    {
      "id": "quick_questions",
      "description": "Route simple questions to quick profile",
      "match_all": [],
      "match_any": ["what", "how", "why", "explain", "define"],
      "route": {"type": "profile", "target": "quick"}
    }
  ]
}
```

## 5. AI Classification (--smart)

When keyword matching isn't sufficient, use `--smart` to let Gemini classify your prompt:

```bash
aos auto --smart "Help me design a caching layer for the API"
```

The AI examines:
- Available profiles and their descriptions
- Available workflows and their purposes
- Your prompt's intent

Returns the best match with reasoning:
```
MATCHED: profile 'dev'
  Reason: AI classification - This task involves code implementation and design.
```

## 6. Debugging & Dry Run

### --explain

Shows detailed rule evaluation:

```bash
aos auto --explain "Fix the login bug"
```

Output:
```
ROUTE SOURCE: free text (precedence 4)
  Query: 'Fix the login bug'
  Parsed tokens: ['fix', 'the', 'login', 'bug']

Evaluating 8 rules (first-match wins):

  Rule 1: bug_fix_workflow
    match_all: ['bug']
    match_any: ['fix', 'broken', 'error', 'issue', 'crash']
    Result: MATCH
    ...
```

### --dry-run

Shows what would run without executing:

```bash
aos auto --dry-run "Write a NIST compliance report"
```

Output:
```
MATCHED: profile 'grc'
  Reason: rule 'grc_policy' matched
    match_all: []
    match_any: ['policy', 'compliance', 'audit', 'nist', 'gdpr'] (any)
    tokens found: ['write', 'a', 'nist', 'compliance', 'report']

[DRY-RUN] Would execute: profile 'grc' with args []
```

### --lint

Validate your rules configuration:

```bash
./scripts/router auto --lint
```

Checks for:
- Valid JSON syntax
- Required fields present
- Unreachable or shadowed rules
- Order issues

## 7. Full Command Reference

### Via aos (recommended)

```bash
aos auto "prompt"                         # Keyword matching
aos auto --smart "prompt"                 # AI classification
aos auto --dry-run "prompt"               # Preview without running
aos auto --explain "prompt"               # Show rule evaluation
aos auto "prompt" -- --full-auto          # Pass options to target profile
aos -p myproject auto --smart "prompt"    # Auto-route on a specific project
```

### Via router directly

```bash
./scripts/router auto "prompt"
./scripts/router auto --smart "prompt"
./scripts/router auto --workflow myworkflow
./scripts/router auto --profile dev
./scripts/router auto --task fix --task bug
./scripts/router auto --strict --task deploy
./scripts/router auto --lint
```

### Options

| Option | Description |
|--------|-------------|
| `--smart` | Use AI (Gemini) to classify and route |
| `--workflow <name>` | Directly specify workflow (highest precedence) |
| `--profile <name>` | Directly specify profile |
| `--task <token>` | Explicit task keyword(s) for matching |
| `--strict` | Require --task flags, disable free-text fallback |
| `--explain` | Show token parsing and rule evaluation |
| `--dry-run` | Print chosen route without executing |
| `--lint` | Validate rules configuration |

## 8. Logging

Auto-routing decisions are logged to:

```text
.agents/logs/YYYY-MM-DDTHH-MM-SSZ-router-auto.json
```

Log entries include:
- Query and parsed tokens
- Matched rule ID
- Target type and name
- Duration in milliseconds
- Exit code

## 9. Best Practices

1. **Start with keyword rules** - They're fast and predictable
2. **Use --smart for ambiguous prompts** - When keywords don't capture intent
3. **Test with --dry-run** - Verify routing before execution
4. **Debug with --explain** - Understand why rules match or don't
5. **Keep rules ordered** - More specific rules should come first
6. **Use empty match_all for broad rules** - Matches if any match_any keyword present
