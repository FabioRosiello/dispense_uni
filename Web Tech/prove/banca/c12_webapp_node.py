"""Capitolo 12: applicazioni web con Node.js (routing per percorso e metodo,
file statici ed errori, template Pug, lettura del corpo delle richieste,
Post/Redirect/Get)."""

from generatore import (Err, aperta, chiusa, combina_errori, famiglia, risposte_server,
                        uscita_js, uscita_pug)

CAP = 12
R = "cap. 12, «%s»"

DOMANDE = []
d = DOMANDE.append


def _unici(esiti):
    visti = []
    for e in esiti:
        if e not in visti:
            visti.append(e)
    return visti


# ----------------------------------------------------------------------
# Famiglia: un router fatto con switch
ROUTER = """
import http from "http";

http.createServer((request, response) => {
  switch (request.url) {
    case "/":
      response.writeHead(200);
      response.end("Home");
      break;
    case "/todo":
      if (request.method === "GET") {
        response.writeHead(200);
        response.end("La lista");
      } else {
        response.writeHead(405);
        response.end("Metodo non supportato");
      }
      break;
    default:
      response.writeHead(404);
      response.end("Pagina non trovata");
  }
}).listen(3000);"""
HOME, LISTA, NO_METODO, NON_TROVATA = ("200 Home", "200 La lista", "405 Metodo non supportato",
                                       "404 Pagina non trovata")
RICHIESTE = ["GET /todo?ordina=si", "GET /todo/", "GET /Todo", "POST /todo", "DELETE /",
             "GET /todo", "PUT /todo"]


def _instrada(richiesta, senza_query=False, ogni_metodo=False, tollerante=False,
              metodo_404=False):
    metodo, url = richiesta.split(" ")
    if senza_query:
        url = url.split("?")[0]
    if tollerante:
        url = url.lower().rstrip("/") or "/"
    if url == "/":
        return NO_METODO if ogni_metodo and metodo != "GET" else HOME
    if url == "/todo":
        if metodo == "GET":
            return LISTA
        return NON_TROVATA if metodo_404 else NO_METODO
    return NON_TROVATA


@famiglia("c12-router", CAP, "routing", varianti=4)
def _router(rng):
    scelte = [rng.choice(RICHIESTE[:3]), rng.choice(RICHIESTE[3:5]),
              rng.choice([r for r in RICHIESTE if r not in RICHIESTE[:1]])]
    while len(set(scelte)) < 3:
        scelte[2] = rng.choice(RICHIESTE)
    rng.shuffle(scelte)
    giusta = [_instrada(r) for r in scelte]
    esiti = _unici([[_instrada(r, **opz) for r in scelte] for opz in
                    ({"senza_query": True}, {"ogni_metodo": True}, {"tollerante": True},
                     {"metodo_404": True}, {"senza_query": True, "tollerante": True},
                     {"senza_query": True, "ogni_metodo": True})])
    esiti = [e for e in esiti if e != giusta]
    alternative = [[HOME, LISTA, NO_METODO, NON_TROVATA] for _ in scelte]
    rng.shuffle(esiti)
    return risposte_server(
        "c12-router", CAP, "routing", ROUTER, scelte, giusta,
        combina_errori(giusta, alternative, rng, esiti=esiti),
        spiegazione="Lo `switch` confronta `request.url` con stringhe **esatte**, e "
                    "`request.url` contiene anche la query string: `/todo?ordina=si`, "
                    "`/todo/` e `/Todo` non sono `/todo` e finiscono nel ramo `404`. Il metodo "
                    "viene controllato solo per `/todo`: lì ogni metodo diverso da `GET` riceve "
                    "`405` (il percorso esiste, il metodo no); `/` risponde a qualunque metodo.",
        rif="cap. 12, «Instradare in base al percorso» e «Instradare anche in base al metodo»")


d(_router)


# ----------------------------------------------------------------------
# Famiglia: decodificare il corpo di un form
VALORI = [("Prove that P=NP", "Prove+that+P%3DNP"), ("C++ & Java", "C%2B%2B+%26+Java"),
          ("50% di sconto", "50%25+di+sconto"), ("a+b=c", "a%2Bb%3Dc"),
          ("Ciao mondo", "Ciao+mondo")]
