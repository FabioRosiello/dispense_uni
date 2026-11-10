"""Capitolo 7: JavaScript nel browser (window, DOM e BOM, ricerca e
navigazione, proprietà dei nodi, modifica della struttura, eventi e loro
propagazione, ordine di esecuzione degli script)."""

from generatore import (FONTE_2024, FONTE_AULA, Err, aperta, chiusa, combina_errori,
                        famiglia, uscita_browser)

CAP = 7
R = "cap. 7, «%s»"
CLIC = ("Si consideri il seguente frammento di documento HTML. Cosa viene stampato in console "
        "in seguito ad un click %s?")

DOMANDE = []
d = DOMANDE.append


def _unici(esiti):
    """Toglie i doppioni da una lista di esiti (liste di righe), in ordine."""
    visti = []
    for e in esiti:
        if e not in visti:
            visti.append(e)
    return visti


def _diversi(a, b):
    """Due esiti (liste di righe o Err) sono diversi?"""
    if isinstance(a, Err) or isinstance(b, Err):
        return not (isinstance(a, Err) and isinstance(b, Err) and a.nome == b.nome)
    return list(a) != list(b)


# ----------------------------------------------------------------------
# Famiglia: i figli del <body> mentre lo script è in esecuzione
ELEMENTI = [("H1", "<h1>Titolo</h1>"), ("P", "<p>Testo</p>"), ("UL", "<ul><li>Uno</li></ul>"),
            ("DIV", "<div>Box</div>"), ("NAV", "<nav>Menu</nav>")]
PROPRIETA = ["childNodes.length", "children.length", "firstChild.nodeName",
             "firstChild.tagName", "firstElementChild.tagName", "lastElementChild.tagName",
             "childNodes[1].nodeName"]


def _proprieta(nodi, prop):
    """Il valore di document.body.<prop>, dati i nomi dei nodi figli del body."""
    elementi = [n for n in nodi if not n.startswith("#")]
    if prop == "childNodes.length":
        return str(len(nodi))
    if prop == "children.length":
        return str(len(elementi))
    if prop == "firstChild.nodeName":
        return nodi[0]
    if prop == "firstChild.tagName":
        return "undefined" if nodi[0].startswith("#") else nodi[0]
    if prop == "firstElementChild.tagName":
        return elementi[0]
    if prop == "lastElementChild.tagName":
        return elementi[-1]
    return nodi[1]                                  # childNodes[1].nodeName


@famiglia("c07-figli", CAP, "navigare il DOM", varianti=4)
def _figli(rng):
    voci = rng.sample(ELEMENTI, rng.choice([2, 3]))
    if rng.random() < 0.6:
        voci.insert(rng.randrange(len(voci) + 1), ("#comment", "<!-- nota -->"))
    nomi = [n for n, _ in voci]
    proprieta = rng.sample(PROPRIETA, 3)
    html = ("<!DOCTYPE html>\n<html>\n<head><title>DOM</title></head>\n<body>\n%s\n"
            "  <script>\n%s\n  </script>\n</body>\n</html>" % (
                "\n".join("  " + sorgente for _, sorgente in voci),
                "\n".join("    console.log(document.body.%s);" % p for p in proprieta)))

    def con_spazi(lista):       # ogni nodo è preceduto dall'a-capo con l'indentazione
        return [x for n in lista for x in ("#text", n)]

    reale = con_spazi(nomi + ["SCRIPT"])
    giusta = [_proprieta(reale, p) for p in proprieta]
    # ragionamenti sbagliati: nessun nodo di testo, lo script non ancora nel DOM,
    # il documento già analizzato per intero, nomi dei tag in minuscolo
    esiti = [[_proprieta(m, p) for p in proprieta]
             for m in (nomi + ["SCRIPT"], con_spazi(nomi), reale + ["#text"])]
    esiti.append([v.lower() if v.isupper() else v for v in giusta])
    alternative = [[e[i] for e in esiti] for i in range(len(proprieta))]
    for i, p in enumerate(proprieta):
        if p == "children.length" and "#comment" in nomi:
            alternative[i].append(str(len(nomi) + 1))       # il commento come elemento
        if p in ("firstChild.tagName", "childNodes[1].nodeName"):
            alternative[i].append("#text" if giusta[i] != "#text" else nomi[0])
    rng.shuffle(esiti)
    return uscita_browser(
        "c07-figli", CAP, "navigare il DOM", html, giusta,
        combina_errori(giusta, alternative, rng, esiti=esiti),
        spiegazione="L'a-capo e l'indentazione fra un tag e l'altro restano nel DOM come **nodi di "
                    "testo** (`#text`): ogni figlio del `<body>` è preceduto da uno di essi. "
                    "Mentre lo script viene eseguito il parser è fermo al tag `<script>`: lo "
                    "script è già nel DOM (è l'ultimo figlio del `<body>`), ciò che lo segue non "
                    "ancora. `nodeName` vale `#text` o `#comment` per testo e commenti e il nome "
                    "del tag in maiuscolo per gli elementi; `tagName` esiste solo per gli "
                    "elementi (su un nodo di testo dà `undefined`). `children` e le proprietà "
                    "`...Element...` considerano soltanto gli elementi.",
        rif=R % "Spazi e a-capo: i nodi di testo che non si vedono")


d(_figli)


