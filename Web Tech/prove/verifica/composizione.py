#!/usr/bin/env python3
"""Controlla che la banca regga a molte estrazioni (senza eseguire il codice).

    python verifica/composizione.py                    i controlli completi
    python verifica/composizione.py --semi 300 --prove 200     più in fretta

1. Ogni famiglia viene generata con molti semi diversi: deve produrre sempre
   una domanda valida (almeno tre distrattori, nessuna opzione ripetuta) che
   si impagina in LaTeX. Una combinazione di parametri sfortunata, che esce
   una volta su mille, farebbe fallire proprio la prova che la pesca.
2. Vengono composte molte prove, con tutti i capitoli e con alcuni
   sottoinsiemi: nessuna deve contenere due volte la stessa domanda e, con
   tutti i capitoli, dieci prove della stessa serie non devono ripetere una
   domanda fissa.

Serve solo Python 3.
"""

import argparse
import collections
import os
import random
import sys

QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(QUI))

from banca import DOMANDE                      # noqa: E402
from generatore.latex import domanda_tex       # noqa: E402
from generatore.modello import Famiglia        # noqa: E402
from generatore.selezione import SERIE, componi   # noqa: E402


def famiglie(semi):
    problemi = 0
    voci = [d for d in DOMANDE if isinstance(d, Famiglia)]
    for famiglia in voci:
        falliti = []
        for seme in range(semi):
            try:
                domanda_tex(famiglia.istanza(random.Random("composizione:%s:%d"
                                                           % (famiglia.id, seme))),
                            soluzioni=True)
            except Exception as errore:        # noqa: BLE001 (si riporta qualunque errore)
                falliti.append((seme, errore))
        if falliti:
            problemi += 1
            seme, errore = falliti[0]
            print("ERRORE %s: %d varianti su %d non valide (per esempio il seme %d: %s)"
                  % (famiglia.id, len(falliti), semi, seme, errore))
    print("Famiglie: %d, %d varianti ciascuna: %d con problemi." % (len(voci), semi, problemi))
    return problemi


def prove(quante):
    fisse = {d.id for d in DOMANDE if not isinstance(d, Famiglia)}
    tutti = sorted(c for c in {d.cap for d in DOMANDE} if c <= 16)
    prove_fatte = problemi = 0
    gruppi = [(None, quante), (tutti[:-1], quante // 4)]
    gruppi += [([c], max(SERIE, quante // 50)) for c in tutti]
    for capitoli, numero in gruppi:
        viste = collections.defaultdict(set)
        for n in range(1, numero + 1):
            prova = componi(n, DOMANDE, capitoli=capitoli)
            prove_fatte += 1
            conta = collections.Counter(i.id for i in prova.istanze)
            doppie = sorted(k for k, v in conta.items() if v > 1)
            if doppie:
                problemi += 1
                print("ERRORE prova %s (capitoli %s): domande doppie %s"
                      % (prova.id_testo, capitoli or "tutti", doppie))
            if capitoli is None:
                serie = viste[(n - 1) // SERIE]
                ripetute = sorted(i.id for i in prova.istanze if i.id in fisse and i.id in serie)
                if ripetute:
                    problemi += 1
                    print("ERRORE prova %s: già uscite nella serie %s" % (prova.id_testo, ripetute))
                serie.update(i.id for i in prova.istanze)
    print("Prove composte: %d (tutti i capitoli, senza l'ultimo, uno solo): %d problemi."
          % (prove_fatte, problemi))
    return problemi


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--semi", type=int, default=2000, help="varianti per famiglia (2000)")
    parser.add_argument("--prove", type=int, default=2000,
                        help="prove da comporre con tutti i capitoli (2000)")
    opzioni = parser.parse_args()
    problemi = famiglie(opzioni.semi) + prove(opzioni.prove)
    sys.exit(1 if problemi else 0)


if __name__ == "__main__":
    main()
