"""Capitolo 4: layout e responsive design (unità, box model, display, float,
posizionamento, Flexbox, Grid, media query, viewport)."""

from generatore import L, aperta, chiusa, famiglia

CAP = 4
R = "cap. 4, «%s»"

DOMANDE = []
d = DOMANDE.append


def _pagina(css, corpo):
    return ("<!DOCTYPE html><html><head><meta charset=\"utf-8\"><style>\n"
            "body { margin: 0; }\n%s\n</style></head><body>\n%s\n</body></html>" % (css, corpo))


def _px(valori):
    """Elenco ordinato e senza ripetizioni di valori in px (come testo)."""
    out = []
    for v in valori:
        t = "`%gpx`" % v
        if v > 0 and t not in out:
            out.append(t)
    return out


# ----------------------------------------------------------------------
@famiglia("c04-box", CAP, "box model", varianti=4)
def _box(rng):
    w = rng.choice([200, 240, 300, 320])
    p = rng.choice([10, 15, 20, 25])
    b = rng.choice([2, 4, 5])
    m = rng.choice([10, 20, 30])
    sizing = rng.choice(["content-box", "border-box"])
    domanda = rng.choice(["bordo", "contenuto"])
    if sizing == "content-box":
        bordo, contenuto = w + 2 * p + 2 * b, w
    else:
        bordo, contenuto = w, w - 2 * p - 2 * b
    giusta = bordo if domanda == "bordo" else contenuto
    candidati = [w, w + 2 * p + 2 * b, w + 2 * p + 2 * b + 2 * m, w - 2 * p - 2 * b, w + p + b,
                 w + 2 * p, w - 2 * p, w + 2 * m]
    sbagliate = [x for x in _px(candidati) if x != "`%gpx`" % giusta]
    rng.shuffle(sbagliate)
    css = (".box {\n  box-sizing: %s;\n  width: %dpx;\n  padding: %dpx;\n"
           "  border: %dpx solid black;\n  margin: %dpx;\n}" % (sizing, w, p, b, m))
    if domanda == "bordo":
        testo = ("Si consideri la regola seguente, applicata a un `div` di classe `box`. Quanto "
                 "è largo il riquadro dell'elemento **fino al bordo** (bordo compreso, margini "
                 "esclusi)?")
        espressione = "String(Math.round(document.querySelector('.box').getBoundingClientRect().width))"
    else:
        testo = ("Si consideri la regola seguente, applicata a un `div` di classe `box`. Quanto "
                 "è largo il **content box** dell'elemento?")
        espressione = ("(() => { const e = document.querySelector('.box'); const s = "
                       "getComputedStyle(e); return String(Math.round(e.clientWidth - "
                       "parseFloat(s.paddingLeft) - parseFloat(s.paddingRight))); })()")
    return chiusa(
        "c04-box", CAP, "box model", testo, "`%gpx`" % giusta, sbagliate[:5], n=4,
        codice=L("css", css),
        spiegazione="Con `box-sizing: content-box` (il valore predefinito) `width` indica la "
                    "larghezza del solo contenuto: padding e bordo si aggiungono (%d + 2·%d + "
                    "2·%d = %d). Con `border-box` `width` arriva fino al bordo e il contenuto "
                    "si restringe (%d − 2·%d − 2·%d = %d). I margini stanno sempre fuori dal "
                    "bordo." % (w, p, b, w + 2 * p + 2 * b, w, p, b, w - 2 * p - 2 * b),
        rif=R % "Il box model",
        verifica=dict(tipo="dom", html=_pagina(css, '<div class="box">testo</div>'),
                      espressione=espressione, atteso=str(giusta)))


d(_box)


