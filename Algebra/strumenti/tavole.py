"""Genera le tavole di verità (LaTeX) e le sostituisce nei template dei capitoli.

Uso: python3 tavole.py <template> <output>
Nel template, ogni segnaposto <<TAB:nome>> viene sostituito con la tavola `nome`.
"""
import itertools
import re
import sys

NOT = lambda a: not a
AND = lambda a, b: a and b
OR = lambda a, b: a or b
IMP = lambda a, b: (not a) or b
IFF = lambda a, b: a == b
XOR = lambda a, b: a != b
NAND = lambda a, b: not (a and b)
NOR = lambda a, b: not (a or b)

# Ogni tavola: (variabili, [(intestazione, funzione, evidenziata)])
T = {}


def tab(nome, variabili, colonne):
    T[nome] = (variabili, colonne)


# --- Connettivi fondamentali ---------------------------------------------
tab("not", "p", [(r"\neg p", lambda p: NOT(p), False)])
tab("binari", "pq", [
    (r"p \wedge q", lambda p, q: AND(p, q), False),
    (r"p \vee q", lambda p, q: OR(p, q), False),
    (r"p \rightarrow q", lambda p, q: IMP(p, q), False),
    (r"p \leftrightarrow q", lambda p, q: IFF(p, q), False),
])

# --- Tautologie notevoli --------------------------------------------------
tab("doppianeg", "p", [
    (r"\neg p", lambda p: NOT(p), False),
    (r"\neg(\neg p)", lambda p: NOT(NOT(p)), False),
    (r"\neg(\neg p) \leftrightarrow p", lambda p: IFF(NOT(NOT(p)), p), True),
])
tab("idempotenza", "p", [
    (r"p \wedge p", lambda p: AND(p, p), False),
    (r"p \vee p", lambda p: OR(p, p), False),
    (r"(p \wedge p) \leftrightarrow p", lambda p: IFF(AND(p, p), p), True),
    (r"(p \vee p) \leftrightarrow p", lambda p: IFF(OR(p, p), p), True),
])
tab("terzoescluso", "p", [
    (r"\neg p", lambda p: NOT(p), False),
    (r"p \vee \neg p", lambda p: OR(p, NOT(p)), True),
])
tab("noncontraddizione", "p", [
    (r"\neg p", lambda p: NOT(p), False),
    (r"p \wedge \neg p", lambda p: AND(p, NOT(p)), False),
    (r"\neg(p \wedge \neg p)", lambda p: NOT(AND(p, NOT(p))), True),
])
tab("commutativita", "pq", [
    (r"p \wedge q", lambda p, q: AND(p, q), 1),
    (r"q \wedge p", lambda p, q: AND(q, p), 1),
    (r"p \vee q", lambda p, q: OR(p, q), 2),
    (r"q \vee p", lambda p, q: OR(q, p), 2),
    (r"p \leftrightarrow q", lambda p, q: IFF(p, q), 3),
    (r"q \leftrightarrow p", lambda p, q: IFF(q, p), 3),
])
tab("noncommimp", "pq", [
    (r"p \rightarrow q", lambda p, q: IMP(p, q), False),
    (r"q \rightarrow p", lambda p, q: IMP(q, p), False),
    (r"(p \rightarrow q) \leftrightarrow (q \rightarrow p)",
     lambda p, q: IFF(IMP(p, q), IMP(q, p)), True),
])
tab("assocand", "pqr", [
    (r"p \wedge q", lambda p, q, r: AND(p, q), False),
    (r"(p \wedge q) \wedge r", lambda p, q, r: AND(AND(p, q), r), True),
    (r"q \wedge r", lambda p, q, r: AND(q, r), False),
    (r"p \wedge (q \wedge r)", lambda p, q, r: AND(p, AND(q, r)), True),
])
tab("assocor", "pqr", [
    (r"p \vee q", lambda p, q, r: OR(p, q), False),
    (r"(p \vee q) \vee r", lambda p, q, r: OR(OR(p, q), r), True),
    (r"q \vee r", lambda p, q, r: OR(q, r), False),
    (r"p \vee (q \vee r)", lambda p, q, r: OR(p, OR(q, r)), True),
])
tab("distr1", "pqr", [
    (r"q \vee r", lambda p, q, r: OR(q, r), False),
    (r"p \wedge (q \vee r)", lambda p, q, r: AND(p, OR(q, r)), True),
    (r"p \wedge q", lambda p, q, r: AND(p, q), False),
    (r"p \wedge r", lambda p, q, r: AND(p, r), False),
    (r"(p \wedge q) \vee (p \wedge r)", lambda p, q, r: OR(AND(p, q), AND(p, r)), True),
])
tab("distr2", "pqr", [
    (r"q \wedge r", lambda p, q, r: AND(q, r), False),
    (r"p \vee (q \wedge r)", lambda p, q, r: OR(p, AND(q, r)), True),
    (r"p \vee q", lambda p, q, r: OR(p, q), False),
    (r"p \vee r", lambda p, q, r: OR(p, r), False),
    (r"(p \vee q) \wedge (p \vee r)", lambda p, q, r: AND(OR(p, q), OR(p, r)), True),
])
tab("demorgan1", "pq", [
    (r"p \vee q", lambda p, q: OR(p, q), False),
    (r"\neg(p \vee q)", lambda p, q: NOT(OR(p, q)), True),
    (r"\neg p", lambda p, q: NOT(p), False),
    (r"\neg q", lambda p, q: NOT(q), False),
    (r"\neg p \wedge \neg q", lambda p, q: AND(NOT(p), NOT(q)), True),
])
tab("demorgan2", "pq", [
    (r"p \wedge q", lambda p, q: AND(p, q), False),
    (r"\neg(p \wedge q)", lambda p, q: NOT(AND(p, q)), True),
    (r"\neg p", lambda p, q: NOT(p), False),
    (r"\neg q", lambda p, q: NOT(q), False),
    (r"\neg p \vee \neg q", lambda p, q: OR(NOT(p), NOT(q)), True),
])
tab("impor", "pq", [
    (r"p \rightarrow q", lambda p, q: IMP(p, q), True),
    (r"\neg p", lambda p, q: NOT(p), False),
    (r"\neg p \vee q", lambda p, q: OR(NOT(p), q), True),
])
tab("contrapposizione", "pq", [
    (r"p \rightarrow q", lambda p, q: IMP(p, q), True),
    (r"\neg q", lambda p, q: NOT(q), False),
    (r"\neg p", lambda p, q: NOT(p), False),
    (r"\neg q \rightarrow \neg p", lambda p, q: IMP(NOT(q), NOT(p)), True),
])
tab("negimp", "pq", [
    (r"p \rightarrow q", lambda p, q: IMP(p, q), False),
    (r"\neg(p \rightarrow q)", lambda p, q: NOT(IMP(p, q)), True),
    (r"\neg q", lambda p, q: NOT(q), False),
    (r"p \wedge \neg q", lambda p, q: AND(p, NOT(q)), True),
])
tab("doppiaimp", "pq", [
    (r"p \leftrightarrow q", lambda p, q: IFF(p, q), True),
    (r"p \rightarrow q", lambda p, q: IMP(p, q), False),
    (r"q \rightarrow p", lambda p, q: IMP(q, p), False),
    (r"(p \rightarrow q) \wedge (q \rightarrow p)",
     lambda p, q: AND(IMP(p, q), IMP(q, p)), True),
])
tab("negdoppiaimp", "pq", [
    (r"p \leftrightarrow q", lambda p, q: IFF(p, q), True),
    (r"\neg p", lambda p, q: NOT(p), False),
    (r"\neg q", lambda p, q: NOT(q), False),
    (r"\neg p \leftrightarrow \neg q", lambda p, q: IFF(NOT(p), NOT(q)), True),
])

