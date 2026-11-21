"""Dalla banca all'HTML: il mini-markup, i listati colorati e i dati
dell'allenamento.

Serve a `genera_allenamento.py`, che produce una pagina HTML autonoma
(nessun file esterno, funziona anche aprendola dal disco) con tutta la banca:
le domande fisse con alcune estrazioni delle opzioni già pronte, le domande
parametriche con alcune varianti, le domande aperte con la traccia.
"""

import html
import random
import re

from .markup import _TOKEN
from .modello import NESSUNA, Famiglia

# ----------------------------------------------------------------------
# Mini-markup


def _esc(testo):
    return html.escape(testo, quote=False)


def a_html(testo):
    """Converte un testo della banca (mini-markup) in HTML."""
    if not testo:
        return ""
    paragrafi = [p for p in re.split(r"\n\s*\n", testo.strip()) if p.strip()]
    return "".join("<p>%s</p>" % _paragrafo(p) for p in paragrafi)


def a_html_riga(testo):
    """Come a_html, ma senza il paragrafo attorno (per opzioni e titoli)."""
    if not testo:
        return ""
    return _paragrafo(testo)


def _paragrafo(testo):
    testo = re.sub(r"\s*\n\s*", " ", testo.strip())
    out = []
    grassetto = corsivo = False
    for pezzo in _TOKEN.split(testo):
        if not pezzo:
            continue
        if pezzo.startswith("``") and pezzo.endswith("``") and len(pezzo) > 4:
            out.append("<code>%s</code>" % _esc(pezzo[2:-2].strip()))
        elif pezzo.startswith("`") and pezzo.endswith("`") and len(pezzo) > 2:
            out.append("<code>%s</code>" % _esc(pezzo[1:-1]))
        elif pezzo == "**":
            out.append("</strong>" if grassetto else "<strong>")
            grassetto = not grassetto
        elif pezzo == "*":
            out.append("</em>" if corsivo else "<em>")
            corsivo = not corsivo
        else:
            out.append(_esc(pezzo))
    return "".join(out)


# ----------------------------------------------------------------------
# Listati colorati

_PAROLE_JS = set("""break case catch class const continue debugger default delete do else
    export extends finally for function if import in instanceof let new return super switch
    this throw try typeof var void while with yield async await of static get set true false
    null undefined from as""".split())
_PAROLE_TS = _PAROLE_JS | set("""interface type enum implements readonly private public
    protected keyof any unknown never string number boolean""".split())
_PAROLE_PHP = set("""echo if else elseif foreach for while function return as isset array
    print true false null""".split())
_PAROLE_SQL = set("""select from where insert into values update set delete create table and
    or not null primary key order by limit join on as like""".split())

_STRINGHE = r"`(?:\\[\s\S]|[^`\\])*`|\"(?:\\.|[^\"\\\n])*\"|'(?:\\.|[^'\\\n])*'"
_REGOLE = {
    "js": [("c", r"//[^\n]*|/\*[\s\S]*?\*/"), ("s", _STRINGHE),
           ("n", r"\b\d+(?:\.\d+)?n?\b"), ("w", r"[A-Za-z_$][\w$]*")],
    "css": [("c", r"/\*[\s\S]*?\*/"), ("s", r"\"[^\"\n]*\"|'[^'\n]*'"),
            ("k", r"@[\w-]+"), ("p", r"--[\w-]+(?=\s*:)|[\w-]+(?=\s*:[^;{}]*[;}])")],
    "scss": [("c", r"//[^\n]*|/\*[\s\S]*?\*/"), ("s", r"\"[^\"\n]*\"|'[^'\n]*'"),
             ("k", r"@[\w-]+|!default\b|!important\b"), ("v", r"\$[\w-]+"),
             ("p", r"--[\w-]+(?=\s*:)|[\w-]+(?=\s*:[^;{}]*[;}])")],
    "json": [("s", r"\"(?:\\.|[^\"\\\n])*\""), ("n", r"-?\b\d+(?:\.\d+)?\b"),
             ("k", r"\b(?:true|false|null)\b")],
    "sh": [("c", r"(?<![\w$])#[^\n]*"), ("s", r"\"(?:\\.|[^\"\\\n])*\"|'[^'\n]*'")],
    "php": [("c", r"//[^\n]*|/\*[\s\S]*?\*/"), ("s", r"\"(?:\\.|[^\"\\\n])*\"|'(?:\\.|[^'\\\n])*'"),
            ("v", r"\$\w+"), ("t", r"<\?php|\?>"), ("w", r"[A-Za-z_]\w*")],
    "sql": [("s", r"'(?:''|[^'\n])*'"), ("w", r"[A-Za-z_]\w*")],
    "pug": [("c", r"//-?[^\n]*"), ("s", r"\"(?:\\.|[^\"\\\n])*\"|'(?:\\.|[^'\\\n])*'"),
            ("t", r"(?:(?<=\n)|^)[ \t]*[a-z][\w-]*(?=[.#(\s=]|$)")],
}
_REGOLE["ts"] = _REGOLE["js"]


def _parole(lingua):
    return {"js": _PAROLE_JS, "ts": _PAROLE_TS, "php": _PAROLE_PHP,
            "sql": _PAROLE_SQL}.get(lingua, set())


def _gettoni(lingua, sorgente):
    """[(classe, testo)]: classe vuota per il testo normale."""
    if lingua == "html":
        return _gettoni_html(sorgente)
    regole = _REGOLE.get(lingua)
    if not regole:
        return [("", sorgente)]
    schema = re.compile("|".join("(?P<%s%d>%s)" % (c, i, r) for i, (c, r) in enumerate(regole)))
    parole = _parole(lingua)
    out, pos = [], 0
    for m in schema.finditer(sorgente):
        if m.start() > pos:
            out.append(("", sorgente[pos:m.start()]))
        classe = m.lastgroup.rstrip("0123456789")
        testo = m.group()
        if classe == "w":
            chiave = testo.lower() if lingua == "sql" else testo
            classe = "k" if chiave in parole else ""
        out.append((classe, testo))
        pos = m.end()
    out.append(("", sorgente[pos:]))
    return out