@famiglia("c04-em-rem", CAP, "unità di misura", varianti=4)
def _em(rng):
    radice = rng.choice([16, 16, 20])
    a = rng.choice([12, 20, 24])
    eb = rng.choice([1.5, 2, 0.5, 1.25])
    unita = rng.choice(["em", "rem", "%"])
    vc = {"em": rng.choice([2, 1.5, 0.5]), "rem": rng.choice([2, 1.5, 3]),
          "%": rng.choice([50, 150, 200])}[unita]
    b = a * eb
    if unita == "em":
        c = b * vc
    elif unita == "rem":
        c = radice * vc
    else:
        c = b * vc / 100
    valore_c = ("%g%s" % (vc, unita))
    radice_css = "html { font-size: %dpx; }\n" % radice if radice != 16 else ""
    css = ("%s.a { font-size: %dpx; }\n.b { font-size: %gem; }\n.c { font-size: %s; }"
           % (radice_css, a, eb, valore_c))
    candidati = [c, radice * vc if unita != "rem" else b * vc, a * vc if unita != "%" else a * vc / 100,
                 16 * vc if unita != "%" else 16 * vc / 100, b, a, radice * eb * (vc if unita != "%" else vc / 100)]
    sbagliate = [x for x in _px(candidati) if x != "`%gpx`" % c]
    rng.shuffle(sbagliate)
    html = '<div class="a">A <div class="b">B <span class="c">C</span></div></div>'
    return chiusa(
        "c04-em-rem", CAP, "unità di misura",
        "Si considerino le regole CSS e il frammento HTML seguenti. Qual è la dimensione del "
        "carattere calcolata per lo `span` di classe `c`?",
        "`%gpx`" % c, sbagliate[:5], n=4,
        codice=[L("css", css), L("html", html)],
        spiegazione="`em` (e `%%` in `font-size`) si riferiscono alla dimensione del carattere "
                    "del **genitore**, `rem` a quella dell'elemento radice (%dpx%s). Qui `.b` "
                    "vale %g·%d = %gpx, e `.c` (%s) vale %gpx." % (
                        radice, "" if radice != 16 else ", il valore predefinito",
                        eb, a, b, valore_c, c),
        rif=R % "Unità relative al carattere",
        verifica=dict(tipo="dom", html=_pagina(css, html),
                      espressione="getComputedStyle(document.querySelector('.c')).fontSize",
                      atteso="%gpx" % c))


d(_em)


@famiglia("c04-grid-fr", CAP, "Grid", varianti=3)
def _grid(rng):
    larghezza = rng.choice([600, 700, 800, 900])
    fisso = rng.choice([100, 150, 200])
    f1, f2 = rng.choice([(1, 2), (1, 3), (2, 3), (1, 1)])
    resto = larghezza - fisso
    col2 = resto * f1 / (f1 + f2)
    col3 = resto * f2 / (f1 + f2)
    css = (".griglia {\n  display: grid;\n  width: %dpx;\n"
           "  grid-template-columns: %dpx %dfr %dfr;\n}" % (larghezza, fisso, f1, f2))
    giusta = "`%gpx`, `%gpx` e `%gpx`" % (fisso, col2, col3)
    candidati = [
        (fisso, larghezza * f1 / (f1 + f2), larghezza * f2 / (f1 + f2)),
        (fisso, resto / 2, resto / 2),
        (larghezza / 3, larghezza / 3, larghezza / 3),
        (fisso, f1 * 100, f2 * 100),
        (fisso * 1.0, resto * f2 / (f1 + f2), resto * f1 / (f1 + f2)),
        (fisso, f1 * resto / 3, f2 * resto / 3),
    ]
    sbagliate = []
    for c in candidati:
        t = "`%gpx`, `%gpx` e `%gpx`" % tuple(round(x, 2) for x in c)
        if t != giusta and t not in sbagliate:
            sbagliate.append(t)
    corpo = '<div class="griglia"><div>1</div><div>2</div><div>3</div></div>'
    return chiusa(
        "c04-grid-fr", CAP, "Grid",
        "Con la regola seguente, quanto sono larghe le tre colonne della griglia?",
        giusta, sbagliate[:5], n=4, codice=L("css", css),
        spiegazione="L'unità `fr` divide lo spazio **rimasto** dopo le colonne a dimensione "
                    "fissa: %d − %d = %dpx, ripartiti in %d parti (%gpx ciascuna)." % (
                        larghezza, fisso, resto, f1 + f2, resto / (f1 + f2)),
        rif=R % "L'unità fr",
        verifica=dict(tipo="dom", html=_pagina(css, corpo),
                      espressione="Array.from(document.querySelectorAll('.griglia > div'))"
                                  ".map(e => +e.getBoundingClientRect().width.toFixed(2)).join(',')",
                      atteso=",".join("%g" % round(x, 2) for x in (fisso, col2, col3))))