# --- Altri connettivi -----------------------------------------------------
tab("xornandnor", "pq", [
    (r"p \XOR q", lambda p, q: XOR(p, q), False),
    (r"p \NAND q", lambda p, q: NAND(p, q), False),
    (r"p \NOR q", lambda p, q: NOR(p, q), False),
])
tab("xoriff", "pq", [
    (r"p \XOR q", lambda p, q: XOR(p, q), True),
    (r"p \leftrightarrow q", lambda p, q: IFF(p, q), False),
    (r"\neg(p \leftrightarrow q)", lambda p, q: NOT(IFF(p, q)), True),
])
tab("xorespl1", "pq", [
    (r"p \XOR q", lambda p, q: XOR(p, q), True),
    (r"p \wedge \neg q", lambda p, q: AND(p, NOT(q)), False),
    (r"q \wedge \neg p", lambda p, q: AND(q, NOT(p)), False),
    (r"(p \wedge \neg q) \vee (q \wedge \neg p)",
     lambda p, q: OR(AND(p, NOT(q)), AND(q, NOT(p))), True),
])
tab("xorespl2", "pq", [
    (r"p \XOR q", lambda p, q: XOR(p, q), True),
    (r"p \vee q", lambda p, q: OR(p, q), False),
    (r"\neg(p \wedge q)", lambda p, q: NOT(AND(p, q)), False),
    (r"(p \vee q) \wedge \neg(p \wedge q)",
     lambda p, q: AND(OR(p, q), NOT(AND(p, q))), True),
])
tab("xorcomm", "pq", [
    (r"p \XOR q", lambda p, q: XOR(p, q), True),
    (r"q \XOR p", lambda p, q: XOR(q, p), True),
])
tab("xorassoc", "pqr", [
    (r"p \XOR q", lambda p, q, r: XOR(p, q), False),
    (r"(p \XOR q) \XOR r", lambda p, q, r: XOR(XOR(p, q), r), True),
    (r"q \XOR r", lambda p, q, r: XOR(q, r), False),
    (r"p \XOR (q \XOR r)", lambda p, q, r: XOR(p, XOR(q, r)), True),
])
tab("riduzioninot", "p", [
    (r"\neg p", lambda p: NOT(p), True),
    (r"p \NAND p", lambda p: NAND(p, p), True),
    (r"p \NOR p", lambda p: NOR(p, p), True),
])
tab("riduzioniand", "pq", [
    (r"p \wedge q", lambda p, q: AND(p, q), 1),
    (r"\neg(p \NAND q)", lambda p, q: NOT(NAND(p, q)), 1),
    (r"p \NAND q", lambda p, q: NAND(p, q), 2),
    (r"\neg(p \wedge q)", lambda p, q: NOT(AND(p, q)), 2),
])
tab("riduzionior", "pq", [
    (r"p \vee q", lambda p, q: OR(p, q), 1),
    (r"\neg(p \NOR q)", lambda p, q: NOT(NOR(p, q)), 1),
    (r"p \NOR q", lambda p, q: NOR(p, q), 2),
    (r"\neg(p \vee q)", lambda p, q: NOT(OR(p, q)), 2),
])

