# DTL Research Notebook

Chronological log of the experiments behind DTL. Every number below is reproducible via `benchmarks/`.

## Phase 1 — The trap (benchmark.py)
Hypothesis: a symbolic invented language saves tokens.
Result: **falsified.** `∀u∈U: ✓(u.email)` = 11t vs plain English 5t. Unicode math symbols cost 2-3t each in o200k. Telegraphic English won: verbose Italian 61t -> telegraphic English 17t (-72%). Data formats: JSON 88t -> CSV 43t.

## Phase 2 — Pushing the limit (extreme_test.py)
Realistic 304t verbose prompt -> 91t structured DTL (-70%) -> 56t extreme (-82%).
Honest ceiling found: on already-decent prompts the gain drops to -24%. ASCII operators (`->`,`!=`,`<=`) all 1t; unicode equivalents 2t.

## Phase 3 — Vocabulary mining (vocab_mining.py)
Enumerated all ~200k o200k tokens. Found **6,586 single-token words ≥10 chars**. All 20 tested dev terms (authentication, middleware, infrastructure...) = 1t. Conclusion: never abbreviate; delete instead. Phrase-rewrite table built (make sure that->ensure etc.): -68% on filler phrases.
Codebook math: 62t codebook + 4t/msg vs 55t/msg verbose -> **-92/93% at scale** with prompt caching.

## Phase 4 — Round 2 micro-benchmarks (round2.py)
- CAPS = 3x cost (AUTHENTICATION 3t vs authentication 1t)
- ISO timestamps 13t -> date 6t -> 20260611 3t
- `- ` lists beat `1. ` by 1t/row; `a,b,c` beats `a, b, c` (3t vs 5t)
- short JSON keys: extra -31% on minified JSON
- traps: e.g.(3t) > "for example"(2t); 1,000,000(5t) > 1000000(3t)
- markdown tables cost +41% vs compact lines

## Phase 5 — Dogfooding
Applied DTL to its own SKILL.md: 2440t -> 1776t (-27%) **while adding ~10 rules** (density per rule ~2x). Compression power on held-out test improved -62% -> -65%.

## Phase 6 — The Engine + auto-codebook (scripts/dtl_engine.py)
Built a deterministic model-free compressor (vs LLMLingua which needs model inference).
First auto-codebook attempt **failed beautifully**: n-gram miner selected 8 overlapping macros, inflating the codebook (+25% worse). Fix: iterative greedy BPE — extract best macro, substitute, re-mine residual. Result: homogeneous corpus -64% asymptotic, heterogeneous (3 mixed task families) -55% at 1000 prompts, fully automatic.

## Phase 7 — Blind validation on a real model (tests/)
3 cases, verbose vs DTL, separate blind judge instance, all on one model (Claude Fable 5 via Claude Code).
Scores: 9, 9, 8. Average prompt compression -62%. DTL outputs also faster (33s->19s on React case).
**Bug found by the test itself**: English DTL prompt silently flips output language to English. Fixed in skill v4: rule 1 now requires explicit `Output language: <lang>` when the deliverable language matters. This is the method working: hypothesis -> test -> failure data -> rule fix.


## Phase 8 — Extreme-mode validation + a contamination lesson (tests/dtl_ab_test_v2.py)
Extreme prompts (-65/72% vs verbose) vs verbose, 2 runs/case, blind judge told to ignore style/language deltas.
First pass showed react_form [9, 2] — investigated: the score=2 was a **harness artifact**, not a DTL failure. `claude -p` has filesystem access; the verbose run found a residual `LoginForm.tsx` from the v1 test and answered "already exists" without code, so the judge penalized the VERBOSE side. Clean rerun: [9, 8].
Final: react_form 8.5, sql_query 9.0, bug_explain 8.5 — **extreme mode validated**. The v4 language rule (`Output language: it`) produced Italian output in both runs.
Structural fix adopted: every `claude -p` call now runs in an isolated temp cwd (no cross-run contamination).
Lesson: agentic test harnesses MUST isolate working directories; a single leftover file can flip a blind judgment.

## Open frontier
The 60-70% of agentic-session tokens (tool results, file reads) remain uncompressed. Next: a Claude Code PostToolUse hook serving files in "skim mode" (signatures+docstrings) during exploration, exact mode only for edits.