# ----------------------------------------------------------------------
# Famiglia: collezioni vive e statiche
@famiglia("c07-collezioni", CAP, "trovare elementi", varianti=3)
def _collezioni(rng):
    n = rng.choice([2, 3, 4])
    lettere = list("ABCD"[:n])
    operazioni = rng.choice([["append"], ["prepend"], ["remove"], ["append", "remove"]])
    istruzioni = {"append": 'ul.append(nuovo("N"));', "prepend": 'ul.prepend(nuovo("N"));',
                  "remove": "ul.firstElementChild.remove();"}
    html = """
<ul>
%s
</ul>
<script>
  function nuovo(testo) {
    const li = document.createElement("li");
    li.textContent = testo;
    return li;
  }
  const ul = document.querySelector("ul");
  const viva = ul.getElementsByTagName("li");
  const statica = ul.querySelectorAll("li");
%s
  console.log(viva.length, statica.length);
  console.log(viva[0].textContent, statica[0].textContent);
</script>""" % ("\n".join("  <li>%s</li>" % c for c in lettere),
                "\n".join("  " + istruzioni[o] for o in operazioni))

    def esegui(scambia=False):
        lista = list(lettere)
        for o in operazioni:
            if scambia and o != "remove":
                o = "prepend" if o == "append" else "append"
            if o == "append":
                lista.append("N")
            elif o == "prepend":
                lista.insert(0, "N")
            else:
                lista.pop(0)
        return lista

    def uscita(viva, statica):
        return ["%d %d" % (len(viva), len(statica)), "%s %s" % (viva[0], statica[0])]

    dopo = esegui()
    giusta = uscita(dopo, lettere)
    esiti = _unici([uscita(dopo, dopo), uscita(lettere, lettere), uscita(lettere, dopo),
                    uscita(esegui(scambia=True), lettere)])
    alternative = [[e[0] for e in esiti], [e[1] for e in esiti]]
    rng.shuffle(esiti)
    return uscita_browser(
        "c07-collezioni", CAP, "trovare elementi", html, giusta,
        combina_errori(giusta, alternative, rng, esiti=esiti),
        spiegazione="`getElementsByTagName` restituisce una `HTMLCollection` **viva**, che riflette "
                    "in ogni momento lo stato del documento; `querySelectorAll` restituisce una "
                    "`NodeList` **statica**, una fotografia scattata al momento della ricerca, "
                    "che continua a contenere gli elementi trovati allora (anche quelli rimossi "
                    "in seguito). `append` inserisce in fondo, `prepend` all'inizio.",
        rif=R % "HTMLCollection e NodeList")


d(_collezioni)


# ----------------------------------------------------------------------
# Famiglia: dove finisce il contenuto inserito
INSERIMENTI = [("prepend", "A"), ("append", "D"), ("append", '"C"'), ("prepend", '"Z"'),
               ("before", '"X"'), ("after", '"Y"')]


@famiglia("c07-inserimento", CAP, "modificare il DOM", varianti=4)
def _inserimento(rng):
    passi = rng.sample(INSERIMENTI, 3)
    righe = []
    for metodo, valore in passi:
        argomento = valore if valore.startswith('"') else 'li("%s")' % valore
        righe.append("  ul.%s(%s);" % (metodo, argomento))
    html = """
<ul><li>B</li></ul>
<script>
  function li(testo) {
    const e = document.createElement("li");
    e.textContent = testo;
    return e;
  }
  const ul = document.querySelector("ul");
%s
  console.log(ul.children.length, ul.childNodes.length);
  console.log(ul.textContent);
</script>""" % "\n".join(righe)

    def esegui(fuori_dentro=False, scambia=False):
        dentro = [("el", "B")]
        for metodo, valore in passi:
            nodo = ("tx", valore.strip('"')) if valore.startswith('"') else ("el", valore)
            if fuori_dentro:
                metodo = {"before": "prepend", "after": "append"}.get(metodo, metodo)
            if scambia:
                metodo = {"prepend": "append", "append": "prepend"}.get(metodo, metodo)
            if metodo == "prepend":
                dentro.insert(0, nodo)
            elif metodo == "append":
                dentro.append(nodo)
        return dentro

    def uscita(dentro, stringhe_elementi=False):
        elementi = len(dentro) if stringhe_elementi else sum(t == "el" for t, _ in dentro)
        return ["%d %d" % (elementi, len(dentro)), "".join(v for _, v in dentro)]

    reale = esegui()
    giusta = uscita(reale)
    esiti = _unici([uscita(reale, stringhe_elementi=True), uscita(esegui(fuori_dentro=True)),
                    uscita(esegui(scambia=True))])
    elementi = sum(t == "el" for t, _ in reale)
    alternative = [[e[0] for e in esiti] + ["%d %d" % (elementi, elementi),
                                            "%d %d" % (elementi + 1, len(reale) + 1)],
                   [e[1] for e in esiti] + ["".join(v for t, v in reale if t == "el")]]
    rng.shuffle(esiti)
    return uscita_browser(
        "c07-inserimento", CAP, "modificare il DOM", html, giusta,
        combina_errori(giusta, alternative, rng, esiti=esiti),
        spiegazione="`prepend` e `append` inseriscono **dentro** l'elemento, all'inizio e in "
                    "fondo; `before` e `after` **fuori**, subito prima e subito dopo di esso. Le "
                    "stringhe diventano nodi di testo: contano in `childNodes` ma non in "
                    "`children`, che contiene solo elementi. `textContent` concatena il testo di "
                    "tutti i discendenti, nell'ordine.",
        rif=R % "Dove: i quattro punti di inserimento")


d(_inserimento)


# ----------------------------------------------------------------------
# Famiglia: onclick e addEventListener
@famiglia("c07-gestori", CAP, "eventi", varianti=3)
def _gestori(rng):
    attributo = rng.random() < 0.6
    n_proprieta = rng.choice([0, 1, 2]) if attributo else rng.choice([1, 2])
    n_listener = rng.choice([1, 2])
    lettere = iter("ABCDE")
    primo = next(lettere) if attributo else None
    proprieta = [next(lettere) for _ in range(n_proprieta)]
    listener = [next(lettere) for _ in range(n_listener)]
    pulsante = ("<button onclick=\"console.log('%s')\">Clic</button>" % primo if attributo
                else "<button>Clic</button>")
    righe = ['  b.onclick = () => console.log("%s");' % p for p in proprieta]
    righe += ['  b.addEventListener("click", () => console.log("%s"));' % x for x in listener]
    html = "%s\n<script>\n  const b = document.querySelector(\"button\");\n%s\n</script>" % (
        pulsante, "\n".join(righe))

    ultimo = proprieta[-1] if proprieta else primo
    giusta = [ultimo] + listener
    esiti = _unici([([primo] if attributo else []) + proprieta + listener,
                    [ultimo] + listener[::-1], listener + [ultimo], [ultimo], listener,
                    [listener[-1]]])
    rng.shuffle(esiti)
    return uscita_browser(
        "c07-gestori", CAP, "eventi", html, giusta, combina_errori(giusta, [], rng, esiti=esiti),
        testo=CLIC % "sul `<button>`", azioni=[{"click": "button"}],
        spiegazione="La proprietà `onclick`, come l'attributo HTML omonimo, contiene **un solo** "
                    "gestore: ogni assegnamento sostituisce il precedente, compreso il codice "
                    "dell'attributo. `addEventListener` invece **aggiunge** un gestore senza "
                    "toccare gli altri. Al clic i gestori vengono eseguiti nell'ordine in cui "
                    "sono stati registrati: qui per primo quello di `onclick`, impostato prima "
                    "dei listener.",
        rif=R % "Gestori di eventi")


