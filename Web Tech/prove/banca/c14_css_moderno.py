"""Capitolo 14: CSS moderno e adattivo (pseudo-classi funzionali e loro
specificità, custom property, calc/min/max/clamp, unità del viewport, gap e
flex, container query, immagini responsive, preferenze dell'utente,
@supports, annidamento)."""

from generatore import L, aperta, chiusa, colore_css, famiglia

CAP = 14
R = "cap. 14, «%s»"

DOMANDE = []
d = DOMANDE.append


def _pagina(css, corpo):
    return ("<!DOCTYPE html><html><head><meta charset=\"utf-8\"><style>\n"
            "body { margin: 0; }\n%s\n</style></head><body>\n%s\n</body></html>" % (css, corpo))


def _somma(*spec):
    return tuple(sum(x) for x in zip(*spec))


def _fmt(spec):
    return "(%d, %d, %d)" % spec


# ----------------------------------------------------------------------
# Famiglia: la specificità delle pseudo-classi funzionali
PREFISSI = [("li", (0, 0, 1)), ("ul > li", (0, 0, 2)), (".menu li", (0, 1, 1)),
            ("#nav li", (1, 0, 1))]
ARGOMENTI = {".attiva": (0, 1, 0), "#primo": (1, 0, 0), ":first-child": (0, 1, 0),
             "[aria-current]": (0, 1, 0), ".attiva.aperta": (0, 2, 0), ".nascosta": (0, 1, 0),
             ".disattiva": (0, 1, 0), "#ultimo": (1, 0, 0), "> a.link": (0, 1, 1),
             "+ .scelta": (0, 1, 0), "a": (0, 0, 1)}
FUNZIONALI = [("is", [".attiva", "#primo"]), ("is", [".attiva", ":first-child"]),
              ("is", ["[aria-current]", ".attiva.aperta"]), ("where", [".attiva", "#primo"]),
              ("not", [".disattiva", ".nascosta"]), ("not", ["#ultimo"]),
              ("has", ["> a.link"]), ("has", ["+ .scelta"]), ("where", ["#primo a"])]
ARGOMENTI["#primo a"] = (1, 0, 1)


@famiglia("c14-specificita", CAP, "pseudo-classi funzionali", varianti=5)
def _specificita(rng):
    prefisso, sp = rng.choice(PREFISSI)
    tipo, argomenti = rng.choice(FUNZIONALI)
    selettore = "%s:%s(%s)" % (prefisso, tipo, ", ".join(argomenti))
    specs = [ARGOMENTI[a] for a in argomenti]
    massimo = max(specs)
    giusta = sp if tipo == "where" else _somma(sp, massimo)
    candidati = [_somma(sp, *specs), _somma(sp, massimo, (0, 1, 0)), _somma(sp, (0, 1, 0)), sp,
                 _somma(sp, massimo), _somma(sp, min(specs)), _somma(sp, (0, 1, 0), *specs)]
    candidati += [_somma(giusta, d) for d in ((0, 0, 1), (0, 1, 0), (1, 0, 0))]
    sbagliate = []
    for c in candidati:
        if c != giusta and _fmt(c) not in sbagliate:
            sbagliate.append(_fmt(c))
    rng.shuffle(sbagliate)
    return chiusa(
        "c14-specificita", CAP, "pseudo-classi funzionali",
        "Qual è la specificità del selettore `%s`?" % selettore,
        _fmt(giusta), sbagliate[:5],
        spiegazione="Le pseudo-classi funzionali non contano come pseudo-classi: `:where()` "
                    "vale sempre zero, con tutto il suo contenuto; `:is()`, `:not()` e `:has()` "
                    "valgono quanto il loro argomento **più specifico** (non la somma degli "
                    "argomenti), anche se a selezionare l'elemento è un altro argomento. Qui "
                    "`%s` vale %s e la parte funzionale %s: in tutto %s." % (
                        prefisso, _fmt(sp), "zero" if tipo == "where" else _fmt(massimo),
                        _fmt(giusta)),
        rif=R % "La specificità delle pseudo-classi funzionali")


d(_specificita)


