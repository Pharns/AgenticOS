# 06 - Doctor & Validation

The `scripts/doctor` command is AgenticOS's built-in health and validation tool. It performs a comprehensive suite of checks to ensure that your AgenticOS environment is correctly configured, all necessary files are in place, and critical components are functioning as expected. This guarantees a stable and predictable execution environment for your agents and workflows.

---

## 1. `doctor --strict` Enforcements

When `scripts/doctor` is run with the `--strict` flag, it elevates the importance of all warnings to failures, ensuring that any deviation from the ideal state is flagged as critical. It enforces a rigorous set of checks across the AgenticOS ecosystem:

*   **Configuration Files Validity:**
    *   **`agents.yaml`:** Checks for existence, readability, and correct YAML syntax.
    *   **`workflows.yaml`:** Checks for existence, readability, and correct YAML syntax.
    *   **`router_auto_rules.json`:** Validates existence, correct JSON syntax, and internal schema (e.g., presence of `version` and `rules` array, unique rule IDs, non-empty `match_all` arrays, valid `route.type` and `route.target`).
*   **Profile Configuration:** For each defined agent profile:
    *   **Prompt Path:** Verifies the existence and readability of the associated prompt file (`.agents/prompts/<profile>.md`).
    *   **Command Template:** Ensures the command template in `agents.yaml` is valid and renders correctly.
    *   **CLI Availability:** Checks if the primary CLI tool (e.g., `codex`, `claude`) specified in the command template is found on the system's PATH.
    *   **Memory File Path:** Validates that the `memory_file` path (if defined) is located under the `.agents/memory` root and that its parent directory is writable.
*   **Directory Writable Checks:**
    *   **Log Directory:** Ensures `.agents/logs` is created and writable.
    *   **Memory Root:** Ensures `.agents/memory` is created and writable.
    *   **Memory Subdirectories:** Verifies writability of `.agents/memory/profiles`, `.agents/memory/sessions`, and `.agents/memory/workflows`.
    *   **Summary File:** Checks if `.agents/memory/summary.md` is writable.
*   **Script Executability:** Confirms that all core AgenticOS scripts are present and executable:
    *   `scripts/agent`
    *   `scripts/agent-workflow`
    *   `scripts/router`
    *   `scripts/memory` (future-looking, present in `doctor` checks)
    *   `scripts/doctor` (self-check)
*   **Log Schema Conformance:**
    *   **Schema File:** Checks for the optional existence of `.agents/schemas/log_v1.json`.
    *   **`jsonschema` Library:** Warns if the `jsonschema` Python library is not installed (optional dependency for full validation).
    *   **Schema Validation:** If `log_v1.json` and `jsonschema` are present, it validates the latest log file against the defined schema.
    *   **Basic Field Checks:** Verifies the presence of `required` log fields (`stdout_norm`, `stderr_norm`, `provider_meta`, `normalization_notes`) and `optional` fields (`sections`, `next_actions`, `delta`, `delta_sources`, `tags`, `run_id`).
*   **Workflow Delta Logging Status:** Checks the latest log entry to ensure that workflow context fields (`workflow_name`, `workflow_step`, `workflow_context_injected`) are properly recorded when a workflow is run, indicating active workflow delta logging.

## 2. Warn-Only Conditions (Phase 2 - Future-Looking)

*(As of v1.x, this feature primarily involves strict checks. The following is a future-looking design note from the `USER_GUIDE.md`.)*

In future phases, `scripts/doctor` may introduce "warn-only" conditions that do not fail execution by default, but provide helpful notifications. An example is:

*   **Warns if workflows run without deltas:** This would flag situations where a workflow execution completes but no explicit delta information is captured, potentially indicating an oversight in the agent's output.

## 3. Exit Codes

`scripts/doctor` communicates its findings through standardized exit codes:

*   `0`: All checks passed (no warnings or failures).
*   `1`: Warnings were present (only in non-strict mode).
*   `2`: Failures were present, or warnings were present in `--strict` mode.
*   `3`: A specified profile (`--profile <name>`) was not found in `agents.yaml`.

These exit codes are critical for integrating `scripts/doctor` into CI/CD pipelines and automated health monitoring systems.