DECODIFICA = """
function decodifica(corpo) {
  let dati = {};
  for (let pezzo of corpo.split("&")) {
    let [nome, valore] = pezzo.split("=");
    nome = decodeURIComponent(nome.replace(/\\+/g, " "));
    valore = %s;
    dati[nome] = valore;
  }
  return dati;
}
const dati = decodifica("%s");
console.log(dati.todo);
console.log(dati.quando);"""
MODI = {
    "giusto": 'decodeURIComponent(valore.replace(/\\+/g, " "))',
    "senza_piu": "decodeURIComponent(valore)",
    "invertito": 'decodeURIComponent(valore).replace(/\\+/g, " ")',
    "senza_decode": 'valore.replace(/\\+/g, " ")',
}


def _js_decodifica(codificato, modo):
    import urllib.parse
    if modo == "giusto":
        return urllib.parse.unquote(codificato.replace("+", " "))
    if modo == "senza_piu":
        return urllib.parse.unquote(codificato)
    if modo == "invertito":
        return urllib.parse.unquote(codificato).replace("+", " ")
    return codificato.replace("+", " ")


@famiglia("c12-corpo", CAP, "corpo delle richieste", varianti=3)
def _corpo(rng):
    testo, codificato = rng.choice(VALORI[:4])
    quando, quando_cod = rng.choice([("fra due giorni", "fra+due+giorni"),
                                     ("entro le 10:30", "entro+le+10%3A30")])
    modo = rng.choice(["giusto", "giusto", "senza_piu", "invertito"])
    corpo = "todo=%s&quando=%s" % (codificato, quando_cod)
    codice = DECODIFICA % (MODI[modo], corpo)
    giusta = [_js_decodifica(codificato, modo), _js_decodifica(quando_cod, modo)]
    esiti = _unici([[_js_decodifica(codificato, m), _js_decodifica(quando_cod, m)]
                    for m in MODI if m != modo])
    esiti += [[codificato, quando_cod], [testo, quando]]
    esiti = [e for e in esiti if e != giusta]
    alternative = [[_js_decodifica(codificato, m) for m in MODI] + [codificato],
                   [_js_decodifica(quando_cod, m) for m in MODI] + [quando_cod]]
    rng.shuffle(esiti)
    return uscita_js(
        "c12-corpo", CAP, "corpo delle richieste", codice, giusta,
        combina_errori(giusta, alternative, rng, esiti=esiti),
        spiegazione="Il corpo di un form è codificato come URL: gli spazi diventano `+` e i "
                    "caratteri speciali sequenze `%XX` (`%2B` è il `+`, `%3D` l'`=`, `%26` la "
                    "`&`, `%25` il `%`). Per decodificarlo bisogna sostituire i `+` con spazi "
                    "**e poi** applicare `decodeURIComponent`: saltare un passaggio, o farli "
                    "nell'ordine sbagliato, produce errori che compaiono solo con certi input "
                    "(un `+` scritto dall'utente diventerebbe uno spazio).",
        rif=R % "Interpretare la stringa")


d(_corpo)


# ----------------------------------------------------------------------
# Famiglia: each ... else
PRODOTTI = [("Pane", 2), ("Latte", 1), ("Uova", 3), ("Mele", 4)]
EACH = """
ul
  each item in items
    li #{item.nome} (#{item.prezzo})
  else
    li Nessun prodotto"""


@famiglia("c12-pug-each", CAP, "template Pug", varianti=3)
def _each(rng):
    items = rng.sample(PRODOTTI, rng.choice([0, 2, 3]))
    chiamata = ("pug.renderFile(\"pagina.pug\", {\n  items: [\n%s\n  ]\n});"
                % "\n".join('    { nome: "%s", prezzo: %d },' % p for p in items)
                if items else 'pug.renderFile("pagina.pug", { items: [] });')
    voci = ["<li>%s (%d)</li>" % p for p in items]
    vuoto = "<li>Nessun prodotto</li>"
    giusta = "<ul>%s</ul>" % ("".join(voci) if items else vuoto)
    sbagliate = ["<ul>%s</ul>" % ("".join(voci) + vuoto), "<ul></ul>",
                 "<ul><li>#{item.nome} (#{item.prezzo})</li></ul>",
                 "<ul>%s</ul>" % "".join(voci[::-1]) if len(items) > 1 else
                 "<ul><li>undefined (undefined)</li></ul>",
                 "".join(voci) if items else vuoto,
                 "<ul><li>%s</li></ul>" % ", ".join("%s (%d)" % p for p in items) if items else
                 "Viene sollevato un errore, perché la lista è vuota."]
    sbagliate = [s for s in _unici(sbagliate) if s != giusta]
    rng.shuffle(sbagliate)
    return uscita_pug(
        "c12-pug-each", CAP, "template Pug", EACH, giusta, sbagliate[:5],
        locals={"items": [{"nome": n, "prezzo": p} for n, p in items]}, chiamata=chiamata,
        spiegazione="`each` ripete il blocco annidato per ogni elemento della collezione, "
                    "nell'ordine; il ramo `else` viene usato **solo** se la collezione è vuota. "
                    "`#{...}` valuta l'espressione e ne inserisce il valore. Pug produce HTML "
                    "compatto, senza spazi fra i tag.",
        rif=R % "Iterazioni")


