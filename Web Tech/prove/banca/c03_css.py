"""Capitolo 3: CSS (regole, inclusione, selettori, combinatori, pseudo-classi,
pseudo-elementi, cascata, specificità, ereditarietà)."""

import json

from generatore import FONTE_2024, FONTE_AULA, L, aperta, chiusa, colore_css, famiglia

CAP = 3
R = "cap. 3, «%s»"

DOMANDE = []
d = DOMANDE.append

COLORI = ["red", "blue", "green", "yellow", "pink", "black", "orange", "purple", "gray",
          "brown"]

# ----------------------------------------------------------------------
# Un piccolo modello della cascata per un documento fisso:
#     <body><div id=C class=B><h1 class="F T" id=G ...>Hi!</h1></div></body>
# Per ogni selettore: (testo con i segnaposto, corrisponde all'h1?, specificità)
SELETTORI = [
    ("h1", True, (0, 0, 1)), (".F", True, (0, 1, 0)), (".T", True, (0, 1, 0)),
    ("#G", True, (1, 0, 0)), ("div h1", True, (0, 0, 2)), ("div > h1", True, (0, 0, 2)),
    ("body h1", True, (0, 0, 2)), ("#C h1", True, (1, 0, 1)), (".B h1", True, (0, 1, 1)),
    ("h1.F", True, (0, 1, 1)), (".F.T", True, (0, 2, 0)), ("#C h1.F", True, (1, 1, 1)),
    ("#C > .T", True, (1, 1, 0)), ("div#C h1", True, (1, 0, 2)), ("body #G", True, (1, 0, 1)),
    ("#C #G", True, (2, 0, 0)), ("h1[id]", True, (0, 1, 1)), ("div *", True, (0, 0, 1)),
    ("div.B h1.F", True, (0, 2, 2)), (".B #G", True, (1, 1, 0)),
    # trappole: sembrano riferirsi all'h1, ma non lo selezionano
    ("h1 .F", False, (0, 1, 1)), (".F h1", False, (0, 1, 1)), ("#G h1", False, (1, 0, 1)),
    ("div.F", False, (0, 1, 1)), ("h1#C", False, (1, 0, 1)), ("body > h1", False, (0, 0, 2)),
    (".T .F", False, (0, 2, 0)), ("span.F", False, (0, 1, 1)),
]
NOMI = [("cont", "box", "g", "f", "t"), ("x", "y", "z", "w", "k"), ("main", "in", "t1", "big", "s"),
        ("c", "b", "a", "f", "h")]


def _sostituisci(testo, nomi):
    C, B, G, F, T = nomi
    out = ""
    i = 0
    while i < len(testo):
        ch = testo[i]
        if ch in "#." and i + 1 < len(testo) and testo[i + 1] in "CBGFT":
            out += ch + {"C": C, "B": B, "G": G, "F": F, "T": T}[testo[i + 1]]
            i += 2
        else:
            out += ch
            i += 1
    return out


def _spec(s):
    return "(%d, %d, %d)" % s


def vincitore(regole, inline):
    """regole: lista di (selettore, corrisponde, specificità, colore, importante).
    inline: colore dello stile inline o None. Restituisce (colore, spiegazione)."""
    valide = [(i, r) for i, r in enumerate(regole) if r[1]]
    importanti = [(i, r) for i, r in valide if r[4]]
    if importanti:
        gruppo = importanti
        motivo = "Le dichiarazioni `!important` stanno in un bucket più prioritario di " \
                 "quello delle dichiarazioni normali, stile inline compreso"
    elif inline:
        return inline, ("Nessuna dichiarazione è `!important`, quindi vince lo stile inline "
                        "(attributo `style`), che sta in un livello più prioritario dei fogli "
                        "di stile, qualunque sia la specificità dei selettori.")
    else:
        gruppo = valide
        motivo = "Non ci sono dichiarazioni `!important` né stili inline"
    migliore = max(s for _, (_, _, s, _, _) in gruppo)
    pari = [(i, r) for i, r in gruppo if r[2] == migliore]
    i, r = pari[-1]
    testo = "%s: fra le regole rimaste vince la specificità più alta, %s (`%s`)" % (
        motivo, _spec(migliore), r[0])
    if len(pari) > 1:
        testo += ", a pari merito con altre regole: vince l'ultima nell'ordine del foglio"
    return r[3], testo + "."


@famiglia("c03-cascata", CAP, "cascata e specificità", varianti=6)
def _cascata(rng):
    nomi = rng.choice(NOMI)
    buone = [s for s in SELETTORI if s[1]]
    trappole = [s for s in SELETTORI if not s[1]]
    scelti = rng.sample(buone, 4) + rng.sample(trappole, 1)
    if rng.random() < 0.4:
        scelti = rng.sample(buone, 3) + rng.sample(trappole, 2)
    rng.shuffle(scelti)
    colori = rng.sample(COLORI, len(scelti) + 1)
    con_inline = rng.random() < 0.7
    inline = colori[-1] if con_inline else None
    n_imp = rng.choice([0, 1, 1, 2, 2])
    importanti = set(rng.sample(range(len(scelti)), n_imp))
    regole = []
    for i, (sel, ok, spec) in enumerate(scelti):
        regole.append((_sostituisci(sel, nomi), ok, spec, colori[i], i in importanti))
    colore, perche = vincitore(regole, inline)

    C, B, G, F, T = nomi
    css = "\n".join("%s { color: %s%s; }" % (sel, col, " !important" if imp else "")
                    for sel, _, _, col, imp in regole)
    stile = ' style="color: %s;"' % inline if inline else ""
    html = ('<body><div id="%s" class="%s">\n  <h1 class="%s %s" id="%s"%s>\n    Hi!\n'
            '  </h1>\n</div></body>' % (C, B, F, T, G, stile))
    opzioni = [c for _, _, _, c, _ in regole] + ([inline] if inline else [])
    if len(opzioni) < 6:
        opzioni += [c for c in COLORI if c not in opzioni][:6 - len(opzioni)]
    sbagliate = [c for c in opzioni if c != colore]
    dettagli = "; ".join("`%s` %s" % (sel, _spec(spec) if ok else "non seleziona l'`h1`")
                         for sel, ok, spec, _, _ in regole)
    return colore_css(
        "c03-cascata", CAP, "cascata e specificità", css, html, "h1", colore, sbagliate,
        n=6,
        spiegazione="%s Le regole: %s." % (perche, dettagli),
        rif=R % "La cascata")