d(_gestori)


# ----------------------------------------------------------------------
# Famiglia: bubbling e stopPropagation
LIVELLI = [("b", "button"), ("p", "p"), ("d", "div"), (None, "document")]


@famiglia("c07-propagazione", CAP, "propagazione degli eventi", varianti=4)
def _propagazione(rng):
    con_gestore = sorted(rng.sample(range(4), rng.choice([3, 4])))
    ferma = rng.choice([None, None] + con_gestore[:-1])
    ordine = list(con_gestore)
    rng.shuffle(ordine)
    righe = []
    for i in ordine:
        ident, nome = LIVELLI[i]
        bersaglio = 'document.getElementById("%s")' % ident if ident else "document"
        if i == ferma:
            righe += ['  %s.addEventListener("click", (e) => {' % bersaglio,
                      '    console.log("%s");' % nome,
                      "    e.stopPropagation();",
                      "  });"]
        else:
            righe.append('  %s.addEventListener("click", () => console.log("%s"));'
                         % (bersaglio, nome))
    html = """
<div id="d">
  <p id="p">
    <button id="b">Clic</button>
  </p>
</div>
<script>
%s
</script>""" % "\n".join(righe)

    def risali(fermati=True, escluso=False):
        uscita = []
        for i in con_gestore:
            if fermati and escluso and i == ferma:
                break
            uscita.append(LIVELLI[i][1])
            if fermati and i == ferma:
                break
        return uscita

    giusta = risali()
    senza_document = [x for x in giusta if x != "document"]
    esiti = _unici([risali()[::-1], risali(fermati=False), risali(fermati=False)[::-1],
                    risali(escluso=True), [LIVELLI[i][1] for i in ordine], giusta[:1],
                    senza_document, ["document"] + senza_document, []])
    rng.shuffle(esiti)
    return uscita_browser(
        "c07-propagazione", CAP, "propagazione degli eventi", html, giusta,
        combina_errori(giusta, [], rng, esiti=esiti),
        testo=CLIC % "sul `<button>`", azioni=[{"click": "#b"}],
        spiegazione="Per il *bubbling*, un clic sul pulsante esegue prima i gestori del pulsante, "
                    "poi quelli del suo genitore e così via, risalendo fino a `document`, "
                    "qualunque sia l'ordine in cui i gestori sono stati registrati. "
                    "`stopPropagation()` non interrompe il gestore in cui viene chiamato, ma "
                    "impedisce all'evento di risalire oltre.",
        rif="cap. 7, «Bubbling» e «Fermare il bubbling»")


d(_propagazione)


# ----------------------------------------------------------------------
# Famiglia: delegazione, event.target e this
VOCI = ["Home", "News", "Corsi", "Contatti"]
LETTURE = ["e.target.tagName", "this.tagName", "e.target.textContent", "this.children.length",
           "e.target === this"]


@famiglia("c07-delegazione", CAP, "propagazione degli eventi", varianti=3)
def _delegazione(rng):
    voci = VOCI[:rng.choice([3, 4])]
    k = rng.randrange(1, len(voci))
    letture = rng.sample(LETTURE, 3)
    html = """
<ul id="menu">
%s
</ul>
<script>
  document.getElementById("menu").addEventListener("click", function (e) {
%s
  });
</script>""" % ("\n".join("  <li>%s</li>" % v for v in voci),
                "\n".join("    console.log(%s);" % x for x in letture))

    def valori(this_e_target=False):
        tabella = {"e.target.tagName": "LI", "this.tagName": "UL",
                   "e.target.textContent": voci[k], "this.children.length": str(len(voci)),
                   "e.target === this": "false"}
        if this_e_target:           # come se this fosse l'elemento cliccato
            tabella.update({"this.tagName": "LI", "this.children.length": "0",
                            "e.target === this": "true"})
        return [tabella[x] for x in letture]

    giusta = valori()
    sbagli = {"e.target.tagName": ["UL"], "this.tagName": ["LI"],
              "e.target.textContent": [voci[0], "undefined"],
              "this.children.length": [str(2 * len(voci) + 1), "1"],
              "e.target === this": ["true"]}
    esiti = [valori(this_e_target=True)]
    return uscita_browser(
        "c07-delegazione", CAP, "propagazione degli eventi", html, giusta,
        combina_errori(giusta, [sbagli[x] for x in letture], rng, esiti=esiti),
        testo=CLIC % ("sulla voce «%s»" % voci[k]), azioni=[{"click": "li:nth-child(%d)" % (k + 1)}],
        spiegazione="Il gestore è registrato sulla `<ul>`, ma il clic avviene su un `<li>`: "
                    "l'evento risale per *bubbling* fino alla lista. Nel gestore `this` è "
                    "l'elemento a cui il gestore è stato assegnato (la `<ul>`), mentre "
                    "`event.target` è l'elemento su cui l'evento è stato effettivamente generato "
                    "(il `<li>` cliccato): è ciò che rende possibile la delegazione.",
        rif=R % "Delegazione degli eventi")


d(_delegazione)


# ----------------------------------------------------------------------
# Famiglia: quando viene eseguito uno script esterno
SCRIPT_BASE = 'const h1 = document.body.querySelector("h1");\nconsole.log(h1.innerText);'
SCRIPT_DCL = ('document.addEventListener("DOMContentLoaded", () => {\n'
              '  const h1 = document.body.querySelector("h1");\n'
              "  console.log(h1.innerText);\n});")
