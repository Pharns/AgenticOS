# 03 - Strict Mode and CI/Automation

AgenticOS emphasizes determinism and auditability, particularly important in automated environments like Continuous Integration (CI) pipelines or regulated systems. "Strict Mode" is a core mechanism to enforce these guarantees, treating any deviation from ideal state as a critical failure.

---

## 1. `scripts/doctor --strict`

The `scripts/doctor` command provides a comprehensive health check for your AgenticOS setup. When invoked with the `--strict` flag, it elevates the severity of all warnings, ensuring that any potential misconfiguration or non-ideal state is treated as a critical failure.

### Behavior

*   **Warning Escalation:** Any check that would normally result in a "warn" status will instead cause `scripts/doctor` to exit with a non-zero code.
*   **Hard Guarantees:** `--strict` enforces a stricter set of invariants, ensuring that the system adheres to a higher standard of operational readiness.

### Exit Codes (when running `scripts/doctor --strict`)

*   `0`: All checks passed with "ok" status. There are no warnings or failures.
*   `1`: Warnings were present and `--strict` mode was enabled (treating warnings as failures).
*   `2`: Failures were present (e.g., missing critical files, parsing errors).
*   `3`: A specified profile (`--profile <name>`) was not found in `agents.yaml`.

### Example

```bash
# Run a strict health check
# This command will exit with '1' if any warnings are present,
# or '2' if any failures are present.
./scripts/doctor --strict; echo "Exit Code: $?"
```

---

## 2. `scripts/router auto --strict`

The `scripts/router auto` command's `--strict` mode ensures that auto-routing decisions are unambiguous and conform to explicit rules. It is particularly useful for preventing unintended free-text matches in automated scenarios.

### Behavior

*   **Requires `--task`:** When `--strict` is used, `router auto` mandates that at least one `--task <token>` argument is provided. Free-text arguments are disabled.
*   **Disables Free-Text Fallback:** The router will not attempt to find a match if only free-text arguments are provided without explicit `--task` keywords.
*   **Exact Keyword Matching:** Matches must be made against the keywords defined in `agents.yaml` or `workflows.yaml` through the rules in `.agents/router_auto_rules.json`.

### Exit Codes (when running `scripts/router auto --strict`)

*   `0`: A matching rule was found and routing was successful.
*   `1`: No rule matched the provided `--task` keywords.
*   `2`: Invalid invocation (e.g., `--strict` was used but no `--task` argument was supplied).

### Example

```bash
# Attempt to route a task strictly
# This command requires a matching keyword to be present in router_auto_rules.json
./scripts/router auto --strict --task bug

# Example of an invalid invocation (missing --task)
./scripts/router auto --strict "fix a bug" # This will error
```

---

## 3. Operational Modes for CI / Automation

For environments requiring maximum predictability and auditability, such as Continuous Integration (CI) pipelines or automated operational scripts, AgenticOS recommends specific practices:

*   **Use `--strict`:** Always invoke `scripts/doctor` and `scripts/router auto` with the `--strict` flag. This ensures that any warnings or non-explicit behaviors are immediately flagged as failures.
*   **Use Explicit Routing:** Prefer explicit commands like `scripts/router run --profile <name>` or `scripts/router run --workflow <name>`. When using auto-routing, always provide explicit `--task` arguments.
*   **Treat Non-Zero Exits as Failures:** Configure your CI/automation system to consider any non-zero exit code from AgenticOS scripts as a job failure. This aligns with the deterministic design philosophy of AgenticOS.
*   **Audit Logs:** Regularly review the JSON logs generated in `.agents/logs/` for every execution to maintain an auditable trail of all agent activities.