d(_cascata)

# ----------------------------------------------------------------------
# Famiglia: quale selettore ha la specificità più alta?
# Documento: <div id="cont" class="box"><ul class="lst"><li class="it" id="x">
#            <a href="#" class="lnk">link</a></li></ul></div>
SEL_A = [
    ("a", (0, 0, 1)), (".lnk", (0, 1, 0)), ("li a", (0, 0, 2)), ("#x a", (1, 0, 1)),
    ("ul.lst li a", (0, 1, 3)), ("#cont .lnk", (1, 1, 0)), ("div ul li a", (0, 0, 4)),
    ("a[href]", (0, 1, 1)), ("li:first-child a", (0, 1, 2)), ("ul > li > a", (0, 0, 3)),
    ("#cont #x a", (2, 0, 1)), (".box .lst .it .lnk", (0, 4, 0)), ("div#cont a.lnk", (1, 1, 2)),
    (".it > .lnk", (0, 2, 0)), ("#x", None), ("body *", (0, 0, 1)),
    (".box .lst li a[href]", (0, 3, 2)), ("#x .lnk", (1, 1, 0)),
]
DOC_A = ('<body><div id="cont" class="box"><ul class="lst">\n'
         '<li class="it" id="x"><a href="#" class="lnk">link</a></li>\n</ul></div></body>')


@famiglia("c03-specificita", CAP, "cascata e specificità", varianti=4)
def _specificita(rng):
    validi = [s for s in SEL_A if s[1] is not None]
    while True:
        scelti = rng.sample(validi, 4)
        spec = sorted((s[1] for s in scelti), reverse=True)
        if spec[0] != spec[1]:
            break
    vincente = max(scelti, key=lambda s: s[1])
    altri = [s for s in scelti if s is not vincente]
    # per la verifica: il vincitore per primo, così l'ordine non lo aiuta
    colori = rng.sample(COLORI, 4)
    css = "\n".join("%s { color: %s; }" % (s[0], c)
                    for s, c in zip([vincente] + altri, colori))
    elenco = ", ".join("`%s` %s" % (s[0], _spec(s[1])) for s in scelti)
    return chiusa(
        "c03-specificita", CAP, "cascata e specificità",
        "Quale dei seguenti selettori ha la **specificità** più alta?",
        "`%s`" % vincente[0], ["`%s`" % s[0] for s in altri], n=4,
        spiegazione="La specificità si confronta componente per componente: prima il numero "
                    "di id, poi quello di classi, attributi e pseudo-classi, poi quello di "
                    "tipi di elemento; non è un numero a tre cifre (una classe batte qualunque "
                    "numero di tipi, un id qualunque numero di classi). Combinatori e `*` non "
                    "contano. Qui: %s." % elenco,
        rif=R % "Specificità",
        # verifica: il vincitore è scritto per primo, quindi l'ordine non lo aiuta;
        # il colore calcolato deve essere il suo
        verifica=dict(tipo="css", css=css, html=DOC_A, selettore="a", proprieta="color",
                      atteso=colori[0], candidati=colori),
    )


d(_specificita)

# ----------------------------------------------------------------------
# Famiglia: :nth-child
ESPRESSIONI = [("2", 0, 2), ("odd", 2, 1), ("even", 2, 0), ("2n+1", 2, 1), ("2n", 2, 0),
               ("3n", 3, 0), ("3n+1", 3, 1), ("n+4", 1, 4), ("-n+3", -1, 3), ("2n+3", 2, 3),
               ("4n-1", 4, -1), ("3n+2", 3, 2)]


def _posizioni(a, b, n):
    out = []
    for p in range(1, n + 1):
        if a == 0:
            ok = p == b
        else:
            k = (p - b) / a
            ok = k >= 0 and k == int(k)
        if ok:
            out.append(p)
    return out


def _descrivi(pos):
    if not pos:
        return "Nessun elemento."
    if len(pos) == 1:
        return "Solo l'elemento in posizione %d." % pos[0]
    return "Gli elementi in posizione %s e %d." % (", ".join(map(str, pos[:-1])), pos[-1])