SCRIPT_OPZ = 'console.log(document.querySelector("h1")?.innerText);'
CASI_ORDINE = [
    (SCRIPT_BASE, "testa", Err("TypeError")),
    (SCRIPT_BASE, "defer", ["JavaScript"]),
    (SCRIPT_BASE, "fondo", ["JavaScript"]),
    (SCRIPT_DCL, "testa", ["JavaScript"]),
    (SCRIPT_OPZ, "testa", ["undefined"]),
    (SCRIPT_OPZ, "defer", ["JavaScript"]),
]


@famiglia("c07-ordine-script", CAP, "ordine di esecuzione degli script", varianti=3)
def _ordine(rng):
    script, dove, giusta = rng.choice(CASI_ORDINE)
    tag = '<script%s src="app.js"></script>' % (" defer" if dove == "defer" else "")
    testa = "\n  " + tag if dove != "fondo" else ""
    fondo = "\n  " + tag if dove == "fondo" else ""
    html = """
<!DOCTYPE html>
<html>
<head>
  <title>Script</title>%s
</head>
<body>
  <h1>JavaScript</h1>%s
</body>
</html>""" % (testa, fondo)
    tutti = [["JavaScript"], ["undefined"], ["null"], Err("TypeError"), [],
             Err("ReferenceError")]
    sbagliate = [e for e in tutti if _diversi(e, giusta)]
    rng.shuffle(sbagliate)
    return uscita_browser(
        "c07-ordine-script", CAP, "ordine di esecuzione degli script", html, giusta, sbagliate,
        file={"app.js": script},
        testo="Si considerino lo script `app.js` (a sinistra) e la pagina che lo include (a "
              "destra). Qual è l'output in console dopo il caricamento completo della pagina?",
        spiegazione="Uno script senza attributi viene scaricato ed eseguito appena il parser lo "
                    "incontra: nell'`<head>` il `<body>` non esiste ancora, `document.body` vale "
                    "`null` e chiamarvi un metodo solleva un `TypeError` (con `?.` si ottiene "
                    "invece `undefined`). Con `defer` lo script esterno viene eseguito dopo "
                    "l'analisi completa della pagina; lo stesso risultato si ottiene mettendo "
                    "lo script in fondo al `<body>` o attendendo l'evento `DOMContentLoaded`.",
        rif=R % "Ordine di esecuzione degli script")


d(_ordine)


# ----------------------------------------------------------------------
# Dalle prove del corso
d(chiusa("c07-prova-bom", CAP, "DOM e BOM",
         "Quali delle seguenti alternative utilizzano **solo** API comunemente considerate parte "
         "del BOM (*Browser Object Model*)?",
         ["`history.back(); let x = location.href;`"],
         ["`window.document.title = \"foo\"`", "Nessuna delle altre",
          "`location.href = document.body.innerHTML;`", "`document.querySelector(\"a.foo\")`",
          "`document.querySelector(\"h1\").textContent`"],
         multi=True, fisse=True,
         spiegazione="`history` e `location` fanno parte del BOM, che serve a lavorare con il "
                     "browser stesso (cronologia, indirizzo, schermo, informazioni sul browser). "
                     "`document`, e tutto ciò che si raggiunge da esso, è invece il DOM, anche "
                     "quando vi si arriva passando da `window`: le altre alternative usano almeno "
                     "un'API del DOM.",
         rif=R % "Il DOM e il BOM", fonte=FONTE_AULA))

d(uscita_browser("c07-prova-script", CAP, "ordine di esecuzione degli script",
                 """
<!DOCTYPE html>
<html>
  <head><title>DOM</title></head>
  <body>
    <script> console.log(document.body.querySelector("h1")?.textContent) </script>
    <h1>Hello</h1>
  </body>
</html>""",
                 ["undefined"],
                 [["<h1>Hello</h1>"], ["Hello"], Err("TypeError")],
                 fisse=True,
                 spiegazione="Lo script viene eseguito appena il parser lo incontra, quando l'`<h1>` "
                             "che lo segue non è ancora nel DOM: `querySelector` restituisce "
                             "`null`. L'operatore `?.` evita l'errore e dà `undefined` (senza `?.` "
                             "si avrebbe un `TypeError`).",
                 rif=R % "Ordine di esecuzione degli script", fonte=FONTE_AULA))

d(uscita_browser("c07-prova-click", CAP, "propagazione degli eventi",
                 """
<div onclick="console.log('div');">
  <p onclick="console.log('p')">
    <button onclick="console.log('b')">click</button>
  </p>
</div>""",
                 ["b", "p", "div"],
                 [["div"], ["b"], ["div", "p", "b"]],
                 testo=CLIC % "sul `<button>`", azioni=[{"click": "button"}], fisse=True,
                 spiegazione="Per il *bubbling* vengono eseguiti prima i gestori dell'elemento su "
                             "cui è avvenuto il clic, poi quelli del genitore e via via degli altri "
                             "antenati: dal più interno al più esterno.",
                 rif=R % "Bubbling", fonte=FONTE_AULA))

d(uscita_browser("c07-prova-head", CAP, "navigare il DOM",
                 """
<!DOCTYPE html>
<html lang="en">
  <head>
    <title>Web</title>
    <meta charset="UTF-8"/></head>
<body>
 <script>
   let h = document.head?.children;
   console.log(h[1]?.outerHTML);
 </script></body></html>""",
                 ['<meta charset="UTF-8">'],
                 [["undefined"], Err("TypeError"), ["<title>Web</title>"], ["null"],
                  "Una stringa contenente solo spazi bianchi."],
                 dividi=True,
                 spiegazione="`document.head.children` contiene solo gli **elementi** figli di "
                             "`<head>`, senza i nodi di testo: `[0]` è `<title>`, `[1]` è "
                             "`<meta>`. `outerHTML` è il codice dell'elemento ricostruito a "
                             "partire dal DOM: la barra di `/>`, che per il parser non conta, non "
                             "compare.",
                 rif=R % "Navigare fra soli elementi", fonte=FONTE_2024))