d(_grid)


@famiglia("c04-media", CAP, "media query", varianti=4)
def _media(rng):
    soglie = sorted(rng.sample([480, 600, 768, 992, 1200], 2))
    colori = rng.sample(["red", "blue", "green", "orange", "purple", "black"], 3)
    stile = rng.choice(["mobile-first", "desktop-first"])
    if stile == "mobile-first":
        css = ("p { color: %s; }\n@media (min-width: %dpx) {\n  p { color: %s; }\n}\n"
               "@media (min-width: %dpx) {\n  p { color: %s; }\n}"
               % (colori[0], soglie[0], colori[1], soglie[1], colori[2]))
    else:
        css = ("p { color: %s; }\n@media (max-width: %dpx) {\n  p { color: %s; }\n}\n"
               "@media (max-width: %dpx) {\n  p { color: %s; }\n}"
               % (colori[0], soglie[1], colori[1], soglie[0], colori[2]))
    larghezza = rng.choice([soglie[0] - 100, soglie[0], (soglie[0] + soglie[1]) // 2,
                            soglie[1], soglie[1] + 200])
    if stile == "mobile-first":
        giusta = colori[2] if larghezza >= soglie[1] else (colori[1] if larghezza >= soglie[0]
                                                           else colori[0])
    else:
        giusta = colori[2] if larghezza <= soglie[0] else (colori[1] if larghezza <= soglie[1]
                                                           else colori[0])
    sbagliate = [c for c in colori if c != giusta] + ["black" if "black" not in colori else "gray"]
    return chiusa(
        "c04-media", CAP, "media query",
        "Un paragrafo è stilizzato con le regole seguenti. Di che colore appare in una finestra "
        "con viewport largo **%dpx**?" % larghezza,
        giusta, sbagliate, n=4, codice=L("css", css),
        spiegazione="`min-width: X` vale quando il viewport è largo **almeno** X pixel, "
                    "`max-width: X` quando è largo **al più** X (gli estremi sono inclusi). Le "
                    "regole dentro una media query hanno la stessa specificità delle altre: fra "
                    "quelle che valgono, vince l'ultima nell'ordine.",
        rif=R % "Media query",
        verifica=dict(tipo="css", css=css, html="<body><p>Testo</p></body>", selettore="p",
                      proprieta="color", atteso=giusta, viewport=[larghezza, 600],
                      candidati=[giusta] + sbagliate))


d(_media)

# ----------------------------------------------------------------------
d(chiusa("c04-pixel", CAP, "unità di misura",
         "Quale fra le seguenti affermazioni sul pixel CSS (`px`) è corretta?",
         "È un'unità di riferimento: su schermi ad alta densità corrisponde a più pixel fisici.",
         ["Corrisponde sempre esattamente a un pixel fisico dello schermo.",
          "È un'unità relativa alla dimensione del carattere dell'elemento.",
          "Equivale all'1% della larghezza del viewport.",
          "Non si può usare per le dimensioni dei caratteri.",
          "Vale un millimetro sullo schermo, qualunque sia il dispositivo."],
         spiegazione="Il `px` CSS è un'unità «logica»: su uno schermo con rapporto di pixel 2 un "
                     "pixel CSS occupa 2×2 pixel fisici. Per questo le pagine hanno "
                     "dimensioni simili su schermi di densità diversa.",
         rif=R % "Unità assolute"))