@famiglia("c03-nth-child", CAP, "pseudo-classi e :nth-child", varianti=4)
def _nth(rng):
    espr, a, b = rng.choice(ESPRESSIONI)
    n = rng.randint(6, 9)
    giuste = _posizioni(a, b, n)
    candidati = [
        [p + 1 for p in _posizioni(a, b, n + 1) if p + 1 <= n],      # contando da 0
        [p for p in _posizioni(a, b, n + 5) if p - 1 >= 1 and p - 1 <= n and p - 1 not in giuste] if a else [b + 1],
        [p for p in range(1, n + 1) if p not in giuste],              # il complemento
        [p for p in _posizioni(a, b + a, n)] if a > 0 else list(range(1, n + 1)),  # da n=1
        [p for p in range(1, n + 1) if p - 1 in giuste],              # sfasati di uno
        list(range(1, n + 1)),
    ]
    sbagliate = []
    for c in candidati:
        c = sorted(set(x for x in c if 1 <= x <= n))
        t = _descrivi(c)
        if c != giuste and t not in sbagliate:
            sbagliate.append(t)
    for extra in ([1, n], [n], [2]):
        if len(sbagliate) >= 4:
            break
        if extra != giuste and _descrivi(extra) not in sbagliate:
            sbagliate.append(_descrivi(extra))
    voci = "\n".join("  <li>%d</li>" % i for i in range(1, n + 1))
    html = "<ul>\n%s\n</ul>" % voci
    return chiusa(
        "c03-nth-child", CAP, "pseudo-classi e :nth-child",
        "Data la lista seguente, quali elementi `li` seleziona il selettore "
        "`li:nth-child(%s)`?" % espr,
        _descrivi(giuste), sbagliate[:5], n=4,
        codice=L("html", html),
        spiegazione="`:nth-child(an+b)` seleziona i figli in posizione `an+b` per n = 0, 1, 2, "
                    "...; le posizioni si contano **a partire da 1**. `odd` equivale a `2n+1` "
                    "ed `even` a `2n`. Con `%s` si ottengono le posizioni %s." % (
                        espr, ", ".join(map(str, giuste)) or "nessuna"),
        rif=R % "Relazioni di posizione",
        verifica=dict(tipo="dom",
                      html="<!DOCTYPE html><html><body>%s</body></html>" % html,
                      espressione="Array.from(document.querySelectorAll('li:nth-child(%s)'))"
                                  ".map(e => e.textContent).join(',')" % espr,
                      atteso=",".join(map(str, giuste))))


d(_nth)


@famiglia("c03-nth-misti", CAP, "pseudo-classi e :nth-child", varianti=2)
def _nth_misti(rng):
    figli = ["h2", "p", "p", "h2", "p", "p", "p"]
    rng.shuffle(figli)
    figli[0] = "h2"
    k = rng.randint(2, 6)
    giusta_el = figli[k - 1]
    # quanti p vengono selezionati da p:nth-child(k)? uno solo se il k-esimo figlio è un p
    righe = "\n".join("  <%s>%s</%s>" % (t, "Titolo" if t == "h2" else "Testo %d" % i, t)
                      for i, t in enumerate(figli, 1))
    html = '<div class="art">\n%s\n</div>' % righe
    p_numerati = [i for i, t in enumerate(figli, 1) if t == "p"]
    if giusta_el == "p":
        giusta = "Il %d° figlio del `div`, che è un paragrafo." % k
    else:
        giusta = "Nessun elemento: il %d° figlio del `div` non è un paragrafo." % k
    sbagliate = []
    if len(p_numerati) >= k:
        sbagliate.append("Il %d° paragrafo del `div`, cioè il %d° figlio." % (k, p_numerati[k - 1]))
    sbagliate += ["Tutti i paragrafi del `div` dal %d° in poi." % k,
                  "Il %d° figlio di ogni paragrafo." % k]
    if giusta_el == "p":
        sbagliate.append("Nessun elemento: `:nth-child` conta solo i paragrafi, e il %d° non "
                         "esiste." % k if len(p_numerati) < k else
                         "Nessun elemento: `:nth-child` non si può combinare con un tipo.")
    else:
        sbagliate.append("Il %d° figlio del `div`, qualunque elemento sia." % k)
    sbagliate = [s for s in sbagliate if s != giusta]
    atteso = str(k) if giusta_el == "p" else ""
    return chiusa(
        "c03-nth-misti", CAP, "pseudo-classi e :nth-child",
        "Che cosa seleziona `.art p:nth-child(%d)` nel frammento seguente?" % k,
        giusta, sbagliate[:5], n=4, codice=L("html", html),
        spiegazione="`:nth-child(k)` conta **tutti** i figli del genitore, di qualunque tipo; "
                    "poi il selettore di tipo `p` controlla che quello in posizione k sia un "
                    "paragrafo. Qui il %d° figlio è un `%s`." % (k, giusta_el),
        rif=R % "Il conteggio senza selettore di tipo",
        verifica=dict(tipo="dom",
                      html="<!DOCTYPE html><html><body>%s</body></html>" % html,
                      espressione="(() => { const s = document.querySelector('.art p:nth-child(%d)');"
                                  " return s ? String(Array.from(s.parentNode.children).indexOf(s)"
                                  " + 1) : ''; })()" % k,
                      atteso=atteso))


d(_nth_misti)

# ----------------------------------------------------------------------
# Famiglia: comporre un selettore (prima prova intercorso 2024, Es. 2)
# (descrizione della posizione, espressioni giuste, condizione sulla
#  posizione, espressioni sbagliate tipiche, pseudo-classe inventata)
POSIZIONI_VOCE = [
    ("di posto pari", ["even", "2n"], lambda p: p % 2 == 0, ["odd", "2"], "even-child"),
    ("di posto dispari", ["odd", "2n+1"], lambda p: p % 2 == 1, ["even", "1"], "odd-child"),
    ("in posizione multipla di 3", ["3n"], lambda p: p % 3 == 0, ["3", "n+3"], "third-child"),
]
LISTE = {"ul": ("non ordinata", "ol"), "ol": ("ordinata", "ul")}
CONTENUTI = {"a": "tutti i link contenuti", "img": "tutte le immagini contenute"}
SIGNIFICATI = {"odd": "seleziona le voci di posto dispari",
               "even": "seleziona le voci di posto pari",
               "1": "seleziona solo la prima voce", "2": "seleziona solo la seconda voce",
               "3": "seleziona solo la terza voce",
               "n+3": "seleziona le voci dalla terza in poi"}


