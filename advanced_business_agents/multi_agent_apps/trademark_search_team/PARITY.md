# Parity Report — Trademark Search Team

| | |
|---|---|
| Source | Original work; first consumer of `core.ParallelHarness` |
| Default model | claude-sonnet-4-6 |
| Last verified | not yet run end-to-end |

## 1. Capability parity (tools × providers)

| Tool / Capability | claude | openai | gemini | xai | ollama | codex |
|---|---|---|---|---|---|---|
| `uspto_fee_estimate` (deterministic) | ✅ | ✅ | ✅ | ✅ | ✅ | ⏳ stub |
| `WebSearch` (provider built-in) | ✅ | ⚠️ (manual MCP) | ⚠️ (manual MCP) | ⚠️ (manual MCP) | ❌ | ⏳ stub |
| `ParallelHarness` orchestration | ✅ | ✅ | ✅ | ✅ | ✅ | ⏳ stub |

The WebSearch dependency is the critical bit. Claude bundles WebSearch
via `claude-agent-sdk`. Other providers need either:
- an MCP search server configured in `mcp_servers:` in the config, OR
- a custom search Tool in `tools.py` (e.g. Brave Search API wrapper).

Without web access, the four research branches will produce no findings
(or worse, hallucinate) — the branch prompts explicitly forbid invention.

## 2. Behavioral parity (golden prompts)

See `tests/golden.jsonl`.

| ID | Scenario | claude | openai | gemini |
|---|---|---|---|---|
| g1 | Distinctive coined mark, single class (Class 9 software) | not yet run | not yet run | not yet run |
| g2 | Generic-leaning mark, likely §2(e) descriptiveness refusal | not yet run | not yet run | not yet run |
| g3 | Crowded class with many similar marks (apparel Class 25) | not yet run | not yet run | not yet run |
| g4 | Multi-class need (downloadable app Class 9 + SaaS Class 42) | not yet run | not yet run | not yet run |
| g5 | Foreign-language mark with English equivalent in the same class | not yet run | not yet run | not yet run |

## 3. UX parity (Streamlit)

- [x] Form inputs (mark, goods/services, state, use status, notes)
- [x] Live progress indicators per branch (since they run in parallel,
      the UI shows which branches have completed and which are still
      working)
- [x] Final synthesis report with markdown rendering
- [x] Expandable "raw branch findings" section for debug/audit
- [x] Download button

## 4. Cost / latency (informational only)

Five LLM calls per run (4 branches + 1 synthesizer). Branches run in
parallel — expected wall-clock latency dominated by `max(branch_durations)`
not the sum. Each branch typically does 5–8 WebSearch calls (config has
`max_turns: 20` to cover this). Synthesizer makes one `uspto_fee_estimate`
tool call (microseconds) + the LLM completion.

Estimated wall time on `claude-sonnet-4-6` with WebSearch: 2–5 minutes
(branch latency ~120–180s + synthesizer ~120s). The first end-to-end
run on 2026-05-14 crashed at 115s due to a config bug (max_turns=8 too
low) — fixed; expect a 2–5 min successful run on retry. Set client
timeouts ≥ 360s.

Compare to a hypothetical 4-branch SEQUENTIAL trademark agent at the
same per-call rate: ~8–12 minutes. ParallelHarness saves ~60% of
wall time on this workload.

## 5. Known gaps

- **US-only**: no EUIPO / Madrid Protocol branches. Adding them is a
  one-line addition since `ParallelHarness` accepts any number of
  `Stage` branches.
- **No domain availability**: a natural future branch.
- **No specimen-of-use guidance**: when the founder files use-in-commerce
  (1(a)) rather than intent-to-use (1(b)), they need to attach a specimen.
  The agent currently produces only the application pre-fill, not the
  specimen.
- **Fee schedule snapshot**: post-Jan-2025 fees baked into
  `uspto_fee_estimate`. USPTO can change fees on October 1 of any year;
  the tool surfaces the source URL so the founder verifies.
- **No `class.advice` for ambiguous categories**: e.g. NFT-related marks
  are split across Class 9 / 35 / 41 in shifting ways. The class-ID
  branch handles common cases but doesn't have specialist knowledge of
  edge classes.
- **§2(d) examination is subjective**: the agent's verdict is research
  output, not the USPTO examining attorney's call. CAUTION verdicts
  should prompt an attorney review before paying the filing fee.

## 6. Verdict

| Provider | Verdict |
|---|---|
| claude | not yet verified (scaffold only — needs end-to-end run with WebSearch) |
| openai | not yet run; requires MCP search or custom Tool |
| gemini | not yet run; requires MCP search or custom Tool |
| xai | community-supported |
| ollama | not supported (no native web search) |
| codex | stub |
