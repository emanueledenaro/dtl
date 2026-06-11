import tiktoken
enc = tiktoken.get_encoding("o200k_base")
def t(s): return len(enc.encode(s))

print("=" * 70)
print("TEST A: Simboli ASCII vs Unicode (per scegliere l'alfabeto del CTP)")
print("=" * 70)
syms = ["->", "→", "=>", ">>", "&", "∧", "+", "!", "≠", "!=", "<=", "≤", "|", "@", "#"]
for s in syms:
    print(f"  '{s}' = {t(s)} tok")

print()
print("=" * 70)
print("TEST B: Prompt realistico VERBOSO -> compressione massima")
print("=" * 70)

# Prompt tipico verboso che uno svilupperebbe scriverebbe
verbose = """Ciao! Avrei bisogno del tuo aiuto per un progetto su cui sto lavorando. Si tratta di un'applicazione web sviluppata con Next.js 14 e TypeScript. Quello che vorrei fare è creare un sistema di autenticazione completo che includa le seguenti funzionalità:

1. Registrazione degli utenti con email e password, dove la password deve essere lunga almeno 8 caratteri e contenere almeno una lettera maiuscola, una minuscola, un numero e un carattere speciale.
2. Login degli utenti con gestione della sessione tramite JWT token, che dovrebbe scadere dopo 24 ore.
3. Funzionalità di recupero password tramite email, con un link che scade dopo 1 ora.
4. Protezione delle route private, in modo che gli utenti non autenticati vengano reindirizzati alla pagina di login.
5. Middleware per la validazione del token su tutte le richieste API.

Per il database sto usando Supabase con PostgreSQL. Vorrei che il codice fosse ben organizzato, con una chiara separazione delle responsabilità, e che includesse anche la gestione degli errori appropriata. Inoltre, sarebbe fantastico se potessi aggiungere anche dei commenti esplicativi nel codice per aiutarmi a capire meglio come funziona ogni parte.

Potresti anche assicurarti che il codice segua le best practice di sicurezza più recenti? Grazie mille in anticipo per il tuo aiuto!"""

# Compressione MASSIMA (regole CTP estreme)
ctp_max = """Next.js 14 + TS + Supabase/PG. Build full auth:
1. signup email+pwd (min8, 1 upper+lower+digit+special)
2. login, JWT session, exp 24h
3. pwd reset via email link, exp 1h
4. protect private routes -> redirect /login
5. API middleware: validate token
Clean separation, error handling, comments, security best practices."""

# Compressione ESTREMA (lossy borderline)
ctp_extreme = """nextjs14+ts+supabase auth: signup(email,pwd:min8+complex), login(jwt,24h), reset(email-link,1h), route-guard->login, api-mw(validate-jwt). clean+err-handling+comments+sec-bp"""

v, m, e = t(verbose), t(ctp_max), t(ctp_extreme)
print(f"  Verboso italiano:    {v} tok (100%)")
print(f"  CTP massimo:         {m} tok ({100*m/v:.0f}%)  -> risparmio {100-100*m/v:.0f}%")
print(f"  CTP estremo:         {e} tok ({100*e/v:.0f}%)  -> risparmio {100-100*e/v:.0f}%")

print()
print("=" * 70)
print("TEST C: Prompt GIA' scritto in modo decente (caso peggiore per noi)")
print("=" * 70)

decent = """Create a Next.js 14 TypeScript auth system with Supabase: signup with email/password validation (min 8 chars, mixed case, number, special char), JWT login with 24h expiry, password reset via email with 1h link expiry, protected routes redirecting to login, and API middleware for token validation. Include error handling and security best practices."""

d = t(decent)
dc = t(ctp_extreme)
print(f"  Prompt gia' decente: {d} tok")
print(f"  CTP estremo:         {dc} tok -> risparmio {100-100*dc/d:.0f}%")

print()
print("=" * 70)
print("TEST D: Dati ripetitivi (caso MIGLIORE - qui il 90% e' possibile)")
print("=" * 70)

import json
# 20 record stile API response
records = [{"transaction_id": f"TXN-2026-{i:05d}", "customer_name": f"Customer {i}", 
            "amount_eur": round(100+i*7.33, 2), "status": "completed" if i%3 else "pending",
            "created_at": f"2026-06-{(i%28)+1:02d}T10:30:00Z"} for i in range(1, 21)]
json_pretty = json.dumps({"transactions": records}, indent=2)
json_min = json.dumps({"transactions": records}, separators=(',',':'))
csv_rows = "id,customer,eur,status,date\n" + "\n".join(
    f"TXN-2026-{i:05d},Customer {i},{round(100+i*7.33,2)},{'completed' if i%3 else 'pending'},2026-06-{(i%28)+1:02d}" 
    for i in range(1, 21))

jp, jm, cv = t(json_pretty), t(json_min), t(csv_rows)
print(f"  JSON pretty:   {jp} tok (100%)")
print(f"  JSON minified: {jm} tok ({100*jm/jp:.0f}%)")
print(f"  CSV compatto:  {cv} tok ({100*cv/jp:.0f}%)  -> risparmio {100-100*cv/jp:.0f}%")
