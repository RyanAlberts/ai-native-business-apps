# Mission 2 — Security Review

_Branch `claude/cool-ramanujan-bD7zK`. Date: 2026-05-30._

Note on the `/security-review` skill: it reviews *pending changes on the current
branch vs. the base*. The Keel refactor already merged to `main` (commit
`3d030e7`), so the branch-vs-`main` diff is effectively empty and an automated
diff review surfaces nothing. The substantive work below is therefore a
**manual review of the merged refactor's security-relevant surfaces**, which is
what matters.

**Overall:** no critical or high-severity vulnerabilities. This is a
local-first, single-user tool with no server, no network-exposed surface, no
secrets in artifacts, and tools that are pure functions. One real low-severity
bug was found and **fixed** (ICS injection). The rest are hardening notes and a
billing-safety footgun.

| # | Severity | Finding | Status |
|---|---|---|---|
| 1 | **Low** | ICS CRLF/control-char injection via `_ics_escape` | ✅ **Fixed** |
| 2 | Low | `Artifact.write` does not sanitize `filename` (latent path traversal) | Flagged |
| 3 | Low | `html_artifact(body_html=...)` is an unescaped sink by contract | Flagged |
| 4 | Low / Info | Subscription guard bypass via spoofable env markers (billing footgun) | Flagged |
| 5 | Info | `bypassPermissions` + future networked MCP tool = prompt-injection→exfil | Flagged |
| 6 | Info | Prompt-injection blast radius (mapped; currently contained) | No action |
| 7 | Info | Dependency review — no new third-party deps | Pass |

---

## 1. ICS CRLF / control-char injection — **Low — FIXED**

`core/artifacts.py::_ics_escape` escaped `\` `;` `,` and `\n`, but **not a raw
`\r`**. RFC 5545 §3.1 forbids raw control characters inside a content line;
line breaks in a value must be the escaped sequence `\n`.

**Repro (before fix):**
```python
ics_artifact("x.ics", [{"date":"2026-06-01",
    "summary":"Evil\r\nBEGIN:VEVENT\r\nUID:injected"}])
# → SUMMARY line contained a raw CR; output had stray \r outside CRLF endings,
#   and "BEGIN:VEVENT" / "UID:" survived in a way a lenient calendar parser
#   could treat as a new property/component.
```

**Impact:** Low. The `.ics` is the user's own download imported into their own
calendar; there is no cross-user trust boundary and nothing is exfiltrated. But
the input is **LLM- or user-supplied** (event summaries, and indirectly
`company.legal_name`), the output was malformed ICS, and a calendar injection is
a clean, cheap thing to close.

**Fix:** normalize `\r\n` → `\r` → `\n` to escaped `\n` (order matters) in
`_ics_escape`. Verified: exactly one real `BEGIN:VEVENT`/`UID:` line remains, no
stray CR, injected text survives only as escaped text inside the value.
Regression test added (`test_ics_neutralizes_crlf_injection`).

_(Note: the `compliance_tax_agent`'s **separate** ICS builder
`tools.py::_escape_ics_text` already stripped `\r` and folds long lines — it was
not vulnerable. The two ICS implementations have now diverged in a good way but
should eventually be unified on `core.artifacts`.)_

## 2. `Artifact.write` filename sanitization — **Low (latent)**

`Artifact.write` does `Path(directory) / self.filename` with no check. Today
this is **safe** because every `filename` in `journey.build_artifacts` is a
hardcoded constant or `f"{i:02d}-{step.key}.md"` where `step.key` is a fixed
literal — **none are user-derived**. I verified that a hostile
`company.legal_name` (`"../../../../etc/passwd"`) cannot escape the output dir,
because `slugify` is only used in the HTML *title*, never as a path component.

**Risk:** latent. A future agent that builds an `Artifact` with a user/LLM-
derived filename would get path traversal for free. **Recommendation
(hardening):** reject or `os.path.basename()`-clamp filenames containing `/`,
`\`, or `..` inside `Artifact.write`.

## 3. `html_artifact(body_html=...)` is a trusted sink — **Low**

`html_artifact` escapes `title` and `meta` but injects `body_html` **verbatim**
(by design — it's "pre-rendered HTML"). The only production caller is
`letter_html`, which escapes every paragraph and is **safe** (verified:
`<script>` in the packet body/title is escaped in the output). So the shipped
path is fine.

**Risk:** if any future agent passes unescaped LLM/user text as `body_html`,
that text lands unescaped in a downloadable `.html`. Opened locally this is
low-impact (no cookies/session on a `file://`), but it's still XSS-in-a-file.
**Recommendation:** document the trust contract on `html_artifact` and prefer
`letter_html` (or an escaping markdown→HTML renderer) for any model output.