# ----------------------------------------------------------------------
d(chiusa("c07-bom", CAP, "DOM e BOM",
         "Quali delle seguenti istruzioni usano **solo** oggetti del BOM (*Browser Object "
         "Model*)?",
         ["`console.log(navigator.userAgent);`", "`history.back();`",
          "`console.log(screen.availWidth);`", "`location.reload();`",
          "`let quante = history.length;`"],
         ["`document.title = location.href;`", "`document.body.style.background = \"pink\";`",
          "`window.document.querySelector(\"p\").remove();`",
          "`let h = document.head.children;`", "`location.href = document.links[0].href;`"],
         multi=True, nessuna=True,
         spiegazione="Il BOM comprende gli oggetti con cui si lavora con il browser: `location` "
                     "(l'URL corrente), `history` (la cronologia), `navigator` (browser e "
                     "piattaforma), `screen` (lo schermo). Tutto ciò che passa da `document` "
                     "appartiene al DOM, anche se vi si arriva da `window`.",
         rif=R % "Il DOM e il BOM"))

d(uscita_browser("c07-window", CAP, "DOM e BOM",
                 """
<script>
  var corso = "TW";
  let anno = 2026;
  function saluta() { return "ciao"; }
  console.log(window.corso, window.anno, typeof window.saluta);
</script>""",
                 ["TW undefined function"],
                 [["TW 2026 function"], ["undefined undefined function"],
                  ["undefined undefined undefined"], ["TW undefined undefined"],
                  Err("ReferenceError")],
                 spiegazione="`window` è l'oggetto globale: le funzioni dichiarate a livello "
                             "globale e le variabili `var` ne diventano proprietà. Le variabili "
                             "`let` e `const` globali vivono invece in uno scope separato e "
                             "**non** diventano proprietà di `window`.",
                 rif=R % "L'oggetto window"))

d(uscita_browser("c07-nessuno", CAP, "trovare elementi",
                 """
<p class="a">Uno</p>
<script>
  console.log(document.querySelector(".b"));
  console.log(document.querySelectorAll(".b").length);
  console.log(document.getElementById("b"));
</script>""",
                 ["null", "0", "null"],
                 [["undefined", "0", "undefined"], ["null", "null", "null"],
                  ["undefined", "undefined", "undefined"], Err("TypeError", ["null"]),
                  ["null", "undefined", "null"]],
                 spiegazione="Quando non trovano nulla, `querySelector` e `getElementById` "
                             "restituiscono `null`. `querySelectorAll` restituisce invece una "
                             "`NodeList` **vuota** (con `length` uguale a 0), come le collezioni "
                             "di `getElementsByTagName` e `getElementsByClassName`: si possono "
                             "scorrere senza controlli.",
                 rif=R % "Trovare elementi"))

d(chiusa("c07-viva", CAP, "trovare elementi",
         "Quali dei seguenti metodi e proprietà restituiscono una collezione **viva**, che si "
         "aggiorna da sola quando il documento cambia?",
         ["`document.getElementsByTagName(\"li\")`", "`document.getElementsByClassName(\"x\")`",
          "`elem.children`", "`elem.childNodes`"],
         ["`document.querySelectorAll(\"li\")`", "`Array.from(elem.children)`",
          "`[...document.getElementsByTagName(\"li\")]`", "`document.querySelector(\"li\")`"],
         multi=True,
         spiegazione="Le `HTMLCollection` (`getElementsByTagName`, `getElementsByClassName`, "
                     "`children`) sono sempre vive, e lo è anche la `NodeList` di `childNodes`. "
                     "La `NodeList` di `querySelectorAll` è statica, e così ogni array ottenuto "
                     "copiando una collezione con `Array.from` o con lo spread. `querySelector` "
                     "restituisce un solo elemento, non una collezione.",
         rif=R % "HTMLCollection e NodeList"))

d(chiusa("c07-interfacce", CAP, "proprietà dei nodi",
         "Sia `input` l'oggetto DOM corrispondente a un elemento `<input type=\"text\">` della "
         "pagina. Quali delle seguenti espressioni valgono `true`?",
         ["`input instanceof HTMLElement`", "`input instanceof Node`",
          "`input instanceof EventTarget`", "`input instanceof Element`"],
         ["`input instanceof Text`", "`input instanceof Document`",
          "`input instanceof HTMLAnchorElement`", "`input instanceof CharacterData`"],
         multi=True,
         spiegazione="Le interfacce del DOM formano una gerarchia: un `<input>` è un "
                     "`HTMLInputElement`, quindi anche un `HTMLElement`, un `Element`, un `Node` "
                     "e un `EventTarget`. Non è un nodo di testo (`Text`, che discende da "
                     "`CharacterData`), né il documento, né un link.",
         rif=R % "La gerarchia delle interfacce",
         verifica=dict(tipo="dom", html='<!DOCTYPE html><input type="text" value="ciao">',
                       espressione="(() => { const input = document.querySelector('input'); "
                                   "return JSON.stringify([input instanceof HTMLElement, "
                                   "input instanceof Node, input instanceof EventTarget, "
                                   "input instanceof Element, input instanceof Text, "
                                   "input instanceof Document, "
                                   "input instanceof HTMLAnchorElement, "
                                   "input instanceof CharacterData]); })()",
                       atteso="[true,true,true,true,false,false,false,false]")))

d(uscita_browser("c07-innerhtml", CAP, "proprietà dei nodi",
                 """
<div id="d">Ciao <b>mondo</b></div>
<script>
  const d = document.getElementById("d");
  console.log(d.innerHTML);
  console.log(d.textContent);
  console.log(d.outerHTML);
</script>""",
                 ["Ciao <b>mondo</b>", "Ciao mondo", '<div id="d">Ciao <b>mondo</b></div>'],
                 [["Ciao mondo", "Ciao <b>mondo</b>", '<div id="d">Ciao <b>mondo</b></div>'],
                  ['<div id="d">Ciao <b>mondo</b></div>', "Ciao mondo", "Ciao <b>mondo</b>"],
                  ["Ciao <b>mondo</b>", "Ciao <b>mondo</b>",
                   '<div id="d">Ciao <b>mondo</b></div>'],
                  ["Ciao <b>mondo</b>", "Ciao mondo", "undefined"],
                  ["Ciao <b>mondo</b>", "Ciao", '<div id="d">Ciao <b>mondo</b></div>']],
                 spiegazione="`innerHTML` è il codice HTML contenuto nell'elemento, `outerHTML` "
                             "quello dell'elemento intero, tag di apertura e chiusura compresi. "
                             "`textContent` è soltanto il testo di tutti i discendenti, senza "
                             "markup.",
                 rif=R % "innerHTML e outerHTML"))

