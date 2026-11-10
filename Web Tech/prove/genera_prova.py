#!/usr/bin/env python3
"""Genera prove di Tecnologie Web nello stile delle prove intercorso.

Esempi:

    python genera_prova.py                  una prova a caso, con le soluzioni
    python genera_prova.py --id 7           la prova numero 7 (sempre la stessa)
    python genera_prova.py --id 1 --quante 10    le prove da 1 a 10
    python genera_prova.py --capitoli 5-8   solo JavaScript
    python genera_prova.py --elenco         che cosa contiene la banca
    python genera_prova.py --raccolta       tutte le domande, con le soluzioni

Serve Python 3 (nessun pacchetto aggiuntivo). Per ottenere i PDF serve pdfLaTeX
(MiKTeX o TeX Live); senza, restano i file .tex da compilare altrove, per
esempio su Overleaf.
"""

import argparse
import os
import random
import shutil
import subprocess
import sys
import tempfile

QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, QUI)

from banca import DOMANDE                                           # noqa: E402
from generatore.latex import prova_tex, raccolta_tex                # noqa: E402
from generatore.modello import Famiglia                             # noqa: E402
from generatore.selezione import SERIE, TITOLI, componi             # noqa: E402


def leggi_capitoli(testo):
    """'1-4,7,9-11' -> [1, 2, 3, 4, 7, 9, 10, 11]"""
    capitoli = set()
    for parte in testo.split(","):
        parte = parte.strip()
        if "-" in parte:
            da, a = parte.split("-", 1)
            capitoli.update(range(int(da), int(a) + 1))
        elif parte:
            capitoli.add(int(parte))
    presenti = {d.cap for d in DOMANDE}
    assenti = sorted(capitoli - presenti)
    if assenti:
        raise SystemExit("Nella banca non ci sono domande per i capitoli: %s" % assenti)
    return sorted(capitoli)


