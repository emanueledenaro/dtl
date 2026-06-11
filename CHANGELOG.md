# Changelog

All notable changes to this project are documented here.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) · versioning: [SemVer](https://semver.org/).

## [Unreleased]

### Planned
- Claude Code PostToolUse hook serving files in "skim mode" (signatures + docstrings) during exploration — targets the 60-70% of agentic-session tokens that DTL does not yet touch (see [RESEARCH.md](RESEARCH.md), *Open frontier*).
- Relay pipeline integration.

## [1.0.0] — 2026-06-11

### Added
- **Skill v5** (`SKILL.md`): four compression layers — L1 syntax (-50/70% lossless, -82% extreme), L2 data (-45/60%), L3 codebook (-90/93% with prompt caching), L4 output (-65/76%).
- **Extreme mode validated**: blind-judge A/B, 2 runs/case, averages 8.5 / 9.0 / 8.5 (threshold ≥8).
- **Explicit output-language rule** (`Output language: <lang>`) — added in skill v4 after the v1 A/B test caught silent language flipping; validated in v2.
- **Engine** (`scripts/dtl_engine.py`): deterministic, model-free compressor — `compress_text` (-48%), `compress_json` (JSON→TOON, -60%), `mine_codebook` (iterative greedy BPE over your own prompt corpus, -64% asymptotic).
- **Benchmarks** (`benchmarks/`): tokenizer research behind every claim — o200k vocabulary mining (6,586 single-token words ≥10 chars), symbolic-language falsification, CAPS/date/list/operator micro-benchmarks.
- **A/B harnesses** (`tests/`): verbose vs DTL with blind judge, runs on a Claude Code subscription (no API key); each call in an isolated temp cwd to prevent cross-run contamination.
- **Research notebook** (`RESEARCH.md`): all 8 phases, failures included.

[Unreleased]: https://github.com/emanueledenaro/dtl/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/emanueledenaro/dtl/releases/tag/v1.0.0
