# DTL rewrite table — verified 1t targets (o200k_base)

## Phrase -> dense word
make sure that->ensure; in order to->to; at the same time->simultaneously; as soon as possible->immediately; a large number of->many; take into account->consider; with respect to->regarding; it is necessary to->must; in the event that->if; due to the fact that->because; has the ability to->can; is able to->can; at this point in time->now; in the near future->soon; on a regular basis->regularly; prior to->before; subsequent to->after; with the exception of->except; in addition to->plus; for the purpose of->for; in spite of the fact that->despite; user interface->UI; as well as->and; each and every->every; whether or not->whether; in the case of->for; a number of->several; at all times->always; in most cases->usually; carry out->do; give rise to->cause; a variety of->various; on the other hand->however; as a result of->from; in the absence of->without; provided that->if; and so on->etc; if and only if->iff

## Traps (compressed form costs MORE — avoid)
e.g.(3t) > for example(2t); i.e.(3t) > that is(2t); 1e6(3t) > 1M(2t); 1,000,000(5t) > 1000000(3t); CAPS = 3x lowercase

## Single-token superwords (use freely, never shorten)
authentication authorization implementation configuration validation middleware registration notification transaction deployment environment asynchronous vulnerability encryption optimization initialization compatibility documentation infrastructure functionality responsibilities simultaneously automatically immediately independently significantly approximately specifically

## Operators, all 1t (ascii only)
-> (then/returns) => (maps to) | (or) & (and) + (with) != <= >= : (define) ? (optional) ! (required/not)
FORBIDDEN 2-3t: ∀ ∈ ∧ ∨ ≠ ✓ ⇒ + any unicode math/arrow

## Structure patterns
- requirement rows: "- item (constraints)" — dash not number (saves 1t/row)
- stack once, first line: "Next.js 14 + TS + Supabase/PG."
- conditions: "if X -> Y" / "on err -> retry(<=3)"
- inline lists: a,b,c (no space after comma)
- output suffix: "Output: <shape>. No explanation."
