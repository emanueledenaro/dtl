# DTL codebook — the 90% layer

For recurring LLM flows (parsers, agents, classifiers, batch): define codebook once in system prompt, reference macros per message.

## Method
1. invariant (identical across calls: task, schema, rules, output format) -> codebook
2. variant (per-call data) -> user message, L2 format
3. macros = single uppercase letters (1t each), max 10
4. definitions written in L1 DTL (codebook itself must be dense)
5. per-message: "<macros>: <data>" — "P+R: <raw text>"

## Template
CODEBOOK:
X=<entity>{field,field,field[]}
Y=<verb> X from input -> <output format>
Z=reject|flag if <condition>
DEFAULT: apply Y+Z to every message unless told otherwise.

DEFAULT clause -> per-message overhead = 0; send data only.

## Economics (measured)
- codebook: 60-150t once; replaces 50-200t/call
- break-even: 1-3 messages
- 100 calls: -92%; 1000: -93% (asymptote = data tokens only)
- prompt caching (anthropic/openai): codebook prefix ~10% cost after first call -> asymptote reached immediately

## Rules
- codebook in SYSTEM prompt (stable prefix = cacheable); never re-send in user messages
- version it (CODEBOOK v2:) on semantic changes
- test once per codebook: known input -> verify output matches verbose baseline before deploy
