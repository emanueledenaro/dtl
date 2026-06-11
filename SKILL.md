---
name: dtl
description: Dense Token Language (DTL) — compress any prompt, system prompt, instruction, or dataset to use 70-93% fewer tokens while preserving meaning and output quality. Use this skill whenever the user wants to reduce token usage, cut API costs, compress a prompt, optimize a system prompt, shrink context, prepare data for an LLM call, or mentions tokens, token budget, prompt compression, API costs, or making prompts/payloads smaller. Also use it proactively when building system prompts or recurring LLM pipelines (parsers, agents, batch jobs) where token efficiency matters.
---

# DTL — dense token language

Built on tokenizer research, not invented symbols. Key fact: BPE encodes full english technical words as 1 token (authentication = 1t = auth) -> never abbreviate words; delete words carrying no information + route data to token-optimal formats.

Measured: -70% typical input (lossless), -82% extreme, -90/93% recurring via codebook, -65/76% output via L4.

Routing: one-shot->L1(50-70%); terse ok->L1 extreme(70-82%); structured data->L2(45-60%); recurring pipeline->L3(90-93%). Always compress INTO english (densest for all tokenizers; italian +20-30%).

## L1 syntax, apply in order

1. translate prompt to english BUT if output must be in another language (user-facing text, client deliverable), append explicit "Output language: <lang>." — english prompt does NOT imply english output unless stated
2. delete zero-information: greetings, courtesy, meta-framing, hedges, restatements
3. imperative verb-first: "Could you create"->"Create"
4. drop articles+copulas where unambiguous
5. one dense word > many small (references/rewrite-table.md); never abbreviate technical words (already 1t)
6. lowercase — CAPS cost 3x; capitalize only proper nouns/code
7. ascii operators only, 1t each: -> => != <= >= | & + : ! ?  forbidden: unicode math (∀ ∈ ∧ = 2-3t)
8. lists: "- " not "1. " (+1t/row); inline: a,b,c no spaces
9. numbers: 1000000 not 1,000,000; 1M best; avoid e.g./i.e. (3t > plain words)
10. always append output constraint: "Output: <shape>. No explanation." (output tokens cost more, dominate latency)

Extreme (VALIDATED: blind-judge avg 8.5-9.0 across cases): drop prepositions where parseable, fuse with +/, single-line. Use when terse style acceptable; round-trip check still mandatory.

## L2 data

- flat table->csv (-61% vs pretty json); repeated nested->toon (users[5]{id,name,role}: + csv rows); single object->minified json
- shorten keys (transaction_identifier->id): -31% extra
- strip fields task doesn't need (biggest win)
- dates: drop time unless used (ISO timestamp 13t vs date 6t vs 20260611 3t)

## L3 codebook — the 90% layer

Recurring flows: macros defined once in system prompt (cached), referenced per message. Method: references/codebook-guide.md. Sketch:

CODEBOOK:
S=trading signal{pair,dir,entry,sl,tp[]}
P=parse S from text -> csv: pair,dir,entry,sl,tp1,tp2,tp3
R=reject if missing entry|sl

Per-message "P+R:" = 4t vs 55t verbose; +caching -> -92/93% at 10+ messages.

## L4 output mode (activate on: "dtl output"/"less tokens"/"output denso")

Apply L1 to own responses: no pleasantries/hedging, verb-first, lowercase prose, ascii operators, answer then stop. NEVER compress: code blocks, error messages (quote exact), commits/PRs, technical terms. Measured: -65/76% output tokens. Output compression compounds: every saved output token is also saved from history on every later turn.

## Guardrails, mandatory

1. NEVER delete: numbers, units, constraints, names, versions, edge cases, negations. That IS the information
2. round-trip: re-read compressed cold; every original requirement recoverable, else restore minimal words
3. report before->after tokens (chars/4, or scripts/count_tokens.py exact) + lossy flags
4. domain jargon verbatim (1t, max information)

## Output

1. DTL version, code block
2. metrics: before->after, % saved
3. lossy flags, one line