def _voci(prefisso, n):
    return "\n".join('  <li><a href="#">%s%d</a> <img src="data:," alt=""></li>'
                     % (prefisso, i) for i in range(1, n + 1))


SELETTORE_HTML = ('<!DOCTYPE html><html><body>\n<p><a href="#">home</a></p>\n'
                  '<ul class="%(c)s">\n' + _voci("u", 7) + '\n</ul>\n'
                  '<ol class="%(c)s">\n' + _voci("o", 6) + '\n</ol>\n'
                  '<ul>\n' + _voci("x", 4) + '\n</ul>\n</body></html>')


@famiglia("c03-selettore-lista", CAP, "selettori", varianti=3)
def _selettore_lista(rng):
    ufficiale = rng.random() < 0.35
    if ufficiale:
        tipo, classe, voce, espr, el = "ul", "lst", POSIZIONI_VOCE[0], "even", "a"
    else:
        tipo = rng.choice(["ul", "ul", "ol"])
        classe = rng.choice(["lst", "menu", "voci", "elenco"])
        voce = rng.choice(POSIZIONI_VOCE)
        espr = rng.choice(voce[1])
        el = rng.choice(["a", "a", "img"])
    nome_lista, altro = LISTE[tipo]
    posto, _, condizione, errate, inventata = voce
    lista = "%s.%s" % (tipo, classe)
    giusta = "%s li:nth-child(%s) %s" % (lista, espr, el)
    if ufficiale:
        # le cinque alternative della prova originale
        scelte = [("ol.lst li:nth-child(even) a", ["lista"]),
                  ("ul.lst::nth-child(2) a", ["pseudo"]),
                  ("ol.lst li:even-child a", ["lista", "inventata"]),
                  ("ul.lst::nth-child(even) a", ["pseudo"]),
                  ("a li:even-child ul .lst", ["inventata", "inverso"])]
    else:
        sintassi = [  # non validi: pseudo-classi inesistenti o scritte come pseudo-elementi
            ("%s::nth-child(%s) %s" % (lista, espr, el), ["pseudo"]),
            ("%s.%s li:%s %s" % (altro, classe, inventata, el), ["lista", "inventata"]),
            ("%s li:%s %s .%s" % (el, inventata, tipo, classe), ["inventata", "inverso"]),
            ("%s li::nth-child(%s) %s" % (lista, espr, el), ["pseudo"]),
        ]
        significato = [  # validi, ma selezionano altro
            ("%s li:nth-child(%s) %s" % (lista, errate[0], el), ["errata0"]),
            ("%s li:nth-child(%s) %s" % (lista, errate[1], el), ["errata1"]),
            ("%s .%s li:nth-child(%s) %s" % (tipo, classe, espr, el), ["spazio"]),
            ("%s:nth-child(%s) %s" % (lista, espr, el), ["su-lista"]),
            ("%s %s:nth-child(%s)" % (lista, el, espr), ["su-elemento"]),
            ("%s#%s li:nth-child(%s) %s" % (tipo, classe, espr, el), ["id"]),
            ("%s li:nth-child(%s) %s" % (el, espr, lista), ["inverso"]),
        ]
        rng.shuffle(sintassi)
        rng.shuffle(significato)
        # la lista del tipo sbagliato è l'errore più frequente: c'è sempre
        scelte = ([("%s.%s li:nth-child(%s) %s" % (altro, classe, espr, el), ["lista"])]
                  + sintassi[:2] + significato[:2])
    motivi = {
        "lista": "`%s.%s` è una lista %s" % (altro, classe, LISTE[altro][0]),
        "pseudo": "`::` introduce gli pseudo-elementi, e `::nth-child` non esiste",
        "inventata": "`:%s` non esiste" % inventata,
        "errata0": "`:nth-child(%s)` %s" % (errate[0], SIGNIFICATI[errate[0]]),
        "errata1": "`:nth-child(%s)` %s" % (errate[1], SIGNIFICATI[errate[1]]),
        "spazio": "`%s .%s`, con lo spazio, è un elemento di classe `%s` dentro una `%s`"
                  % (tipo, classe, classe, tipo),
        "su-lista": "`%s:nth-child(…)` guarda la posizione della lista stessa" % lista,
        "su-elemento": "`%s:nth-child(…)` guarda la posizione di `%s` dentro la voce" % (el, el),
        "id": "`#%s` indica un id, non una classe" % classe,
        "inverso": "l'ordine conta: a sinistra va il contenitore più esterno",
    }
    usati = {m for _, chiavi in scelte for m in chiavi}
    sbagliate = [s for s, _ in scelte]
    posizioni = [p for p in range(1, 8 if tipo == "ul" else 7) if condizione(p)]
    controllo = (
        "(() => { const opzioni = %s;"
        " const lista = document.querySelector('body > %s');"
        " const attesi = [];"
        " Array.from(lista.children).forEach((li, i) => {"
        " if (%s.includes(i + 1)) attesi.push(...li.getElementsByTagName('%s')); });"
        " const uguali = (a, b) => a.length === b.length && a.every((x, i) => x === b[i]);"
        " return opzioni.filter(s => { try {"
        " return uguali(Array.from(document.querySelectorAll(s)), attesi); }"
        " catch (e) { return false; } }).join(' | '); })()"
        % (json.dumps([giusta] + sbagliate), lista, json.dumps(posizioni), el))
    return chiusa(
        "c03-selettore-lista", CAP, "selettori",
        "Quale dei seguenti selettori CSS seleziona %s in `<li>` %s in una lista %s con "
        "classe `%s`?" % (CONTENUTI[el], posto, nome_lista, classe),
        "`%s`" % giusta, ["`%s`" % s for s in sbagliate], n=6,
        spiegazione="Il selettore si legge da sinistra a destra, dal contenitore più esterno: "
                    "`%s` è una lista %s **e** di classe `%s` (senza spazio: selettore "
                    "composto); lo spazio è il combinatore discendente; `li:nth-child(%s)` "
                    "sono le voci %s; `%s` sono gli elementi cercati, a qualunque profondità "
                    "dentro la voce. Nelle alternative: %s." % (
                        lista, nome_lista, classe, espr, posto, el,
                        "; ".join(v for k, v in motivi.items() if k in usati)),
        rif=R % "Combinatori" + "; «Relazioni di posizione»",
        fonte=FONTE_2024 if ufficiale else None,
        verifica=dict(tipo="dom", html=SELETTORE_HTML % {"c": classe}, espressione=controllo,
                      atteso=giusta))


