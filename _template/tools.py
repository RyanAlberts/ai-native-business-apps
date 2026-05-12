# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""Custom Tools for this agent.

Define your tools as small Tool objects and return them from `all_tools()`.
The agent.py wires them into whichever provider is configured.

The Business Idea Validator template needs no tools (the LLM reasons over
the user's input). This file exists as a placeholder showing the pattern.
"""
from __future__ import annotations

from core import Tool


def all_tools() -> list[Tool]:
    """Return the list of tools this agent should have available."""
    return []


# Example: a custom tool you can adapt.
#
# async def _save_summary(args: dict) -> str:
#     from pathlib import Path
#     path = Path(args["path"]).expanduser()
#     path.write_text(args["content"])
#     return f"saved {len(args['content'])} chars to {path}"
#
# SAVE_SUMMARY = Tool(
#     name="save_summary",
#     description="Save the validation summary to a local file path.",
#     input_schema={
#         "type": "object",
#         "properties": {
#             "path":    {"type": "string", "description": "Filesystem path."},
#             "content": {"type": "string", "description": "Markdown content."},
#         },
#         "required": ["path", "content"],
#     },
#     handler=_save_summary,
# )
