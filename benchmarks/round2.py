import tiktoken
enc = tiktoken.get_encoding("o200k_base")
def t(s): return len(enc.encode(s))

print("R1: MAIUSCOLE vs minuscole")
for a, b in [("AUTHENTICATION", "authentication"), ("ERROR HANDLING", "error handling"),
             ("IMPORTANT", "important"), ("Validation", "validation")]:
    print(f"  '{a}'={t(' '+a)}t  vs  '{b}'={t(' '+b)}t")

print("\nR2: NUMERI")
for n in ["1000000", "1,000,000", "1M", "1e6", "0.001", "1e-3", "24 hours", "24h", "8 characters", "min8"]:
    print(f"  '{n}' = {t(n)}t")

print("\nR3: DATE/TIMESTAMP")
for d in ["2026-06-11T10:30:00Z", "2026-06-11 10:30", "2026-06-11", "11/06/2026", "Jun 11", "20260611"]:
    print(f"  '{d}' = {t(d)}t")

print("\nR4: MARCATORI DI LISTA (per riga)")
for m in ["1. item", "- item", "* item", "; item", "| item", "item;"]:
    print(f"  '{m}' = {t(m)}t")

print("\nR5: NEWLINE e SPAZI")
for s, label in [("\n", "newline singolo"), ("\n\n", "doppio newline"), ("    ", "4 spazi indent"),
                 ("\t", "tab"), ("a\nb\nc", "3 righe"), ("a;b;c", "3 con ;"), ("a, b, c", "3 con , spazio"), ("a,b,c", "3 con ,")]:
    print(f"  {label!r:25s} = {t(s)}t")

print("\nR6: CHIAVI JSON corte vs lunghe (minified, 5 record)")
import json
long_k = json.dumps([{"transaction_identifier": i, "customer_full_name": f"C{i}", "total_amount_euros": i*10} for i in range(5)], separators=(',',':'))
short_k = json.dumps([{"id": i, "name": f"C{i}", "eur": i*10} for i in range(5)], separators=(',',':'))
print(f"  chiavi lunghe: {t(long_k)}t | chiavi corte: {t(short_k)}t  -> -{100-100*t(short_k)/t(long_k):.0f}%")

print("\nR7: camelCase vs snake_case vs kebab")
for s in ["getUserProfile", "get_user_profile", "get-user-profile", "getuserprofile"]:
    print(f"  '{s}' = {t(s)}t")

print("\nR8: ALTRE RISCRITTURE candidate (verifica)")
pairs = [("is able to", "can"), ("in the case of", "for"), ("a number of", "several"),
         ("at all times", "always"), ("in most cases", "usually"), ("carry out", "do"),
         ("give rise to", "cause"), ("a variety of", "various"), ("on the other hand", "however"),
         ("as a result of", "from"), ("in the absence of", "without"), ("provided that", "if"),
         ("with regard to", "re:"), ("for example", "e.g."), ("that is to say", "i.e."),
         ("and so on", "etc"), ("step by step", "stepwise"), ("if and only if", "iff")]
for a, b in pairs:
    print(f"  '{a}'({t(' '+a)}t) -> '{b}'({t(' '+b)}t)")

print("\nR9: TABELLA MARKDOWN vs lista compatta (per la skill stessa)")
table = """| Situation | Layer | Saving |
|---|---|---|
| One-shot prompt | Layer 1 | 50-70% |
| Terse accepted | Layer 1 extreme | 70-82% |
| Tabular data | Layer 2 | 45-60% |
| Recurring pipeline | Layer 3 | 90-93% |"""
compact = """one-shot->L1(50-70%); terse->L1x(70-82%); tabular data->L2(45-60%); recurring pipeline->L3(90-93%)"""
print(f"  tabella md: {t(table)}t | riga compatta: {t(compact)}t -> -{100-100*t(compact)/t(table):.0f}%")

print("\nR10: SKILL.md attuale — quanto pesa?")
with open("/home/claude/dtl/SKILL.md") as f: skill = f.read()
with open("/home/claude/dtl/references/rewrite-table.md") as f: rt = f.read()
with open("/home/claude/dtl/references/codebook-guide.md") as f: cg = f.read()
print(f"  SKILL.md: {t(skill)}t | rewrite-table: {t(rt)}t | codebook-guide: {t(cg)}t | TOT: {t(skill)+t(rt)+t(cg)}t")
