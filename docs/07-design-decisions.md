# 07 - Design Decisions

The core design philosophy of AgenticOS prioritizes specific attributes to ensure a robust, predictable, and auditable agent operating layer. These intentional choices differentiate AgenticOS from more experimental or autonomous AI systems.

---

## 1. Core Design Philosophy

AgenticOS chooses the following principles as its foundational design decisions:

*   **Explicit contracts over intelligence:** Rather than attempting to infer intent or leverage black-box AI intelligence for core operations, AgenticOS relies on clearly defined contracts, rules, and configurations. This ensures transparency and removes ambiguity from agent behavior.
*   **Ordered rules over scoring:** For decision-making processes, particularly in routing, AgenticOS utilizes a strict, ordered set of rules. This eliminates the uncertainty of probabilistic scoring models, guaranteeing deterministic outcomes.
*   **Determinism over convenience:** While some AI systems might prioritize user convenience through adaptive or "smart" features, AgenticOS opts for determinism. Given the same inputs, the system will always produce the same outputs, which is critical for auditability and reliability in sensitive environments.
*   **Boring correctness over novelty:** AgenticOS's development eschews bleeding-edge, unproven AI techniques in favor of established, auditable, and easily verifiable methods. The focus is on stable and correct operation rather than experimental novelty.

---

## 2. Architectural Decisions

### 2.1 Router-First Architecture

**Decision:** The router (`scripts/router`) is the primary entry point, not the agent.

**Rationale:**
- Separates *deciding what to run* from *running it*
- Enables policy enforcement before execution
- Provides a single point for logging and auditing
- Supports both explicit (`run`) and automatic (`auto`) routing

**Alternative considered:** Direct agent invocation. Rejected because it bypasses routing logic and makes auditing harder.

### 2.2 No Auto-Execution of Workflows

**Decision:** Workflows display steps but don't automatically execute them.

**Rationale:**
- Human-in-the-loop for multi-step operations
- Each step can be reviewed before proceeding
- Avoids runaway automation
- Workflow context is injected via environment variables

**Alternative considered:** Automatic sequential execution. Rejected due to safety concerns in production environments.

### 2.3 First-Match-Wins Routing

**Decision:** Auto-routing uses first-match-wins, not best-match scoring.

**Rationale:**
- Deterministic: same input always yields same match
- Debuggable: `--explain` shows exactly which rule matched
- Predictable: rule order defines priority explicitly
- No hidden weights or ML models

**Alternative considered:** Semantic similarity scoring. Rejected because it introduces non-determinism.

---

## 3. Security Decisions

### 3.1 No Shell=True

**Decision:** All subprocess calls avoid `shell=True`.

**Rationale:**
- Prevents shell injection attacks
- Commands are parsed with `shlex.split()`
- Arguments passed as lists, not strings
- Prompt content is fed via stdin, not command line

### 3.2 Provider Isolation

**Decision:** Each provider (codex, claude, gemini, cursor-agent) has dedicated handling.

**Rationale:**
- Different CLIs have different argument patterns
- System prompts are injected provider-specifically
- Authentication is handled per-provider
- Failures in one provider don't affect others

### 3.3 Logs Are Gitignored

**Decision:** `.agents/logs/` is excluded from version control.

**Rationale:**
- Logs may contain sensitive prompt/response data
- Prevents accidental credential exposure
- Each deployment maintains its own audit trail

---

## 4. Memory System Decisions

### 4.1 Markdown Memory Files

**Decision:** Memory is stored as Markdown, not JSON or database.

**Rationale:**
- Human-readable without tooling
- Easy to edit manually if needed
- Works with Obsidian and other note systems
- Git-friendly for tracking changes

### 4.2 Delta Computation

**Decision:** Each session computes delta from previous session.

**Rationale:**
- Shows what changed between runs
- Enables progress tracking
- Supports "what's new since last time" queries
- Stored in workflow memory for multi-step context

---

## 5. Configuration Decisions

### 5.1 YAML Over JSON

**Decision:** Profiles and workflows use YAML.

**Rationale:**
- More readable than JSON
- Supports comments for documentation
- Widely used in DevOps tooling
- Python's PyYAML is stable and well-tested

### 5.2 JSON for Rules

**Decision:** Router auto-rules use JSON.

**Rationale:**
- Stricter parsing (no ambiguity)
- Schema validation with jsonschema
- Machine-generated rules are easier in JSON
- Rules are more structured than prose

---

## 6. Portability Decisions

### 6.1 Cross-Platform Scripts

**Decision:** All scripts use `#!/usr/bin/env python3`.

**Rationale:**
- Works on macOS and Linux
- Respects virtualenv activation
- No hardcoded paths

### 6.2 Venv Auto-Activation

**Decision:** Scripts auto-exec into venv if not activated.

**Rationale:**
- Users don't need to remember `source .venv/bin/activate`
- Ensures correct Python and dependencies
- Seamless experience across platforms

---

## 7. What We Explicitly Don't Do

- **No AI-based routing:** Routing is rule-based, not LLM-based
- **No auto-approval:** All executions require explicit invocation
- **No persistent agents:** Each run is stateless (memory is optional context)
- **No internet access by default:** Providers handle their own network access
- **No credential storage:** Auth is delegated to provider CLIs

---

## 8. Influenced By

AgenticOS design draws from:

- **Riley Goodside:** Constraint and precision in prompts
- **Sander Schulhoff:** Agentic clarity and structured reasoning
- **Daniel Miessler:** Threat modeling and security-first design
- **Dr. Jules White:** Grounding and repeatable patterns
- **Ethan Mollick:** Pragmatic usefulness over theoretical elegance

---

This design philosophy ensures AgenticOS remains a predictable, explainable, and safe platform for AI-assisted workflows.
