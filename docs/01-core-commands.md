# 01 - Core Commands Reference

AgenticOS is controlled through a set of core command-line interface (CLI) scripts designed for predictability, explainability, and auditability. These scripts form the backbone of AgenticOS's deterministic behavior.

---

## 1. `scripts/agent`

The `scripts/agent` command is the primary tool for executing individual agent profiles or workflows within a controlled environment.

### Key Properties

*   **No Hidden Prompt Mutation:** The agent runs on a static prompt as defined in its profile, ensuring no unexpected changes to its instructions.
*   **Structured Output Expectations:** Designed to process and normalize LLM output into structured sections (Plan, Code Changes, Verification, Next Actions).
*   **Optional Workflow Context:** Can receive and log workflow-specific context via environment variables.
*   **Logs and Deltas:** Emits comprehensive JSON logs for every session and contributes to memory deltas.
*   **Memory Preview:** Optionally displays a preview of the profile's memory file upon startup.

### Usage

```bash
./scripts/agent --profile <name> [options] [-- <extra_args_for_cli>]
```

### Arguments

*   `--profile <name>` (Required): Specifies the agent profile to run (e.g., `dev`, `grc`, `research`, `ops`).
*   `--timeout <seconds>`: Sets a timeout (in seconds) for the underlying agent CLI command. Defaults to `120` seconds. Can also be set via the `AGENT_TIMEOUT` environment variable.
*   `--no-memory`: Skips loading and surfacing project memory for this session.
*   `--no-normalize`: Disables provider output normalization, logging raw `stdout`/`stderr`.
*   `--print <mode>`: Controls which section of the agent's processed output is printed to `stdout`.
    *   `norm` (default): Prints the structured, normalized output.
    *   `raw`: Prints the raw `stdout` from the underlying CLI.
    *   `clean`: Prints just the answer, stripping section headers and placeholders.
    *   `plan`: Prints the "Plan" section.
    *   `code`: Prints the "Code Changes" section.
    *   `verification`: Prints the "Verification" section.
    *   `next-actions`: Prints the "Next Actions" section.
    *   `summary`: Prints a brief, 3-bullet summary.
    *   `delta`: Prints the computed delta for the session.
*   `--quiet`: Suppresses the memory banner at startup.
*   `--tag <tags>`: A comma-separated list of tags to attach to the session log and memory entries (e.g., `--tag bug-fix,urgent`).
*   `-- <extra_args_for_cli>`: Any arguments following `--` are passed directly to the underlying agent's CLI command (e.g., `codex exec`, `claude chat`).

### Environment Variables

*   `WORKFLOW`: Specifies the name of the workflow currently being executed (e.g., `auto_fix_bug`). Used for logging and memory context.
*   `WORKFLOW_STEP`: Specifies the current step within a workflow (e.g., `plan`, `implement`). Used for logging and memory context.
*   `AGENT_TIMEOUT`: Sets the default timeout for agent CLI commands. Overridden by `--timeout` flag.

### Example

```bash
# Run the 'dev' agent with a specific task
./scripts/agent --profile dev -- "Review the new authentication module for vulnerabilities"

# Run the 'ops' agent within a workflow context and log tags
WORKFLOW=ops_check WORKFLOW_STEP=diagnostics ./scripts/agent --profile ops --tag security,critical
```

---

## 2. `scripts/router`

The `scripts/router` command is a unified router for AgenticOS, capable of explicitly dispatching to profiles or workflows, or deterministically auto-routing based on intent.

### Key Properties

*   **Explicit Routing:** Directly invokes a specified profile or workflow.
*   **Deterministic Auto-Routing:** Selects a target (profile or workflow) based on predefined rules, ensuring predictable behavior.
*   **Explain and Dry-Run Modes:** Provides mechanisms to understand routing decisions without actual execution.
*   **Logging:** Records its own routing actions in JSON logs.

### Usage

```bash
./scripts/router <command> [options]
```

### Commands

*   `list`: Displays all available agent profiles and workflows defined in `agents.yaml` and `workflows.yaml`.

    ```bash
    # Example
    ./scripts/router list
    ```

*   `run <target> [-- <extra_args>]`: Directly executes the specified `<target>`, which can be either a profile name (e.g., `dev`) or a workflow name (e.g., `auto_fix_bug`). All arguments after `--` are passed to the underlying `scripts/agent` or `scripts/agent-workflow` command.

    ```bash
    # Example: Run the 'research' profile
    ./scripts/router run research

    # Example: Run the 'auto_fix_bug' workflow
    ./scripts/router run auto_fix_bug
    ```

