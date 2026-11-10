"""Generatore di prove di Tecnologie Web.

Questo modulo espone ciò che serve per scrivere la banca delle domande:

    L(lingua, sorgente)        un listato
    chiusa(...)                domanda a risposta chiusa
    aperta(...)                domanda a risposta aperta
    uscita_js(...)             «che cosa stampa questo codice?» (verificabile con Node)
    uscita_browser(...)        lo stesso, per un documento HTML (verificabile con Chromium)
    colore_css(...)            «di che colore è l'elemento?» (verificabile con Chromium)
    famiglia(...)              decoratore per le domande parametriche
    Err(nome, prima=[...])     un esito che termina con un'eccezione
"""

from .modello import Aperta, Chiusa, ErroreBanca, Famiglia, L, Listato   # noqa: F401

chiusa = Chiusa
aperta = Aperta

STRICT = 'Si assuma la presenza di `"use strict";`.'


class Err:
    """Esito di un frammento che solleva un'eccezione non gestita, dopo aver
    eventualmente stampato qualcosa."""

    def __init__(self, nome, prima=()):
        self.nome = nome
        self.prima = [str(r) for r in prima]


def _cod(valore):
    valore = str(valore)
    if valore == "":
        return "*(riga vuota)*"
    return "`` %s ``" % valore if "`" in valore else "`%s`" % valore


def esito(e):
    """Il testo dell'opzione che descrive un esito.

    Un esito è la lista delle righe stampate, un Err, oppure una stringa
    libera (già nel mini-markup).
    """
    if isinstance(e, str):
        return e
    if isinstance(e, Err):
        if e.prima:
            return "%s, poi viene sollevato un `%s`." % (", ".join(map(_cod, e.prima)), e.nome)
        return "Viene sollevato un `%s`." % e.nome
    righe = list(e)
    if not righe:
        return "Non viene stampato nulla."
    return ", ".join(map(_cod, righe)) + "."


def _esito_atteso(e):
    """La forma dell'esito che lo script di verifica confronta con la realtà."""
    if isinstance(e, Err):
        return {"righe": e.prima, "errore": e.nome}
    if isinstance(e, str):
        raise ErroreBanca("la risposta giusta di una domanda sull'output deve essere "
                          "un elenco di righe o un Err, non un testo libero")
    return {"righe": [str(r) for r in e], "errore": None}


def uscita_js(id, cap, tema, codice, giusta, sbagliate, testo=None, strict=True, **altro):
    """Domanda «qual è l'output?» su un frammento JavaScript.

    giusta e sbagliate sono esiti (vedi `esito`). La risposta giusta viene
    confrontata con l'output reale di Node dallo script di verifica.
    """
    if testo is None:
        testo = "Qual è il risultato dell'esecuzione del seguente frammento di codice JavaScript?"
        if strict:
            testo += " " + STRICT
    listato = L("js", codice)
    verifica = dict(tipo="node", strict=strict, codice=listato.sorgente, **_esito_atteso(giusta))
    return Chiusa(id, cap, tema, testo, [esito(giusta)], [esito(s) for s in sbagliate],
                  codice=listato, verifica=verifica, **altro)


def uscita_browser(id, cap, tema, html, giusta, sbagliate, testo=None, azioni=None,
                   dividi=False, **altro):
    """Domanda «qual è l'output in console?» su un documento HTML.

    azioni: elenco di passi da eseguire dopo il caricamento, per la verifica:
    {"click": "selettore"}, {"attendi": millisecondi}.
    """
    if testo is None:
        testo = ("Qual è l'output in console dopo il caricamento completo del documento "
                 "HTML riportato di seguito?")
    listato = L("html", html)
    verifica = dict(tipo="browser", html=listato.sorgente, azioni=azioni or [],
                    **_esito_atteso(giusta))
    codice = listato
    if dividi:
        meta = (len(listato.righe) + 1) // 2
        codice = [L("html", "\n".join(listato.righe[:meta])),
                  L("html", "\n".join(listato.righe[meta:]), primo=meta + 1)]
    return Chiusa(id, cap, tema, testo, [esito(giusta)], [esito(s) for s in sbagliate],
                  codice=codice, verifica=verifica, **altro)


def colore_css(id, cap, tema, css, html, selettore, giusta, sbagliate, testo=None,
               proprieta="color", **altro):
    """Domanda sulla cascata: il valore finale di una proprietà di un elemento.

    La risposta viene confrontata con lo stile calcolato da Chromium.
    """
    if testo is None:
        testo = ("Si consideri il seguente insieme di regole CSS incluse in un singolo foglio "
                 "di stile importato nella pagina web il cui `<body>` è riportato di seguito. "
                 "Qual è il colore finale dell'elemento `%s`?" % selettore)
    foglio, pagina = L("css", css), L("html", html)
    verifica = dict(tipo="css", css=foglio.sorgente, html=pagina.sorgente, selettore=selettore,
                    proprieta=proprieta, atteso=giusta)
    return Chiusa(id, cap, tema, testo, [giusta], sbagliate, codice=[foglio, pagina],
                  verifica=verifica, **altro)


def famiglia(id, cap, tema, varianti=3):
    """Decoratore: trasforma una funzione `f(rng) -> Chiusa` in una domanda
    parametrica della banca."""
    def decora(funzione):
        return Famiglia(id, cap, tema, funzione, varianti=varianti)
    return decora
