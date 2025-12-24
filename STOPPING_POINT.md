# Stopping Point — 2025-12-23

## 1) Current status
- **Claude provider fully operational** — research and grc profiles work end-to-end
- **Gemini provider fully operational** — quick profile works end-to-end
- **Codex provider fully operational** — dev and ops profiles work end-to-end
- **Cursor-agent provider integrated** — refactor profile configured (currently rate-limited)
- **Phase 1: Project Detection COMPLETE** — `--project` flag working in router

## 2) What is fully complete and verified
- Agent runner hardened: no `shell=True`, stdin-fed prompts, wrapper flags isolated from provider, SIGPIPE handled, run_id logged.
- **Claude Code CLI integration**: Added `_is_claude()` helper and stdin passthrough in `build_command_argv()` for proper `--system-prompt` injection.
- **Gemini CLI integration**: Added `_is_gemini()` helper; system prompt prepended to user query as positional argument.
- **Cursor-agent CLI integration**: Added `_is_cursor_agent()` helper; system prompt prepended to user query as positional argument with `-p --output-format text`.
- **Updated agents.yaml**: Claude profiles use `claude -p -`, Gemini uses `gemini`, Cursor-agent uses `cursor-agent`.
- Normalization/summary tightened to structured sections only; summary prints exactly three bullets.
- Codex paths defaulted to `.agents/codex` and `.agents/codex_sessions` with writability preflight; env recorded in logs.
- Doctor strict passes end-to-end (40 OK, 0 WARN, 0 FAIL).
- Documentation updated with links to the 2025-12-12 technical update (README/USER_GUIDE).

### Phase 1: Project Detection (NEW)
- Added `--project` / `-p` global flag to `scripts/router`
- Implemented `detect_project()` function to find `.agents/` folders in any directory
- Implemented `get_project_config_paths()` to map project config file locations
- Implemented `validate_project()` to check project structure and warn on missing files
- Updated `load_configs()` to load project-specific or default configs
- Updated `list_targets()` to show project context when `--project` is used
- Updated `dispatch_run()` to pass project info via environment variables:
  - `AGENTICOS_PROJECT_ROOT` — path to project root
  - `AGENTICOS_PROJECT_AGENTS` — path to project's `.agents/` directory
- Fixed `dispatch_run()` to pass `--profile` flag correctly to agent script

## 3) What is known-broken and why
- **Cursor-agent executions** currently return `resource_exhausted` error (rate limiting). This is external; integration is complete.
- **Agent script not project-aware** — The agent script (`scripts/agent`) does not yet read `AGENTICOS_PROJECT_ROOT` and `AGENTICOS_PROJECT_AGENTS` environment variables. This is Phase 2 work.

## 4) Exact commands to resume
```bash
# Test Claude profiles (working)
./scripts/agent --profile research --print norm <<< "Your query here"
./scripts/agent --profile grc --print summary <<< "Your query here"

# Test Gemini profile (working)
./scripts/agent --profile quick --print norm <<< "Your query here"

# Test Codex profiles (working)
./scripts/agent --profile dev --print norm <<< "Your query here"
./scripts/agent --profile ops --print norm <<< "Your query here"

# Test Cursor-agent profile (rate-limited, retry later)
./scripts/agent --profile refactor --print norm <<< "Your query here"

# Test project detection (Phase 1)
./scripts/router --project /path/to/project list
./scripts/router -p /path/to/project list

# Run validation
./scripts/doctor --strict
./scripts/router list
```

## 5) Clear next objectives

### Phase 2: Master Prompt Override
- Update `scripts/agent` to read `AGENTICOS_PROJECT_AGENTS` environment variable
- Load project-specific `agents.yaml` when project context is present
- Load project-specific prompt files from project's `.agents/prompts/`
- Update memory paths to use project's `.agents/memory/`

### Phase 3: Context Ingestion (Safe)
- Add ability to read project context files (`README.md`, `ARCHITECTURE.md`, etc.)
- Implement file size limits and security controls
- Add `--context-file` flag to specify additional context

### Phase 4: Project Workflows
- Load project-specific `workflows.yaml`
- Update `agent-workflow` script to be project-aware

### Phase 5: Structured Outputs
- Create `outputs/` directory in project
- Write AI outputs to organized folder structure

### Other Tasks
- **Cursor-agent rate limit**: Wait for rate limit to reset and verify refactor profile.
- **Portfolio documentation**: Prepare project writeup for online portfolio.

## 6) Session log — 2025-12-23

### Phase 1 Implementation
- Added `--project` / `-p` flag to router argparser
- Created `detect_project()` function — checks for `.agents/` in given path
- Created `get_project_config_paths()` — maps config file paths
- Created `validate_project()` — warns on missing optional files
- Updated `load_configs()` — supports project-specific config loading
- Updated `list_targets()` — shows project path and config when `--project` used
- Updated `dispatch_run()` — sets `AGENTICOS_PROJECT_ROOT` and `AGENTICOS_PROJECT_AGENTS` env vars
- Fixed `dispatch_run()` — now passes `--profile` flag correctly to agent script
- Tested with sample project directory — all scenarios pass

### Files Modified
- `scripts/router` — Added Phase 1 project detection (~100 lines)
- `STOPPING_POINT.md` — Updated with Phase 1 status

### Test Results
- Doctor strict: 40 OK, 0 WARN, 0 FAIL
- Router list: Works with and without `--project`
- Router run: Validates profiles against project config
- Environment variables: Correctly passed to subprocess