d(uscita_browser("c07-attributi", CAP, "proprietà dei nodi",
                 """
<input id="x" class="inp ok" custom="y" data-user-id="42">
<script>
  const i = document.querySelector("input");
  i.custom = "z";
  console.log(i.id, i.className, i.custom, i.getAttribute("custom"));
  console.log(i.dataset.userId, i.classList.length);
</script>""",
                 ["x inp ok z y", "42 2"],
                 [["x inp ok z z", "42 2"], ["x undefined z y", "42 2"],
                  ["x inp ok y y", "42 2"], ["x inp ok z y", "undefined 2"],
                  ["x inp ok z y", "42 1"]],
                 spiegazione="Per gli attributi **standard** (`id`, `class`...) il browser crea "
                             "proprietà corrispondenti (per `class` si chiamano `className` e "
                             "`classList`, perché `class` è una parola riservata). Per un "
                             "attributo non standard no: `i.custom = \"z\"` crea solo una "
                             "proprietà JavaScript, e `getAttribute` continua a leggere il valore "
                             "scritto nell'HTML. Gli attributi `data-*` si leggono da `dataset`, "
                             "con i nomi in *camelCase*.",
                 rif=R % "Attributi"))

d(uscita_browser("c07-crea", CAP, "modificare il DOM",
                 """
<ul><li>A</li><li>B</li></ul>
<ol></ol>
<script>
  const h = document.createElement("h1");
  h.textContent = "Titolo";
  console.log(document.querySelectorAll("h1").length);
  const ul = document.querySelector("ul");
  document.querySelector("ol").append(ul.firstElementChild);
  console.log(ul.children.length, document.querySelectorAll("li").length);
</script>""",
                 ["0", "1 2"],
                 [["1", "1 2"], ["0", "2 3"], ["1", "2 3"], ["0", "1 1"], ["0", "2 2"]],
                 spiegazione="`createElement` crea l'elemento solo in memoria: finché non viene "
                             "inserito con `append`, `prepend`, `before` o `after` non fa parte "
                             "del documento. `append` di un nodo già presente non lo copia, lo "
                             "**sposta**: un nodo può stare in un solo punto dell'albero.",
                 rif=R % "Come: creare i nodi"))

d(chiusa("c07-prompt", CAP, "interagire con l'utente",
         "Uno script esegue `let n = prompt(\"Inserisci un numero:\");` e l'utente scrive `3` e "
         "preme OK. Che cosa contiene `n`?",
         "La stringa `\"3\"`.",
         ["Il numero `3`.", "Il valore `true`.", "Il valore `undefined`.", "Il valore `null`.",
          "Un oggetto evento che contiene il valore digitato."],
         spiegazione="`prompt` restituisce sempre il testo digitato **come stringa** (per usarlo "
                     "come numero serve una conversione, per esempio con `parseInt`), oppure "
                     "`null` se l'utente preme Annulla. `confirm` restituisce un booleano, "
                     "`alert` nulla.",
         rif=R % "Interagire con l'utente"))

d(chiusa("c07-bloccanti", CAP, "interagire con l'utente",
         "Quali delle seguenti affermazioni su `alert`, `confirm` e `prompt` sono **vere**?",
         ["Sospendono l'esecuzione dello script finché l'utente non risponde.",
          "`confirm` restituisce `true` se l'utente preme OK e `false` se preme Annulla.",
          "`prompt` restituisce `null` se l'utente preme Annulla."],
         ["`alert` restituisce `true` quando l'utente preme OK.",
          "Lo script prosegue mentre la finestra è aperta, e la risposta arriva in una callback.",
          "`prompt` converte automaticamente in numero un valore numerico digitato.",
          "Sono funzioni del linguaggio JavaScript, disponibili anche in Node.js.",
          "Il loro aspetto si personalizza con i CSS della pagina."],
         multi=True,
         spiegazione="Sono finestre di dialogo **bloccanti** fornite dal browser: lo script si "
                     "ferma finché l'utente non risponde. `alert` non restituisce nulla, "
                     "`confirm` un booleano, `prompt` il testo digitato (sempre una stringa) o "
                     "`null`. Non si possono impaginare: nelle applicazioni reali si preferiscono "
                     "finestre costruite nel DOM.",
         rif=R % "Interagire con l'utente"))

d(uscita_browser("c07-chiamare", CAP, "eventi",
                 """
<button>Salutami</button>
<script>
  function saluta() { console.log("Ciao!"); }
  const btn = document.querySelector("button");
  btn.addEventListener("click", saluta());
  console.log("pronto");
</script>""",
                 ["Ciao!", "pronto"],
                 [["pronto", "Ciao!"], ["Ciao!", "pronto", "Ciao!"], ["pronto"],
                  Err("TypeError", ["Ciao!"]), ["Ciao!", "Ciao!", "pronto"]],
                 testo="Qual è l'output complessivo in console dopo il caricamento del documento "
                       "HTML riportato di seguito e un click sul pulsante?",
                 azioni=[{"click": "button"}],
                 spiegazione="Con le parentesi `saluta()` viene **chiamata subito**, durante il "
                             "caricamento, e ad `addEventListener` arriva il suo valore di "
                             "ritorno, `undefined`: nessun gestore viene registrato e il clic non "
                             "stampa nulla. Per registrare un gestore si passa la funzione senza "
                             "parentesi: `addEventListener(\"click\", saluta)`.",
                 rif=R % "Evento e funzione gestore: chi chiama chi"))

