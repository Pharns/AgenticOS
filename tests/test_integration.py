#!/usr/bin/env python3
"""
AgenticOS Integration Tests

Run with: python3 tests/test_integration.py
Or: ./tests/test_integration.py
"""

import json
import os
import subprocess
import sys
from pathlib import Path

# Ensure we're in the right directory
ROOT = Path(__file__).resolve().parent.parent
os.chdir(ROOT)

# Colors for output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"

def run(cmd: list[str], timeout: int = 30) -> tuple[int, str, str]:
    """Run a command and return (exit_code, stdout, stderr)."""
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=ROOT,
        )
        return proc.returncode, proc.stdout, proc.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "TIMEOUT"
    except Exception as e:
        return -2, "", str(e)

def test_doctor_strict():
    """Doctor --strict should pass with 0 failures."""
    code, out, err = run(["./scripts/doctor", "--strict"])

    # Check for "fail=0" in output
    if "fail=0" in out and code == 0:
        return True, "Doctor strict passed"
    else:
        return False, f"Doctor failed: exit={code}, output={out[-200:]}"

def test_router_list():
    """Router list should show profiles and workflows."""
    code, out, err = run(["./scripts/router", "list"])

    if code != 0:
        return False, f"Router list failed: exit={code}"

    # Check for expected content
    required = ["Profiles:", "Workflows:", "dev", "research", "grc"]
    missing = [r for r in required if r not in out]

    if missing:
        return False, f"Router list missing: {missing}"

    return True, f"Router list shows {out.count('-')} entries"

def test_router_auto_explain():
    """Router auto --explain should show matching logic."""
    code, out, err = run(["./scripts/router", "auto", "--task", "fix bug", "--explain"])

    if code != 0:
        return False, f"Router auto failed: exit={code}"

    if "matched" in out.lower() or "rule" in out.lower():
        return True, "Router auto explains matching"

    return False, f"Router auto missing explanation: {out[:200]}"

def test_agent_workflow_view():
    """Agent-workflow should display workflow steps."""
    code, out, err = run(["./scripts/agent-workflow", "ops_check"])

    if code != 0:
        return False, f"Agent-workflow failed: exit={code}"

    if "diagnostics" in out and "review" in out:
        return True, "Workflow steps displayed correctly"

    return False, f"Workflow output unexpected: {out[:200]}"

def test_configs_valid():
    """YAML configs should be valid."""
    import yaml

    configs = [
        ".agents/agents.yaml",
        ".agents/workflows.yaml",
    ]

    for cfg_path in configs:
        try:
            with open(ROOT / cfg_path) as f:
                yaml.safe_load(f)
        except Exception as e:
            return False, f"Invalid YAML in {cfg_path}: {e}"

    return True, f"All {len(configs)} config files valid"

def test_router_rules_valid():
    """Router auto rules should be valid JSON."""
    rules_path = ROOT / ".agents" / "router_auto_rules.json"

    try:
        with open(rules_path) as f:
            data = json.load(f)

        if "rules" not in data:
            return False, "Missing 'rules' key in router_auto_rules.json"

        return True, f"Router rules valid: {len(data['rules'])} rules"
    except Exception as e:
        return False, f"Invalid JSON: {e}"

def test_memory_dirs_exist():
    """Memory directories should exist."""
    required_dirs = [
        ".agents/memory",
        ".agents/memory/profiles",
        ".agents/memory/sessions",
        ".agents/memory/workflows",
        ".agents/logs",
    ]

    missing = [d for d in required_dirs if not (ROOT / d).is_dir()]

    if missing:
        return False, f"Missing dirs: {missing}"

    return True, f"All {len(required_dirs)} memory dirs exist"

def test_prompts_exist():
    """All profile prompts should exist."""
    import yaml

    with open(ROOT / ".agents" / "agents.yaml") as f:
        agents = yaml.safe_load(f)

    profiles = agents.get("profiles", {})
    missing = []

    for name, cfg in profiles.items():
        prompt_path = cfg.get("prompt", "")
        if prompt_path and not (ROOT / prompt_path).exists():
            missing.append(f"{name}: {prompt_path}")

    if missing:
        return False, f"Missing prompts: {missing}"

    return True, f"All {len(profiles)} profile prompts exist"

def main():
    """Run all tests and report results."""
    tests = [
        ("Doctor strict", test_doctor_strict),
        ("Router list", test_router_list),
        ("Router auto explain", test_router_auto_explain),
        ("Agent-workflow view", test_agent_workflow_view),
        ("Config validation", test_configs_valid),
        ("Router rules", test_router_rules_valid),
        ("Memory directories", test_memory_dirs_exist),
        ("Prompt files", test_prompts_exist),
    ]

    print("=" * 50)
    print("  AgenticOS Integration Tests")
    print("=" * 50)
    print()

    passed = 0
    failed = 0

    for name, test_fn in tests:
        try:
            success, message = test_fn()
            if success:
                print(f"{GREEN}✓ PASS{RESET}: {name}")
                print(f"         {message}")
                passed += 1
            else:
                print(f"{RED}✗ FAIL{RESET}: {name}")
                print(f"         {message}")
                failed += 1
        except Exception as e:
            print(f"{RED}✗ ERROR{RESET}: {name}")
            print(f"         {e}")
            failed += 1
        print()

    print("=" * 50)
    print(f"  Results: {GREEN}{passed} passed{RESET}, {RED if failed else ''}{failed} failed{RESET}")
    print("=" * 50)

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
