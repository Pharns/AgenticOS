# 04 - Workflow Memory & Delta

AgenticOS implements a robust system for capturing and tracking changes across agent sessions, particularly within the context of workflows. This "memory" system allows for continuous context, auditability, and clear understanding of progress and decisions.

---

## 1. Purpose

The primary purpose of Workflow Memory and Delta is to capture **what changed and why** for every agent or workflow run. This creates a persistent, human-readable record of actions, outputs, and the evolution of a task over time.

## 2. Delta Sources

AgenticOS collects delta information from two primary sources:

1.  **Agent-Authored Delta:** This is the most common source, where the agent's output explicitly includes a `Delta:` section. The `scripts/agent` command's output normalization process extracts this section directly from the agent's response. This allows agents to explicitly state what they have changed or observed.
2.  **Optional Git Delta:** When explicitly requested via a flag (future-looking, not yet fully implemented in core commands but supported by logging), AgenticOS can incorporate a delta derived from the Git repository's status.

### Agent-Authored Delta

Agents are encouraged to include a `Delta:` section in their output to describe changes. This information is processed by `scripts/agent` and stored in the session logs and memory.

### Git Delta (Future-Looking)

*(As of v1.x, this is a future-looking feature. The underlying `get_artifacts_touched` in `scripts/agent` has the capability to interact with Git, but a `--delta-from-git` flag is not yet exposed in core agent commands.)*

When fully implemented and activated (e.g., via a `--delta-from-git` flag on `scripts/agent`), and if the current directory is within a Git repository:

*   **Captures File Names Only:** It records the names of files that have been modified, added, or deleted.
    *   Unstaged changes: `git diff --name-only`
    *   Staged changes: `git diff --name-only --staged`
*   **No File Contents:** Only the paths of touched files are recorded; file content is not stored directly in the delta for security and brevity.
*   **Silently Skipped if Unavailable:** If Git is not installed, or the current directory is not a Git repository, this feature will be silently skipped without causing errors.

## 3. Workflow Memory Location

AgenticOS stores memory files in a structured manner under the `.agents/memory/` directory.

### Profile-Specific Memory

Each agent profile can have its own dedicated memory file, specified by the `memory_file` key in `agents.yaml`. These files typically reside in `.agents/memory/profiles/`.

```text
.agents/memory/profiles/<profile_name>.md
```

### Workflow-Specific Memory

Workflows maintain their state and history in dedicated files, typically named after the workflow:

```text
.agents/memory/workflows/<workflow_name>.md
```

Each run of a workflow through `scripts/agent` (when `WORKFLOW` and `WORKFLOW_STEP` environment variables are set) or interaction with `scripts/agent-workflow` can append a new entry to the respective workflow memory file. These entries contain:

*   Timestamp (UTC)
*   Tags
*   Summary of the run
*   Artifacts touched
*   Next actions suggested
*   Computed delta (comparing with the previous entry)

### Last Session Summary

A global `last-session.md` file is also maintained, capturing the summary of the most recent agent or workflow execution regardless of profile.

```text
.agents/memory/last-session.md
```

## 4. Delta Computation

The `scripts/agent` and `scripts/agent-workflow` scripts both implement `compute_delta` functions. These functions compare the current state (e.g., summary, next actions, artifacts) with the last recorded state in the respective memory file to identify and summarize changes.

Typical delta lines might include:

*   `- First recorded session for this profile.`
*   `- Summary updated.`
*   `- Next actions refreshed.`
*   `- Artifacts updated.`
*   `- No major changes detected.`