d(_each)


# ----------------------------------------------------------------------
# Famiglia: if / else if / else
CONDIZIONALE = """
if !user
  a(href="/login") Accedi
else if user.isAdmin
  p Ai tuoi ordini, #{user.name}
else
  p Bentornato, #{user.name}"""


@famiglia("c12-pug-if", CAP, "template Pug", varianti=3)
def _condizionale(rng):
    nome = rng.choice(["Ada", "Alan", "Grace"])
    caso = rng.choice(["anonimo", "admin", "utente"])
    rami = {"anonimo": '<a href="/login">Accedi</a>', "admin": "<p>Ai tuoi ordini, %s</p>" % nome,
            "utente": "<p>Bentornato, %s</p>" % nome}
    if caso == "anonimo":
        chiamata = 'pug.renderFile("pagina.pug", {});'
        locals_ = {}
    else:
        chiamata = ('pug.renderFile("pagina.pug", {\n  user: { name: "%s", isAdmin: %s }\n});'
                    % (nome, "true" if caso == "admin" else "false"))
        locals_ = {"user": {"name": nome, "isAdmin": caso == "admin"}}
    giusta = rami[caso]
    sbagliate = [v for k, v in rami.items() if k != caso]
    sbagliate += ["".join(rami.values()), rami["admin"] + rami["utente"],
                  "<p>Bentornato, </p>" if caso != "utente" else "<p>Bentornato, user.name</p>"]
    if caso == "anonimo":
        sbagliate.append("Viene sollevato un errore, perché `user` non è definito.")
    sbagliate = [s for s in _unici(sbagliate) if s != giusta]
    rng.shuffle(sbagliate)
    return uscita_pug(
        "c12-pug-if", CAP, "template Pug", CONDIZIONALE, giusta, sbagliate[:5],
        locals=locals_, chiamata=chiamata,
        spiegazione="In un condizionale Pug finisce nell'HTML **solo** il ramo scelto. Se "
                    "`user` manca, `!user` è vero e si mostra il link di accesso (le espressioni "
                    "degli altri rami non vengono nemmeno valutate); altrimenti si sceglie in "
                    "base a `user.isAdmin`.",
        rif=R % "Condizionali")


d(_condizionale)


# ----------------------------------------------------------------------
# Famiglia: ereditarietà fra template
LAYOUT = """
html
  body
    block intestazione
      h1 Il mio sito
    block contenuto
    block piede
      footer Predefinito"""
BLOCCHI = {"intestazione": "  h1 Offerte", "contenuto": "  p Benvenuto!",
           "piede": "  footer Contatti"}
HTML_BLOCCHI = {"intestazione": ("<h1>Il mio sito</h1>", "<h1>Offerte</h1>"),
                "contenuto": ("", "<p>Benvenuto!</p>"),
                "piede": ("<footer>Predefinito</footer>", "<footer>Contatti</footer>")}
ORDINE = ["intestazione", "contenuto", "piede"]


