#!/usr/bin/env python3
"""DTL A/B v2 — extreme mode vs verbose. Multi-run, averaged blind-judge scores.
Runs on Claude Code subscription (claude -p), no API key.

Usage: python3 dtl_ab_test_v2.py            # 2 runs/case (12 resp + 6 judge = 18 calls)
       python3 dtl_ab_test_v2.py --runs 3   # 3 runs/case (27 calls)
       python3 dtl_ab_test_v2.py --quick    # case 1 only
"""
import subprocess, os, sys, time, re, statistics, tempfile

CASES = [
("react_form",
"""Ciao! Avrei bisogno che tu creassi un componente React con TypeScript per un form di login. Il form dovrebbe avere un campo per l'email e uno per la password. Vorrei che la validazione avvenisse in tempo reale: l'email deve essere un'email valida e la password deve avere almeno 8 caratteri. Quando l'utente invia il form, dovrebbe essere chiamata una funzione onSubmit passata come prop. Per favore mostra anche i messaggi di errore sotto ogni campo. Grazie mille!""",
"""react+ts login: email+password fields, realtime validation(valid email,password>=8), errors under fields, submit->onSubmit prop. code only."""),
("sql_query",
"""Avrei bisogno del tuo aiuto per scrivere una query SQL per PostgreSQL. Ho una tabella chiamata orders con le colonne id, customer_id, total, created_at, e una tabella customers con id, name, country. Quello che vorrei ottenere è il fatturato totale per paese negli ultimi 30 giorni, ma solamente per i paesi che hanno generato più di 10000 euro, ordinato dal fatturato più alto al più basso. Grazie!""",
"""postgresql: orders(id,customer_id,total,created_at)+customers(id,name,country). revenue/country last 30d having>10000 desc. sql only."""),
("bug_explain",
"""Ciao Claude, ho un problema con il mio codice Python e speravo potessi aiutarmi a capire cosa non va. Ho una funzione che dovrebbe rimuovere i duplicati da una lista mantenendo l'ordine originale degli elementi, ma per qualche motivo a volte l'ordine cambia. Sto usando list(set(my_list)). Potresti spiegarmi perché succede e come posso risolvere il problema? Grazie in anticipo!""",
"""python list(set(x)) dedupe changes order: why+fix preserving order. <=4 sentences+code. Output language: it."""),
]

JUDGE = """Compare two AI responses to the same underlying task. Score functional equivalence 0-10 (10 = fully equivalent quality/correctness; ignore verbosity/style/language differences if information matches). Output ONLY json: {{"score": n, "reason": "<15 words"}}

TASK: {task}
RESPONSE A:
{a}
RESPONSE B:
{b}"""

def cl(prompt):
    # isolated empty cwd per call: prevents cross-run file contamination (lesson from v2 run 1)
    with tempfile.TemporaryDirectory() as d:
        r = subprocess.run(["claude","-p",prompt], capture_output=True, text=True, timeout=300, cwd=d)
    return r.stdout.strip()

def main():
    runs = 3 if "--runs" in sys.argv and "3" in sys.argv else 2
    cases = CASES[:1] if "--quick" in sys.argv else CASES
    os.makedirs("dtl_results_v2", exist_ok=True)
    summary = []
    for name, verbose, extreme in cases:
        scores = []
        print(f"\n=== {name} (x{runs} run) ===")
        for r in range(runs):
            print(f"  run {r+1}: verbose...", end=" ", flush=True); ov = cl(verbose)
            print("extreme...", end=" ", flush=True); oe = cl(extreme)
            print("judge...", end=" ", flush=True); j = cl(JUDGE.format(task=name, a=ov, b=oe))
            m = re.search(r'"score"\s*:\s*(\d+)', j)
            s = int(m.group(1)) if m else -1
            scores.append(s); print(f"score={s}")
            with open(f"dtl_results_v2/{name}_run{r+1}.md","w") as f:
                f.write(f"# {name} run{r+1}\n\n## verbose out\n{ov}\n\n## extreme out\n{oe}\n\n## judge\n{j}\n")
            if name == "bug_explain":
                it = any(w in oe.lower() for w in ["perché","ordine","perche","insieme","mantiene"])
                print(f"    lingua output extreme = {'ITALIANO ok' if it else 'NON italiano — regola lingua FALLITA'}")
        avg = statistics.mean([s for s in scores if s>=0])
        summary.append((name, scores, avg))
    print("\n" + "="*50 + "\nSUMMARY (extreme mode)")
    for name, scores, avg in summary:
        print(f"  {name}: runs={scores} avg={avg:.1f} {'PASS' if avg>=8 else 'FAIL — extreme troppo aggressivo qui'}")
    ok = all(avg >= 8 for _,_,avg in summary)
    print(f"\nverdetto: {'EXTREME VALIDATO (tutti avg>=8)' if ok else 'NON validato: almeno un caso <8'} — dettagli: ./dtl_results_v2/")

if __name__ == "__main__":
    main()
