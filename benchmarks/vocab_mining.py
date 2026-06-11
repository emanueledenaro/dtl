import tiktoken
enc = tiktoken.get_encoding("o200k_base")
def t(s): return len(enc.encode(s))

print("=" * 70)
print("FASE 1: Mining del vocabolario — le 'superparole' da 1 token")
print("=" * 70)

# Decodifico TUTTO il vocabolario e cerco parole intere lunghe = 1 token
superwords = []
for i in range(enc.n_vocab):
    try:
        s = enc.decode([i])
    except Exception:
        continue
    w = s.strip()
    # parole alfabetiche pure, con spazio iniziale (= parola in mezzo a frase)
    if s.startswith(" ") and w.isalpha() and w.islower() and len(w) >= 10:
        superwords.append(w)

superwords.sort(key=len, reverse=True)
print(f"Parole minuscole >=10 caratteri che costano 1 SOLO token: {len(superwords)}")
print("\nTop 30 piu' lunghe:")
for w in superwords[:30]:
    print(f"  {len(w):2d} ch -> 1 tok : {w}")

print()
print("=" * 70)
print("FASE 2: Test parole tecniche — quali concetti dev costano 1 token?")
print("=" * 70)
tech = ["authentication", "authorization", "implementation", "configuration",
        "validation", "middleware", "registration", "notification",
        "transaction", "deployment", "environment", "asynchronous",
        "vulnerability", "encryption", "optimization", "initialization",
        "compatibility", "documentation", "infrastructure", "functionality"]
for w in tech:
    print(f"  ' {w}' = {t(' '+w)} tok ({len(w)} ch)")

print()
print("=" * 70)
print("FASE 3: Tabella di riscrittura — frasi multi-token -> 1 parola densa")
print("=" * 70)
rewrites = [
    ("make sure that", "ensure"),
    ("in order to", "to"),
    ("at the same time", "simultaneously"),
    ("as soon as possible", "immediately"),
    ("a large number of", "many"),
    ("take into account", "consider"),
    ("with respect to", "regarding"),
    ("it is necessary to", "must"),
    ("user interface", "UI"),
    ("error handling and logging", "observability"),
]
total_before = total_after = 0
for a, b in rewrites:
    ta, tb = t(" "+a), t(" "+b)
    total_before += ta; total_after += tb
    print(f"  '{a}' ({ta}t) -> '{b}' ({tb}t)")
print(f"\n  Totale: {total_before}t -> {total_after}t = -{100-100*total_after/total_before:.0f}%")

print()
print("=" * 70)
print("FASE 4: CODEBOOK + CACHING — la matematica del 90% effettivo")
print("=" * 70)
# Idea: workflow ripetitivo (es. parser Relay). Il codebook/glossario si paga
# una volta (o costa ~0 con prompt caching). Ogni messaggio paga solo la sigla.
codebook = """CODEBOOK v1 (cached):
SIG=trading signal{pair,dir,entry,sl,tp[]}
P=parse SIG from text, output CSV: pair,dir,entry,sl,tp1,tp2,tp3
R=reject if missing entry|sl; dir in {buy,sell}"""

msg_verbose = """Please parse the following trading signal message and extract the currency pair, the direction (buy or sell), the entry price, the stop loss, and all take profit levels. Return the result as structured data. If the entry price or stop loss is missing, reject the signal."""
msg_ctp = """P+R:"""

cb, mv, mc = t(codebook), t(msg_verbose), t(msg_ctp)
print(f"  Codebook (una tantum/cached): {cb} tok")
print(f"  Istruzione verbosa per msg:   {mv} tok")
print(f"  Istruzione CTP per msg:       {mc} tok")
for n in [10, 100, 1000]:
    before = mv * n
    after = cb + mc * n   # senza caching
    after_cached = cb * 0.1 + mc * n  # caching ~90% sconto sul prefisso
    print(f"  Su {n:5d} msg: verboso={before:6d}t | CTP={after:6.0f}t (-{100-100*after/before:.0f}%) | CTP+cache={after_cached:6.0f}t (-{100-100*after_cached/before:.0f}%)")