# ----------------------------------------------------------------------
# Famiglia: la cascata con le pseudo-classi funzionali
CORPO_LISTA = """<main id="contenuto">
  <ul class="lista">
    <li class="voce attiva" id="primo">Uno</li>
    <li class="voce">Due</li>
  </ul>
</main>"""
REGOLE = [  # selettore, seleziona #primo?, specificità
    ("li", True, (0, 0, 1)), (".voce", True, (0, 1, 0)),
    (":where(#contenuto) li", True, (0, 0, 1)), (":where(.lista .attiva)", True, (0, 0, 0)),
    ("li:is(.attiva, #nessuno)", True, (1, 0, 1)), (":is(main, .lista) li", True, (0, 1, 1)),
    ("li:not(.disattiva)", True, (0, 1, 1)), ("ul:has(.attiva) > li", True, (0, 1, 2)),
    (":is(#contenuto, main) .attiva", True, (1, 1, 0)), (".lista > :not(#secondo)", True, (1, 1, 0)),
    ("li:has(+ .voce)", True, (0, 1, 1)), ("#contenuto :where(li)", True, (1, 0, 0)),
    ("li:not(.attiva)", False, (0, 1, 1)), (".voce:not(:first-child)", False, (0, 2, 0)),
    ("#contenuto li + li", False, (1, 0, 2)),
]
COLORI = ["red", "blue", "green", "orange", "purple", "teal"]


@famiglia("c14-cascata", CAP, "pseudo-classi funzionali", varianti=6)
def _cascata(rng):
    while True:
        scelte = rng.sample(REGOLE, 4)
        valide = [r for r in scelte if r[1]]
        if len(valide) >= 2:
            break
    colori = rng.sample(COLORI, 4)
    vincitore, miglior = None, None
    for i, (sel, ok, sp) in enumerate(scelte):
        if ok and (miglior is None or sp >= miglior):
            vincitore, miglior = i, sp
    css = "\n".join("%s { color: %s; }" % (sel, c) for (sel, _, _), c in zip(scelte, colori))
    giusta = colori[vincitore]
    sbagliate = [c for c in colori if c != giusta] + ["black"]
    rng.shuffle(sbagliate)
    dettagli = ", ".join("`%s` %s" % (sel, _fmt(sp) if ok else "(non seleziona l'elemento)")
                         for sel, ok, sp in scelte)
    return colore_css(
        "c14-cascata", CAP, "pseudo-classi funzionali", css, CORPO_LISTA, "#primo", giusta,
        sbagliate,
        spiegazione="Specificità delle regole: %s. Vince la specificità più alta fra le regole "
                    "che selezionano l'elemento (a parità, l'ultima nel foglio di stile): "
                    "`%s`." % (dettagli, scelte[vincitore][0]),
        rif=R % "La specificità delle pseudo-classi funzionali")


d(_cascata)


# ----------------------------------------------------------------------
# Famiglia: custom property
CORPO_TEMA = """<div class="tema">
  <p class="nota" id="dentro">Avviso</p>
</div>
<p class="nota" id="fuori">Altro avviso</p>"""
VARIANTI_VAR = [
    (":root { --colore: blue; }\n.tema { --colore: red; }\n.nota { color: var(--colore, green); }",
     "#dentro", "red",
     "La custom property è ereditata: il paragrafo dentro `.tema` riceve `red` dal suo "
     "genitore, che sovrascrive il valore di `:root`. Il valore di riserva serve solo se la "
     "proprietà non è definita."),
    (":root { --colore: blue; }\n.tema { --colore: red; }\n.nota { color: var(--colore, green); }",
     "#fuori", "blue",
     "Il paragrafo fuori da `.tema` eredita `--colore` da `:root` (attraverso `body`): `blue`."),
    (".tema { --colore: red; }\n.nota { color: var(--accento, green); }", "#dentro", "green",
     "`--accento` non è definita da nessuna parte: `var()` usa il valore di riserva, `green`."),
    ("@property --colore {\n  syntax: \"<color>\";\n  inherits: false;\n  initial-value: teal;\n}\n"
     ".tema { --colore: red; }\n.nota { color: var(--colore, green); }", "#dentro", "teal",
     "Con `@property` e `inherits: false` la proprietà non viene ereditata: il paragrafo non la "
     "dichiara, quindi vale il valore iniziale registrato, `teal` (il valore di riserva non "
     "serve, perché la proprietà ha comunque un valore)."),
    (".tema { --Colore: red; }\n.nota { color: var(--colore, green); }", "#dentro", "green",
     "I nomi delle custom property distinguono maiuscole e minuscole: `--Colore` e `--colore` "
     "sono due proprietà diverse, e la seconda non è definita. Si usa il valore di riserva."),
    (".tema { --colore: red; }\n.nota {\n  --colore: orange;\n  color: var(--colore);\n}",
     "#dentro", "orange",
     "Il paragrafo dichiara lui stesso `--colore`: il valore dichiarato prevale su quello "
     "ereditato dal genitore, come per ogni altra proprietà."),
]


