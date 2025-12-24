#!/usr/bin/env bash
#
# AgenticOS Installer — macOS + Ubuntu
# Creates Python venv, installs PyYAML, sets executable permissions,
# and verifies environment readiness.
#

set -e

echo "────────────────────────────────────────────"
echo "  AgenticOS Installer (Ubuntu + macOS)"
echo "────────────────────────────────────────────"
echo ""

# Detect OS for messaging
OS="$(uname -s)"
echo "Detected OS: $OS"
echo ""

# Ensure we are inside AgenticOS directory
if [ ! -d ".agents" ] || [ ! -d "scripts" ]; then
    echo "ERROR: install.sh must be run from inside the AgenticOS root directory."
    exit 1
fi

# Create Python venv if missing
if [ ! -d ".venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv .venv
else
    echo "Virtual environment already exists. Skipping creation."
fi

# Activate venv
echo "Activating virtual environment..."
# shellcheck disable=SC1091
source .venv/bin/activate

# Upgrade pip safely
echo "Upgrading pip..."
python3 -m pip install --upgrade pip

# Install dependencies from requirements.txt
echo "Installing dependencies from requirements.txt..."
if [ -f "requirements.txt" ]; then
    python3 -m pip install -r requirements.txt
else
    echo "requirements.txt not found, installing defaults..."
    python3 -m pip install pyyaml jsonschema
fi

# Make scripts executable
missing_scripts=0
for script_path in scripts/agent scripts/agent-workflow scripts/router scripts/doctor scripts/memory scripts/aos; do
    if [ -f "$script_path" ]; then
        chmod +x "$script_path"
    else
        echo "WARNING: $script_path not found; skipping chmod (create it before running)."
        missing_scripts=1
    fi
done

echo ""
if [ "$missing_scripts" -eq 0 ]; then
    echo "✔ Scripts are executable."
else
    echo "⚠ Some scripts were missing; ensure they exist and are executable."
fi
echo "✔ Dependencies installed."
echo "✔ Virtual environment ready."
echo ""

# Check for provider CLIs
echo "Checking provider CLIs..."
providers_found=0
providers_missing=0

for cli in codex claude gemini cursor-agent; do
    if command -v "$cli" &> /dev/null; then
        version=$("$cli" --version 2>&1 | head -1 || echo "unknown")
        echo "  ✔ $cli: $version"
        providers_found=$((providers_found + 1))
    else
        echo "  ⚠ $cli: not found (optional)"
        providers_missing=$((providers_missing + 1))
    fi
done

echo ""
if [ "$providers_found" -gt 0 ]; then
    echo "✔ Found $providers_found provider CLI(s)."
fi
if [ "$providers_missing" -gt 0 ]; then
    echo "⚠ $providers_missing provider CLI(s) not found."
    echo "  See docs/08-provider-integration.md for installation instructions."
fi
echo ""

# Symlink Codex auth if available
if [ -f "$HOME/.codex/auth.json" ] && [ ! -f ".agents/codex/auth.json" ]; then
    echo "Linking Codex authentication..."
    mkdir -p .agents/codex
    ln -sf "$HOME/.codex/auth.json" .agents/codex/auth.json
    echo "✔ Codex auth linked."
fi

# Install global 'aos' command symlink
AOS_SCRIPT="$(pwd)/scripts/aos"
AOS_LINK="/usr/local/bin/aos"

echo ""
echo "────────────────────────────────────────────"
echo "  Global 'aos' Command Installation"
echo "────────────────────────────────────────────"
echo ""

if [ -L "$AOS_LINK" ]; then
    current_target=$(readlink "$AOS_LINK" 2>/dev/null || echo "unknown")
    if [ "$current_target" = "$AOS_SCRIPT" ]; then
        echo "✔ 'aos' symlink already exists and points to this installation."
    else
        echo "⚠ 'aos' symlink exists but points to: $current_target"
        echo "  To update it, run: sudo ln -sf \"$AOS_SCRIPT\" \"$AOS_LINK\""
    fi
elif [ -f "$AOS_LINK" ]; then
    echo "⚠ '$AOS_LINK' exists but is not a symlink."
    echo "  Remove it first if you want to install the 'aos' command."
else
    echo "Would you like to install 'aos' globally? (requires sudo)"
    echo "This creates a symlink: $AOS_LINK -> $AOS_SCRIPT"
    echo ""
    read -p "Install global 'aos' command? [y/N] " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        if sudo ln -sf "$AOS_SCRIPT" "$AOS_LINK"; then
            echo "✔ 'aos' command installed globally."
            echo "  You can now run 'aos' from anywhere."
        else
            echo "✗ Failed to create symlink. You can do it manually:"
            echo "  sudo ln -sf \"$AOS_SCRIPT\" \"$AOS_LINK\""
        fi
    else
        echo "Skipped. To install later, run:"
        echo "  sudo ln -sf \"$AOS_SCRIPT\" \"$AOS_LINK\""
    fi
fi

# Final summary
echo ""
echo "────────────────────────────────────────────"
echo "  AgenticOS Installation Complete"
echo "────────────────────────────────────────────"
echo ""
echo "Next steps:"
echo "  1. Run: aos doctor"
echo "  2. Run: aos list"
echo "  3. Try: aos q 'Hello, quick test!'"
echo ""
echo "Quick reference:"
echo "  aos              # List profiles & workflows"
echo "  aos d 'prompt'   # Run dev profile"
echo "  aos q 'prompt'   # Run quick profile"
echo "  aos help         # Show all commands"
echo ""
echo "For provider setup, see: docs/08-provider-integration.md"
echo ""
echo "You're ready to begin."