@famiglia("c12-pug-blocchi", CAP, "template Pug", varianti=3)
def _blocchi(rng):
    sovrascritti = ["contenuto"] + rng.sample(["intestazione", "piede"], rng.choice([1, 2]))
    rng.shuffle(sovrascritti)
    pagina = "extends layout.pug\n\n" + "\n".join(
        "block %s\n%s" % (b, BLOCCHI[b]) for b in sovrascritti)

    def genera(predefiniti=True, sostituisci=True, in_coda=False):
        parti = []
        for b in ORDINE:
            base, nuovo = HTML_BLOCCHI[b]
            if b in sovrascritti and not in_coda:
                parti.append(nuovo if sostituisci else base + nuovo)
            elif b not in sovrascritti and predefiniti:
                parti.append(base)
            elif b in sovrascritti and in_coda:
                parti.append(base)
        if in_coda:
            parti += [HTML_BLOCCHI[b][1] for b in sovrascritti]
        return "<html><body>%s</body></html>" % "".join(parti)

    giusta = genera()
    sbagliate = _unici([genera(predefiniti=False), genera(sostituisci=False),
                        genera(in_coda=True),
                        "<html><body>%s</body></html>" % "".join(
                            HTML_BLOCCHI[b][1] for b in sovrascritti),
                        "<html><body>%s</body></html>" % "".join(
                            HTML_BLOCCHI[b][0] for b in ORDINE)])
    sbagliate = [s for s in sbagliate if s != giusta]
    rng.shuffle(sbagliate)
    return uscita_pug(
        "c12-pug-blocchi", CAP, "template Pug", pagina, giusta, sbagliate,
        file={"layout.pug": LAYOUT},
        testo="Il template `pagina.pug` (a destra) estende `layout.pug` (a sinistra). Quale "
              "codice HTML genera `pagina.pug`?",
        spiegazione="Con `extends` la pagina figlia riprende il layout e **sostituisce** i "
                    "blocchi che ridefinisce, nella posizione che hanno nel layout; i blocchi "
                    "che non ridefinisce mantengono il contenuto predefinito (un blocco vuoto "
                    "nel layout, se non ridefinito, non produce nulla).",
        rif=R % "Ereditarietà fra template")


d(_blocchi)

# ----------------------------------------------------------------------
d(uscita_pug("c12-pug-escape", CAP, "template Pug",
             """
- let titolo = "Prodotti"
h1 #{titolo.toUpperCase()}
p Offerta: #{descrizione}""",
             "<h1>PRODOTTI</h1><p>Offerta: &lt;b&gt;sconto&lt;/b&gt;</p>",
             ["<h1>PRODOTTI</h1><p>Offerta: <b>sconto</b></p>",
              "- let titolo = \"Prodotti\"<h1>PRODOTTI</h1><p>Offerta: <b>sconto</b></p>",
              "<h1>#{titolo.toUpperCase()}</h1><p>Offerta: #{descrizione}</p>",
              "<h1>Prodotti</h1><p>Offerta: &lt;b&gt;sconto&lt;/b&gt;</p>",
              "<h1>PRODOTTI</h1><p>Offerta: sconto</p>"],
             locals={"descrizione": "<b>sconto</b>"},
             chiamata='pug.renderFile("pagina.pug", {\n  descrizione: "<b>sconto</b>"\n});',
             spiegazione="Una riga che inizia con `-` contiene codice JavaScript eseguito ma non "
                         "stampato. Il codice fra `#{` e `}` viene valutato e il risultato "
                         "**sottoposto a escaping**: i caratteri `<` e `>` diventano `&lt;` e "
                         "`&gt;`, e il markup contenuto nei dati arriva al browser come testo, "
                         "non come HTML (è ciò che impedisce l'iniezione di script).",
             rif=R % "Locals: passare i dati al template"))

d(uscita_pug("c12-pug-attributi", CAP, "template Pug",
             """
nav#menu
  a.attivo(href="/") Home
  a(href="/todo") La lista""",
             '<nav id="menu"><a class="attivo" href="/">Home</a><a href="/todo">La lista</a></nav>',
             ['<nav class="menu"><a id="attivo" href="/">Home</a><a href="/todo">La lista</a></nav>',
              '<nav id="menu"><a class="attivo" href="/">Home<a href="/todo">La lista</a></a></nav>',
              '<nav#menu><a.attivo href="/">Home</a><a href="/todo">La lista</a></nav#menu>',
              '<nav id="menu"></nav><a class="attivo" href="/">Home</a><a href="/todo">La lista</a>',
              '<nav id="menu"><a class="attivo" href="/" Home></a><a href="/todo" La lista></a></nav>'],
             spiegazione="Come nei selettori CSS, `#` abbrevia l'attributo `id` e `.` l'attributo "
                         "`class`; gli altri attributi si scrivono fra parentesi tonde, e il testo "
                         "dopo il tag ne è il contenuto. L'indentazione stabilisce l'annidamento: "
                         "i due link, allo stesso livello, sono fratelli dentro il `<nav>`.",
             rif=R % "Pug"))

