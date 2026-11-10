"""Dal mini-markup della banca al LaTeX.

Nei testi delle domande si scrive in modo semplice:

    `codice`          codice in linea (tutto letterale, nessun escape da fare)
    ``co`di`ce``      codice in linea che contiene un accento grave
    **grassetto**     grassetto
    *corsivo*         corsivo
    riga vuota        nuovo capoverso

Tutto il resto è testo normale: i caratteri speciali di LaTeX vengono protetti
da qui, quindi nella banca non si scrive mai LaTeX a mano.
"""

import re

# Caratteri speciali di LaTeX, validi sia nel testo sia nel codice.
_SPECIALI = {
    "\\": r"\textbackslash{}",
    "{": r"\{",
    "}": r"\}",
    "#": r"\#",
    "$": r"\$",
    "%": r"\%",
    "&": r"\&",
    "_": r"\_",
    "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
}

# Solo nel codice: apici dritti e accento grave come si digitano.
_SOLO_CODICE = {
    "'": r"\textquotesingle{}",
    "`": r"\textasciigrave{}",
}

# Caratteri Unicode ammessi nel testo oltre all'ASCII (gli altri sono un errore
# di battitura quasi certo, e pdfLaTeX si fermerebbe).
AMMESSI_TESTO = set("àèéìòùÀÈÉÌÒÙ«»“”‘’–—…×·°€→←↔⇒≥≤≠≈−")
# Nel codice in linea e nei listati.
AMMESSI_CODICE = set("àèéìòùÀÈÉÌÒÙ«»’…€→·×–—")


class ErroreMarkup(ValueError):
    pass


def _controlla(testo, ammessi, dove):
    for c in testo:
        if ord(c) > 126 and c not in ammessi:
            raise ErroreMarkup(
                "carattere %r (U+%04X) non previsto %s: %r" % (c, ord(c), dove, testo[:60])
            )
        if c == "\t":
            raise ErroreMarkup("tabulazione %s: usare gli spazi (%r)" % (dove, testo[:60]))


def escape_testo(testo):
    """Protegge un tratto di testo normale."""
    _controlla(testo, AMMESSI_TESTO, "nel testo")
    return "".join(_SPECIALI.get(c, c) for c in testo)


def escape_codice(codice):
    """Protegge il contenuto di un tratto di codice in linea (va dentro \\cod{})."""
    _controlla(codice, AMMESSI_CODICE, "nel codice in linea")
    out = []
    precedente = ""
    for i, c in enumerate(codice):
        if c == " ":
            # gli spazi ripetuti, iniziali o finali non devono sparire
            if precedente == " " or i == 0 or i == len(codice) - 1:
                out.append(r"\ ")
            else:
                out.append(" ")
        elif c in _SPECIALI:
            out.append(_SPECIALI[c])
        elif c in _SOLO_CODICE:
            out.append(_SOLO_CODICE[c])
        else:
            # "--", "<<", ">>" e ",," sono legature in alcuni font: le si spezza
            if c in "-<>," and precedente == c:
                out.append("{}")
            out.append(c)
        # nel codice lungo (URL, percorsi) si può andare a capo dopo / ? & = #
        if len(codice) > 24 and c in "/?&=#" and 0 < i < len(codice) - 1:
            out.append(r"\codbreak{}")
        precedente = c
    return "".join(out)


_TOKEN = re.compile(r"(``.+?``|`[^`\n]+`|\*\*|\*)", re.S)


def a_latex(testo):
    """Converte un testo della banca in LaTeX."""
    if testo is None:
        return ""
    paragrafi = [p for p in re.split(r"\n\s*\n", testo.strip()) if p.strip()]
    return "\n\n".join(_paragrafo(p) for p in paragrafi)


