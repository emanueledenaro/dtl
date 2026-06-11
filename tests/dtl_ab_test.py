#!/usr/bin/env python3
"""DTL A/B test harness — runs on Claude Code subscription (claude -p), no API key.

Usage:
  python3 dtl_ab_test.py            # run all test cases
  python3 dtl_ab_test.py --quick    # first case only

Requires: claude CLI installed and logged in (Max plan). Results in ./dtl_results/
"""
import subprocess, json, os, sys, time

# ----- test cases: (name, verbose prompt, DTL prompt) — add yours freely -----
CASES = [
("react_form",
"""Ciao! Avrei bisogno che tu creassi un componente React con TypeScript per un form di login. Il form dovrebbe avere un campo per l'email e uno per la password. Vorrei che la validazione avvenisse in tempo reale: l'email deve essere un'email valida e la password deve avere almeno 8 caratteri. Quando l'utente invia il form, dovrebbe essere chiamata una funzione onSubmit passata come prop. Per favore mostra anche i messaggi di errore sotto ogni campo. Grazie mille!""",
"""react+ts login form component:
- fields: email,password
- realtime validation: valid email; password >=8 chars
- errors shown under each field
- submit -> call onSubmit prop
Output: code only."""),

("sql_query",
"""Avrei bisogno del tuo aiuto per scrivere una query SQL per PostgreSQL. Ho una tabella chiamata orders con le colonne id, customer_id, total, created_at, e una tabella customers con id, name, country. Quello che vorrei ottenere è il fatturato totale per paese negli ultimi 30 giorni, ma solamente per i paesi che hanno generato più di 10000 euro, ordinato dal fatturato più alto al più basso. Grazie!""",
"""postgresql query:
tables: orders(id,customer_id,total,created_at), customers(id,name,country)
revenue per country, last 30 days, having >10000, order desc
Output: sql only."""),

("bug_explain",
"""Ciao Claude, ho un problema con il mio codice Python e speravo potessi aiutarmi a capire cosa non va. Ho una funzione che dovrebbe rimuovere i duplicati da una lista mantenendo l'ordine originale degli elementi, ma per qualche motivo a volte l'ordine cambia. Sto usando list(set(my_list)). Potresti spiegarmi perché succede e come posso risolvere il problema? Grazie in anticipo!""",
"""python: list(set(my_list)) used to dedupe but order changes. why + fix preserving order.
Output: <=4 sentences + code."""),
]

JUDGE_TMPL = """Compare two AI responses to the same underlying task. Score functional equivalence 0-10 (10 = fully equivalent quality/correctness). Output ONLY json: {{"score": n, "reason": "<15 words"}}

TASK: {task}
RESPONSE A:
{a}
RESPONSE B:
{b}"""

def run_claude(prompt):
    t0 = time.time()
    r = subprocess.run(["claude", "-p", prompt], capture_output=True, text=True, timeout=300)
    return r.stdout.strip(), time.time() - t0

def main():
    cases = CASES[:1] if "--quick" in sys.argv else CASES
    os.makedirs("dtl_results", exist_ok=True)
    report = []
    for name, verbose, dtl in cases:
        print(f"\n=== {name} ===")
        cv, ch = len(verbose), len(dtl)
        print(f"prompt chars: verbose={cv} dtl={ch} (-{100-100*ch/cv:.0f}%, ~token proxy)")
        print("running verbose...", end=" ", flush=True)
        out_v, tv = run_claude(verbose); print(f"{tv:.0f}s")
        print("running dtl...", end=" ", flush=True)
        out_d, td = run_claude(dtl); print(f"{td:.0f}s")
        print("judging...", end=" ", flush=True)
        judge, _ = run_claude(JUDGE_TMPL.format(task=name, a=out_v, b=out_d))
        print(judge)
        with open(f"dtl_results/{name}.md", "w") as f:
            f.write(f"# {name}\n\n## verbose prompt ({cv} ch)\n{verbose}\n\n## dtl prompt ({ch} ch)\n{dtl}\n\n"
                    f"## verbose output\n{out_v}\n\n## dtl output\n{out_d}\n\n## judge\n{judge}\n")
        report.append((name, cv, ch, judge))
    print("\n" + "="*50 + "\nSUMMARY")
    for name, cv, ch, judge in report:
        print(f"  {name}: prompt -{100-100*ch/cv:.0f}% | judge: {judge[:80]}")
    print("\ndetails in ./dtl_results/  — equivalence score >=8 means DTL holds quality.")

if __name__ == "__main__":
    main()
