#!/usr/bin/env python3
"""DTL token counter — exact token counts for before/after comparison.
Usage: python count_tokens.py file1 [file2 ...]   or   echo "text" | python count_tokens.py
Requires: pip install tiktoken
"""
import sys

try:
    import tiktoken
except ImportError:
    sys.exit("pip install tiktoken --break-system-packages")

enc = tiktoken.get_encoding("o200k_base")

def report(label, text):
    n = len(enc.encode(text))
    print(f"{label}: {n} tokens, {len(text)} chars ({len(text)/max(n,1):.2f} chars/tok)")
    return n

if len(sys.argv) > 1:
    counts = []
    for p in sys.argv[1:]:
        with open(p) as f:
            counts.append(report(p, f.read()))
    if len(counts) == 2:
        a, b = counts
        print(f"\nSaving: {a} -> {b} tokens = -{100-100*b/a:.0f}%")
else:
    report("stdin", sys.stdin.read())