# --- Teoria degli insiemi ---------------------------------------------------
tab("inclusione", "pq", [
    (r"p \rightarrow q", lambda p, q: IMP(p, q), 1),
    (r"(p \wedge q) \leftrightarrow p", lambda p, q: IFF(AND(p, q), p), 1),
    (r"(p \vee q) \leftrightarrow q", lambda p, q: IFF(OR(p, q), q), 1),
    (r"\neg(p \wedge \neg q)", lambda p, q: NOT(AND(p, NOT(q))), 1),
    (r"(p \XOR q) \leftrightarrow (q \wedge \neg p)", lambda p, q: IFF(XOR(p, q), AND(q, NOT(p))), 1),
])
tab("distrxor", "pqr", [
    (r"q \XOR r", lambda p, q, r: XOR(q, r), 0),
    (r"p \wedge (q \XOR r)", lambda p, q, r: AND(p, XOR(q, r)), 1),
    (r"p \wedge q", lambda p, q, r: AND(p, q), 0),
    (r"p \wedge r", lambda p, q, r: AND(p, r), 0),
    (r"(p \wedge q) \XOR (p \wedge r)", lambda p, q, r: XOR(AND(p, q), AND(p, r)), 1),
])


def valore(b):
    return r"$\vero$" if b else r"$\falso$"


def latex(nome):
    variabili, colonne = T[nome]
    tipo = {0: "c", 1: "T", 2: "U", 3: "K"}   # 0 = normale, 1/True, 2, 3 = gruppi da confrontare
    spec = "c" * len(variabili) + "|" + "".join(tipo[int(ev)] for _, _, ev in colonne)
    righe = [r"\begin{tavola}{" + spec + "}"]
    intest = " & ".join(f"${v}$" for v in variabili) + " & " + " & ".join(f"${h}$" for h, _, _ in colonne)
    righe.append(r"  \intestazione " + intest + r" \\ \hline")
    # ordine delle righe come negli appunti: V prima di F
    for combo in itertools.product([True, False], repeat=len(variabili)):
        celle = [valore(b) for b in combo] + [valore(f(*combo)) for _, f, _ in colonne]
        righe.append("  " + " & ".join(celle) + r" \\")
    righe.append(r"\end{tavola}")
    return "\n".join(righe)


def verifica():
    """Controlla che le colonne evidenziate delle tautologie siano come atteso."""
    tautologie = ["doppianeg", "idempotenza", "terzoescluso", "noncontraddizione"]
    for nome in tautologie:
        variabili, colonne = T[nome]
        ultima = colonne[-1][1]
        assert all(ultima(*c) for c in itertools.product([True, False], repeat=len(variabili))), nome
    # le coppie evidenziate devono coincidere riga per riga
    coppie = ["assocand", "assocor", "distr1", "distr2", "demorgan1", "demorgan2", "impor",
              "contrapposizione", "negimp", "doppiaimp", "negdoppiaimp", "xoriff", "xorespl1",
              "xorespl2", "xorcomm", "xorassoc", "riduzioninot", "riduzioniand", "riduzionior",
              "commutativita", "inclusione", "distrxor"]
    for nome in coppie:
        variabili, colonne = T[nome]
        for gruppo in (1, 2, 3):
            ev = [f for _, f, e in colonne if int(e) == gruppo]
            for c in itertools.product([True, False], repeat=len(variabili)):
                assert len({f(*c) for f in ev}) <= 1, (nome, gruppo)
    # (p -> q) <-> (q -> p) NON è una tautologia
    assert not all(IFF(IMP(p, q), IMP(q, p)) for p, q in itertools.product([True, False], repeat=2))


if __name__ == "__main__":
    verifica()
    testo = open(sys.argv[1], encoding="utf-8").read()
    usate = set()

    def sostituisci(m):
        usate.add(m.group(1))
        return latex(m.group(1))

    testo = re.sub(r"<<TAB:([a-z0-9]+)>>", sostituisci, testo)
    open(sys.argv[2], "w", encoding="utf-8").write(testo)
    print("tavole inserite:", ", ".join(sorted(usate)))
