#!/usr/bin/env python3
"""L3 codebook end-to-end test — exact-match vs ground truth, no judge needed.
Verbose instruction per-message VS codebook+macro. 10 claude -p calls. Isolated cwd."""
import subprocess, tempfile, re, sys

VERBOSE = """Parse the following trading signal and extract pair, direction, entry price, stop loss and all take profit levels. Output ONLY one CSV line: pair,dir,entry,sl,tp1,tp2(if present). If entry or stop loss is missing output ONLY the word REJECT. Signal: {sig}"""

CODEBOOK = """CODEBOOK:
S=trading signal{{pair,dir,entry,sl,tp[]}}
P=parse S from text -> output ONLY one csv line: pair,dir,entry,sl,tp1,tp2(if present)
R=if entry|sl missing -> output ONLY: REJECT

P+R: {sig}"""

# (signal, expected fields | "REJECT")
CASES = [
 ("GOLD BUY NOW 2340 SL 2330 TP 2350 2360", ["gold","buy","2340","2330","2350","2360"]),
 ("EURUSD SELL 1.0850 SL 1.0880 TP 1.0820", ["eurusd","sell","1.0850","1.0880","1.0820"]),
 ("XAUUSD buy limit 2335, sl 2325, tp1 2345 tp2 2355", ["xauusd","buy","2335","2325","2345","2355"]),
 ("US30 SELL 38900 SL 39050 TP 38700", ["us30","sell","38900","39050","38700"]),
 ("GBPUSD BUY 1.2500 TP 1.2600", "REJECT"),   # niente SL -> testa la regola R
]

def cl(p):
    with tempfile.TemporaryDirectory() as d:
        r = subprocess.run(["claude","-p",p], capture_output=True, text=True, timeout=300, cwd=d)
    return r.stdout.strip()

def score(out, expect):
    o = out.lower()
    if expect == "REJECT":
        return (1.0, "reject ok") if "reject" in o else (0.0, f"atteso REJECT, got: {out[:60]}")
    hit = sum(1 for f in expect if f in o)
    return hit/len(expect), f"{hit}/{len(expect)} campi"

def main():
    tot_v = tot_c = 0
    print(f"{'#':<3}{'verbose':<22}{'codebook':<22}")
    for i,(sig, exp) in enumerate(CASES,1):
        sv,_ = score(cl(VERBOSE.format(sig=sig)), exp)
        sc,note = score(cl(CODEBOOK.format(sig=sig)), exp)
        tot_v += sv; tot_c += sc
        print(f"{i:<3}{sv:<22.2f}{sc:<22.2f}{note}")
    av, ac = tot_v/len(CASES), tot_c/len(CASES)
    print(f"\naccuracy: verbose={av:.0%} codebook={ac:.0%}")
    print("L3 VALIDATO: codebook regge la qualità" if ac >= av - 0.05 else
          "L3 NON validato: la macro-indirection perde informazione — non usare in produzione")
    # economia: prompt token ~ chars/4
    pv = len(VERBOSE.format(sig=CASES[0][0]))//4; pc = len("P+R: "+CASES[0][0])//4
    print(f"economia per msg (codebook in system, cached): ~{pv}t -> ~{pc}t (-{100-100*pc/pv:.0f}%)")

if __name__ == "__main__": main()