d(uscita_browser("c07-this", CAP, "eventi",
                 """
<button id="b1">Uno</button>
<button id="b2">Due</button>
<script>
  document.getElementById("b1").addEventListener("click", function () {
    console.log(this.id);
  });
  document.getElementById("b2").addEventListener("click", () => {
    console.log(this === window);
  });
</script>""",
                 ["b1", "true"],
                 [["b1", "false"], ["undefined", "true"], ["undefined", "false"],
                  ["window", "true"], ["b1", "undefined"]],
                 testo=CLIC % "sul pulsante «Uno» e poi su «Due»",
                 azioni=[{"click": "#b1"}, {"click": "#b2"}],
                 spiegazione="In un gestore definito con `function`, `this` è l'elemento a cui il "
                             "gestore è stato assegnato. Le *arrow function* non hanno un `this` "
                             "proprio e usano quello del codice in cui sono scritte: qui il "
                             "livello globale dello script, dove `this` è `window`.",
                 rif=R % "Il valore di this in un gestore"))

d(uscita_browser("c07-dispatch", CAP, "eventi",
                 """
<button>Clic</button>
<script>
  const b = document.querySelector("button");
  b.addEventListener("click", (e) => console.log(e.type, e.isTrusted));
  b.dispatchEvent(new Event("click"));
</script>""",
                 ["click false"],
                 [["click true"], [], ["click undefined"], Err("TypeError"), ["undefined false"]],
                 spiegazione="Con `dispatchEvent` un evento si può generare da JavaScript: i gestori "
                             "registrati per quel tipo di evento vengono eseguiti come per un evento "
                             "vero. La proprietà `isTrusted` permette di distinguerli: vale `false` "
                             "per gli eventi generati da uno script, `true` per quelli prodotti "
                             "dall'utente.",
                 rif=R % "Generare eventi da JavaScript"))

d(chiusa("c07-domcontentloaded", CAP, "eventi",
         "Quale evento scatta **appena** l'HTML della pagina è stato analizzato per intero e il "
         "DOM è completo, senza attendere che la pagina sia stata caricata e disegnata?",
         "`DOMContentLoaded`",
         ["`load`", "`ready`", "`submit`", "`focus`", "`parsed`"],
         spiegazione="`DOMContentLoaded` scatta quando il DOM è completo; `load` più tardi, quando "
                     "la pagina è stata caricata e disegnata per intero. Registrare il codice "
                     "come gestore di `DOMContentLoaded` permette a uno script di trovare gli "
                     "elementi della pagina ovunque sia incluso.",
         rif=R % "Eventi"))

d(chiusa("c07-focus", CAP, "propagazione degli eventi",
         "Quale dei seguenti eventi **non** fa *bubbling*?",
         "`focus`",
         ["`click`", "`keydown`", "`mouseover`", "`keyup`", "`mousedown`"],
         spiegazione="Il *bubbling* vale per la maggior parte degli eventi, ma non per tutti: gli "
                     "eventi di `focus` non risalgono verso gli antenati.",
         rif=R % "Bubbling"))

d(chiusa("c07-delega-vantaggi", CAP, "propagazione degli eventi",
         "Una tabella ha centinaia di celle `<td>`, a cui si aggiungono righe nuove durante l'uso "
         "della pagina. Perché conviene un solo gestore sulla `<table>` invece di uno per cella?",
         "Il gestore riceve i clic di tutte le celle per *bubbling*, anche di quelle aggiunte "
         "dopo, e `event.target` dice quale cella è stata cliccata.",
         ["Perché i gestori registrati sulle `<td>` vengono ignorati dal browser.",
          "Perché un gestore sulla `<table>` viene eseguito prima di quelli delle celle.",
          "Perché `this` nel gestore della tabella è la cella cliccata.",
          "Perché le celle aggiunte dopo il caricamento non generano eventi.",
          "Perché con un solo gestore l'evento non fa *bubbling*."],
         spiegazione="È la **delegazione degli eventi**: grazie al *bubbling* basta un gestore "
                     "sull'antenato comune, e `event.target` indica l'elemento su cui l'evento è "
                     "stato generato (`this` resta la tabella). Le righe aggiunte dinamicamente "
                     "funzionano subito, senza registrare nuovi gestori.",
         rif=R % "Delegazione degli eventi"))

d(chiusa("c07-testo-utente", CAP, "proprietà dei nodi",
         "Si vuole mostrare in un `<div>` il nome scritto dall'utente in un campo di testo. Quale "
         "proprietà conviene assegnare, per evitare che eventuale markup nel nome venga "
         "interpretato?",
         "`textContent`",
         ["`innerHTML`", "`outerHTML`", "`tagName`", "`nodeName`", "`className`"],
         spiegazione="`innerHTML` e `outerHTML` passano la stringa al parser HTML: un nome che "
                     "contiene markup (per esempio un `<img onerror=...>`) verrebbe interpretato, "
                     "ed è la porta per un attacco di *Cross-Site Scripting* (XSS). "
                     "`textContent` (o `innerText`) inserisce soltanto testo.",
         rif=R % "innerHTML e outerHTML"))

d(chiusa("c07-script-attributi", CAP, "ordine di esecuzione degli script",
         "Quali delle seguenti affermazioni sull'esecuzione degli script in una pagina sono "
         "**vere**?",
         ["Senza attributi, l'analisi della pagina si sospende mentre lo script viene scaricato "
          "ed eseguito.",
          "Uno script esterno con `defer` viene scaricato in parallelo ed eseguito dopo l'analisi "
          "completa della pagina.",
          "Uno script esterno con `async` viene eseguito appena è stato scaricato.",
          "Gli script di tipo modulo si comportano come `defer` per impostazione predefinita."],
         ["Uno script con `defer` viene eseguito appena è stato scaricato, interrompendo "
          "l'analisi della pagina.",
          "Uno script con `async` attende sempre l'evento `DOMContentLoaded`.",
          "Uno script senza attributi nell'`<head>` può già accedere agli elementi del `<body>`.",
          "Gli script `async` vengono sempre eseguiti nell'ordine in cui compaiono.",
          "Senza attributi, gli script vengono eseguiti solo dopo l'evento `load`."],
         multi=True,
         spiegazione="Uno script normale blocca l'analisi finché non è stato scaricato ed "
                     "eseguito, e vede solo la parte di pagina che lo precede. `defer` e `async` "
                     "fanno scaricare lo script in parallelo: con `defer` viene eseguito a pagina "
                     "analizzata, con `async` appena pronto (quindi in un momento, e in un "
                     "ordine, non prevedibili). I moduli sono differiti per impostazione "
                     "predefinita.",
         rif=R % "Ordine di esecuzione degli script"))