d(chiusa("c04-vw", CAP, "unità di misura",
         "Che cosa indica `50vw`?",
         "Metà della larghezza del viewport.",
         ["Metà della larghezza dell'elemento genitore.",
          "Metà della larghezza dello schermo fisico del dispositivo.",
          "50 volte la dimensione del carattere corrente.",
          "Metà della larghezza del documento, compresa la parte non visibile.",
          "50 pixel, su qualunque dispositivo."],
         spiegazione="`vw` e `vh` valgono l'1% della larghezza e dell'altezza del viewport (l'area "
                     "della finestra in cui si vede la pagina). Le percentuali `%` si riferiscono "
                     "invece, di solito, al blocco contenitore.",
         rif=R % "Unità relative al viewport"))

d(chiusa("c04-padding-margin", CAP, "box model",
         "Quale fra le seguenti affermazioni su `padding` e `margin` è corretta?",
         "Il padding sta dentro il bordo e prende lo sfondo; il margine sta fuori, trasparente.",
         ["Il margine sta dentro il bordo e prende lo sfondo; il padding sta fuori, trasparente.",
          "Sono sinonimi: l'uno o l'altro si sceglie in base al browser.",
          "Il padding si può applicare solo agli elementi in linea.",
          "Il margine è sempre incluso nella larghezza indicata da `width`.",
          "Il padding non può avere valori diversi sui quattro lati."],
         spiegazione="Dall'interno verso l'esterno: contenuto, padding, bordo, margine. Lo sfondo "
                     "dell'elemento si estende sotto contenuto e padding (fino al bordo); il "
                     "margine è spazio vuoto che separa l'elemento dagli altri.",
         rif=R % "Il box model"))

d(chiusa("c04-none-hidden", CAP, "display",
         "Che differenza c'è fra `display: none` e `visibility: hidden`?",
         "Con `display: none` l'elemento non occupa spazio; con `visibility: hidden` sì.",
         ["Con `visibility: hidden` l'elemento non occupa spazio; con `display: none` sì.",
          "`display: none` rimuove l'elemento dal DOM, `visibility: hidden` no.",
          "Nessuna: sono due modi equivalenti di nascondere un elemento.",
          "`visibility: hidden` nasconde anche il contenuto dei figli, `display: none` no.",
          "`display: none` vale solo per gli elementi di blocco."],
         spiegazione="Entrambi nascondono l'elemento, che resta nel DOM. Con `display: none` "
                     "non viene generato alcun riquadro, quindi gli altri elementi ne occupano "
                     "il posto; con `visibility: hidden` il riquadro c'è ma è invisibile, e lo "
                     "spazio resta vuoto.",
         rif=R % "La proprietà display",
         verifica=dict(tipo="dom",
                       html=_pagina("p { margin: 0; height: 20px; }",
                                    '<p id="a" style="display:none">A</p><p id="b">B</p>'
                                    '<p id="c" style="visibility:hidden">C</p><p id="d">D</p>'),
                       espressione="[document.getElementById('b').getBoundingClientRect().top,"
                                   " document.getElementById('d').getBoundingClientRect().top]"
                                   ".join(',')",
                       atteso="0,40")))

d(chiusa("c04-inline", CAP, "display",
         "Quali delle seguenti affermazioni sugli elementi con `display: inline` (come "
         "`<span>` o `<a>`) sono **vere**?",
         ["Non vanno a capo: si dispongono uno dopo l'altro sulla riga.",
          "Ignorano `width` e `height`."],
         ["Occupano tutta la larghezza disponibile del contenitore.",
          "Iniziano sempre su una nuova riga.",
          "Non possono contenere testo.",
          "Non possono avere padding né bordi.",
          "Diventano elementi di blocco se hanno un `id`."],
         multi=True, n=5,
         spiegazione="Gli elementi in linea scorrono nel testo e la loro dimensione dipende dal "
                     "contenuto: `width` e `height` non hanno effetto. `inline-block` li lascia "
                     "sulla riga ma accetta le dimensioni; `block` li fa andare a capo e "
                     "occupare tutta la larghezza.",
         rif=R % "La proprietà display"))

