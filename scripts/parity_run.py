#!/usr/bin/env python3
# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""Capture an agent's output on its golden prompts.

Usage:
    python scripts/parity_run.py <agent_module> [--provider claude]

Examples:
    python scripts/parity_run.py _template
    python scripts/parity_run.py starter_business_agents.01_incorporation_agent

Writes timestamped output to <agent_folder>/tests/runs/<provider>-<date>.md.
Compare against <agent_folder>/tests/baselines/ (or another provider's run)
to fill out PARITY.md.
"""
from __future__ import annotations

import argparse
import asyncio
import datetime as dt
import importlib
import json
import os
import sys
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("agent_module", help="dotted path, e.g. _template")
    ap.add_argument("--provider", default=None, help="override config.yaml provider")
    args = ap.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(repo_root))

    mod = importlib.import_module(f"{args.agent_module}.agent")
    if not hasattr(mod, "run"):
        print(f"error: {args.agent_module}.agent has no async `run()` function")
        return 2

    agent_dir = Path(mod.__file__).resolve().parent
    golden_path = agent_dir / "tests" / "golden.jsonl"
    if not golden_path.exists():
        print(f"error: no golden.jsonl at {golden_path}")
        return 2

    if args.provider:
        os.environ["__PARITY_PROVIDER_OVERRIDE"] = args.provider
        # If your agent honors this override, it can read it in load_config.
        # The simple approach: just edit config.yaml for the run.

    provider = args.provider or _read_config_provider(agent_dir / "config.yaml")
    date = dt.date.today().isoformat()
    out_dir = agent_dir / "tests" / "runs"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{provider}-{date}.md"

    with out_path.open("w") as out:
        out.write(f"# Parity run — {args.agent_module}\n")
        out.write(f"Provider: {provider} · Date: {date}\n\n")
        for line in golden_path.read_text().splitlines():
            line = line.strip()
            if not line:
                continue
            case = json.loads(line)
            cid, prompt = case["id"], case["prompt"]
            print(f"  [{cid}] {prompt[:60]}...")
            result = asyncio.run(mod.run(prompt))
            out.write(f"## {cid}\n\n**Prompt:** {prompt}\n\n**Output:**\n\n{result}\n\n---\n\n")

    print(f"wrote {out_path}")
    return 0


def _read_config_provider(path: Path) -> str:
    if not path.exists():
        return "unknown"
    import yaml
    return (yaml.safe_load(path.read_text()) or {}).get("provider", "unknown")


if __name__ == "__main__":
    sys.exit(main())