# ----------------------------------------------------------------------
# Domande aperte
d(aperta("c07-a-async-defer", CAP, "ordine di esecuzione degli script",
         "Si spieghino brevemente analogie e differenze tra gli attributi `async` e `defer` in un "
         "elemento `<script>`.",
         ["Analogie: valgono per gli script esterni (con `src`); con entrambi lo script viene "
          "scaricato in parallelo all'analisi della pagina, senza sospenderla durante il "
          "download.",
          "`defer`: lo script viene eseguito dopo l'analisi completa della pagina (prima di "
          "`DOMContentLoaded`): trova il DOM completo, e più script `defer` rispettano l'ordine "
          "in cui compaiono.",
          "`async`: lo script viene eseguito appena è stato scaricato, anche a pagina non ancora "
          "analizzata: non si sa se il DOM sia completo, né in che ordine vengano eseguiti più "
          "script `async`.",
          "`defer` per gli script che usano il DOM o dipendono l'uno dall'altro; `async` per "
          "quelli indipendenti. I moduli sono differiti per impostazione predefinita."],
         rif=R % "Ordine di esecuzione degli script", fonte=FONTE_2024))

d(aperta("c07-a-dom-bom", CAP, "DOM e BOM",
         "Che cosa sono il DOM e il BOM? Si descriva il ruolo dell'oggetto `window` e si "
         "facciano esempi di oggetti e operazioni di ciascuno.",
         ["`window` è l'oggetto globale dell'ambiente del browser (funzioni e variabili `var` "
          "globali ne diventano proprietà) e rappresenta la finestra del browser.",
          "Il DOM rappresenta il contenuto del documento come un albero di nodi (elementi, "
          "testo, commenti) con radice `document`: serve a leggere e modificare la pagina "
          "(`querySelector`, `textContent`, `append`...).",
          "Il BOM comprende gli oggetti per lavorare con il browser stesso: `location` (URL), "
          "`history` (cronologia), `navigator` (browser e piattaforma), `screen` (schermo).",
          "Entrambi sono forniti dall'ambiente ospite, non dal linguaggio: in Node.js non "
          "esistono."],
         rif=R % "L'ambiente del browser"))

d(aperta("c07-a-collezioni", CAP, "trovare elementi",
         "Si spieghino le differenze fra `HTMLCollection` e `NodeList`, indicando quali metodi e "
         "proprietà le restituiscono e che cosa significa che una collezione è *viva*.",
         ["`HTMLCollection` contiene solo elementi; `NodeList` può contenere nodi di qualunque "
          "tipo (anche testo e commenti).",
          "`getElementsByTagName`, `getElementsByClassName` e `children` restituiscono "
          "`HTMLCollection`; `querySelectorAll`, `getElementsByName` e `childNodes` restituiscono "
          "`NodeList`.",
          "Viva: riflette in ogni momento lo stato del documento (le `HTMLCollection`, "
          "`childNodes`); statica: una fotografia al momento della ricerca (`querySelectorAll`).",
          "Entrambe hanno `length` e indici e si scorrono con `for...of`, ma non sono array: per "
          "`map` o `filter` si converte con `Array.from` o con lo spread."],
         rif=R % "HTMLCollection e NodeList"))

d(aperta("c07-a-eventi", CAP, "eventi",
         "Si descrivano i modi per associare un gestore a un evento in una pagina web, il "
         "meccanismo del *bubbling* e il pattern della delegazione degli eventi.",
         ["Attributo HTML `onclick=\"...\"` (codice come stringa), proprietà `elem.onclick = f` "
          "(un solo gestore: un nuovo assegnamento lo sostituisce), `addEventListener(\"click\", "
          "f)` (più gestori, rimovibili con `removeEventListener`).",
          "Il gestore è una callback: si passa la funzione senza chiamarla; il browser la "
          "invoca a ogni evento passandole l'oggetto evento, e `this` è l'elemento del gestore.",
          "*Bubbling*: dopo i gestori dell'elemento su cui è avvenuto l'evento vengono eseguiti "
          "quelli dei suoi antenati, fino a `document`; `stopPropagation()` ferma la risalita.",
          "Delegazione: un solo gestore sull'antenato comune, che usa `event.target` per sapere "
          "dove è avvenuto l'evento; funziona anche per gli elementi aggiunti in seguito."],
         rif="cap. 7, «Eventi» e «Propagazione degli eventi»"))

d(aperta("c07-a-innerhtml", CAP, "proprietà dei nodi",
         "Si confrontino `innerHTML`, `outerHTML` e `textContent`, e si spieghi perché assegnare "
         "a `innerHTML` dati forniti dall'utente è pericoloso.",
         ["`innerHTML` è il codice HTML contenuto nell'elemento, `outerHTML` quello dell'intero "
          "elemento (tag compresi), `textContent` solo il testo dei discendenti.",
          "Sono scrivibili: assegnare `innerHTML` sostituisce il contenuto, assegnare "
          "`outerHTML` l'elemento intero; la stringa passa dal parser HTML, che la interpreta "
          "(e la corregge) come farebbe con un file.",
          "Se la stringa contiene dati dell'utente, l'eventuale markup viene interpretato "
          "(`<script>`, attributi come `onerror`): è la via per il *Cross-Site Scripting* (XSS).",
          "Per inserire testo si usa `textContent` (o `innerText`), oppure si creano i nodi con "
          "`createElement` e `createTextNode`."],
         rif=R % "innerHTML e outerHTML"))
