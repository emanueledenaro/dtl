# 🧬 DTL — Dense Token Language

**Stop abbreviating. Start deleting.**

A prompt-compression language built on empirical tokenizer research — not invented symbols, not caveman grunts. **-70% tokens on typical prompts (lossless), -82% extreme, -93% on recurring pipelines.** Validated with blind-judge A/B testing on real models.

## The counterintuitive findings that power DTL

We mined the full o200k vocabulary (~200k tokens) and benchmarked everything. Four discoveries break common intuition:

1. **Abbreviations are useless.** `authentication` (14 chars) = **1 token** = same as `auth`. So do `configuration`, `infrastructure`, `vulnerability`... 6,586 words ≥10 chars cost exactly 1 token. The tokenizer already compressed English for you.
2. **Symbolic "AI languages" lose.** `∀u∈U: ✓(u.email)` looks compact but costs **11 tokens** vs 5 for plain "for each user check email". Unicode math symbols tokenize at 2-3t each. Every symbol-based compression scheme fights the tokenizer instead of exploiting it.
3. **CAPS cost 3x.** `AUTHENTICATION` = 3t, `authentication` = 1t.
4. **`e.g.` is a trap.** It costs 3 tokens — *more* than "for example" (2t).

## The four layers

| Layer | Target | Measured saving |
|---|---|---|
| **L1 syntax** | any prompt | -50/70% (lossless), -82% extreme |
| **L2 data** | JSON/structured payloads | -45/60% (TOON/CSV + short keys + clean dates) |
| **L3 codebook** | recurring pipelines | **-90/93%** (macros + prompt caching) |
| **L4 output** | model responses | -65/76% (beats caveman's -65% on its own examples) |

## Validation (blind judge, real model)

3 tasks (React component, SQL query, bug explanation), verbose vs DTL, judged blind by a separate model instance scoring functional equivalence 0-10:

| Case | Base DTL | Judge | Extreme DTL | Judge (avg, 2 runs) |
|---|---|---|---|---|
| react_form | -59% | 9 | -72% | 8.5 |
| sql_query | -57% | 9 | -65% | 9.0 |
| bug_explain | -69% | 8 | -70% | 8.5 |

**Both modes pass (≥8 everywhere). Same quality, up to -72% tokens, faster responses** (19s vs 33s on the React case). The explicit `Output language:` rule was validated in the wild (Italian output from English prompts). Reproduce it yourself: `tests/` runs on a Claude Code subscription, no API key — each call in an isolated temp dir to prevent cross-run contamination.

## Install (as a Claude skill)

```bash
npx skills add SeriumTW/dtl
```
Or download `SKILL.md` + `references/` + `scripts/` into your skills folder.

Then just ask Claude to "compress this prompt" / "optimize tokens" — the skill triggers automatically.

## The Engine (programmatic, model-free)

Unlike LLMLingua, `scripts/dtl_engine.py` needs **no model, no GPU, zero inference cost** — pure verified token-table rules:

```python
from dtl_engine import compress_text, compress_json, mine_codebook

compress_text(verbose_prompt)        # -48% deterministic
compress_json(api_payload)           # -60%: JSON -> TOON, short keys, clean dates
mine_codebook(your_prompt_corpus)    # auto-extracts macros: -64% asymptotic
```

`mine_codebook` is, to our knowledge, novel: an **iterative greedy BPE running on top of the model's BPE**, trained on *your own* prompt corpus. Feed it N raw prompts, it finds the invariants, promotes them to macros only when the token balance is positive, and emits a ready-to-cache codebook.

## DTL vs caveman 🪨

[caveman](https://github.com/JuliusBrussee/caveman) is great fun — but it only compresses **output** (their README says so). DTL is full-duplex:

| Front | caveman | DTL |
|---|---|---|
| Output | -65% avg | **-76%** (their own README example: 22t vs our 15t) |
| Input prompts | 0% | -65/82% |
| Structured data | 0% | -60% |
| Recurring pipelines | 0% | -93% |

## The research journey

This started as "invent a compressed language for AI" and survived contact with reality: the symbolic approach failed measurably, the abbreviation approach turned out pointless, and the winning strategy emerged from vocabulary mining + amortized codebooks. Full lab notebook with every experiment, failure and fix: [RESEARCH.md](RESEARCH.md).

## License

MIT — © 2026 Emanuele Denaro ([@SeriumTW](https://github.com/SeriumTW))
