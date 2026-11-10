"""Generatore di prove di Tecnologie Web.

Questo modulo espone ciò che serve per scrivere la banca delle domande:

    L(lingua, sorgente)        un listato
    chiusa(...)                domanda a risposta chiusa
    aperta(...)                domanda a risposta aperta
    uscita_js(...)             «che cosa stampa questo codice?» (verificabile con Node)
    uscita_browser(...)        lo stesso, per un documento HTML (verificabile con Chromium)
    colore_css(...)            «di che colore è l'elemento?» (verificabile con Chromium)
    uscita_pug(...)            «quale HTML genera questo template?» (verificabile con Pug)
    risposte_server(...)       «che cosa risponde il server?» (verificabile avviandolo)
    famiglia(...)              decoratore per le domande parametriche
    Err(nome, prima=[...])     un esito che termina con un'eccezione
    combina_errori(...)        distrattori costruiti dagli errori tipici, riga per riga
"""

from .modello import Aperta, Chiusa, ErroreBanca, Famiglia, L, Listato   # noqa: F401

chiusa = Chiusa
aperta = Aperta

STRICT = 'Si assuma la presenza di `"use strict";`.'

# Fonti delle domande riprese dalle prove del corso (compaiono nelle soluzioni)
FONTE_2024 = "prima prova intercorso del 23 aprile 2024"
FONTE_AULA = "facsimile mostrato in aula"


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


def uscita_js(id, cap, tema, codice, giusta, sbagliate, testo=None, strict=True, modulo=False,
              file=None, **altro):
    """Domanda «qual è l'output?» su un frammento JavaScript.

    giusta e sbagliate sono esiti (vedi `esito`). La risposta giusta viene
    confrontata con l'output reale di Node dallo script di verifica.
    modulo: il frammento è un modulo ES (può usare import). file: {nome:
    contenuto} dei file che il frammento legge, creati accanto a esso.
    """
    if testo is None:
        testo = "Qual è il risultato dell'esecuzione del seguente frammento di codice JavaScript?"
        if strict:
            testo += " " + STRICT
    listato = L("js", codice)
    verifica = dict(tipo="node", strict=strict, codice=listato.sorgente, **_esito_atteso(giusta))
    if modulo:
        verifica["modulo"] = True
    if file:
        verifica["file"] = dict(file)
    return Chiusa(id, cap, tema, testo, [esito(giusta)], [esito(s) for s in sbagliate],
                  codice=listato, verifica=verifica, **altro)


def uscita_pug(id, cap, tema, sorgente, giusta, sbagliate, locals=None, chiamata=None,
               file=None, testo=None, **altro):
    """Domanda «quale HTML genera questo template Pug?».

    giusta e sbagliate sono codice HTML. locals: l'oggetto passato al
    template; chiamata: il codice JavaScript che lo passa, mostrato accanto al
    template. file: {nome: sorgente} degli altri template (inclusi o estesi),
    mostrati prima del template principale, che si chiama «pagina.pug».
    La risposta giusta viene confrontata con l'HTML prodotto davvero da Pug.
    """
    if testo is None:
        testo = "Quale codice HTML genera il seguente template Pug?"
        if chiamata:
            testo = ("Si consideri il template Pug `pagina.pug` riportato di seguito, trasformato "
                     "in HTML con la chiamata a destra. Quale codice HTML viene generato?")
    listato = L("pug", sorgente)
    verifica = dict(tipo="pug", sorgente=listato.sorgente, principale="pagina.pug",
                    locals=locals or {}, atteso=giusta)
    codice = [listato]
    if file:
        altri = [L("pug", s) for s in file.values()]
        verifica["file"] = {nome: l.sorgente for nome, l in zip(file, altri)}
        codice = altri + codice
    if chiamata:
        codice.append(L("js", chiamata))
    if len(codice) > 2:
        raise ErroreBanca("domanda %r: al più due listati" % id)
    return Chiusa(id, cap, tema, testo, [_html(giusta)], [_html(s) for s in sbagliate],
                  codice=codice, verifica=verifica, **altro)


def _html(testo):
    """Un'opzione di una domanda su Pug: il codice HTML fra apici inversi; una
    frase senza tag (per esempio «Viene sollevato un errore.») resta tale."""
    if "<" not in testo:
        return testo
    return "`` %s ``" % testo if "`" in testo else "`%s`" % testo


def _richiesta(r):
    if isinstance(r, str):
        metodo, percorso = r.split(" ", 1)
        return {"metodo": metodo, "percorso": percorso}
    return dict(r)