d(_selettore_lista)

# ----------------------------------------------------------------------
# Le domande delle prove degli anni scorsi (verificate in Chromium)
d(colore_css("c03-prova-2024", CAP, "cascata e specificità",
             """
.f { color: yellow; }
#g { color: blue; }
div h1 { color: pink !important; }
h1 .f { color: green !important; }
#cont h1.f { color: black; }""",
             """
<body><div id="cont">
  <h1 class="f" id="g" style="color: red;">
    Hi!
  </h1>
</div></body>""", "h1", "pink", ["yellow", "blue", "green", "black", "red"], n=6,
             spiegazione="Le dichiarazioni `!important` battono quelle normali, compreso lo stile "
                         "inline. Fra le due marcate `!important`, `h1 .f` **non** seleziona "
                         "l'`h1`: indica un elemento di classe `f` *dentro* un `h1` (combinatore "
                         "discendente). Resta `div h1`, quindi il colore è `pink`.",
             rif=R % "La cascata", fonte=FONTE_2024))

d(colore_css("c03-prova-2025", CAP, "cascata e specificità",
             """
div h1 { color: orange; }
#x .w { color: blue; }
.y #z { color: red; }
div.y h1.w { color: green; }""",
             """
<body><div id="x" class="y">
  <h1 class="w" id="z">
    Hi!
  </h1>
</div></body>""", "h1", "red", ["orange", "blue", "green"], n=4,
             spiegazione="Tutte e quattro le regole selezionano l'`h1`. Specificità: `div h1` "
                         "(0, 0, 2), `#x .w` (1, 1, 0), `.y #z` (1, 1, 0), `div.y h1.w` "
                         "(0, 2, 2). Vincono a pari merito le due con un id e una classe; a "
                         "parità di specificità prevale l'ultima nell'ordine: `red`.",
             rif=R % "Specificità", fonte=FONTE_AULA))

d(colore_css("c03-ereditarieta", CAP, "ereditarietà",
             """
#cont { color: red; }
.box { color: green !important; }
h1 { color: blue; }""",
             """
<body><div id="cont" class="box">
  <h1>Titolo</h1>
</div></body>""", "h1", "blue", ["red", "green", "black"], n=4,
             testo="Si considerino le regole e il documento seguenti. Qual è il colore finale "
                   "dell'elemento `h1`?",
             spiegazione="Le prime due regole selezionano il `div`, non l'`h1`: all'`h1` "
                         "arriverebbe il colore solo per **ereditarietà**, che ha la priorità "
                         "più bassa in assoluto. Basta una regola qualunque che selezioni "
                         "direttamente l'`h1` (qui `h1`, con specificità minima) per vincere, "
                         "indipendentemente da id e `!important` delle regole del genitore.",
             rif=R % "Ereditarietà"))

d(colore_css("c03-inline-important", CAP, "cascata e specificità",
             """
#t { color: blue; }
p { color: green !important; }
#t.nota { color: orange; }""",
             """
<body>
  <p id="t" class="nota" style="color: red;">
    Testo
  </p>
</body>""", "#t", "green", ["blue", "red", "orange"], n=4,
             testo="Si considerino le regole e il documento seguenti. Qual è il colore finale "
                   "del paragrafo?",
             spiegazione="`!important` porta la dichiarazione nel bucket più prioritario: batte "
                         "lo stile inline (che è una dichiarazione normale) e i selettori più "
                         "specifici. La specificità conta solo fra dichiarazioni dello stesso "
                         "bucket.",
             rif=R % "Origine e importanza"))

# ----------------------------------------------------------------------
d(chiusa("c03-anatomia", CAP, "regole CSS",
         "Nella regola `p.nota { color: gray; margin: 0; }`, che cosa sono `p.nota`, "
         "`color` e `gray`?",
         "Il selettore, una proprietà e il suo valore.",
         ["La proprietà, il selettore e la dichiarazione.",
          "Il blocco di dichiarazione, un valore e una proprietà.",
          "Il selettore, un valore e la sua unità di misura.",
          "Il nome della regola, un attributo HTML e il suo valore.",
          "L'elemento, la classe e lo stile inline."],
         spiegazione="Una regola è formata da un selettore e da un blocco di dichiarazioni fra "
                     "graffe; ogni dichiarazione è una coppia `proprietà: valore`, terminata "
                     "da `;`.",
         rif=R % "Anatomia di una regola"))

