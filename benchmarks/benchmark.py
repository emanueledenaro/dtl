import tiktoken

# o200k_base = tokenizer GPT-4o/o1, buon proxy moderno (Anthropic non pubblica il suo,
# ma i BPE moderni si comportano in modo simile: favoriscono inglese comune)
enc = tiktoken.get_encoding("o200k_base")

def t(s): return len(enc.encode(s))

print("=" * 70)
print("TEST 1: Stessa istruzione, stili diversi")
print("=" * 70)

samples = {
    "Italiano verboso (come scriviamo di solito)": 
        """Per favore, potresti analizzare attentamente il seguente codice e verificare se ci sono eventuali problemi di sicurezza? In particolare vorrei che controllassi le query SQL per possibili SQL injection, la gestione dell'autenticazione degli utenti e la validazione degli input. Grazie mille!""",

    "Inglese verboso":
        """Please carefully analyze the following code and check whether there are any security issues. In particular I would like you to check the SQL queries for possible SQL injection, the user authentication handling, and input validation. Thank you!""",

    "Inglese telegrafico (stop words rimosse)":
        """Analyze code for security issues: SQL injection in queries, auth handling, input validation.""",

    "Simbolico/matematico ('linguaggio inventato')":
        """∀q∈SQL: chk(inj); chk(auth∧validate(input)) → report(sec_issues)""",

    "Abbreviazioni estreme":
        """anlz cd sec: sqli, auth, inp vld""",
}

base = None
for name, text in samples.items():
    n = t(text)
    if base is None: base = n
    print(f"{n:5d} tok ({100*n/base:5.1f}%)  chars={len(text):4d}  ratio chars/tok={len(text)/n:.2f}  | {name}")

print()
print("=" * 70)
print("TEST 2: Il caso simboli Unicode — sembrano corti ma...")
print("=" * 70)

pairs = [
    ("for each user check email", "∀u∈U: ✓(u.email)"),
    ("if error then retry max 3 times", "err→retry(≤3)"),
    ("function returns list of active users", "f()→[u|u.active]"),
]
for plain, sym in pairs:
    print(f"  '{plain}'  = {t(plain)} tok ({len(plain)} ch)")
    print(f"  '{sym}'  = {t(sym)} tok ({len(sym)} ch)   <- simbolico")
    print()

print("=" * 70)
print("TEST 3: Dati strutturati — JSON vs CSV vs TOON-style")
print("=" * 70)

json_data = '''{"users":[{"id":1,"name":"Marco","role":"admin","active":true},{"id":2,"name":"Lucia","role":"editor","active":true},{"id":3,"name":"Paolo","role":"viewer","active":false},{"id":4,"name":"Anna","role":"editor","active":true},{"id":5,"name":"Luca","role":"admin","active":false}]}'''

csv_data = '''id,name,role,active
1,Marco,admin,true
2,Lucia,editor,true
3,Paolo,viewer,false
4,Anna,editor,true
5,Luca,admin,false'''

toon_data = '''users[5]{id,name,role,active}:
1,Marco,admin,true
2,Lucia,editor,true
3,Paolo,viewer,false
4,Anna,editor,true
5,Luca,admin,false'''

for name, d in [("JSON", json_data), ("CSV", csv_data), ("TOON", toon_data)]:
    print(f"  {name}: {t(d)} tok ({len(d)} chars)")

print()
print("=" * 70)
print("TEST 4: Lingua conta? Italiano vs Inglese, stesso contenuto tecnico")
print("=" * 70)

it = "Crea un componente React con un form di registrazione che valida email e password, mostra errori in tempo reale e invia i dati a un endpoint API."
en = "Create a React component with a registration form that validates email and password, shows real-time errors, and sends data to an API endpoint."
en_compact = "React component: registration form, validate email+password, realtime errors, POST to API."

print(f"  Italiano:        {t(it)} tok")
print(f"  Inglese:         {t(en)} tok")
print(f"  Inglese compatto: {t(en_compact)} tok")
