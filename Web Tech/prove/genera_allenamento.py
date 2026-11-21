#!/usr/bin/env python3
"""Genera la pagina HTML per allenarsi con la banca delle domande.

    python genera_allenamento.py                 scrive allenamento.html
    python genera_allenamento.py --uscita x.html in un altro file

La pagina è un unico file autonomo (nessuno script o foglio di stile
esterno): si apre con un doppio clic, anche senza connessione. Si scelgono i
capitoli e la modalità (allenamento con correzione immediata, oppure
simulazione d'esame con il tempo), e si possono chiedere solo le domande a
trabocchetto o solo quelle delle prove del corso.

Serve solo Python 3. Va rigenerata dopo aver modificato la banca.
"""

import argparse
import datetime
import json
import os
import sys

QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, QUI)

from banca import DOMANDE                                  # noqa: E402
from generatore.html import esporta                        # noqa: E402
from generatore.selezione import PESI, TITOLI, ULTIMO      # noqa: E402

MODELLO = os.path.join(QUI, "generatore", "allenamento.html")


def dati(data):
    capitoli = sorted(c for c in {d.cap for d in DOMANDE} if c <= ULTIMO)
    domande = [d for d in DOMANDE if d.cap in capitoli]
    return {
        "generato": data,
        "capitoli": {str(c): TITOLI.get(c, "Capitolo %d" % c) for c in capitoli},
        "pesi": {str(c): PESI.get(c, 1) for c in capitoli},
        "domande": esporta(domande),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--uscita", default=os.path.join(QUI, "allenamento.html"),
                        help="file da scrivere (predefinito: allenamento.html)")
    parser.add_argument("--data", default=datetime.date.today().strftime("%d/%m/%Y"),
                        help="data mostrata nella pagina (predefinita: oggi)")
    opzioni = parser.parse_args()

    contenuto = dati(opzioni.data)
    testo = json.dumps(contenuto, ensure_ascii=False, separators=(",", ":"))
    # dentro <script> la sequenza "</" chiuderebbe l'elemento
    testo = testo.replace("</", "<\\/")
    with open(MODELLO, encoding="utf-8") as f:
        pagina = f.read()
    if pagina.count("@@DATI@@") != 1:
        raise SystemExit("il modello deve contenere una volta sola il segnaposto @@DATI@@")
    pagina = pagina.replace("@@DATI@@", testo)
    with open(opzioni.uscita, "w", encoding="utf-8") as f:
        f.write(pagina)
    domande = contenuto["domande"]
    print("Scritto %s: %d domande (%d chiuse, %d aperte, %d a trabocchetto), %d kB."
          % (os.path.relpath(opzioni.uscita), len(domande),
             sum(1 for d in domande if not d.get("a")), sum(1 for d in domande if d.get("a")),
             sum(1 for d in domande if d["x"]), len(pagina.encode("utf-8")) // 1024))


if __name__ == "__main__":
    main()
