#!/usr/bin/env python3
"""Controlla la banca delle domande eseguendo davvero il codice.

    python verifica/verifica.py              tutte le domande verificabili
    python verifica/verifica.py --varianti 30    più varianti per le famiglie
    python verifica/verifica.py --solo c05   solo gli id che contengono "c05"

Per ogni domanda con codice confronta la risposta marcata come giusta con ciò
che succede davvero: l'output di Node, la console di Chromium, lo stile
calcolato da Chromium, l'HTML prodotto da Pug, le risposte di un server Node
o Express avviato davvero. Per le domande parametriche (famiglie) prova più
varianti.

Serve Node.js con Playwright (per Chromium) e, per le domande su Pug ed
Express, i pacchetti di questa cartella (npm install).
"""

import argparse
import json
import os
import random
import subprocess
import sys
import tempfile

QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(QUI))

from banca import DOMANDE                      # noqa: E402
from generatore.latex import domanda_tex       # noqa: E402
from generatore.modello import Famiglia        # noqa: E402


def casi_della_banca(varianti, filtro):
    """(chiave, domanda Chiusa) per tutte le domande con una verifica."""
    for voce in DOMANDE:
        if filtro and filtro not in voce.id:
            continue
        if isinstance(voce, Famiglia):
            for seme in range(varianti):
                domanda = voce.genera(random.Random("verifica:%s:%d" % (voce.id, seme)))
                # anche ogni variante deve comporsi in LaTeX senza errori
                domanda_tex(domanda.istanza(random.Random(seme)), soluzioni=True)
                if domanda.verifica:
                    yield "%s#%d" % (voce.id, seme), domanda
        elif getattr(voce, "verifica", None):
            yield voce.id, voce


def prepara(chiave, domanda):
    caso = dict(domanda.verifica)
    caso["chiave"] = chiave
    if caso["tipo"] == "css" and not caso.get("candidati"):
        caso["candidati"] = list(domanda.giuste) + list(domanda.sbagliate)
    return caso


def confronta(caso, domanda, reale):
    """Restituisce None se va tutto bene, altrimenti la descrizione del problema."""
    if reale is None:
        return "nessun risultato"
    if "eccezione" in reale:
        return "eccezione nell'esecuzione: " + reale["eccezione"]
    tipo = caso["tipo"]
    if tipo in ("node", "browser"):
        atteso = {"righe": caso["righe"], "errore": caso["errore"]}
        ottenuto = {"righe": reale["righe"], "errore": reale["errore"]}
        if atteso != ottenuto:
            return "atteso %s, ottenuto %s" % (json.dumps(atteso), json.dumps(ottenuto))
    elif tipo == "css":
        atteso = caso.get("atteso", domanda.giuste[0])
        if reale["corrispondenti"] != [atteso]:
            return "valore calcolato %s: corrisponde a %s, non solo a %r" % (
                reale["reale"], reale["corrispondenti"], atteso)
    elif tipo == "dom":
        if reale.get("errore"):
            return "errore nella pagina: %s" % reale["errore"]
        if reale["valore"] != caso["atteso"]:
            return "atteso %r, ottenuto %r" % (caso["atteso"], reale["valore"])
    elif tipo == "pug":
        if reale["html"] != caso["atteso"]:
            return "HTML atteso %r, ottenuto %r" % (caso["atteso"], reale["html"])
    elif tipo == "express":
        if reale.get("stderr"):
            return "il server non è partito: " + reale["stderr"]
        if reale["risposte"] != caso["atteso"]:
            return "risposte attese %s, ottenute %s" % (caso["atteso"], reale["risposte"])
        if "log" in caso and reale["log"] != caso["log"]:
            return "log atteso %s, ottenuto %s" % (caso["log"], reale["log"])
    return None


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--varianti", type=int, default=12,
                        help="varianti da provare per ogni famiglia (12)")
    parser.add_argument("--solo", default="", help="solo gli id che contengono questo testo")
    parser.add_argument("--mostra", action="store_true", help="stampare anche gli esiti corretti")
    opzioni = parser.parse_args()

    coppie = list(casi_della_banca(opzioni.varianti, opzioni.solo))
    casi = [prepara(chiave, domanda) for chiave, domanda in coppie]
    print("Casi da eseguire: %d" % len(casi))
    with tempfile.TemporaryDirectory() as lavoro:
        file_casi = os.path.join(lavoro, "casi.json")
        file_esiti = os.path.join(lavoro, "esiti.json")
        with open(file_casi, "w", encoding="utf-8") as f:
            json.dump(casi, f)
        subprocess.run(["node", os.path.join(QUI, "esegui.js"), file_casi, file_esiti],
                       check=True)
        with open(file_esiti, encoding="utf-8") as f:
            esiti = json.load(f)

    problemi = 0
    per_tipo = {}
    for (chiave, domanda), caso in zip(coppie, casi):
        reale = esiti.get(chiave)
        errore = confronta(caso, domanda, reale)
        per_tipo[caso["tipo"]] = per_tipo.get(caso["tipo"], 0) + 1
        if errore:
            problemi += 1
            print("ERRORE %s: %s" % (chiave, errore))
        elif opzioni.mostra:
            print("ok     %s: %s" % (chiave, json.dumps(reale)[:150]))
    riepilogo = ", ".join("%s %d" % (t, n) for t, n in sorted(per_tipo.items()))
    print("Verificati %d casi (%s): %d problemi." % (len(casi), riepilogo, problemi))
    sys.exit(1 if problemi else 0)


if __name__ == "__main__":
    main()