## 4. Subscription guard — **Low / Informational (billing footgun, not a vuln)**

`core/llm/claude.py::_enforce_subscription_guard` lets an `ANTHROPIC_API_KEY`
pass through in `subscription` mode if `ALLOW_API_KEY=1` **or** any of
`CLAUDECODE` / `CLAUDE_CODE_ENTRYPOINT` / `CLAUDE_CODE_SDK_HAS_OAUTH_REFRESH` /
`CURSOR_CLAUDE_OAUTH` is set.

- **Are the markers spoofable?** Yes — they're plain env vars any process can
  set. But this is **not a security boundary**: it's the user's own machine,
  own env, own key. Spoofing them only affects *that* user's own billing. There
  is no cross-trust escalation.
- **Can a paid key leak through when the user expects subscription-only?** Yes —
  this is the real (low) issue. Inside Claude Code, `CLAUDECODE=1` is always
  set. If a user *also* has a genuine **paid** `ANTHROPIC_API_KEY` exported in
  their shell, the guard assumes it's an OAuth-refreshed subscription token and
  **lets it through silently** — the user could be billed against their API
  account while believing they're on subscription.
- **Secret handling:** ✅ the key is **never logged**, never written to an
  artifact, never embedded in `company.json`. Confirmed by reading
  `claude.py` and grepping the artifact builders. The guard only reads
  `os.environ.get(...)` for presence.

**Recommendation:** when a marker-based pass-through occurs with a key present,
emit a one-time stderr notice ("Using ANTHROPIC_API_KEY detected in your env via
IDE pass-through; this may bill your API account. Set `ALLOW_API_KEY=1` to
silence or unset the key for pure subscription mode."). Low priority.

## 5. `bypassPermissions` + tools — **Informational**

`ClaudeClient.complete` defaults `permission_mode="bypassPermissions"`, so tool
calls execute without prompting. Today this is **safe** because every agent's
tools are **pure, in-process functions** (deadline math, vesting tables, state
lookups, fee calculators, ICS string-building) — none touch the network or the
filesystem outside the artifact dir, and `setting_sources=[]` isolates the run
from the user's global Claude skills/hooks/plugins (good).

**Risk to watch:** the moment an agent adds a *networked* or *filesystem* MCP
tool to its `allowed_tools`, `bypassPermissions` means prompt-injected text (see
#6) could trigger it with no human gate. **Recommendation:** keep
`bypassPermissions` paired with an explicit allowlist review whenever
`allowed_tools` gains a non-pure tool.

## 6. Prompt-injection blast radius — **Informational (contained)**

A hostile `company.one_liner` / `notes` flows through `Company.to_context()`
into **all five journey steps and the synthesizer**, and each step's output is
threaded into the next via the transcript. Mapped blast radius:

- **No exfiltration path.** The tools can't make network/file calls, so injected
  instructions have nowhere to send data.
- **Worst case:** the attacker (who is the founder, against their own packet)
  steers the generated *advice text* or pollutes the synthesized packet. This is
  a self-inflicted content issue, not a breach.
- `setting_sources=[]` prevents injected text from reaching host hooks/skills.

No action required now; revisit if/when networked tools or multi-tenant use is
added.

## 7. Dependency review — **Pass**

No new third-party dependencies. The new core modules (`company`, `artifacts`,
`util`, `brand`) are **stdlib-only** (`json`, `dataclasses`, `html`,
`datetime`, `re`, `pathlib`). `pyproject.toml` deps are unchanged
(`claude-agent-sdk`, `anyio`, `pyyaml`, `python-dotenv`, `streamlit`). Install
path is `pip install -e .`. ✅

## Fixes applied

- `core/artifacts.py::_ics_escape` — CRLF/control-char normalization (#1).
- `core/tests/test_artifacts.py` — regression test for #1.

## Flagged for the owner (not fixed)

- #2 `Artifact.write` filename clamp (hardening).
- #3 document `html_artifact` trust contract.
- #4 subscription-guard billing notice.
- #5 keep `bypassPermissions` reviews tied to `allowed_tools` changes.
