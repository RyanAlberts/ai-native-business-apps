#!/usr/bin/env bash
# Keel dev-environment setup.
#
# Run automatically by the SessionStart hook (see .claude/settings.json) so a
# fresh Claude Code session can (a) run the test suite and linters and (b)
# actually execute the agents, which need `claude-agent-sdk`.
#
# Why a venv: the agents depend on `claude-agent-sdk`, and installing it into
# some base images fails because `pip` tries to upgrade a distro-managed
# package (e.g. Debian's PyJWT) and can't uninstall it. A clean virtualenv
# sidesteps that entirely.
set -euo pipefail
cd "$(dirname "$0")/.."

# Founder-mode guard: fresh clones run the Founding Journey agent-natively
# (see playbooks/) with zero Python setup — the SessionStart hook must not
# make them sit through a pip install. Provision the venv only for
# contributors who opted in: `.venv` already exists, or KEEL_DEV=1 is set.
if [ ! -d .venv ] && [ "${KEEL_DEV:-0}" != "1" ]; then
  echo "Keel: skipping dev-env setup (agent-native mode needs no Python)."
  echo "  Working on Keel itself? Opt in once:  KEEL_DEV=1 bash scripts/dev_setup.sh"
  exit 0
fi

if [ ! -d .venv ]; then
  python3 -m venv .venv
fi

.venv/bin/pip install -q --upgrade pip
.venv/bin/pip install -q -e ".[dev]" || .venv/bin/pip install -q -e . pytest ruff

echo "Keel env ready (.venv): claude-agent-sdk + pytest + ruff installed."
echo "  Tests:  .venv/bin/python -m pytest -q"
echo "  Agents: .venv/bin/keel founding-journey   (or activate .venv)"
echo
echo "  Live-run note: the Claude Agent SDK passes --dangerously-skip-"
echo "  permissions, which the CLI refuses under root. If running as root,"
echo "  set  extra.permission_mode: default  in the agent's config.yaml,"
echo "  or run as a non-root user."