_TAG = re.compile(r"<!--[\s\S]*?-->|<(/?)([A-Za-z][\w-]*)((?:\s+[^\s=>/]+(?:\s*=\s*"
                  r"(?:\"[^\"]*\"|'[^']*'|[^\s>]+))?)*)\s*(/?)>|<!DOCTYPE[^>]*>", re.I)
_ATTRIBUTO = re.compile(r"(\s+)([^\s=>/]+)(?:(\s*=\s*)(\"[^\"]*\"|'[^']*'|[^\s>]+))?")


def _gettoni_html(sorgente):
    out, pos = [], 0
    while True:
        m = _TAG.search(sorgente, pos)
        if not m:
            out.append(("", sorgente[pos:]))
            return out
        out.append(("", sorgente[pos:m.start()]))
        if m.group(0).startswith("<!--"):
            out.append(("c", m.group(0)))
        elif m.group(2) is None:
            out.append(("t", m.group(0)))
        else:
            out.append(("t", "<" + m.group(1) + m.group(2)))
            for a in _ATTRIBUTO.finditer(m.group(3) or ""):
                out.append(("", a.group(1)))
                out.append(("a", a.group(2)))
                if a.group(3):
                    out.append(("", a.group(3)))
                    out.append(("s", a.group(4)))
            out.append(("t", (" " if m.group(4) else "") + m.group(4) + ">"))
        pos = m.end()
        nome = (m.group(2) or "").lower()
        if nome in ("script", "style") and not m.group(1):
            fine = re.compile(r"</%s\s*>" % nome, re.I).search(sorgente, pos)
            fine = fine.start() if fine else len(sorgente)
            out.extend(_gettoni("js" if nome == "script" else "css", sorgente[pos:fine]))
            pos = fine


def listato_html(listato):
    """Un listato con i numeri di riga e i colori, come nelle prove."""
    righe = [[]]
    for classe, testo in _gettoni(listato.lingua, listato.sorgente):
        for i, pezzo in enumerate(testo.split("\n")):
            if i:
                righe.append([])
            if pezzo:
                righe[-1].append(("<span class=\"%s\">%s</span>" % (classe, _esc(pezzo)))
                                 if classe else _esc(pezzo))
    corpo = "".join("<span class=\"riga\" data-n=\"%d\">%s</span>"
                    % (listato.primo + n, "".join(pezzi)) for n, pezzi in enumerate(righe))
    return "<pre class=\"listato\" data-lingua=\"%s\"><code>%s</code></pre>" % (
        listato.lingua, corpo)


# ----------------------------------------------------------------------
# Esportazione della banca

ISTANZE_FISSE = 6        # estrazioni delle opzioni per ogni domanda fissa
VARIANTI_FAMIGLIA = 10   # varianti per ogni domanda parametrica
ISTANZE_VARIANTE = 2     # estrazioni per ogni variante


def _variante(domanda, semi):
    """Una domanda chiusa: testi in HTML, tutte le opzioni e alcune
    estrazioni (indici delle opzioni mostrate, nell'ordine)."""
    opzioni = list(domanda.giuste) + list(domanda.sbagliate)
    indice = {t: i for i, t in enumerate(opzioni)}
    nessuna = False
    istanze = []
    for seme in semi:
        istanza = domanda.istanza(random.Random(seme))
        scelte = []
        for testo, _ in istanza.opzioni:
            if testo == NESSUNA:
                nessuna = True
                scelte.append(len(opzioni))
            else:
                scelte.append(indice[testo])
        if scelte not in istanze:
            istanze.append(scelte)
    testi = [a_html_riga(t) for t in opzioni] + ([a_html_riga(NESSUNA)] if nessuna else [])
    return {"t": a_html(domanda.testo), "c": [listato_html(l) for l in domanda.codice],
            "d": a_html(domanda.dopo), "s": a_html(domanda.spiegazione), "o": testi,
            "g": len(domanda.giuste), "n": 1 if nessuna else 0, "i": istanze}


def esporta(banca):
    """La banca come struttura JSON per la pagina di allenamento."""
    voci = []
    for d in banca:
        voce = {"id": d.id, "cap": d.cap, "tema": d.tema, "p": d.punti,
                "x": 1 if getattr(d, "trabocchetto", False) else 0}
        fonte = getattr(d, "fonte", None)
        if fonte:
            voce["f"] = fonte
        if d.aperta:
            voce.update(a=1, t=a_html(d.testo), c=[listato_html(l) for l in d.codice],
                        tr=[a_html_riga(p) for p in d.traccia], r=a_html_riga(d.rif or ""))
        elif isinstance(d, Famiglia):
            varianti = []
            for v in range(VARIANTI_FAMIGLIA):
                domanda = d.genera(random.Random("html:%s:%d" % (d.id, v)))
                variante = _variante(domanda, ["html:%s:%d:%d" % (d.id, v, k)
                                               for k in range(ISTANZE_VARIANTE)])
                if variante not in varianti:
                    varianti.append(variante)
                voce.setdefault("r", a_html_riga(domanda.rif or ""))
            voce["v"] = varianti
        else:
            voce["v"] = [_variante(d, ["html:%s:%d" % (d.id, k) for k in range(ISTANZE_FISSE)])]
            voce["r"] = a_html_riga(d.rif or "")
        voci.append(voce)
    return voci
