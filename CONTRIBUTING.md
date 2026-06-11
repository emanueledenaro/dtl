# Contributing to DTL

DTL is empirical: every rule exists because a measurement says it saves tokens without losing information. Contributions follow the same standard — **numbers over opinions**.

## Setup

```bash
pip install tiktoken          # the only dependency (o200k token counts)
python -m unittest discover -s tests -p "test_*.py"   # engine unit tests, no model needed
```

The A/B harnesses (`tests/dtl_ab_test*.py`) additionally require the `claude` CLI logged into a Claude Code subscription. No API key.

## Repository layout

| Path | Purpose |
|---|---|
| `SKILL.md` | The Claude skill (root placement required by `npx skills add`) |
| `references/` | Rewrite table + codebook method, loaded on demand by the skill |
| `scripts/` | `dtl_engine.py` (model-free compressor), `count_tokens.py` (exact o200k counts) |
| `benchmarks/` | Phase 1-4 experiments — every number in the README is reproducible here |
| `tests/` | Blind-judge A/B harnesses + CI unit tests |
| `RESEARCH.md` | Lab notebook, failures included |

## Proposing a compression rule

Open an issue with the *rule proposal* template, or a PR directly. A rule needs:

1. **Token measurement** — before/after counts via `scripts/count_tokens.py` (o200k), not estimates.
2. **Quality evidence** — if the rule could be lossy, a blind-judge A/B run (`tests/dtl_ab_test_v2.py`, add your case to `CASES`) scoring ≥8 average.
3. **A failure check** — what input breaks the rule? Document it. Rules that delete numbers, units, constraints, names, versions, negations or edge cases are rejected: that *is* the information.

A falsification (showing a current rule loses tokens or information) is just as valuable as a new rule — see RESEARCH.md phase 1.

## Pull requests

- One rule / one fix per PR.
- CI must pass (`compileall` + unit tests).
- Update `SKILL.md` *and* the corresponding benchmark or test when behavior changes.
- Keep docs in DTL style: dense, no filler. Practice what we compress.

## Test harness hygiene

Lesson from phase 8: agentic test calls **must** run in an isolated temp cwd — a single leftover file can flip a blind judgment. `cl()` in `dtl_ab_test_v2.py` already does this; keep it that way.