d(risposte_server("c12-prg", CAP, "corpo delle richieste",
                  """
import http from "http";

let todos = [];
http.createServer((request, response) => {
  if (request.url === "/todo" && request.method === "POST") {
    let corpo = "";
    request.on("data", (pezzo) => { corpo += pezzo; });
    request.on("end", () => {
      todos.push(new URLSearchParams(corpo).get("todo"));
      response.writeHead(303, { "Location": "/todo" });
      response.end();
    });
  } else if (request.url === "/todo") {
    response.writeHead(200);
    response.end(todos.join(", ") || "Lista vuota");
  } else {
    response.writeHead(404);
    response.end("Pagina non trovata");
  }
}).listen(3000);""",
                  ["GET /todo", {"metodo": "POST", "percorso": "/todo", "corpo": "todo=Pane"},
                   {"metodo": "POST", "percorso": "/todo", "corpo": "todo=Latte"}, "GET /todo"],
                  ["200 Lista vuota", "303 -> /todo", "303 -> /todo", "200 Pane, Latte"],
                  [["200 Lista vuota", "200 Pane", "200 Pane, Latte", "200 Pane, Latte"],
                   ["200 Lista vuota", "303 -> /todo", "303 -> /todo", "200 Latte"],
                   ["200 ", "303 -> /todo", "303 -> /todo", "200 Pane, Latte"],
                   ["200 Lista vuota", "201 Pane", "201 Latte", "200 Pane, Latte"],
                   ["200 Lista vuota", "404 Pagina non trovata", "404 Pagina non trovata",
                    "200 Lista vuota"]],
                  spiegazione="Il gestore della `POST` legge il corpo (che arriva a pezzi, con gli "
                              "eventi `data` ed `end`), salva l'elemento e risponde con un "
                              "reindirizzamento `303` verso `/todo`: è il pattern "
                              "*Post/Redirect/Get*, grazie al quale ricaricare la pagina non "
                              "reinvia il form. L'array `todos` resta in memoria fra una "
                              "richiesta e l'altra, finché il server non viene riavviato.",
                  rif=R % "Mettere insieme i pezzi"))

# ----------------------------------------------------------------------
d(chiusa("c12-405", CAP, "routing",
         "Un'applicazione gestisce `GET` e `POST` sul percorso `/todo`. Quale risposta è più "
         "corretta per una richiesta `DELETE /todo`?",
         "`405 Method Not Allowed`",
         ["`404 Not Found`", "`400 Bad Request`", "`200 OK` con la lista", "`204 No Content`",
          "`500 Internal Server Error`"],
         spiegazione="Quando il percorso esiste ma il metodo non è previsto, la risposta corretta "
                     "è `405`, non `404`: client e *proxy* sanno distinguere i due casi, e la "
                     "distinzione torna utile soprattutto nelle API REST.",
         rif=R % "Instradare anche in base al metodo"))

d(chiusa("c12-url", CAP, "routing",
         "Un router confronta `request.url` con la stringa `\"/delete\"`. Perché una richiesta "
         "`GET /delete?id=3` non viene riconosciuta, e come si rimedia?",
         "`request.url` contiene anche la query string; si separano percorso e parametri con "
         "`new URL(request.url, ...)`, usando `pathname` e `searchParams`.",
         ["`request.url` contiene anche il nome dell'host; si rimedia con "
          "`request.url.toLowerCase()`.",
          "Le richieste con parametri arrivano sempre con il metodo `POST`.",
          "Node.js scarta le richieste con la query string; bisogna usare un form.",
          "`request.url` vale `undefined` quando c'è una query string.",
          "Il router dovrebbe confrontare `request.method` invece di `request.url`."],
         spiegazione="Per `/delete?id=3`, `request.url` vale proprio `\"/delete?id=3\"`, che non è "
                     "uguale a `\"/delete\"`. La classe `URL` separa il percorso "
                     "(`url.pathname`) dai parametri (`url.searchParams.get(\"id\")`).",
         rif=R % "Estendere l'applicazione: cancellare un elemento"))

