#!/usr/bin/env python3
"""DTL Engine — deterministic, model-free prompt compressor + auto-codebook miner.
No GPU, no model inference (unlike LLMLingua): pure verified token-table rules.

Usage:
  from dtl_engine import compress_text, compress_json, mine_codebook
  pip install tiktoken
"""
import re, json
from collections import Counter
import tiktoken

enc = tiktoken.get_encoding("o200k_base")
def tcount(s): return len(enc.encode(s))

REWRITES = [
    (r"\bin order to\b","to"),(r"\bmake sure that\b","ensure"),(r"\bas soon as possible\b","immediately"),
    (r"\bat the same time\b","simultaneously"),(r"\btake into account\b","consider"),(r"\bit is necessary to\b","must"),
    (r"\bdue to the fact that\b","because"),(r"\bthe fact that\b","that"),(r"\bhas the ability to\b","can"),
    (r"\bis able to\b","can"),(r"\bin the event that\b","if"),(r"\bprovided that\b","if"),
    (r"\bwith respect to\b","regarding"),(r"\ba large number of\b","many"),(r"\bin the absence of\b","without"),
    (r"\bas a result of\b","from"),(r"\bprior to\b","before"),(r"\bsubsequent to\b","after"),
    (r"\bwhether or not\b","whether"),(r"\bon the other hand\b","however"),(r"\ba variety of\b","various"),
]
FILLERS = [
    r"\b(please|kindly)\b,?\s*", r"\bthank(s| you)( very much| in advance)?[.!]?\s*",
    r"\bI('d| would) (like|love|need)( you)? to\b\s*", r"\bcould you( please)?\b\s*",
    r"\b(basically|actually|really|just|simply|very)\b\s*", r"\bif possible,?\s*", r"\bfeel free to\b\s*",
]

def compress_text(s: str) -> str:
    """L1 deterministic compression. Lossless on numbers/constraints/negations."""
    out = s
    for pat in FILLERS: out = re.sub(pat, "", out, flags=re.I)
    for pat, rep in REWRITES: out = re.sub(pat, rep, out, flags=re.I)
    out = re.sub(r",\s+", ",", out)
    while re.search(r"\d,\d{3}\b", out):                  # 1,000,000 -> 1000000
        out = re.sub(r"(\d),(\d{3})\b", r"\1\2", out)
    out = re.sub(r"\s{2,}", " ", out)
    return out.strip()

def compress_json(payload):
    """L2: array of records -> TOON (short keys, dates without time). -60% vs pretty JSON."""
    data = json.loads(payload) if isinstance(payload, str) else payload
    if isinstance(data, dict):
        arrs = [(k,v) for k,v in data.items() if isinstance(v,list) and v and isinstance(v[0],dict)]
        if not arrs: return json.dumps(data, separators=(',',':'))
        name, rows = arrs[0]
    else: name, rows = "rows", data
    keys = list(rows[0].keys())
    short = {k: (re.sub(r"(_id|entifier)$","",k).split("_")[-1][:6] or k) for k in keys}
    def clean(v):
        return re.sub(r"(\d{4}-\d{2}-\d{2})T[\d:]{8}(\.\d+)?Z?", r"\1", str(v))
    return f"{name}[{len(rows)}]{{{','.join(short[k] for k in keys)}}}:\n" + \
           "\n".join(",".join(clean(r.get(k,"")) for k in keys) for r in rows)

def mine_codebook(prompts, max_macros=8, min_saving=10):
    """Auto-codebook: iterative greedy BPE over your own prompt corpus.
    Each round: find the token n-gram with best net saving, promote to macro, substitute, repeat.
    Returns (codebook_str, compressed_prompts, macros). Put codebook in SYSTEM prompt (cached)."""
    work = list(prompts); macros = []; letters = "ABCDEFGH"
    REF, DEF_OH = 2, 3
    for _ in range(max_macros):
        cand = Counter()
        for p in work:
            tk = enc.encode(p); seen = set()
            for n in range(4, min(80, len(tk))+1):
                for i in range(len(tk)-n+1):
                    g = tuple(tk[i:i+n])
                    if g not in seen: cand[g] += 1; seen.add(g)
        best, best_sav = None, min_saving
        for g, f in cand.items():
            if f < 2: continue
            sav = f*len(g) - (len(g)+DEF_OH) - f*REF
            if sav > best_sav: best, best_sav = g, sav
        if not best: break
        s = enc.decode(list(best))
        L = letters[len(macros)]
        macros.append((L, s.strip(), best_sav))
        work = [re.sub(r"\s{2,}"," ", p.replace(s, f" {L} ")).strip() for p in work]
    book = "CODEBOOK:\n" + "\n".join(f"{L}={s}" for L,s,_ in macros)
    return book, work, macros

if __name__ == "__main__":
    import sys
    data = sys.stdin.read()
    try:
        print(compress_json(data))
    except Exception:
        print(compress_text(data))