d(chiusa("c04-float", CAP, "float e clear",
         "A che cosa serve la proprietà `clear: both`?",
         "A far scendere l'elemento sotto gli elementi flottanti che lo precedono.",
         ["A rimuovere tutti gli stili applicati all'elemento.",
          "A far flottare l'elemento sia a destra sia a sinistra.",
          "A centrare l'elemento orizzontalmente nel contenitore.",
          "A nascondere gli elementi flottanti che precedono l'elemento.",
          "A eliminare margini e padding dell'elemento."],
         spiegazione="`float` toglie un elemento dal flusso normale e lo sposta a sinistra o a "
                     "destra, con il testo che gli scorre attorno. `clear` impedisce a un "
                     "elemento di affiancarsi ai float precedenti: con `both` scende sotto "
                     "quelli di entrambi i lati.",
         rif=R % "Float e clear"))

d(chiusa("c04-relative", CAP, "posizionamento",
         "Un elemento ha `position: relative; top: 20px; left: 10px`. Che cosa succede?",
         "Si sposta rispetto alla sua posizione normale e il suo spazio originale resta "
         "occupato.",
         ["Si sposta rispetto all'angolo del viewport e non occupa più spazio.",
          "Si sposta rispetto al primo antenato posizionato e lascia libero il suo spazio.",
          "Resta fermo: `top` e `left` non hanno effetto con `position: relative`.",
          "Si sposta di 20px verso l'alto e di 10px verso destra.",
          "Resta fisso nello schermo anche quando si scorre la pagina."],
         spiegazione="Con `relative` l'elemento resta nel flusso: gli altri elementi si "
                     "dispongono come se fosse nella posizione normale, e lui viene solo "
                     "disegnato spostato (qui 20px più in basso e 10px più a destra).",
         rif=R % "relative",
         verifica=dict(tipo="dom",
                       html=_pagina("p { margin: 0; height: 30px; }",
                                    '<p id="a">A</p><p id="b" style="position:relative;top:20px;'
                                    'left:10px">B</p><p id="c">C</p>'),
                       espressione="(() => { const b = document.getElementById('b')"
                                   ".getBoundingClientRect(); const c = document.getElementById"
                                   "('c').getBoundingClientRect(); return [b.top, b.left, c.top]"
                                   ".join(','); })()",
                       atteso="50,10,60")))

d(chiusa("c04-absolute", CAP, "posizionamento",
         "Rispetto a quale elemento viene posizionato il `div` di classe `badge`?",
         "Rispetto al `div` di classe `card`, il primo antenato posizionato.",
         ["Rispetto al `div` di classe `wrap`, il genitore diretto.",
          "Rispetto al `body`, perché `absolute` usa sempre il documento.",
          "Rispetto al viewport, perché `absolute` equivale a `fixed`.",
          "Rispetto alla sua posizione normale nel flusso.",
          "Rispetto al primo antenato con una larghezza impostata."],
         codice=L("html", """
<div class="card" style="position: relative;">
  <div class="wrap">
    <div class="badge" style="position: absolute; top: 0; right: 0;">
      Nuovo
    </div>
  </div>
</div>"""),
         spiegazione="Un elemento con `position: absolute` esce dal flusso e si posiziona "
                     "rispetto al **primo antenato posizionato** (con `position` diversa da "
                     "`static`): qui la `card`, perché la `wrap` non è posizionata. Se non c'è "
                     "alcun antenato posizionato si usa il blocco iniziale (la pagina).",
         rif=R % "absolute",
         verifica=dict(tipo="dom",
                       html=_pagina(".card { width: 300px; margin: 40px; } .wrap { margin: 20px; "
                                    "width: 100px; }",
                                    '<div class="card" style="position: relative;"><div '
                                    'class="wrap"><div class="badge" style="position: absolute;'
                                    ' top: 0; right: 0;">Nuovo</div></div></div>'),
                       espressione="(() => { const c = document.querySelector('.card')"
                                   ".getBoundingClientRect(); const b = document.querySelector"
                                   "('.badge').getBoundingClientRect(); return String(b.top === "
                                   "c.top && b.right === c.right); })()",
                       atteso="true")))