def _descrivi_richiesta(r):
    testo = "`%s %s`" % (r["metodo"], r["percorso"])
    aggiunte = ["corpo `%s`" % r["corpo"]] if r.get("corpo") else []
    aggiunte += ["l'header `%s: %s`" % (k, v) for k, v in (r.get("intestazioni") or {}).items()
                 if k.lower() != "content-type"]
    if aggiunte:
        testo += " (con %s)" % " e ".join(aggiunte)
    return testo


def risposte_server(id, cap, tema, codice, richieste, giusta, sbagliate, testo=None,
                    applicazione="Node.js", **altro):
    """Domanda sulle risposte di un server (il modulo http di Node o Express)
    a una sequenza di richieste.

    richieste: stringhe «METODO /percorso» oppure dict con metodo, percorso,
    corpo e intestazioni. giusta e sbagliate: liste di risposte nella forma
    «200 corpo» (per un reindirizzamento «302 -> /url»). La verifica avvia
    davvero il server sulla porta 3000 e gli invia le richieste.
    """
    richieste = [_richiesta(r) for r in richieste]
    for r in richieste:
        r.setdefault("metodo", "GET")
        if r.get("corpo") and "intestazioni" not in r:
            r["intestazioni"] = {"Content-Type": "application/x-www-form-urlencoded"}
    if testo is None:
        elenco = [_descrivi_richiesta(r) for r in richieste]
        elenco = ", ".join(elenco[:-1]) + " e " + elenco[-1] if len(elenco) > 1 else elenco[0]
        testo = ("Si consideri la seguente applicazione %s, in ascolto sulla porta 3000. Quali "
                 "risposte (codice di stato e corpo) ottengono, nell'ordine, %s %s?"
                 % (applicazione, "le richieste" if len(richieste) > 1 else "la richiesta",
                    elenco))
    listato = L("js", codice)
    verifica = dict(tipo="express", codice=listato.sorgente, richieste=richieste,
                    atteso=[str(r) for r in giusta])

    def opzione(risposte):
        return esito(risposte) if not isinstance(risposte, str) else risposte

    return Chiusa(id, cap, tema, testo, [opzione(giusta)], [opzione(s) for s in sbagliate],
                  codice=listato, verifica=verifica, **altro)


def uscita_browser(id, cap, tema, html, giusta, sbagliate, testo=None, azioni=None,
                   dividi=False, file=None, **altro):
    """Domanda «qual è l'output in console?» su un documento HTML.

    azioni: elenco di passi da eseguire dopo il caricamento, per la verifica:
    {"click": "selettore"}, {"attendi": millisecondi}.
    file: {nome: sorgente} dei file inclusi dalla pagina (per esempio uno
    script esterno), mostrati prima della pagina e messi accanto a essa
    durante la verifica.
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
    if file:
        esterni = [L(nome.rsplit(".", 1)[-1], sorgente) for nome, sorgente in file.items()]
        verifica["file"] = {nome: l.sorgente for nome, l in zip(file, esterni)}
        codice = esterni + [listato]
    return Chiusa(id, cap, tema, testo, [esito(giusta)], [esito(s) for s in sbagliate],
                  codice=codice, verifica=verifica, **altro)


def combina_errori(giusta, alternative, rng, quanti=5, esiti=()):
    """Distrattori per le domande sull'output, costruiti dagli errori tipici.

    giusta: le righe stampate davvero. alternative[i]: i valori (sbagliati ma
    plausibili) che chi sbaglia scriverebbe alla riga i. esiti: esiti interi
    già pronti (per esempio quelli di un ragionamento sbagliato applicato a
    tutto il codice), che hanno la precedenza. Poi vengono le righe con un solo
    errore e quelle con due errori insieme.
    """
    giusta = [str(r) for r in giusta]
    valori = [[str(v) for v in alt if str(v) != giusta[i]] for i, alt in enumerate(alternative)]
    singoli = []
    for i, vs in enumerate(valori):
        for v in vs:
            riga = list(giusta)
            riga[i] = v
            singoli.append(riga)
    doppi = []
    for i in range(len(valori)):
        for j in range(i + 1, len(valori)):
            if valori[i] and valori[j]:
                riga = list(giusta)
                riga[i], riga[j] = rng.choice(valori[i]), rng.choice(valori[j])
                doppi.append(riga)
    rng.shuffle(singoli)
    rng.shuffle(doppi)
    scelti = []
    for e in list(esiti) + singoli[:3] + doppi + singoli[3:]:
        confronto = e if isinstance(e, (Err, str)) else [str(r) for r in e]
        if confronto != giusta and confronto not in scelti:
            scelti.append(confronto)
    return scelti[:quanti]


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
