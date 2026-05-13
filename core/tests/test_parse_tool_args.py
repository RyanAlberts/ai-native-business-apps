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


# --- dict-input path (Gemini / Ollama shapes) -------------------------


def test_dict_input_passes_through_as_copy():
    src = {"state": "CA"}
    out = parse_tool_args(src, "t")
    assert out == {"state": "CA"}
    # Should be a copy — mutating the result doesn't leak back.
    assert out is not src
    out["state"] = "TX"
    assert src["state"] == "CA"


def test_dict_like_iterable_of_pairs_coerces():
    # Gemini sometimes hands back a Mapping-like object that's iterable
    # as (k, v) pairs but isn't a plain dict.
    pairs = [("state", "CA"), ("city", "SF")]
    assert parse_tool_args(pairs, "t") == {"state": "CA", "city": "SF"}


def test_non_coercible_returns_error_string():
    # An integer can't be coerced to a dict — must not crash.
    result = parse_tool_args(42, "my_tool")
    assert isinstance(result, str)
    assert "my_tool" in result
    assert "coerce" in result.lower()


def test_empty_dict_passes_through():
    assert parse_tool_args({}, "t") == {}