d(chiusa("c04-fixed-sticky", CAP, "posizionamento",
         "Quali delle seguenti affermazioni sono **vere**?",
         ["Un elemento `fixed` resta fermo nel viewport quando si scorre la pagina.",
          "Un elemento `sticky` scorre con la pagina finché non raggiunge la soglia indicata "
          "(es. `top: 0`), poi vi resta attaccato.",
          "Un elemento `absolute` non occupa spazio nel flusso del documento."],
         ["Un elemento `fixed` si posiziona rispetto al suo genitore diretto.",
          "Un elemento `sticky` esce dal flusso come un elemento `absolute`.",
          "`static` è il valore che rende efficaci `top` e `left`.",
          "Un elemento `relative` non occupa più spazio nel flusso.",
          "`fixed` e `sticky` funzionano solo sugli elementi in linea."],
         multi=True,
         spiegazione="`static` è il valore predefinito (nessun posizionamento). `relative` sposta "
                     "senza togliere dal flusso; `absolute` toglie dal flusso e usa l'antenato "
                     "posizionato; `fixed` usa il viewport; `sticky` si comporta come "
                     "`relative` finché non raggiunge la soglia, poi come `fixed` dentro il "
                     "contenitore.",
         rif=R % "Posizionamento"))

d(chiusa("c04-flex-assi", CAP, "Flexbox",
         "In un contenitore con `display: flex` e `flex-direction: column`, quale proprietà "
         "allinea gli elementi lungo l'asse **verticale**?",
         "`justify-content`", ["`align-items`", "`vertical-align`", "`align-content`",
                               "`text-align`", "`flex-wrap`"],
         spiegazione="`justify-content` agisce sull'asse principale, `align-items` su quello "
                     "trasversale. Con `flex-direction: column` l'asse principale diventa "
                     "verticale, quindi è `justify-content` a distribuire gli elementi dall'alto "
                     "in basso.",
         rif="cap. 4, «justify-content» e «align-content e align-items»"))

d(chiusa("c04-flex-items", CAP, "Flexbox",
         "Quali elementi diventano *flex item* con la regola `.menu { display: flex; }`?",
         "I figli diretti dell'elemento di classe `menu`.",
         ["Tutti i discendenti dell'elemento di classe `menu`.",
          "L'elemento di classe `menu` stesso.",
          "Gli elementi fratelli dell'elemento di classe `menu`.",
          "Solo i figli che hanno a loro volta `display: flex`.",
          "Solo gli elementi in linea contenuti nel menu."],
         spiegazione="`display: flex` rende l'elemento un contenitore flex e i suoi **figli "
                     "diretti** flex item. I discendenti più interni seguono il normale flusso "
                     "dentro il proprio flex item.",
         rif=R % "Contenitori flex"))