*   `auto [query] [-- <extra_args>]`: Automatically routes to a profile or workflow based on a task. Supports keyword matching (default) or AI classification.

    *   `--smart`: Uses AI (Gemini) to intelligently classify the query and select the best profile.
    *   `--task <keywords>`: Explicit keywords for rule matching. Multiple `--task` arguments can be provided.
    *   `--explain`: Shows the tokens parsed from the input and the evaluation of matching rules.
    *   `--dry-run`: Prints the selected route without executing. Can be combined with `--explain`.
    *   `--strict`: Enforces strict matching rules. (See `03-strict-mode.md` for details).
    *   `--lint`: Validates the router rules configuration.

    ```bash
    # Example: Auto-route with free text (keyword matching)
    ./scripts/router auto "Fix the login bug"

    # Example: Auto-route with AI classification
    ./scripts/router auto --smart "Help me design an API"

    # Example: Explain auto-routing
    ./scripts/router auto --explain "Write a security policy"

    # Example: Dry run
    ./scripts/router auto --dry-run "Debug the memory leak"
    ```

---

## 3. `scripts/doctor`

The `scripts/doctor` command performs comprehensive offline health checks and validations of the AgenticOS setup. It ensures that the environment, configuration, and scripts are correctly configured for reliable operation.

### Key Properties

*   **System Health Validation:** Checks for file existence, permissions, YAML syntax, CLI tool availability, and log schema conformance.
*   **Configuration Checks:** Validates `agents.yaml`, `workflows.yaml`, and `router_auto_rules.json`.
*   **Writability Checks:** Ensures log and memory directories are writable.
*   **Executable Checks:** Verifies that core scripts (`agent`, `router`, etc.) are executable.

### Usage

```bash
./scripts/doctor [options]
```

### Arguments

*   `--strict`: Treats all warnings as failures. If any check results in a "warn" status, the script will exit with a non-zero code (typically `2`).
*   `--json`: Outputs the diagnostic results in JSON format, suitable for machine processing.
*   `--profile <name>`: Restricts profile-specific checks to only the specified profile.
*   `--fix`: Attempts best-effort automated fixes for common issues, such as creating missing directories or setting execute permissions on scripts.

### Exit Codes

*   `0`: All checks passed (or no failures/warnings in non-strict mode).
*   `1`: Warnings present (in non-strict mode) or a non-critical issue detected.
*   `2`: Failures present, or warnings in strict mode.
*   `3`: Specified profile not found.

### Example

```bash
# Run a basic health check
./scripts/doctor

# Run a strict health check, treating warnings as failures
./scripts/doctor --strict

# Run a health check and attempt to fix issues
./scripts/doctor --fix
```

---

## 4. `scripts/aos` (Unified CLI)

The `aos` command is the unified CLI wrapper that provides simplified access to all AgenticOS functionality. It's the recommended way to interact with AgenticOS.

### Key Properties

*   **Profile Shortcuts:** Direct profile invocation with aliases (e.g., `aos q` for quick, `aos d` for dev).
*   **Auto-Routing:** Intelligent profile selection via `aos auto`.
*   **Project Management:** Register and switch between multiple AgenticOS projects.
*   **Clean Output Mode:** The `quick` profile defaults to clean, answer-only output.

### Installation

```bash
# Via install.sh (recommended)
./install.sh

# Or manual symlink
sudo ln -sf "$(pwd)/scripts/aos" /usr/local/bin/aos
```

### Usage

```bash
aos                              # List profiles & workflows
aos <profile> "prompt"           # Run a profile
aos auto "prompt"                # Auto-pick best profile
aos auto --smart "prompt"        # AI-powered routing
aos -p <project> <profile> "prompt"  # Run on specific project
```

### Profile Aliases

| Alias | Profile | Special Behavior |
|-------|---------|------------------|
| `d` | dev | Standard output |
| `q` | quick | Clean output, no memory (use `-v` for verbose) |
| `g` | grc | Standard output |
| `r` | research | Standard output |
| `o` | ops | Standard output |

### Commands

*   `doctor [--fix]`: Run health checks
*   `list [--json]`: List profiles and workflows
*   `auto "prompt"`: Auto-route to best profile
*   `wf <name> "prompt"`: Execute a workflow
*   `continue`: Continue last session
*   `logs [--tail|--rotate N]`: View or manage logs
*   `memory [profile|--clear p]`: View or clear memory
*   `projects`: Manage registered projects
*   `init`: Initialize .agents/ in current directory

### Examples

```bash
# Quick question (clean output)
aos q "What is 2+2?"

# Quick question with verbose output
aos q "Explain recursion" -v

# Auto-route a task
aos auto "Fix the authentication bug"

# Work on a specific project
aos -p myproject d "Add user validation"

# List registered projects
aos projects
aos projects -v  # With details
```

See `docs/aos-quickstart.md` for comprehensive usage guide.