d(chiusa("c03-inclusione", CAP, "includere il CSS",
         "Quali dei seguenti sono modi validi per applicare regole CSS a una pagina HTML?",
         ['``<link rel="stylesheet" href="stile.css">`` nell\'`head`',
          "Un elemento `<style>` con le regole al suo interno",
          'L\'attributo ``style="..."`` su un singolo elemento'],
         ['``<script src="stile.css">`` nell\'`head`',
          '``<css href="stile.css">`` nell\'`head`',
          '``<style src="stile.css">`` senza contenuto',
          '``<link rel="css" src="stile.css">`` nel `body`',
          "Un commento HTML che contiene le regole"],
         multi=True,
         spiegazione="Foglio esterno con `<link rel=\"stylesheet\">`, elemento `<style>` nel "
                     "documento e attributo `style` (stile inline). Il foglio esterno è da "
                     "preferire: separa contenuto e presentazione e si condivide fra più "
                     "pagine (e il browser lo tiene in cache).",
         rif=R % "Come includere il CSS in una pagina"))

d(chiusa("c03-attributi", CAP, "selettori",
         "Quale selettore seleziona tutti i collegamenti che puntano a un file **PDF** "
         "(cioè il cui `href` termina con `.pdf`)?",
         '``a[href$=".pdf"]``',
         ['``a[href^=".pdf"]``', '``a[href*=".pdf"]``', '``a[href=".pdf"]``', "``a.pdf``",
          '``a[href~=".pdf"]``'],
         spiegazione="Nei selettori di attributo `^=` significa «inizia con», `$=` «termina "
                     "con», `*=` «contiene», `=` «è uguale a». `a.pdf` selezionerebbe i link "
                     "con classe `pdf`.",
         rif=R % "Corrispondenza parziale sugli attributi",
         verifica=dict(tipo="dom",
                       html='<!DOCTYPE html><html><body><a id="a1" href="x.pdf">1</a>'
                            '<a id="a2" href="pdf.html">2</a><a id="a3" href=".pdf/x">3</a>'
                            '<a id="a4" href="doc/y.pdf">4</a></body></html>',
                       espressione="Array.from(document.querySelectorAll('a[href$=\".pdf\"]'))"
                                   ".map(e => e.id).join(',')",
                       atteso="a1,a4")))

d(chiusa("c03-composti", CAP, "selettori",
         "Che differenza c'è fra i selettori `p.nota` e `p .nota`?",
         "`p.nota`: paragrafi di classe `nota`; `p .nota`: elementi di classe `nota` dentro un "
         "paragrafo.",
         ["Nessuna: lo spazio nei selettori viene ignorato.",
          "`p.nota`: elementi di classe `nota` dentro un paragrafo; `p .nota`: paragrafi di "
          "classe `nota`.",
          "`p .nota` seleziona sia i paragrafi sia gli elementi di classe `nota`.",
          "`p.nota` non è valido: classe e tipo vanno separati da uno spazio.",
          "`p .nota` seleziona i paragrafi che seguono un elemento di classe `nota`."],
         spiegazione="Senza spazio le condizioni si riferiscono allo stesso elemento (selettore "
                     "composto: è un `p` **e** ha classe `nota`); lo spazio è il combinatore "
                     "discendente.",
         rif=R % "Selettori composti"))

COMBINATORI_HTML = """<div id="d">
  <h2 id="t">Titolo</h2>
  <p id="p1">Uno</p>
  <section id="s">
    <p id="p2">Due</p>
  </section>
  <p id="p3">Tre</p>
</div>"""

for sel, giusta, sbagliate, spieg in [
    ("div > p", "`p1` e `p3`", ["`p1`, `p2` e `p3`", "Solo `p1`", "Solo `p2`", "`p2` e `p3`"],
     "Il combinatore figlio `>` seleziona solo i figli diretti: `p2` è dentro la `section`, "
     "quindi è un discendente del `div` ma non un suo figlio."),
    ("div p", "`p1`, `p2` e `p3`", ["`p1` e `p3`", "Solo `p2`", "Solo `p1`", "Nessuno"],
     "Il combinatore discendente (lo spazio) seleziona gli elementi a qualunque profondità "
     "dentro il `div`, compreso `p2`, che sta nella `section`."),
    ("h2 + p", "Solo `p1`", ["`p1` e `p3`", "`p1`, `p2` e `p3`", "Solo `p3`", "Nessuno"],
     "`+` seleziona il fratello **immediatamente** successivo: solo `p1` segue direttamente "
     "l'`h2`."),
    ("h2 ~ p", "`p1` e `p3`", ["Solo `p1`", "`p1`, `p2` e `p3`", "Solo `p3`", "`p2` e `p3`"],
     "`~` seleziona tutti i fratelli successivi di quel tipo: `p1` e `p3` sono fratelli "
     "dell'`h2` che lo seguono; `p2` non è un fratello (sta nella `section`)."),
    ("section + p", "Solo `p3`", ["`p1` e `p3`", "Solo `p2`", "`p2` e `p3`", "Nessuno"],
     "`p3` è il fratello immediatamente successivo della `section`."),
]:
    atteso = giusta.replace("`", "").replace("Solo ", "").replace(" e ", ",").replace(", ", ",")
    d(chiusa("c03-comb-" + sel.replace(" ", "").replace(">", "figlio").replace("+", "adiac")
             .replace("~", "fratelli"), CAP, "combinatori",
             "Quali paragrafi seleziona il selettore `%s` nel frammento seguente?" % sel,
             giusta, sbagliate, n=4, codice=L("html", COMBINATORI_HTML),
             spiegazione=spieg, rif=R % "Combinatori",
             verifica=dict(tipo="dom",
                           html="<!DOCTYPE html><html><body>%s</body></html>" % COMBINATORI_HTML,
                           espressione="Array.from(document.querySelectorAll('%s'))"
                                       ".map(e => e.id).join(',')" % sel,
                           atteso=atteso)))