def _paragrafo(testo):
    testo = re.sub(r"\s*\n\s*", " ", testo.strip())
    out = []
    grassetto = corsivo = False
    for pezzo in _TOKEN.split(testo):
        if not pezzo:
            continue
        if pezzo.startswith("``") and pezzo.endswith("``") and len(pezzo) > 4:
            out.append(r"\cod{%s}" % escape_codice(pezzo[2:-2].strip()))
        elif pezzo.startswith("`") and pezzo.endswith("`") and len(pezzo) > 2:
            out.append(r"\cod{%s}" % escape_codice(pezzo[1:-1]))
        elif pezzo == "**":
            out.append("}" if grassetto else r"\textbf{")
            grassetto = not grassetto
        elif pezzo == "*":
            out.append("}" if corsivo else r"\textit{")
            corsivo = not corsivo
        else:
            if "`" in pezzo:
                raise ErroreMarkup("accento grave non chiuso in: %r" % testo[:80])
            out.append(escape_testo(pezzo))
    if grassetto or corsivo:
        raise ErroreMarkup("grassetto o corsivo non chiuso in: %r" % testo[:80])
    return "".join(out)


def testo_semplice(testo):
    """Il testo senza markup (per i confronti fra opzioni e per l'elenco).

    Gli asterischi dentro il codice restano: `a[href*="x"]` e `a[href="x"]` sono
    selettori diversi.
    """
    if testo is None:
        return ""
    out = []
    for pezzo in _TOKEN.split(testo):
        if not pezzo or pezzo in ("**", "*"):
            continue
        if pezzo.startswith("``") and pezzo.endswith("``") and len(pezzo) > 4:
            out.append(pezzo[2:-2].strip())
        elif pezzo.startswith("`") and pezzo.endswith("`") and len(pezzo) > 2:
            out.append(pezzo[1:-1])
        else:
            out.append(pezzo)
    return "".join(out)


def larghezza_stimata(testo):
    """Larghezza approssimativa, in punti, di un testo composto in corpo 10.

    Serve a decidere se le opzioni stanno su due colonne. Il codice (Latin
    Modern Mono) occupa 5,25 pt per carattere; per il testo si usano le
    larghezze reali dei caratteri di Linux Libertine, ridotte del 2% per
    tenere conto delle crenature.
    """
    if testo is None:
        return 0.0
    larghezza = 0.0
    for pezzo in _TOKEN.split(testo):
        if not pezzo or pezzo in ("**", "*"):
            continue
        if pezzo.startswith("``") and len(pezzo) > 4:
            larghezza += 5.25 * len(pezzo[2:-2].strip())
        elif pezzo.startswith("`") and len(pezzo) > 2:
            larghezza += 5.25 * (len(pezzo) - 2)
        else:
            larghezza += 0.98 * sum(_LARGHEZZE.get(c, 5.0) for c in pezzo)
    return larghezza


# Larghezze dei caratteri di Linux Libertine in corpo 10 (dal file .tfm).
_CARATTERI = (" !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`"
              "abcdefghijklmnopqrstuvwxyz{|}~àèéìòùÀÈÉ«»’“”–—")
_MISURE = [2.5, 2.88, 3.36, 4.65, 4.65, 6.37, 7.05, 2.68, 2.98, 2.98, 3.69, 5.5, 2.2, 3.38,
           2.2, 3.23, 4.65, 4.65, 4.65, 4.65, 4.65, 4.65, 4.65, 4.65, 4.65, 4.65, 2.36, 2.36,
           5.5, 5.5, 5.5, 4.35, 8.95, 6.95, 5.88, 6.46, 7.01, 5.57, 4.85, 6.85, 7.3, 2.97,
           3.22, 6.37, 5.28, 8.39, 6.99, 7.02, 5.41, 7.02, 5.87, 4.85, 5.97, 6.61, 6.52, 9.51,
           6.6, 5.75, 6.04, 3.56, 2.87, 3.56, 5.18, 4.86, 2.68, 4.57, 4.93, 4.28, 5.06, 4.47,
           3.1, 5.0, 5.38, 2.71, 2.72, 5.12, 2.64, 7.9, 5.42, 5.04, 5.19, 5.03, 3.72, 3.9,
           3.16, 5.31, 4.97, 7.47, 4.9, 5.15, 4.24, 2.77, 2.05, 2.77, 4.49, 4.57, 4.47, 4.47,
           2.71, 5.04, 5.31, 6.95, 5.57, 5.57, 5.43, 5.43, 2.68, 3.75, 3.75, 5.48, 7.42]
assert len(_CARATTERI) == len(_MISURE)
_LARGHEZZE = dict(zip(_CARATTERI, _MISURE))