d(chiusa("c04-flex-justify", CAP, "Flexbox",
         "Come si distribuiscono tre elementi in un contenitore flex in riga con "
         "`justify-content: space-between`?",
         "Il primo all'inizio, l'ultimo alla fine, lo spazio libero diviso fra loro.",
         ["Tutti e tre al centro, uno accanto all'altro.",
          "Con lo stesso spazio prima del primo, fra gli elementi e dopo l'ultimo.",
          "Tutti e tre all'inizio, con lo spazio libero dopo l'ultimo.",
          "Uno sotto l'altro, distanziati in modo uniforme.",
          "Allargati fino a occupare tutto lo spazio disponibile."],
         spiegazione="`space-between` mette il primo e l'ultimo elemento ai bordi e divide lo "
                     "spazio rimanente in parti uguali **fra** gli elementi; `space-around` e "
                     "`space-evenly` lasciano spazio anche ai lati; `center` li raggruppa al "
                     "centro.",
         rif=R % "justify-content",
         verifica=dict(tipo="dom",
                       html=_pagina(".c { display: flex; justify-content: space-between; "
                                    "width: 600px; } .c div { width: 100px; }",
                                    '<div class="c"><div>1</div><div>2</div><div>3</div></div>'),
                       espressione="Array.from(document.querySelectorAll('.c div')).map(e => "
                                   "e.getBoundingClientRect().left).join(',')",
                       atteso="0,250,500")))

d(chiusa("c04-grid-aree", CAP, "Grid",
         "Che cosa fa la proprietà `grid-template-areas` di un contenitore Grid?",
         "Dà un nome alle aree della griglia, che i figli occupano con `grid-area`.",
         ["Stabilisce quante righe deve avere la griglia, in base al contenuto.",
          "Imposta lo spazio fra le righe e le colonne della griglia.",
          "Assegna automaticamente un nome di classe a ogni cella.",
          "Disegna i bordi delle aree della griglia.",
          "Converte i figli in flex item disposti in colonna."],
         spiegazione="Con `grid-template-areas` si disegna la griglia «a parole" + "» (es. "
                     "`\"header header\" \"nav main\"`), poi ogni figlio si piazza in un'area "
                     "con `grid-area: main`. Rende il layout leggibile e facile da cambiare con "
                     "le media query.",
         rif=R % "Aree con nome"))

d(chiusa("c04-viewport", CAP, "meta viewport",
         "Che effetto ha l'assenza di ``<meta name=\"viewport\" content=\"width=device-width, "
         "initial-scale=1\">`` in una pagina responsive vista su uno smartphone?",
         "Il browser impagina la pagina su un viewport largo come un desktop e la rimpicciolisce.",
         ["La pagina non viene visualizzata e il browser mostra un errore.",
          "Le media query vengono ignorate solo sui browser desktop.",
          "Il browser carica automaticamente la versione mobile del sito.",
          "Le immagini vengono scaricate in bassa risoluzione.",
          "Nessuno: il tag serve solo ai motori di ricerca."],
         spiegazione="Senza il meta tag i browser mobili simulano uno schermo largo circa 980px "
                     "e poi riducono tutto: le media query pensate per gli schermi stretti non "
                     "scattano e il testo risulta minuscolo. `width=device-width` fa "
                     "coincidere il viewport con la larghezza reale del dispositivo.",
         rif=R % "Il meta tag viewport"))

d(chiusa("c04-responsive", CAP, "responsive design",
         "Che cosa distingue un layout **responsive** da uno **adattivo**?",
         "Il responsive si adatta con continuità a ogni larghezza; l'adattivo usa alcune "
         "larghezze fisse.",
         ["L'adattivo si adatta con continuità; il responsive usa alcune larghezze fisse.",
          "Il responsive richiede un sito separato per i dispositivi mobili.",
          "L'adattivo funziona solo con JavaScript.",
          "Il responsive usa solo unità assolute come `px`.",
          "Nessuna: sono due nomi della stessa tecnica."],
         spiegazione="Un layout adattivo prevede alcuni layout a larghezza fissa e sceglie il più "
                     "adatto; un layout responsive combina dimensioni fluide (percentuali, `fr`, "
                     "Flexbox) e media query per adattarsi a qualunque larghezza. Esistono poi "
                     "i layout fissi, quelli liquidi e i siti mobili separati.",
         rif=R % "Responsive design"))