d(chiusa("c12-get-sicuro", CAP, "routing",
         "Per cancellare un elemento, un'applicazione mostra accanto a ogni voce un link "
         "`<a href=\"/delete?id=3\">`. Perché è una cattiva idea?",
         "Perché una `GET` dovrebbe essere sicura: browser che precaricano i link, crawler o "
         "estensioni potrebbero cancellare elementi senza che nessuno l'abbia chiesto.",
         ["Perché i link non possono contenere parametri nella query string.",
          "Perché il server non può leggere i parametri di una `GET`.",
          "Perché una `GET` non può ricevere come risposta una pagina HTML.",
          "Perché l'identificativo dovrebbe essere la posizione dell'elemento nell'array.",
          "Non è una cattiva idea: le `GET` sono il metodo giusto per cancellare."],
         spiegazione="Le operazioni che modificano lo stato del server vanno affidate a metodi "
                     "non sicuri: qui un form con metodo `POST` e l'identificativo in un campo "
                     "nascosto (o, in un'API, una `DELETE`).",
         rif=R % "Estendere l'applicazione: cancellare un elemento"))

d(chiusa("c12-prg-concetto", CAP, "corpo delle richieste",
         "Che problema risolve il pattern *Post/Redirect/Get*?",
         "Ricaricando la pagina mostrata dopo l'invio di un form, il browser non reinvia la "
         "`POST` (e non salva di nuovo i dati), perché la pagina è il risultato di una `GET`.",
         ["Rende più veloce l'invio dei form, perché il corpo viaggia nell'URL.",
          "Impedisce che i dati del form vengano intercettati in rete.",
          "Permette di inviare un form senza ricaricare la pagina.",
          "Trasforma le `GET` in `POST` per renderle sicure.",
          "Evita che il server debba leggere il corpo della richiesta."],
         spiegazione="Dopo una `POST` il server risponde con un reindirizzamento (`303 See "
                     "Other`, o `302`) verso la pagina da mostrare; il browser la chiede con una "
                     "`GET`, che si può ricaricare quante volte si vuole.",
         rif=R % "Mettere insieme i pezzi"))

d(chiusa("c12-corpo-eventi", CAP, "corpo delle richieste",
         "In un server scritto con il modulo `http` di Node.js, come si legge il corpo di una "
         "richiesta `POST`?",
         "Raccogliendo i pezzi con l'evento `data` della richiesta e ricomponendoli quando "
         "arriva l'evento `end`.",
         ["Leggendo la proprietà `request.body`, già pronta quando parte il gestore.",
          "Chiamando `request.read()`, che attende in modo sincrono tutto il corpo.",
          "Dalla query string di `request.url`.",
          "Dall'header `Content-Length`, che contiene i dati.",
          "Con `fs.readFile`, perché il corpo viene salvato su un file temporaneo."],
         spiegazione="Il corpo potrebbe non essere ancora arrivato quando il gestore parte. "
                     "`request` è uno stream leggibile: emette `data` per ogni pezzo e `end` alla "
                     "fine. Per esporre il risultato si può avvolgere il tutto in una Promise.",
         rif=R % "Il corpo arriva a pezzi"))

d(chiusa("c12-id", CAP, "routing",
         "Nei link per cancellare gli elementi di una lista si usa un identificativo "
         "(`/delete?id=7`) invece della posizione nell'array. Perché?",
         "Perché dopo una cancellazione le posizioni degli elementi successivi cambiano, e un "
         "link generato prima punterebbe all'elemento sbagliato.",
         ["Perché la posizione nell'array non si può scrivere in un URL.",
          "Perché gli array di JavaScript non hanno indici numerici.",
          "Perché l'identificativo è più corto della posizione.",
          "Perché la posizione è un dato sensibile da non mostrare.",
          "Non c'è differenza: è solo una convenzione."],
         spiegazione="Un identificativo resta legato all'elemento; la posizione no. Un "
                     "identificativo che non esiste più produce invece, giustamente, un `404`.",
         rif=R % "Estendere l'applicazione: cancellare un elemento"))

d(chiusa("c12-template", CAP, "template Pug",
         "Quali delle seguenti affermazioni sui motori di template (come Pug) sono **vere**?",
         ["Permettono di descrivere la struttura della pagina in un file separato, con dei "
          "segnaposto riempiti con i dati a tempo di esecuzione.",
          "Con `include` e con l'ereditarietà (`extends` e `block`) le parti comuni si scrivono "
          "una volta sola.",
          "In Pug l'indentazione sostituisce i tag di chiusura.",
          "I dati interpolati con `#{...}` vengono sottoposti a escaping."],
         ["Il template viene inviato al browser, che lo trasforma in HTML.",
          "Pug è l'unico motore di template disponibile per Node.js.",
          "In Pug gli attributi si scrivono fra parentesi quadre.",
          "Un template non può contenere condizionali né cicli.",
          "Il ramo `else` di un `each` viene eseguito dopo l'ultimo elemento."],
         multi=True,
         spiegazione="Il template engine genera l'HTML sul server, combinando il modello con i "
                     "*locals*. Pug ha una sintassi sensibile agli spazi (attributi fra "
                     "parentesi tonde), supporta inclusioni, ereditarietà, condizionali e cicli "
                     "(con `else` per le collezioni vuote). Altri motori: EJS, Nunjucks, "
                     "LiquidJS...",
         rif=R % "Motori di template"))