@famiglia("c14-var", CAP, "custom property", varianti=4)
def _var(rng):
    css, bersaglio, giusta, perche = rng.choice(VARIANTI_VAR)
    presenti = [c for c in ["red", "blue", "green", "teal", "orange"] if c in css]
    sbagliate = [c for c in presenti if c != giusta] + ["black"]
    if len(sbagliate) < 3:
        sbagliate += [c for c in ["blue", "teal", "red"] if c != giusta and c not in sbagliate]
    rng.shuffle(sbagliate)
    return colore_css(
        "c14-var", CAP, "custom property", css, CORPO_TEMA, bersaglio, giusta, sbagliate[:4],
        testo="Si consideri il seguente foglio di stile, applicato alla pagina il cui `<body>` è "
              "riportato di seguito. Qual è il colore finale dell'elemento `%s`?" % bersaglio,
        spiegazione=perche,
        rif=R % "Custom properties")


d(_var)


# ----------------------------------------------------------------------
# Famiglia: calc(), min(), max(), clamp()
@famiglia("c14-calc", CAP, "valori calcolati", varianti=5)
def _calc(rng):
    w = rng.choice([200, 300, 400, 500])
    forma = rng.choice(["calc", "calc-senza-spazi", "min", "max", "clamp"])
    n = rng.choice([20, 40, 60])
    m = rng.choice([100, 150, 250])
    if forma == "calc":
        valore, giusta = "calc(100%% - %dpx)" % n, w - n
        altri = [w, n, w + n, w - 2 * n]
    elif forma == "calc-senza-spazi":
        valore, giusta = "calc(100%%-%dpx)" % n, w
        altri = [w - n, n, w + n, 0]
    elif forma == "min":
        valore, giusta = "min(%dpx, 100%% - 2rem)" % m, min(m, w - 32)
        altri = [max(m, w - 32), m, w - 32, w - 2, w]
    elif forma == "max":
        valore, giusta = "max(%dpx, 50%%)" % m, max(m, w // 2)
        altri = [min(m, w // 2), m, w // 2, w, m + w // 2]
    else:
        lo, hi = rng.choice([(120, 220), (150, 300), (100, 180)])
        valore, giusta = "clamp(%dpx, 50%%, %dpx)" % (lo, hi), min(max(lo, w // 2), hi)
        altri = [lo, hi, w // 2, w, (lo + hi) // 2]
    css = ".contenitore {\n  width: %dpx;\n}\n.elemento {\n  width: %s;\n}" % (w, valore)
    sbagliate = []
    # gli errori tipici, poi valori vicini se gli errori coincidono con la risposta
    for a in altri + [w, w // 2, m, w - 32, giusta + 32, giusta - 20, giusta + 50]:
        t = "`%dpx`" % a
        if a > 0 and a != giusta and t not in sbagliate:
            sbagliate.append(t)
    sbagliate = sbagliate[:5]
    rng.shuffle(sbagliate)
    return chiusa(
        "c14-calc", CAP, "valori calcolati",
        "Si considerino le regole seguenti, applicate a un `div` di classe `elemento` contenuto "
        "in un `div` di classe `contenitore`. Quanto è largo l'elemento (con `1rem` pari a "
        "16px)?",
        "`%dpx`" % giusta, sbagliate[:5],
        codice=L("css", css),
        spiegazione="Nella proprietà `width` le percentuali si riferiscono alla larghezza del "
                    "contenitore (%dpx). `min()` e `max()` scelgono il più piccolo e il più grande "
                    "degli argomenti, `clamp(minimo, preferito, massimo)` vincola il valore "
                    "preferito fra i due estremi. Dentro `calc()` gli operatori `+` e `-` vanno "
                    "circondati da spazi: senza, la dichiarazione non è valida e viene scartata, "
                    "e il `div` resta largo quanto il contenitore." % w,
        rif=R % "Valori calcolati",
        verifica=dict(tipo="dom",
                      html=_pagina(css, '<div class="contenitore"><div class="elemento">x</div>'
                                        '</div>'),
                      espressione="String(Math.round(document.querySelector('.elemento')"
                                  ".getBoundingClientRect().width))",
                      atteso=str(giusta)))


d(_calc)


# ----------------------------------------------------------------------
# Famiglia: la scorciatoia flex
def _cresci(w, basi, fattori):
    libero = w - sum(basi)
    return [b + libero * f / sum(fattori) for b, f in zip(basi, fattori)]


def _restringi(w, basi, fattori):
    mancante = sum(basi) - w
    pesi = [f * b for f, b in zip(fattori, basi)]
    return [b - mancante * p / sum(pesi) for b, p in zip(basi, pesi)]


CASI_FLEX = [  # larghezza, (grow, shrink, basis) per i tre elementi
    (500, [(1, 1, 100), (1, 1, 100), (1, 1, 100)]),
    (500, [(2, 1, 100), (1, 1, 100), (1, 1, 100)]),
    (500, [(0, 1, 100), (1, 1, 100), (1, 1, 100)]),
    (600, [(1, 1, 200), (1, 1, 100), (2, 1, 0)]),
    (300, [(1, 1, 200), (1, 1, 200), (1, 1, 200)]),
    (300, [(1, 0, 200), (1, 1, 200), (1, 1, 200)]),
    (300, [(1, 2, 200), (1, 1, 200), (1, 1, 200)]),
    (400, [(1, 1, 300), (1, 1, 100), (1, 1, 200)]),
]


@famiglia("c14-flex", CAP, "flex e gap", varianti=4)
def _flex(rng):
    w, elementi = rng.choice(CASI_FLEX)
    basi = [b for _, _, b in elementi]
    if sum(basi) <= w:
        reale = _cresci(w, basi, [g for g, _, _ in elementi])
        errori = [[w * g / sum(g_ for g_, _, _ in elementi) for g, _, _ in elementi],
                  [b + (w - sum(basi)) / 3 for b in basi], basi]
    else:
        fattori = [s for _, s, _ in elementi]
        reale = _restringi(w, basi, fattori)
        mancante = sum(basi) - w
        errori = [[b - mancante * s / sum(fattori) for b, s in zip(basi, fattori)],
                  [w / 3] * 3, basi]
    errori.append(reale[::-1])

    def fmt(valori):
        return "`%gpx`, `%gpx` e `%gpx`" % tuple(round(v, 1) for v in valori)

    giusta = fmt(reale)
    sbagliate = []
    for e in errori:
        if fmt(e) != giusta and fmt(e) not in sbagliate and all(v >= 0 for v in e):
            sbagliate.append(fmt(e))
    for delta in ([20, -10, -10], [-10, 20, -10], [10, 10, -20]):
        if len(sbagliate) >= 4:
            break
        t = fmt([r + x for r, x in zip(reale, delta)])
        if t != giusta and t not in sbagliate:
            sbagliate.append(t)
    css = (".contenitore {\n  display: flex;\n  width: %dpx;\n}\n" % w +
           "\n".join(".%s { flex: %d %d %dpx; }" % (n, g, s, b)
                     for n, (g, s, b) in zip("abc", elementi)))
    return chiusa(
        "c14-flex", CAP, "flex e gap",
        "Un contenitore di classe `contenitore` ha tre figli vuoti, nell'ordine di classe `a`, "
        "`b` e `c`, a cui si applicano le regole seguenti. Quanto sono larghi, "
        "rispettivamente, i tre figli?",
        giusta, sbagliate[:5],
        codice=L("css", css),
        spiegazione="`flex: grow shrink basis`: si parte dalle basi (qui %s, in tutto %dpx) e le "
                    "si confronta con il contenitore (%dpx). Lo spazio che avanza si distribuisce "
                    "in proporzione a `flex-grow`; quello che manca si toglie in proporzione a "
                    "`flex-shrink` **moltiplicato per la base**." % (
                        ", ".join("%dpx" % b for b in basi), sum(basi), w),
        rif=R % "La scorciatoia flex",
        verifica=dict(tipo="dom",
                      html=_pagina(css, '<div class="contenitore"><div class="a"></div>'
                                        '<div class="b"></div><div class="c"></div></div>'),
                      espressione="['.a', '.b', '.c'].map(s => Math.round(document."
                                  "querySelector(s).getBoundingClientRect().width * 10) / 10)"
                                  ".join(',')",
                      atteso=",".join("%g" % round(v, 1) for v in reale)))


d(_flex)


# ----------------------------------------------------------------------
# Famiglia: container query
@famiglia("c14-container", CAP, "container query", varianti=4)
def _container(rng):
    w_main, w_aside = rng.choice([(350, 200), (500, 250), (280, 400), (250, 220)])
    contenitori = rng.choice([["aside"], ["main"], ["main", "aside"]])
    regola = rng.choice(["@container", "@container", "@media"])
    css = ".card { background-color: lightblue; }\n"
    css += "".join("%s { container-type: inline-size; }\n" % c for c in contenitori)
    css += ("%s (max-width: 300px) {\n  .card { background-color: lightgreen; }\n}" % regola)
    corpo = ('<main style="width: %dpx">\n  <div class="card">Main</div>\n</main>\n'
             '<aside style="width: %dpx">\n  <div class="card">Aside</div>\n</aside>'
             % (w_main, w_aside))

    def verde(nome, larghezza):
        return regola == "@container" and nome in contenitori and larghezza <= 300

    nomi = {True: "verde (`lightgreen`)", False: "azzurro (`lightblue`)"}
    esito = (verde("main", w_main), verde("aside", w_aside))
    combinazioni = [(a, b) for a in (False, True) for b in (False, True)]

    def testo(c):
        return "Nel `<main>` %s, nell'`<aside>` %s." % (nomi[c[0]], nomi[c[1]])

    rgb = {True: "rgb(144, 238, 144)", False: "rgb(173, 216, 230)"}
    return chiusa(
        "c14-container", CAP, "container query",
        "Si consideri il seguente foglio di stile, applicato alla pagina riportata di seguito e "
        "visualizzata in una finestra larga 1000px. Di che colore è lo sfondo delle due card?",
        testo(esito), [testo(c) for c in combinazioni if c != esito],
        codice=[L("css", css), L("html", corpo)],
        spiegazione="Una media query osserva il **viewport**, che qui è largo 1000px. Una "
                    "container query osserva il contenitore più vicino, cioè l'antenato con "
                    "`container-type`, e vale per i suoi **discendenti**: una card diventa verde "
                    "solo se sta in un contenitore largo al più 300px.",
        rif=R % "Container query",
        verifica=dict(tipo="dom", html=_pagina(css, corpo),
                      espressione="[...document.querySelectorAll('.card')].map(c => "
                                  "getComputedStyle(c).backgroundColor).join(';')",
                      atteso="%s;%s" % (rgb[esito[0]], rgb[esito[1]])))


d(_container)


# ----------------------------------------------------------------------
# Famiglia: annidamento nativo
NIDO = """.card {
  color: black;

  p {
    color: green;
  }

  & > h2 {
    color: red;
  }

  .scuro & {
    color: white;
  }
}"""
CORPO_NIDO = """<section class="scuro">
  <div class="card">
    <h2>Titolo</h2>
    <p>Testo <span>bis</span></p>
    <small>Nota</small>
  </div>
</section>"""
BERSAGLI_NIDO = [
    ("h2", "red", "`& > h2` equivale a `.card > h2`: il titolo è rosso."),
    ("span", "green", "`p` annidato equivale a `.card p`; lo `span` non ha regole proprie ed "
                      "eredita il colore del paragrafo, `green`."),
    ("small", "white", "`.scuro &` equivale a `.scuro .card`, con specificità (0, 2, 0): batte "
                       "`.card` (0, 1, 0) e la card diventa bianca; lo `small` ne eredita il "
                       "colore."),
]


@famiglia("c14-annidamento", CAP, "annidamento", varianti=3)
def _annidamento(rng):
    bersaglio, giusta, perche = rng.choice(BERSAGLI_NIDO)
    sbagliate = [c for c in ["black", "red", "green", "white"] if c != giusta]
    return colore_css(
        "c14-annidamento", CAP, "annidamento", NIDO, CORPO_NIDO, bersaglio, giusta, sbagliate,
        testo="Si consideri il seguente foglio di stile, che usa l'annidamento nativo, applicato "
              "alla pagina il cui `<body>` è riportato di seguito. Qual è il colore finale "
              "dell'elemento `%s`?" % bersaglio,
        spiegazione="Una regola annidata senza `&` si combina con quella esterna come "
                    "**discendente**; `&` si riferisce esplicitamente al selettore della regola "
                    "genitore, e può stare anche in fondo (`.scuro &`). " + perche,
        rif=R % "Annidamento nativo")


d(_annidamento)

# ----------------------------------------------------------------------
d(colore_css("c14-has", CAP, "pseudo-classi funzionali",
             "li { color: black; }\nli:has(+ .scelta) { color: red; }\n"
             "ol:has(.attiva) li { color: blue; }",
             """<ol>
  <li id="a">A</li>
  <li class="scelta">B</li>
  <li class="attiva">C</li>
</ol>""", "#a", "blue", ["red", "black", "green"],
             spiegazione="Entrambe le regole colorate selezionano `#a`: `li:has(+ .scelta)` perché "
                         "il suo fratello immediatamente successivo ha la classe `scelta` "
                         "(specificità (0, 1, 1)), `ol:has(.attiva) li` perché l'elenco contiene "
                         "un elemento `.attiva` (specificità (0, 1, 2)). Vince la seconda.",
             rif=R % ":has()"))

d(colore_css("c14-commento", CAP, "pseudo-classi funzionali",
             "ol:has(.attiva) {\n  // gli elenchi con un elemento attivo\n"
             "  background-color: lightgray;\n  color: navy;\n}",
             """<ol>
  <li>A</li>
  <li class="attiva">B</li>
</ol>""", "ol", "transparent", ["lightgray", "navy", "white"],
             testo="Si consideri il seguente foglio di stile, applicato alla pagina il cui "
                   "`<body>` è riportato di seguito. Qual è il colore di sfondo finale "
                   "dell'elemento `ol`?",
             proprieta="background-color",
             spiegazione="In CSS i commenti si scrivono solo con `/* */`. `//` viene letto come "
                         "l'inizio di una dichiarazione non valida, che arriva fino al primo punto "
                         "e virgola: viene scartata insieme a `background-color`. Lo sfondo resta "
                         "quello predefinito, trasparente (`color: navy` invece si applica).",
             rif=R % ":has()"))

d(chiusa("c14-viewport", CAP, "unità del viewport",
         "Su uno smartphone la barra degli indirizzi compare e scompare durante lo scorrimento. "
         "Quale unità corrisponde all'altezza del viewport **corrente**, che cambia di "
         "conseguenza?",
         "`dvh`",
         ["`svh`", "`lvh`", "`vw`", "`vmin`", "`rem`"],
         spiegazione="`svh` è l'altezza con i controlli del browser visibili (la più piccola), "
                     "`lvh` quella con i controlli nascosti (la più grande, come `vh`), `dvh` "
                     "l'altezza corrente, che passa dall'una all'altra mentre si scorre.",
         rif=R % "L'altezza del viewport sui dispositivi mobili"))

d(chiusa("c14-flex-valori", CAP, "flex e gap",
         "A quale terna di `flex-grow`, `flex-shrink` e `flex-basis` equivale `flex: 1`?",
         "`1 1 0%`",
         ["`1 1 auto`", "`1 0 auto`", "`0 1 auto`", "`1 0 0%`", "`0 0 auto`"],
         spiegazione="`flex: 1` equivale a `1 1 0%`: base nulla, quindi tutto lo spazio viene "
                     "diviso in parti uguali, indipendentemente dal contenuto. `flex: auto` è "
                     "`1 1 auto`, `flex: none` è `0 0 auto`, e il valore iniziale è `0 1 auto`.",
         rif=R % "La scorciatoia flex"))

d(chiusa("c14-gap", CAP, "flex e gap",
         "Un contenitore flex ha `gap: 30px` e `padding: 10px`. Dove si trova lo spazio di 30px?",
         "Solo fra un figlio e l'altro (anche fra le righe, se vanno a capo), mai fra i figli "
         "e il bordo del contenitore.",
         ["Attorno a ogni figlio, anche verso il bordo del contenitore.",
          "Solo fra il primo figlio e il bordo sinistro del contenitore.",
          "Fra il bordo e il contenuto del contenitore, come il padding.",
          "Solo fra le righe, quando i figli vanno a capo.",
          "`gap` funziona solo con Grid: nel contenitore flex non ha effetto."],
         spiegazione="`gap` si usa sia con Grid sia con Flexbox e aggiunge spazio solo fra gli "
                     "elementi; verso il bordo provvede il `padding` del contenitore.",
         rif=R % "gap con Grid e Flexbox"))

d(chiusa("c14-srcset", CAP, "immagini responsive",
         "Un'immagine larga quanto il viewport ha `srcset=\"foto-400.jpg 400w, foto-800.jpg 800w, "
         "foto-1200.jpg 1200w\"`. Quale file scaricherà presumibilmente uno smartphone con un "
         "viewport largo 375px e densità di pixel 2?",
         "`foto-800.jpg`",
         ["`foto-400.jpg`", "`foto-1200.jpg`", "Tutti e tre i file, poi sceglie.",
          "Il file indicato in `src`, perché `srcset` vale solo sui desktop."],
         spiegazione="Senza `sizes` l'immagine si considera larga `100vw`: servono 375 · 2 = 750 "
                     "pixel, e il candidato più adatto è quello da 800. Il browser scarica solo "
                     "il file scelto; `src` resta il valore di riserva per chi non supporta "
                     "`srcset`.",
         rif=R % "srcset"))

d(chiusa("c14-picture", CAP, "immagini responsive",
         "Quali delle seguenti affermazioni sull'elemento `<picture>` sono **vere**?",
         ["Il browser usa il primo `<source>` la cui media query è vera.",
          "Se nessuna media query è vera, viene usato il file dell'`<img>`.",
          "L'`<img>` è obbligatoria: è l'elemento che viene davvero mostrato.",
          "Permette l'*art direction*: versioni diverse dell'immagine per condizioni diverse."],
         ["Il browser scarica tutti i file indicati e poi sceglie il migliore.",
          "Il browser usa l'ultimo `<source>` la cui media query è vera.",
          "Se c'è almeno un `<source>`, l'`<img>` viene ignorata.",
          "Funziona solo con immagini dello stesso formato e dello stesso ritaglio."],
         multi=True,
         spiegazione="I `<source>` cambiano solo il file dell'`<img>`, che resta l'elemento "
                     "mostrato; si usa il primo `<source>` adatto, altrimenti il file "
                     "dell'`<img>`, e viene scaricato solo il file scelto. L'*art direction* "
                     "sceglie il contenuto più adatto (per esempio un ritaglio diverso), non solo "
                     "la risoluzione.",
         rif=R % "picture e art direction"))

d(chiusa("c14-prefers", CAP, "preferenze dell'utente",
         "Quale media query applica degli stili solo agli utenti che hanno chiesto, nelle "
         "impostazioni, di ridurre le animazioni?",
         "`@media (prefers-reduced-motion: reduce)`",
         ["`@media (prefers-reduced-motion: reduced)`", "`@media (prefers-color-scheme: dark)`",
          "`@media (reduce-motion: true)`", "`@media (prefers-contrast: more)`",
          "`@supports (animation: none)`"],
         spiegazione="Le media query sulle preferenze dell'utente riflettono le impostazioni del "
                     "browser o del sistema: `prefers-reduced-motion`, `prefers-color-scheme`, "
                     "`prefers-contrast`, `prefers-reduced-transparency`. Il valore è `reduce`: "
                     "con `reduced` la media query non è valida e viene ignorata.",
         rif=R % "Media query sulle preferenze dell'utente"))

d(chiusa("c14-supports", CAP, "preferenze dell'utente",
         "A che cosa serve la regola `@supports (display: grid) { ... }`?",
         "Ad applicare gli stili che contiene solo se il browser supporta `display: grid`, "
         "lasciando agli altri le regole di riserva.",
         ["A caricare una libreria che aggiunge il supporto per Grid ai browser vecchi.",
          "Ad applicare gli stili solo se l'elemento ha già `display: grid`.",
          "A segnalare un errore nella console se il browser non supporta Grid.",
          "A trasformare automaticamente i layout Flexbox in Grid.",
          "Ad applicare gli stili solo sugli schermi larghi."],
         spiegazione="`@supports` verifica il supporto di una proprietà con un certo valore. "
                     "Prima si scrive una regola che funziona ovunque, poi la si arricchisce dove "
                     "possibile: è il *progressive enhancement*.",
         rif=R % "@supports"))

d(chiusa("c14-amp", CAP, "annidamento",
         "Dentro la regola `.card { ... }`, che differenza c'è fra la regola annidata "
         "`&:hover { ... }` e la regola annidata `:hover { ... }`?",
         "La prima equivale a `.card:hover` (la card sotto il puntatore), la seconda a "
         "`.card :hover` (un qualunque discendente della card sotto il puntatore).",
         ["Nessuna: in entrambi i casi il selettore è `.card:hover`.",
          "La prima equivale a `.card :hover`, la seconda a `.card:hover`.",
          "La seconda non è valida: le pseudo-classi non si possono annidare.",
          "La prima vale solo per il primo figlio della card.",
          "La seconda vale per qualunque elemento della pagina sotto il puntatore."],
         spiegazione="Senza `&` un selettore annidato si combina con quello esterno come "
                     "**discendente**. `&` rappresenta il selettore della regola genitore e "
                     "serve quando la regola riguarda l'elemento stesso o un combinatore diverso "
                     "dallo spazio: tutta la differenza sta in uno spazio.",
         rif=R % "Il selettore &"))

# ----------------------------------------------------------------------
# Domande aperte
d(aperta("c14-a-pseudoclassi", CAP, "pseudo-classi funzionali",
         "Si descrivano le pseudo-classi funzionali `:is()`, `:where()`, `:not()` e `:has()`, "
         "con un esempio d'uso ciascuna, e le regole con cui contribuiscono alla specificità.",
         ["`:is()` raggruppa selettori alternativi (es. `:is(header, main, footer) a em`); "
          "`:where()` fa lo stesso ma con specificità zero, utile per stili predefiniti facili "
          "da sovrascrivere.",
          "`:not()` esclude gli elementi che corrispondono ad almeno un argomento (es. "
          "`li:not(.selected, .active)`).",
          "`:has()` seleziona in base a discendenti o elementi collegati, con selettori relativi "
          "(es. `ol:has(.active)`, `li:has(+ .selected)`).",
          "Specificità: non contano come pseudo-classi; `:where()` vale zero; le altre valgono "
          "quanto il loro argomento più specifico, qualunque sia quello che seleziona "
          "l'elemento."],
         rif=R % "Selettori moderni"))

d(aperta("c14-a-custom", CAP, "custom property",
         "Che cosa sono le *custom property* del CSS? Se ne descrivano dichiarazione e uso, il "
         "rapporto con cascata ed ereditarietà, i valori di riserva e la regola `@property`.",
         ["Valori definiti da chi scrive il foglio di stile e riutilizzabili: nome con due "
          "trattini (`--primary-color: #663399`, maiuscole significative), letti con `var()`.",
          "Partecipano alla cascata, sono ereditate e si possono sovrascrivere: definite in "
          "`:root` valgono per tutta la pagina, ridefinite in un elemento valgono per i suoi "
          "discendenti (temi, modalità scura con una media query).",
          "`var(--nome, riserva)`: il secondo argomento si usa se la proprietà non è definita.",
          "`@property` registra la proprietà con tipo (`syntax`), ereditarietà (`inherits`) e "
          "valore iniziale (`initial-value`)."],
         rif=R % "Custom properties"))

d(aperta("c14-a-container", CAP, "container query",
         "Che limite delle media query superano le *container query*? Si mostri con un esempio "
         "come si dichiara un contenitore e come si scrive una query.",
         ["Le media query osservano il viewport: un componente (es. una card) non può adattarsi "
          "allo spazio del contenitore in cui si trova, grande o piccolo che sia.",
          "Le container query permettono di dare stile a un componente in base alle dimensioni "
          "di un suo antenato, il contenitore.",
          "Il contenitore si dichiara con `container-type: inline-size` (si interroga sulla "
          "larghezza).",
          "Le query si scrivono con `@container (max-width: 300px) { ... }` e valgono per i "
          "discendenti del contenitore più vicino, non per il contenitore stesso."],
         rif=R % "Container query"))

d(aperta("c14-a-immagini", CAP, "immagini responsive",
         "Perché servono le immagini responsive? Si descrivano l'attributo `srcset` (con i due "
         "tipi di descrittori e l'attributo `sizes`) e l'elemento `<picture>`.",
         ["Scaricare un'immagine ad alta risoluzione per rimpicciolirla su uno schermo piccolo "
          "spreca byte: si forniscono più file (candidati) e il browser scarica solo quello "
          "adatto.",
          "`srcset` con descrittori di larghezza (`800w`, la larghezza del file) o di densità "
          "(`2x`); `src` resta il valore di riserva.",
          "`sizes` dice quanto sarà larga l'immagine (predefinito `100vw`): larghezza per "
          "densità dà i pixel necessari, e il browser sceglie il candidato più adatto.",
          "`<picture>` con più `<source media=... srcset=...>` e un'`<img>` obbligatoria: si usa "
          "il primo `<source>` adatto; serve per l'*art direction* (contenuti diversi, non solo "
          "risoluzioni)."],
         rif=R % "Immagini responsive"))