d(chiusa("c04-overflow", CAP, "box model",
         "Un `div` alto 100px contiene un testo che richiederebbe 300px. Quale valore di "
         "`overflow` mostra una barra di scorrimento **solo se serve**?",
         "`auto`", ["`visible`", "`hidden`", "`scroll`", "`clip-auto`", "`wrap`"],
         spiegazione="`visible` (predefinito) lascia uscire il contenuto dal riquadro, `hidden` "
                     "lo taglia, `scroll` mostra sempre le barre, `auto` le mostra solo quando "
                     "il contenuto non ci sta.",
         rif=R % "Il box model"))

# ----------------------------------------------------------------------
# Domande aperte
d(aperta("c04-a-box", CAP, "box model",
         "Si descriva il **box model** del CSS e si spieghi l'effetto della proprietà "
         "`box-sizing`, con un esempio numerico.",
         ["Ogni elemento è un riquadro: contenuto, padding, bordo, margine (dall'interno).",
          "Il padding prende lo sfondo dell'elemento, il margine è spazio trasparente esterno.",
          "Con `content-box` (predefinito) `width` è la larghezza del contenuto: `width: 200px; "
          "padding: 20px; border: 5px` occupa 250px fino al bordo.",
          "Con `border-box` `width` arriva fino al bordo: gli stessi valori danno 200px, con "
          "un contenuto di 150px. Spesso si imposta `* { box-sizing: border-box; }`."],
         rif=R % "Il box model"))

d(aperta("c04-a-flex-grid", CAP, "Flexbox",
         "Si confrontino **Flexbox** e **Grid**: a che cosa servono, quali sono i concetti "
         "principali di ciascuno e quando conviene usare l'uno o l'altro.",
         ["Flexbox dispone gli elementi lungo **una** dimensione (riga o colonna): asse "
          "principale e trasversale, `justify-content`, `align-items`, `flex-wrap`.",
          "Grid dispone gli elementi in **due** dimensioni: `grid-template-columns`/`rows`, "
          "unità `fr`, aree con nome (`grid-template-areas`, `grid-area`).",
          "In entrambi i casi gli stili si applicano al contenitore e i figli diretti diventano "
          "item.",
          "Flexbox per barre, menu, allineamenti di componenti; Grid per l'impaginazione "
          "complessiva della pagina. Si possono combinare."],
         rif="cap. 4, «Flexbox» e «Grid»"))

d(aperta("c04-a-responsive", CAP, "responsive design",
         "Che cos'è il **responsive design**? Si descrivano gli strumenti con cui si realizza "
         "(media query, unità relative, meta tag viewport) con un breve esempio.",
         ["Un'unica pagina che si adatta a schermi di ogni dimensione, invece di un sito mobile "
          "separato o di layout fissi.",
          "Media query: `@media (max-width: 600px) { ... }` applica regole solo in certe "
          "condizioni (larghezza, orientamento, ...); approccio *mobile first* con `min-width`.",
          "Dimensioni fluide: percentuali, `fr`, Flexbox e Grid, unità relative come `rem`.",
          "Meta tag `<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">`: "
          "senza, i browser mobili simulano uno schermo da desktop e rimpiccioliscono la "
          "pagina."],
         rif=R % "Responsive design"))

d(aperta("c04-a-position", CAP, "posizionamento",
         "Si descrivano i valori della proprietà `position` (`static`, `relative`, `absolute`, "
         "`fixed`, `sticky`), indicando per ciascuno rispetto a che cosa si posiziona "
         "l'elemento e se resta nel flusso.",
         ["`static`: valore predefinito, nel flusso; `top`/`left` non hanno effetto.",
          "`relative`: spostato rispetto alla posizione normale, il suo spazio resta occupato.",
          "`absolute`: fuori dal flusso, rispetto al primo antenato posizionato (o alla "
          "pagina).",
          "`fixed`: fuori dal flusso, rispetto al viewport (resta fermo durante lo "
          "scorrimento).",
          "`sticky`: come `relative` finché non raggiunge la soglia, poi resta attaccato."],
         rif=R % "Posizionamento"))
