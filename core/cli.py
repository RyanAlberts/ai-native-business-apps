# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""`agent` CLI launcher.

Discovers agent packages on disk (any folder with an `agent.py` under
`starter_business_agents/` or `advanced_business_agents/`) and launches
them by short name, in Streamlit mode by default.

Usage:
    agent                       # interactive picker
    agent list                  # print all available agents
    agent <name>                # launch <name> via Streamlit
    agent <name> --cli "input"  # run agent.run() once, print result
    agent --help
"""
from __future__ import annotations

import argparse
import asyncio
import importlib
import sys
from pathlib import Path


def _repo_root() -> Path:
    """Locate the repo root by walking up from this file."""
    return Path(__file__).resolve().parents[1]


def _discover() -> dict[str, dict]:
    """Return {short_name: {dotted_path, agent_dir, kind, description}}."""
    root = _repo_root()
    found: dict[str, dict] = {}
    search_roots = [
        ("starter", root / "starter_business_agents"),
        ("advanced", root / "advanced_business_agents"),
    ]
    for kind, search_root in search_roots:
        if not search_root.exists():
            continue
        for agent_py in search_root.rglob("agent.py"):
            agent_dir = agent_py.parent
            rel = agent_dir.relative_to(root)
            dotted = ".".join(rel.parts)
            full_name = agent_dir.name
            short = _shorten(full_name)
            description = _read_one_line_desc(agent_dir / "README.md")
            found[short] = {
                "name": full_name,
                "short": short,
                "dotted": dotted,
                "dir": agent_dir,
                "kind": kind,
                "description": description,
            }
    return found


_SUFFIXES = ("_agent", "_team", "_manager")


def _shorten(folder: str) -> str:
    """`incorporation_agent` -> `incorporation`,
    `business_plan_implementation_manager` -> `business-plan`."""
    name = folder
    for suffix in _SUFFIXES:
        if name.endswith(suffix):
            name = name[: -len(suffix)]
            break
    name = name.replace("_implementation", "").replace("_application", "")
    return name.replace("_", "-")


def _read_one_line_desc(readme: Path) -> str:
    if not readme.exists():
        return ""
    for line in readme.read_text().splitlines():
        stripped = line.strip()
        if stripped.startswith("> "):
            return stripped[2:].strip()
        if stripped and not stripped.startswith("#") and not stripped.startswith("!"):
            return stripped[:120]
    return ""


def _resolve(name: str, agents: dict[str, dict]) -> dict | None:
    """Match by exact short name, then by case-insensitive prefix, then by substring."""
    if name in agents:
        return agents[name]
    lower = name.lower()
    prefixes = [a for s, a in agents.items() if s.startswith(lower)]
    if len(prefixes) == 1:
        return prefixes[0]
    subs = [a for s, a in agents.items() if lower in s]
    if len(subs) == 1:
        return subs[0]
    return None


def _print_list(agents: dict[str, dict]) -> None:
    from .brand import CLI, banner

    if not agents:
        print("No agents found.")
        return
    print(f"\n{banner()}\n")
    print(f"{len(agents)} agents available:\n")
    width = max(len(s) for s in agents) + 2
    # Surface the flagship journey first, then the rest alphabetically.
    ordered = sorted(
        agents.items(), key=lambda kv: (kv[0] != "founding-journey", kv[0])
    )
    for short, info in ordered:
        marker = "🚀" if info["kind"] == "advanced" else "📂"
        star = " ⭐" if short == "founding-journey" else ""
        print(f"  {marker}  {short:<{width}} {info['description']}{star}")
    print(f"\nRun:  {CLI} <name>            (Streamlit UI)")
    print(f"      {CLI} <name> --cli ...   (one-shot CLI)")
    print(f"\nNew here? Start with the full back office:  {CLI} founding-journey\n")


def _pick_free_port(preferred: int = 8501, max_tries: int = 50) -> int:
    """Return `preferred` if free; else the next free port within max_tries."""
    import socket
    for port in range(preferred, preferred + max_tries):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("127.0.0.1", port))
            except OSError:
                continue
            return port
    return preferred  # fall back; let streamlit error if truly stuck


def _wait_for_port(port: int, timeout: float = 10.0) -> bool:
    """Poll the port until it accepts connections, or timeout."""
    import socket
    import time
    deadline = time.time() + timeout
    while time.time() < deadline:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            try:
                s.connect(("127.0.0.1", port))
                return True
            except (ConnectionRefusedError, OSError):
                time.sleep(0.2)
    return False


def _launch_streamlit(agent: dict) -> int:
    import shutil
    import subprocess
    import webbrowser

    streamlit = shutil.which("streamlit")
    if not streamlit:
        print("error: streamlit not found. Install with: pip install streamlit")
        return 1
    app_path = agent["dir"] / "app.py"
    if not app_path.exists():
        print(f"error: no app.py at {app_path}")
        return 1

    port = _pick_free_port(8501)
    url = f"http://localhost:{port}"

    # Run streamlit headless so its own auto-open doesn't race with ours.
    cmd = [
        streamlit,
        "run",
        str(app_path),
        "--server.port",
        str(port),
        "--server.headless",
        "true",
        "--browser.gatherUsageStats",
        "false",
    ]
    print(f"Starting {agent['short']} on {url} ...")
    proc = subprocess.Popen(cmd)

    try:
        if _wait_for_port(port, timeout=10.0):
            webbrowser.open(url)
            print(f"Opened in your browser: {url}")
        else:
            print(f"Server didn't respond in 10s — open manually: {url}")
        return proc.wait()
    except KeyboardInterrupt:
        proc.terminate()
        try:
            return proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
            return proc.wait()


def _run_cli(agent: dict, user_input: str) -> int:
    sys.path.insert(0, str(_repo_root()))
    mod = importlib.import_module(f"{agent['dotted']}.agent")
    if not hasattr(mod, "run"):
        print(f"error: {agent['dotted']}.agent has no `run` function")
        return 2
    from .brand import with_disclaimer

    result = asyncio.run(mod.run(user_input))
    # `.final` covers HarnessResult / JourneyResult; otherwise it's the
    # plain markdown string a starter agent returns. Either way, append the
    # disclaimer once so the piped/redirected output carries it too.
    text = result.final if hasattr(result, "final") else result
    print(with_disclaimer(text))
    return 0


def _interactive_pick(agents: dict[str, dict]) -> dict | None:
    items = sorted(agents.items())
    print("\nWhich agent?\n")
    for i, (short, info) in enumerate(items, 1):
        marker = "🚀" if info["kind"] == "advanced" else "📂"
        print(f"  {i:2d}. {marker}  {short}  —  {info['description'][:70]}")
    print()
    try:
        choice = input("Number (or short name): ").strip()
    except (EOFError, KeyboardInterrupt):
        print()
        return None
    if not choice:
        return None
    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(items):
            return items[idx][1]
        print("invalid number")
        return None
    return _resolve(choice, agents)


def main(argv: list[str] | None = None) -> int:
    from .brand import CLI, banner

    parser = argparse.ArgumentParser(
        prog=CLI,
        description=banner(),
        epilog=(
            f"examples:\n  {CLI}\n  {CLI} list\n  {CLI} founding-journey"
            f"\n  {CLI} incorporation\n  {CLI} business-plan --cli \"my business idea\""
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("name", nargs="?", help="agent short name (or 'list')")
    parser.add_argument(
        "--cli",
        metavar="INPUT",
        help="run the agent once with INPUT as user message; print result to stdout",
    )
    args = parser.parse_args(argv)
    agents = _discover()

    if args.name == "list":
        _print_list(agents)
        return 0

    if args.name is None:
        agent = _interactive_pick(agents)
        if agent is None:
            return 0
    else:
        agent = _resolve(args.name, agents)
        if agent is None:
            print(f"error: no agent matching '{args.name}'.")
            _print_list(agents)
            return 2

    if args.cli:
        return _run_cli(agent, args.cli)
    return _launch_streamlit(agent)


if __name__ == "__main__":
    sys.exit(main())