# ----------------------------------------------------------------------
# Domande aperte
d(aperta("c12-a-problemi", CAP, "routing",
         "Realizzando un'applicazione web con il solo modulo `http` di Node.js bisogna "
         "affrontare tre problemi: routing, templating e analisi del corpo delle richieste. Si "
         "descriva ciascuno e come lo si può risolvere.",
         ["Routing: scegliere il codice che serve la richiesta in base a percorso (`pathname`, "
          "senza la query) e metodo; `404` se il percorso non esiste, `405` se il metodo non è "
          "previsto. Con uno `switch` diventa difficile con parametri nel percorso e controlli "
          "di accesso.",
          "Templating: generare l'HTML da un modello con segnaposto e dati (Pug: inclusioni, "
          "ereditarietà, locals con escaping, condizionali, cicli), invece di concatenare "
          "stringhe.",
          "Corpo: arriva a pezzi (eventi `data` ed `end`), va ricomposto e decodificato "
          "(`&`, `=`, `+` come spazio, `decodeURIComponent`).",
          "Dopo una `POST` conviene rispondere con un reindirizzamento (Post/Redirect/Get); le "
          "`GET` non devono modificare lo stato."],
         rif="cap. 12, «Routing», «Motori di template» e «Analizzare il corpo delle richieste»"))

d(aperta("c12-a-template", CAP, "template Pug",
         "Che cos'è un motore di template? Si descrivano, con piccoli esempi in Pug, "
         "l'interpolazione dei dati, i condizionali, le iterazioni e l'ereditarietà fra "
         "template.",
         ["Genera l'HTML combinando un modello con segnaposto e i dati (*locals*) passati a "
          "`render`/`renderFile`; evita di concatenare stringhe e favorisce il riuso.",
          "Interpolazione: `h1 #{product.name}` valuta l'espressione e ne fa l'escaping; le "
          "righe che iniziano con `-` sono codice eseguito ma non stampato.",
          "Condizionali (`if`, `else if`, `else`: solo il ramo scelto finisce nell'HTML) e "
          "iterazioni (`each item in items`, con `else` per la collezione vuota).",
          "Ereditarietà: il layout definisce i `block`, la pagina con `extends` ridefinisce "
          "quelli che le servono; gli altri mantengono il contenuto predefinito. Con `include` "
          "si inseriscono frammenti comuni."],
         rif=R % "Motori di template"))

d(aperta("c12-a-prg", CAP, "corpo delle richieste",
         "Nella lista di cose da fare realizzata con Node.js, che cosa succede se, dopo aver "
         "aggiunto un elemento con il form, l'utente ricarica la pagina? Si descriva il "
         "pattern *Post/Redirect/Get* e si spieghi perché cancellare un elemento con un "
         "semplice collegamento (`/delete?id=3`) non è una buona idea.",
         ["La pagina mostrata è la risposta alla `POST`: ricaricandola, il browser chiede se "
          "reinviare il form, e l'elemento verrebbe salvato due volte.",
          "Post/Redirect/Get: il gestore della `POST` salva e risponde con un reindirizzamento "
          "(`303` e `Location: /todo`); il browser chiede da solo la lista con una `GET`, che "
          "si può ricaricare senza effetti.",
          "Una `GET` è un metodo sicuro: non deve modificare lo stato del server. Crawler, "
          "precaricamento dei link o estensioni potrebbero «visitare» `/delete?id=3` e "
          "cancellare l'elemento.",
          "La versione corretta usa un form con `method=\"POST\"` e l'identificativo in un "
          "campo nascosto; il router deve guardare il `pathname` (`new URL(...)`), perché "
          "`request.url` contiene anche la query."],
         rif="cap. 12, «Mettere insieme i pezzi» ed «Estendere l'applicazione: cancellare "
             "un elemento»"))