def compila(sorgente, destinazione, tieni_tex=False, solo_tex=False):
    """Scrive il .tex e, se c'è pdfLaTeX, lo compila. Restituisce il file prodotto."""
    radice = os.path.splitext(destinazione)[0]
    pdflatex = None if solo_tex else shutil.which("pdflatex")
    if pdflatex is None:
        with open(radice + ".tex", "w", encoding="utf-8") as f:
            f.write(sorgente)
        return radice + ".tex"
    with tempfile.TemporaryDirectory() as lavoro:
        with open(os.path.join(lavoro, "prova.tex"), "w", encoding="utf-8") as f:
            f.write(sorgente)
        esito = subprocess.run(
            [pdflatex, "-interaction=nonstopmode", "-halt-on-error", "prova.tex"],
            cwd=lavoro, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        if esito.returncode != 0 or not os.path.exists(os.path.join(lavoro, "prova.pdf")):
            with open(radice + ".tex", "w", encoding="utf-8") as f:
                f.write(sorgente)
            testo = esito.stdout.decode("utf-8", "replace")
            errori = [r for r in testo.splitlines() if r.startswith("!") or r.startswith("l.")]
            raise SystemExit("pdfLaTeX si è fermato su %s.tex:\n  %s"
                             % (radice, "\n  ".join(errori[:6]) or testo[-600:]))
        shutil.copyfile(os.path.join(lavoro, "prova.pdf"), radice + ".pdf")
    if tieni_tex:
        with open(radice + ".tex", "w", encoding="utf-8") as f:
            f.write(sorgente)
    return radice + ".pdf"


def elenco():
    print("Banca delle domande: %d voci\n" % len(DOMANDE))
    print("%-4s %-34s %7s %9s %7s" % ("cap.", "titolo", "chiuse", "famiglie", "aperte"))
    totali = [0, 0, 0]
    for cap in sorted({d.cap for d in DOMANDE}):
        voci = [d for d in DOMANDE if d.cap == cap]
        famiglie = sum(isinstance(d, Famiglia) for d in voci)
        aperte = sum(d.aperta for d in voci)
        chiuse = len(voci) - famiglie - aperte
        totali = [totali[0] + chiuse, totali[1] + famiglie, totali[2] + aperte]
        print("%-4d %-34s %7d %9d %7d" % (cap, TITOLI.get(cap, ""), chiuse, famiglie, aperte))
        temi = sorted({d.tema for d in voci})
        print("     " + "; ".join(temi))
    print("%-39s %7d %9d %7d" % ("totale", totali[0], totali[1], totali[2]))
    print("\nLe famiglie sono domande parametriche: ogni volta escono con dati diversi.")


def raccolta(capitoli, cartella, tieni_tex, solo_tex):
    sezioni = []
    for cap in capitoli:
        voci = [d for d in DOMANDE if d.cap == cap]
        voci.sort(key=lambda d: d.aperta)       # prima le chiuse, poi le aperte
        if voci:
            sezioni.append(("Capitolo %d — %s" % (cap, TITOLI.get(cap, "")),
                            [d.istanza_completa() for d in voci]))
    sottotitolo = "capitoli %d–%d" % (capitoli[0], capitoli[-1])
    prodotto = compila(raccolta_tex(sezioni, sottotitolo),
                       os.path.join(cartella, "raccolta-domande.pdf"), tieni_tex, solo_tex)
    print("Raccolta: %s" % prodotto)


def main():
    parser = argparse.ArgumentParser(
        description="Genera prove di Tecnologie Web nello stile delle prove intercorso.")
    parser.add_argument("--id", type=int, help="numero della prova (da 1); a caso se manca")
    parser.add_argument("--quante", type=int, default=1, help="quante prove generare (ID consecutivi)")
    parser.add_argument("--chiuse", type=int, default=8, help="domande chiuse da 2 punti (8)")
    parser.add_argument("--aperte", type=int, default=3, help="domande aperte da 5 punti (3)")
    parser.add_argument("--capitoli", default=None,
                        help="capitoli della dispensa, es. 1-15 oppure 3,5-8 (predefinito: 1-16)")
    parser.add_argument("--minuti", type=int, default=45, help="tempo indicato nelle istruzioni (45)")
    parser.add_argument("--titolo", default="Prova Scritta di Tecnologie Web")
    parser.add_argument("--cartella", default=os.path.join(QUI, "generate"),
                        help="dove salvare i file (predefinito: la cartella generate)")
    parser.add_argument("--senza-soluzioni", action="store_true", help="non produrre le soluzioni")
    parser.add_argument("--solo-tex", action="store_true", help="scrivere i .tex senza compilarli")
    parser.add_argument("--tieni-tex", action="store_true", help="conservare anche i .tex")
    parser.add_argument("--elenco", action="store_true", help="mostrare il contenuto della banca")
    parser.add_argument("--raccolta", action="store_true",
                        help="un solo PDF con tutte le domande e le soluzioni")
    opzioni = parser.parse_args()

    if opzioni.elenco:
        elenco()
        return
    capitoli = leggi_capitoli(opzioni.capitoli) if opzioni.capitoli else \
        sorted(c for c in {d.cap for d in DOMANDE} if c <= 16)
    os.makedirs(opzioni.cartella, exist_ok=True)
    if opzioni.raccolta:
        raccolta(capitoli, opzioni.cartella, opzioni.tieni_tex, opzioni.solo_tex)
        return

    primo = opzioni.id if opzioni.id is not None else random.randint(1, 99999)
    if not opzioni.solo_tex and shutil.which("pdflatex") is None:
        print("pdfLaTeX non trovato: scrivo i file .tex (si compilano con pdfLaTeX, "
              "anche su Overleaf).")
    for numero in range(primo, primo + opzioni.quante):
        prova = componi(numero, DOMANDE, opzioni.chiuse, opzioni.aperte, capitoli,
                        opzioni.titolo, opzioni.minuti)
        base = os.path.join(opzioni.cartella, "prova-%s" % prova.id_testo)
        prodotti = [compila(prova_tex(prova), base + ".pdf", opzioni.tieni_tex,
                            opzioni.solo_tex)]
        if not opzioni.senza_soluzioni:
            prodotti.append(compila(prova_tex(prova, soluzioni=True),
                                    base + "-soluzioni.pdf", opzioni.tieni_tex,
                                    opzioni.solo_tex))
        capitoli_toccati = sorted({i.cap for i in prova.istanze})
        print("Prova %s: %s  (capitoli %s)" % (
            prova.id_testo, ", ".join(os.path.basename(p) for p in prodotti),
            ", ".join(map(str, capitoli_toccati))))
    if opzioni.quante > 1 or opzioni.id is None:
        print("Le prove di una stessa decina di ID (1-%d, %d-%d, ...) non ripetono le domande."
              % (SERIE, SERIE + 1, 2 * SERIE))


if __name__ == "__main__":
    main()