d(chiusa("c03-pseudoclassi", CAP, "pseudo-classi e :nth-child",
         "Quali delle seguenti sono **pseudo-classi** CSS?",
         ["`:hover`", "`:focus`", "`:first-child`", "`:visited`", "`:invalid`"],
         ["`::before`", "`::first-line`", "`::selection`", "`.hover`", "`[hover]`"],
         multi=True,
         spiegazione="Le pseudo-classi (un solo `:`) selezionano elementi in base a uno stato "
                     "(`:hover`, `:focus`, `:visited`, `:invalid`) o alla posizione "
                     "(`:first-child`, `:nth-child`). Gli pseudo-elementi (`::`) selezionano "
                     "invece *parti* di un elemento o contenuto generato.",
         rif="cap. 3, «Pseudo-classi» e «Pseudo-elementi»"))

d(chiusa("c03-visited", CAP, "pseudo-classi e :nth-child",
         "Perché i browser limitano le proprietà che si possono applicare con `:visited` "
         "(sostanzialmente ai soli colori)?",
         "Per impedire a una pagina di scoprire, misurando lo stile, quali siti ha visitato "
         "l'utente.",
         ["Perché i link visitati non fanno parte del DOM.",
          "Perché `:visited` funziona solo sui link con `target=\"_blank\"`.",
          "Perché la cronologia è salvata sul server e non è accessibile al CSS.",
          "Perché le altre proprietà richiederebbero di ricaricare la pagina.",
          "Perché `:visited` è stata deprecata ed esiste solo per compatibilità."],
         spiegazione="Se `:visited` potesse cambiare dimensioni o posizione, uno script "
                     "potrebbe misurare i link e ricostruire la cronologia dell'utente: è un "
                     "problema di privacy, e i browser lo evitano consentendo solo modifiche "
                     "di colore, che restano invisibili a JavaScript.",
         rif=R % "Stati storici"))

d(chiusa("c03-pseudoelementi", CAP, "pseudo-elementi",
         "Quali delle seguenti affermazioni sul contenuto generato con `::before` e "
         "`::after` sono **vere**?",
         ["Richiede la proprietà `content` per comparire.",
          "Non fa parte del DOM: non si trova, per esempio, con `querySelector`.",
          "Non dovrebbe contenere informazioni essenziali, perché non è vero contenuto."],
         ["Viene aggiunto al codice HTML della pagina inviata dal server.",
          "Si può selezionare con `document.querySelector('::before')`.",
          "Si inserisce prima o dopo l'elemento, fuori dal suo riquadro.",
          "Funziona solo sugli elementi vuoti come `<img>` e `<input>`.",
          "Sostituisce il contenuto dell'elemento a cui si applica."],
         multi=True,
         spiegazione="`::before` e `::after` creano un figlio fittizio all'inizio o alla fine "
                     "del contenuto dell'elemento, solo se `content` è impostato. Non esiste "
                     "nel DOM e non è affidabile per lettori di schermo e copia-incolla: va "
                     "usato per decorazioni, non per informazioni.",
         rif=R % "Pseudo-elementi"))

d(chiusa("c03-ordine-bucket", CAP, "origine e importanza",
         "Qual è l'ordine dei bucket di origine e importanza, dal **meno** al **più** "
         "prioritario?",
         "User agent, utente, autore, autore `!important`, utente `!important`, user agent "
         "`!important`.",
         ["User agent, utente, autore, user agent `!important`, utente `!important`, autore "
          "`!important`.",
          "Autore, utente, user agent, autore `!important`, utente `!important`, user agent "
          "`!important`.",
          "User agent `!important`, utente `!important`, autore `!important`, autore, utente, "
          "user agent.",
          "User agent, autore, utente, utente `!important`, autore `!important`, user agent "
          "`!important`."],
         n=4,
         spiegazione="Fra le dichiarazioni normali vince l'autore (che sovrascrive gli stili "
                     "predefiniti del browser); fra le `!important` l'ordine si **inverte**: "
                     "le esigenze dell'utente (per esempio l'alto contrasto per accessibilità) "
                     "devono poter battere quelle del sito.",
         rif=R % "Origine e importanza"))

d(chiusa("c03-spec-numero", CAP, "cascata e specificità",
         "Un selettore con **undici** classi e un selettore con **un** id selezionano lo "
         "stesso elemento e impostano proprietà in conflitto. Quale prevale?",
         "Quello con l'id, perché la specificità si confronta per componenti.",
         ["Quello con le undici classi, perché 11 è maggiore di 1.",
          "Il più recente nell'ordine del foglio di stile, perché la specificità è pari.",
          "Nessuno dei due: in caso di conflitto si applica il valore predefinito.",
          "Quello con le undici classi, ma solo se è scritto dopo.",
          "Quello con l'id, ma solo se è marcato `!important`."],
         spiegazione="La specificità è una terna (id, classi, tipi) confrontata da sinistra: "
                     "(1, 0, 0) batte (0, 11, 0). Non è un numero a tre cifre in cui le classi "
                     "«riportano» negli id.",
         rif=R % "Specificità"))

d(chiusa("c03-ereditati", CAP, "ereditarietà",
         "Quali delle seguenti proprietà vengono **ereditate** per impostazione predefinita "
         "dagli elementi figli?",
         ["`color`", "`font-family`", "`font-size`", "`text-align`"],
         ["`border`", "`margin`", "`padding`", "`background-color`", "`width`"],
         multi=True,
         spiegazione="Si ereditano soprattutto le proprietà legate al testo (colore, font, "
                     "allineamento); quelle del riquadro (bordi, margini, padding, sfondo, "
                     "dimensioni) no. Con il valore `inherit` si può forzare l'ereditarietà di "
                     "qualunque proprietà.",
         rif=R % "Ereditarietà"))

