# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
"""Tests for core.llm.base.parse_tool_args.

The helper exists to keep a malformed JSON tool-call from the model from
crashing the agent (OpenAI / xAI providers). The contract: dict on success,
error-string on failure.
"""
from __future__ import annotations

from core.llm.base import parse_tool_args


def test_parses_valid_json_to_dict():
    assert parse_tool_args('{"state": "CA"}', "lookup") == {"state": "CA"}


def test_empty_string_returns_empty_dict():
    assert parse_tool_args("", "lookup") == {}


def test_none_returns_empty_dict():
    assert parse_tool_args(None, "lookup") == {}


def test_malformed_json_returns_error_string_with_tool_name():
    result = parse_tool_args("{not json", "my_tool")
    assert isinstance(result, str)
    assert "my_tool" in result
    assert "malformed" in result.lower()


def test_nested_json_preserved():
    raw = '{"states": ["CA", "TX"], "options": {"verbose": true}}'
    assert parse_tool_args(raw, "t") == {
        "states": ["CA", "TX"],
        "options": {"verbose": True},
    }


def test_json_array_is_not_a_dict_but_does_not_raise():
    # The model is supposed to send an object, but if it sends an array
    # we still must not crash. The current contract returns the array
    # as-is (a list, not a dict), and downstream tool handlers will fail
    # validation — but the agent stays alive.
    result = parse_tool_args("[1, 2, 3]", "t")
    assert result == [1, 2, 3]