d(chiusa("c03-ua", CAP, "regole CSS",
         "Una pagina senza alcun foglio di stile mostra comunque i titoli `h1` grandi e in "
         "grassetto e i link blu e sottolineati. Perché?",
         "Per gli stili predefiniti del browser (*user agent styles*).",
         ["Perché HTML stabilisce l'aspetto di ogni elemento, senza bisogno di CSS.",
          "Perché il server aggiunge un foglio di stile predefinito alla risposta.",
          "Perché il sistema operativo applica il proprio tema alle pagine web.",
          "Per gli stili inline che il browser aggiunge al codice HTML.",
          "Perché i tag `h1` e `a` contengono già gli attributi di stile."],
         spiegazione="Ogni browser applica un proprio foglio di stile di base (origine *user "
                     "agent*), con la priorità più bassa fra le dichiarazioni normali. Proprio "
                     "perché differisce fra browser, molti progetti partono da un «CSS reset».",
         rif=R % "Gli stili predefiniti del browser"))

# ----------------------------------------------------------------------
# Domande aperte
d(aperta("c03-a-origini", CAP, "origine e importanza",
         "Quali sono le possibili origini di regole CSS nello step di analisi dei bucket di "
         "origine-importanza nell'algoritmo *cascade* di risoluzione dei conflitti?",
         ["Tre origini: stili dello *user agent* (il browser), stili locali dell'utente "
          "(estensioni, impostazioni di accessibilità), stili dell'autore della pagina.",
          "Combinate con l'importanza (`!important` o no) danno sei bucket.",
          "Dal meno al più prioritario: user agent, utente, autore, autore `!important`, "
          "utente `!important`, user agent `!important`.",
          "L'inversione fra le `!important` protegge le esigenze dell'utente (accessibilità); "
          "a parità di bucket decidono livelli (stili inline in cima), specificità e ordine."],
         rif=R % "Origine e importanza", fonte=FONTE_2024))

d(aperta("c03-a-specificita", CAP, "cascata e specificità",
         "Si spieghi come si calcola e come si confronta la **specificità** di un selettore "
         "CSS, con almeno tre esempi, e in quale punto dell'algoritmo della cascata "
         "interviene.",
         ["Terna (a, b, c): a = id, b = classi, attributi e pseudo-classi, c = tipi di elemento "
          "e pseudo-elementi; `*` e combinatori non contano.",
          "Si confronta componente per componente da sinistra: non è un numero a tre cifre.",
          "Esempi: `h1` (0, 0, 1), `.nota p` (0, 1, 1), `#menu a:hover` (1, 1, 1).",
          "Interviene dopo origine/importanza e livelli (lo stile inline vince sui fogli di "
          "stile); a parità di specificità vince la dichiarazione che compare per ultima."],
         rif=R % "Specificità"))

d(aperta("c03-a-ereditarieta", CAP, "ereditarietà",
         "Si spieghi che cos'è l'**ereditarietà** in CSS: quali proprietà si ereditano, che "
         "priorità ha rispetto alla cascata e come la si può controllare.",
         ["Alcune proprietà, se non impostate su un elemento, prendono il valore calcolato del "
          "genitore.",
          "Si ereditano soprattutto le proprietà del testo (`color`, `font-*`, `text-align`), "
          "non quelle del riquadro (`margin`, `border`, `background`).",
          "Ha la priorità più bassa in assoluto: qualunque regola che selezioni l'elemento "
          "batte il valore ereditato, anche se il genitore ha selettori più specifici o "
          "`!important`.",
          "Si controlla con le parole chiave `inherit` (forza l'ereditarietà) e `initial` "
          "(valore iniziale)."],
         rif=R % "Ereditarietà"))

d(aperta("c03-a-inclusione", CAP, "includere il CSS",
         "Si descrivano i tre modi per applicare regole CSS a un documento HTML, "
         "discutendone vantaggi e svantaggi.",
         ["Foglio esterno con `<link rel=\"stylesheet\" href=\"...\">`: separa contenuto e "
          "stile, è condiviso fra le pagine e messo in cache; richiede una richiesta in più.",
          "Elemento `<style>` nella pagina: utile per stili di una sola pagina, ma non "
          "riutilizzabile.",
          "Attributo `style`: vale per un solo elemento, mescola contenuto e presentazione ed "
          "è difficile da mantenere; ha la priorità più alta fra le dichiarazioni normali.",
          "Preferibile il foglio esterno."],
         rif=R % "Come includere il CSS in una pagina"))

d(aperta("c03-a-pseudo", CAP, "pseudo-elementi",
         "Si spieghi la differenza fra **pseudo-classi** e **pseudo-elementi**, con due "
         "esempi per ciascuno.",
         ["Pseudo-classe (`:`): seleziona elementi in un certo stato o posizione, come se "
          "avessero una classe in più.",
          "Esempi: `a:hover`, `input:focus`, `li:nth-child(2n)`, `input:invalid`.",
          "Pseudo-elemento (`::`): seleziona una parte di un elemento o crea contenuto "
          "generato.",
          "Esempi: `p::first-line`, `p::first-letter`, `.nota::before` con `content`, "
          "`::selection`; il contenuto generato non fa parte del DOM."],
         rif="cap. 3, «Pseudo-classi» e «Pseudo-elementi»"))
