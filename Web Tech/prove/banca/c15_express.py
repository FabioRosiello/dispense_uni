"""Capitolo 15: Express (framework e inversione del controllo, routing,
parametri e router, risposte e template, middleware, gestione degli errori,
middleware utili, sessioni, cookie e messaggi flash)."""

from generatore import aperta, chiusa, combina_errori, famiglia, risposte_server

CAP = 15
R = "cap. 15, «%s»"

DOMANDE = []
d = DOMANDE.append


def _unici(esiti):
    visti = []
    for e in esiti:
        if e not in visti:
            visti.append(e)
    return visti


def _app(corpo):
    return 'import express from "express";\n\nconst app = express();\n\n%s\n\napp.listen(3000);' % corpo


# ----------------------------------------------------------------------
# Famiglia: quale rotta risponde
ROTTA_STRINGA = 'app.get("/webtech", (req, res) => res.send("A"));'
ROTTA_REGEX = 'app.get(/^\\/w.*tech$/, (req, res) => res.send("B"));'
ALTRE_ROTTE = ('app.get("/corsi/:id", (req, res) => res.send("C " + req.params.id));\n'
               'app.post("/corsi/:id", (req, res) => res.send("D " + req.params.id));')
RICHIESTE_ROTTE = ["GET /webtech", "GET /wirelesstech", "GET /webtechs", "GET /corsi/42",
                   "DELETE /corsi/42", "GET /corsi", "GET /corsi/42/esami", "POST /corsi/tw"]


def _rotta(richiesta, regex_prima, ultima_vince=False, regex_libera=False, parametri_avidi=False,
           metodo_405=False, parametro_vuoto=False):
    import re
    metodo, url = richiesta.split(" ")
    if metodo == "GET":
        stringa = url == "/webtech"
        regex = re.search(r"/w.*tech", url) if regex_libera else re.fullmatch(r"/w.*tech", url)
        if stringa and regex:
            return "200 " + ("A" if regex_prima == ultima_vince else "B")
        if stringa:
            return "200 A"
        if regex:
            return "200 B"
    parti = url.strip("/").split("/")
    if parti[0] == "corsi":
        if len(parti) == 2 or (parametri_avidi and len(parti) > 2) or (parametro_vuoto and len(parti) == 1):
            valore = "/".join(parti[1:])
            if metodo == "GET":
                return ("200 C " + valore).strip()
            if metodo == "POST":
                return ("200 D " + valore).strip()
            if metodo_405:
                return "405 Method Not Allowed"
    return "404 Cannot %s %s" % (metodo, url)


@famiglia("c15-rotte", CAP, "routing", varianti=4)
def _rotte(rng):
    regex_prima = rng.random() < 0.4
    prime = [ROTTA_REGEX, ROTTA_STRINGA] if regex_prima else [ROTTA_STRINGA, ROTTA_REGEX]
    codice = _app("\n".join(prime) + "\n" + ALTRE_ROTTE)
    scelte = [rng.choice(RICHIESTE_ROTTE[:3]), rng.choice(RICHIESTE_ROTTE[3:5]),
              rng.choice(RICHIESTE_ROTTE[5:])]
    rng.shuffle(scelte)
    giusta = [_rotta(r, regex_prima) for r in scelte]
    esiti = _unici([[_rotta(r, regex_prima, **{k: True}) for r in scelte]
                    for k in ("ultima_vince", "regex_libera", "parametri_avidi", "metodo_405",
                              "parametro_vuoto")])
    esiti = [e for e in esiti if e != giusta]
    alternative = [_unici([_rotta(r, regex_prima, **{k: True}) for k in
                           ("ultima_vince", "regex_libera", "parametri_avidi", "metodo_405",
                            "parametro_vuoto")] + ["404 Cannot %s %s" % tuple(r.split(" "))])
                   for r in scelte]
    rng.shuffle(esiti)
    return risposte_server(
        "c15-rotte", CAP, "routing", codice, scelte, giusta,
        combina_errori(giusta, alternative, rng, esiti=esiti), applicazione="Express",
        spiegazione="Quando più rotte corrispondono vince **la prima** dichiarata. L'espressione "
                    "regolare `/^\\/w.*tech$/` vuole tutto il percorso, dalla `w` dopo la barra "
                    "fino a `tech` in fondo. Un parametro (`:id`) cattura esattamente un "
                    "segmento, e `req.params` contiene stringhe. Per un percorso senza rotta, o "
                    "per un metodo senza rotta, Express risponde `404` (*Cannot METODO "
                    "percorso*).",
        rif="cap. 15, «Percorsi delle rotte» e «Parametri di rotta»")


d(_rotte)


# ----------------------------------------------------------------------
# Famiglia: l'ordine dei middleware
PASSI = [
    ("tutti", 'app.use((req, res, next) => { req.passi.push("%s"); next(); });'),
    ("monta_x", 'app.use("/x", (req, res, next) => { req.passi.push("%s"); next(); });'),
    ("monta_y", 'app.use("/y", (req, res, next) => { req.passi.push("%s"); next(); });'),
    ("get_x", 'app.get("/x", (req, res, next) => { req.passi.push("%s"); next(); });'),
    ("post_x", 'app.post("/x", (req, res, next) => { req.passi.push("%s"); next(); });'),
    ("get_xid", 'app.get("/x/:id", (req, res, next) => { req.passi.push("%s"); next(); });'),
    ("risponde", 'app.get("/x", (req, res) => res.send(req.passi.concat("%s").join(",")));'),
]
CORRISPONDE = {"tutti": True, "monta_x": True, "monta_y": False, "get_x": True,
               "post_x": False, "get_xid": False, "risponde": True}


@famiglia("c15-middleware", CAP, "middleware", varianti=4)
def _middleware(rng):
    while True:
        tipi = rng.sample([t for t, _ in PASSI], 4)
        if sum(CORRISPONDE[t] for t in tipi) >= 2:
            break
    lettere = iter("BCDEFGH")
    righe, passi = [], []
    for t in tipi:
        modello = dict(PASSI)[t]
        lettera = next(lettere)
        righe.append(modello % lettera)
        passi.append((t, lettera))
    righe = (['app.use((req, res, next) => { req.passi = ["A"]; next(); });'] + righe +
             ['app.get("/x", (req, res) => res.send(req.passi.join(",")));'])

    def esegui(tutti=False, prefisso_no=False, ignora_risposta=False, metodo_no=False):
        uscita = ["A"]
        for t, lettera in passi:
            corrisponde = CORRISPONDE[t] or tutti
            if prefisso_no and t == "monta_x":
                corrisponde = False
            if metodo_no and t in ("get_x", "post_x"):
                corrisponde = True
            if corrisponde:
                uscita.append(lettera)
                if t == "risponde" and not ignora_risposta:
                    return "200 " + ",".join(uscita)
        return "200 " + ",".join(uscita)

    giusta = [esegui()]
    esiti = _unici([[esegui(**{k: True})] for k in ("tutti", "prefisso_no", "ignora_risposta",
                                                     "metodo_no")])
    lettere_usate = [l for _, l in passi]
    esiti += [["200 A," + ",".join(lettere_usate)], ["200 A"],
              ["200 " + ",".join(reversed(giusta[0][4:].split(",")))]]
    esiti = [e for e in _unici(esiti) if e != giusta]
    rng.shuffle(esiti)
    return risposte_server(
        "c15-middleware", CAP, "middleware", _app("\n".join(righe)), ["GET /x"], giusta,
        esiti[:5], applicazione="Express",
        testo="Si consideri la seguente applicazione Express, in ascolto sulla porta 3000. Che "
              "cosa risponde a una richiesta `GET /x`?",
        spiegazione="Middleware e gestori vengono eseguiti **nell'ordine in cui sono "
                    "dichiarati**, ciascuno solo se corrisponde alla richiesta: `app.use` senza "
                    "percorso vale per tutte, `app.use(\"/x\", ...)` per `/x` e per i percorsi "
                    "che cominciano con `/x/`, `app.get` solo per le `GET` con quel percorso "
                    "esatto (`/x/:id` vuole un segmento in più). `next()` passa al successivo; il "
                    "primo che risponde chiude il ciclo, e chi viene dopo non viene eseguito.",
        rif="cap. 15, «I middleware» e «Più gestori per una rotta»")


d(_middleware)


# ----------------------------------------------------------------------
# Famiglia: dove finisce un errore
GESTORE_4 = ('app.use((err, req, res, next) => {\n'
             '  res.status(500).send("Gestito: " + err.message);\n});')
GESTORE_3 = ('app.use((err, req, res) => {\n'
             '  res.status(500).send("Gestito: " + err.message);\n});')
GESTORE_200 = ('app.use((err, req, res, next) => {\n'
               '  res.send("Gestito: " + err.message);\n});')
OK = 'app.get("/ok", (req, res) => res.send("ok"));'
SINCRONO = 'app.get("/errore", (req, res) => {\n  throw new Error("Rotto");\n});'
ASINCRONO = ('app.get("/errore", async (req, res) => {\n'
             '  await Promise.reject(new Error("Rotto"));\n  res.send("mai");\n});')
CALLBACK = ('app.get("/errore", (req, res, next) => {\n'
            '  setTimeout(() => next(new Error("Rotto")), 10);\n});')
CASI_ERRORE = [
    ([OK, SINCRONO, GESTORE_4], "500 Gestito: Rotto",
     "L'errore sollevato nel codice sincrono di un gestore arriva al gestore di errori "
     "personalizzato, che ha quattro parametri ed è dichiarato dopo le rotte."),
    ([OK, SINCRONO], "500 Error: Rotto",
     "Senza un gestore personalizzato interviene quello predefinito di Express, che risponde "
     "`500` con il messaggio (e, in sviluppo, la traccia dello stack)."),
    ([OK, ASINCRONO, GESTORE_4], "500 Gestito: Rotto",
     "Da Express 5, se un gestore restituisce una Promise rifiutata (qui una funzione `async` "
     "il cui `await` solleva l'errore) viene invocato automaticamente `next(err)`."),
    ([OK, SINCRONO, GESTORE_3], "500 Error: Rotto",
     "Il gestore personalizzato ha **tre** parametri: per Express è un middleware normale, "
     "che viene saltato quando c'è un errore. Risponde il gestore predefinito."),
    ([GESTORE_4, OK, SINCRONO], "500 Error: Rotto",
     "Il gestore personalizzato è dichiarato **prima** delle rotte: un errore passa solo ai "
     "gestori di errori che vengono dopo il punto in cui si è verificato. Risponde quello "
     "predefinito."),
    ([OK, CALLBACK, GESTORE_4], "500 Gestito: Rotto",
     "L'errore nato in una callback asincrona viene consegnato esplicitamente a `next(err)`, e "
     "arriva al gestore personalizzato."),
    ([OK, SINCRONO, GESTORE_200], "200 Gestito: Rotto",
     "Il gestore personalizzato riceve l'errore ma non imposta il codice di stato: la risposta "
     "parte con il valore predefinito, `200`."),
]


@famiglia("c15-errori", CAP, "gestione degli errori", varianti=4)
def _errori(rng):
    pezzi, risposta, perche = rng.choice(CASI_ERRORE)
    giusta = ["200 ok", risposta]
    possibili = ["500 Gestito: Rotto", "500 Error: Rotto", "200 Gestito: Rotto",
                 "500 Internal Server Error"]
    esiti = [["200 ok", p] for p in possibili if p != risposta]
    esiti.append(["500 Gestito: Rotto", risposta] if risposta != "500 Gestito: Rotto" else
                 ["500 Error: Rotto", "500 Error: Rotto"])
    rng.shuffle(esiti)
    return risposte_server(
        "c15-errori", CAP, "gestione degli errori", _app("\n".join(pezzi)),
        ["GET /ok", "GET /errore"], giusta, esiti, applicazione="Express",
        spiegazione=perche + " Un gestore di errori si riconosce dall'**arità**: quattro "
                             "parametri, `(err, req, res, next)`.",
        rif=R % "Gestione degli errori")


d(_errori)


# ----------------------------------------------------------------------
# Famiglia: chi analizza il corpo
@famiglia("c15-corpo", CAP, "middleware utili", varianti=3)
def _corpo(rng):
    parser = rng.choice([["urlencoded"], ["json"], ["urlencoded", "json"], []])
    righe = []
    if "urlencoded" in parser:
        righe.append("app.use(express.urlencoded({ extended: false }));")
    if "json" in parser:
        righe.append("app.use(express.json());")
    righe.append('app.post("/form", (req, res) => {\n'
                 '  res.send(`msg=${req.body?.msg}; num=${req.body?.num}`);\n});')
    forma = {"metodo": "POST", "percorso": "/form", "corpo": "msg=Ciao+mondo&num=42",
             "intestazioni": {"Content-Type": "application/x-www-form-urlencoded"}}
    json = {"metodo": "POST", "percorso": "/form", "corpo": '{"msg": "Ciao", "num": 7}',
            "intestazioni": {"Content-Type": "application/json"}}
    vuoto = "200 msg=undefined; num=undefined"
    risposte = {"form": "200 msg=Ciao mondo; num=42", "json": "200 msg=Ciao; num=7"}
    giusta = [risposte["form"] if "urlencoded" in parser else vuoto,
              risposte["json"] if "json" in parser else vuoto]
    tutte = [[a, b] for a in (risposte["form"], vuoto, "200 msg=Ciao+mondo; num=42")
             for b in (risposte["json"], vuoto)]
    esiti = [e for e in tutte if e != giusta]
    rng.shuffle(esiti)
    return risposte_server(
        "c15-corpo", CAP, "middleware utili", _app("\n".join(righe)), [forma, json], giusta,
        esiti[:5], applicazione="Express",
        testo="Si consideri la seguente applicazione Express, in ascolto sulla porta 3000. Che "
              "cosa rispondono due richieste `POST /form`, la prima con il corpo "
              "`msg=Ciao+mondo&num=42` e l'header `Content-Type: "
              "application/x-www-form-urlencoded`, la seconda con il corpo `{\"msg\": \"Ciao\", "
              "\"num\": 7}` e l'header `Content-Type: application/json`?",
        spiegazione="`express.urlencoded` analizza i corpi codificati come URL (quelli dei form, "
                    "decodifica compresa), `express.json` quelli in JSON: è il `Content-Type` a "
                    "decidere, e ciascuno ignora le richieste che non sono nel suo formato. Se "
                    "nessun middleware analizza il corpo, `req.body` resta indefinito.",
        rif="cap. 15, «express.urlencoded» e «express.json»")


d(_corpo)

# ----------------------------------------------------------------------
d(risposte_server("c15-risposte", CAP, "rispondere al client",
                  _app('app.get("/a", (req, res) => res.send({ ok: true }));\n'
                       'app.get("/b", (req, res) => res.sendStatus(404));\n'
                       'app.get("/c", (req, res) => res.status(201).send("creato"));\n'
                       'app.get("/d", (req, res) => res.redirect("/a"));'),
                  ["GET /a", "GET /b", "GET /c", "GET /d"],
                  ['200 {"ok":true}', "404 Not Found", "201 creato", "302 -> /a"],
                  [['200 [object Object]', "404 Not Found", "201 creato", "302 -> /a"],
                   ['200 {"ok":true}', "404 ", "201 creato", "302 -> /a"],
                   ['200 {"ok":true}', "404 Not Found", "200 creato", "302 -> /a"],
                   ['200 {"ok":true}', "404 Not Found", "201 creato", '200 {"ok":true}'],
                   ['200 {"ok":true}', "200 404", "201 creato", "301 -> /a"]],
                  applicazione="Express",
                  spiegazione="`res.send` con un oggetto lo converte in JSON (e imposta "
                              "`Content-Type: application/json`); `res.sendStatus` imposta il "
                              "codice e invia come corpo la sua rappresentazione testuale; "
                              "`res.status` imposta il codice e restituisce `res`, per "
                              "concatenare l'invio; `res.redirect` risponde con un `302` e "
                              "l'header `Location` (il browser seguirebbe da solo il "
                              "reindirizzamento).",
                  rif=R % "Rispondere al client"))

d(risposte_server("c15-router", CAP, "routing",
                  _app('const router = express.Router();\n'
                       'router.get("/echo/:valore", (req, res) => res.send(req.params.valore));\n'
                       '\napp.use("/custom", router);'),
                  ["GET /custom/echo/ciao", "GET /echo/ciao", "GET /custom/echo"],
                  ["200 ciao", "404 Cannot GET /echo/ciao", "404 Cannot GET /custom/echo"],
                  [["200 ciao", "200 ciao", "404 Cannot GET /custom/echo"],
                   ["404 Cannot GET /custom/echo/ciao", "200 ciao", "404 Cannot GET /custom/echo"],
                   ["200 ciao", "404 Cannot GET /echo/ciao", "200 "],
                   ["200 ciao", "404 Cannot GET /echo/ciao", "200 undefined"],
                   ["200 /custom/echo/ciao", "404 Cannot GET /echo/ciao",
                    "404 Cannot GET /custom/echo"]],
                  applicazione="Express",
                  spiegazione="Un router modulare montato con `app.use(\"/custom\", router)` "
                              "gestisce percorsi **relativi** a quel prefisso: "
                              "`/custom/echo/ciao` arriva alla rotta `/echo/:valore`, mentre "
                              "`/echo/ciao` da solo non esiste. Il parametro deve catturare un "
                              "segmento: `/custom/echo` non corrisponde.",
                  rif=R % "Rotte concatenabili e router modulari"))

d(risposte_server("c15-route", CAP, "routing",
                  _app("app.route(\"/book\")\n"
                       "  .get((req, res) => res.send(\"Get a book\"))\n"
                       "  .post((req, res) => res.send(\"Add a book\"))\n"
                       "  .delete((req, res) => res.send(\"Delete a book\"));"),
                  ["GET /book", "DELETE /book", "PUT /book"],
                  ["200 Get a book", "200 Delete a book", "404 Cannot PUT /book"],
                  [["200 Get a book", "200 Delete a book", "405 Method Not Allowed"],
                   ["200 Get a book", "200 Delete a book", "200 Add a book"],
                   ["200 Get a book", "404 Cannot DELETE /book", "404 Cannot PUT /book"],
                   ["200 Get a book", "200 Delete a book", "200 Get a book"],
                   ["200 Get a book", "200 Delete a book", "500 Internal Server Error"]],
                  applicazione="Express",
                  spiegazione="`app.route()` specifica il percorso una volta sola e concatena i "
                              "gestori per metodo. Per un metodo che non ha gestore (qui `PUT`) "
                              "Express risponde `404`, come per un percorso inesistente.",
                  rif=R % "Rotte concatenabili e router modulari"))

d(risposte_server("c15-cookie", CAP, "sessioni e cookie",
                  'import express from "express";\nimport cookieParser from "cookie-parser";\n\n'
                  'const app = express();\napp.use(cookieParser());\n\n'
                  'app.get("/contatore", (req, res) => {\n'
                  '  const n = req.cookies.count ? parseInt(req.cookies.count) + 1 : 1;\n'
                  '  res.cookie("count", n, { maxAge: 10 * 60 * 1000 });\n'
                  '  res.send(`Visita numero ${n}`);\n});\n\napp.listen(3000);',
                  ["GET /contatore",
                   {"percorso": "/contatore", "intestazioni": {"Cookie": "count=41"}},
                   {"percorso": "/contatore", "intestazioni": {"Cookie": "count=abc"}}],
                  ["200 Visita numero 1", "200 Visita numero 42", "200 Visita numero NaN"],
                  [["200 Visita numero 1", "200 Visita numero 1", "200 Visita numero 1"],
                   ["200 Visita numero 1", "200 Visita numero 2", "200 Visita numero 3"],
                   ["200 Visita numero 1", "200 Visita numero 411", "200 Visita numero abc1"],
                   ["200 Visita numero 1", "200 Visita numero 42", "200 Visita numero 1"],
                   ["200 Visita numero 1", "200 Visita numero 42", "400 Bad Request"]],
                  applicazione="Express",
                  testo="Si consideri la seguente applicazione Express, in ascolto sulla porta "
                        "3000. Che cosa rispondono tre richieste `GET /contatore`: la prima senza "
                        "cookie, la seconda con l'header `Cookie: count=41`, la terza con "
                        "l'header `Cookie: count=abc`?",
                  spiegazione="`cookie-parser` mette i cookie della richiesta in `req.cookies`, "
                              "come stringhe. Il contatore sta nel client, che può inviare il "
                              "valore che vuole: il server crede a `41`, e con `abc` "
                              "`parseInt` dà `NaN`. Con `express-session` il contatore starebbe "
                              "invece sul server, e il cookie conterrebbe solo l'identificatore "
                              "firmato della sessione.",
                  rif=R % "cookie-parser"))

# ----------------------------------------------------------------------
d(chiusa("c15-ioc", CAP, "framework",
         "Che cosa si intende con *inversione del controllo* (la «legge di Hollywood»), "
         "caratteristica distintiva dei framework?",
         "Che è il framework a controllare il flusso di esecuzione e a invocare il codice "
         "scritto dallo sviluppatore quando serve, e non il contrario.",
         ["Che il codice dello sviluppatore invoca le funzioni del framework, che poi gli "
          "restituiscono il controllo.",
          "Che il client controlla il server, invece del contrario.",
          "Che le richieste HTTP vengono elaborate in ordine inverso.",
          "Che il framework impone di scrivere il codice dalla fine all'inizio.",
          "Che il database controlla la logica dell'applicazione."],
         spiegazione="«Non chiamarci tu, ti chiamiamo noi»: con una libreria è il nostro codice a "
                     "chiamare le funzioni, che restituiscono il controllo; con un framework il "
                     "nostro codice viene innestato nel framework, che riceve la richiesta e lo "
                     "invoca (per esempio i gestori delle rotte).",
         rif=R % "Inversione del controllo"))

d(chiusa("c15-opinionated", CAP, "framework",
         "Express si definisce un framework *unopinionated*. Che cosa significa?",
         "Che non impone un modo specifico di organizzare l'applicazione: le scelte (struttura, "
         "librerie, convenzioni) restano allo sviluppatore.",
         ["Che non ha una documentazione ufficiale.",
          "Che non permette di usare motori di template.",
          "Che impone un insieme rigido di convenzioni decise dai suoi autori.",
          "Che non gestisce il routing.",
          "Che funziona solo con le API REST."],
         spiegazione="Un framework fortemente *opinionated* arriva con convenzioni rigide: più "
                     "coerenza e velocità, ma più rigidità e una curva di apprendimento più "
                     "ripida. Express è minimalista e unopinionated: per questo, per esempio, non "
                     "esiste un unico modo giusto di organizzarne un'applicazione.",
         rif=R % "Framework opinionated"))

d(chiusa("c15-middleware-def", CAP, "middleware",
         "Quali delle seguenti affermazioni sui middleware di Express sono **vere**?",
         ["Ricevono come argomenti `req`, `res` e `next`.",
          "Vengono eseguiti nell'ordine in cui sono dichiarati.",
          "Possono aggiungere proprietà all'oggetto richiesta, che i middleware successivi "
          "trovano già pronte.",
          "Se non chiamano `next()` e non rispondono, la richiesta resta appesa."],
         ["Vengono eseguiti dopo che la risposta è stata inviata.",
          "Montati con `app.use` senza percorso, valgono solo per la rotta `/`.",
          "Express li ordina automaticamente per percorso.",
          "Devono sempre inviare una risposta.",
          "Possono essere usati solo per l'autenticazione."],
         multi=True,
         spiegazione="I middleware stanno nel mezzo del ciclo richiesta-risposta: elaborano la "
                     "richiesta (log, corpo, cookie, sessione, autenticazione...) e passano al "
                     "successivo con `next()`, oppure rispondono e chiudono il ciclo. Dimenticare "
                     "`next()` senza rispondere lascia la richiesta appesa fino al timeout, senza "
                     "alcun messaggio d'errore.",
         rif=R % "I middleware"))

d(chiusa("c15-express5", CAP, "gestione degli errori",
         "Un gestore di rotta è una funzione `async` che fa `await` di una Promise che viene "
         "rifiutata. Che cosa succede con Express 5?",
         "Express invoca automaticamente `next(err)`: l'errore arriva al gestore degli errori.",
         ["Il rifiuto non viene gestito e Node.js termina l'intero processo.",
          "La richiesta resta appesa finché il client non va in timeout.",
          "Express risponde `200` con un corpo vuoto.",
          "L'errore viene ignorato e si passa alla rotta successiva.",
          "Express riavvia il server."],
         spiegazione="Da Express 5 i gestori che restituiscono una Promise rifiutata invocano "
                     "`next(err)` da soli. Con Express 4 la Promise veniva ignorata: il rifiuto "
                     "non gestito faceva terminare il processo, e bisognava usare `try/catch` e "
                     "chiamare `next(err)` a mano.",
         rif=R % "Le Promise in Express 5"))

d(chiusa("c15-static", CAP, "middleware utili",
         "Un'applicazione esegue `app.use(\"/static\", express.static(\"public\"))`. Con quale URL "
         "si ottiene il file `public/css/style.css`?",
         "`/static/css/style.css`",
         ["`/public/css/style.css`", "`/css/style.css`", "`/static/public/css/style.css`",
          "`/style.css`", "`/static/style.css`"],
         spiegazione="`express.static` serve i file di una cartella, ricavando il "
                     "`Content-Type` dall'estensione. Montato sul percorso virtuale `/static`, "
                     "mappa `/static/<percorso>` sul file `public/<percorso>`; montato senza "
                     "percorso, `public/css/style.css` sarebbe `/css/style.css`.",
         rif=R % "express.static"))

d(chiusa("c15-sessione", CAP, "sessioni e cookie",
         "Quali delle seguenti affermazioni su `express-session` e `cookie-parser` sono "
         "**vere**?",
         ["Con `express-session` i dati stanno sul server e il cookie contiene solo "
          "l'identificatore della sessione.",
          "L'identificatore della sessione è firmato con il `secret`: se il client lo modifica, "
          "il server lo ignora.",
          "Con `cookie-parser` i valori stanno nei cookie, e il client può modificarli a "
          "piacere.",
          "L'archivio predefinito di `express-session` tiene le sessioni in memoria: in "
          "produzione ne serve uno dedicato."],
         ["`cookie-parser` cifra i cookie, che il client non può leggere.",
          "`express-session` salva i dati della sessione nel browser.",
          "Il `secret` di `express-session` si può pubblicare senza rischi.",
          "Una richiesta senza cookie di sessione riceve comunque la sessione dell'ultimo "
          "client.",
          "`saveUninitialized: false` crea una sessione per ogni visitatore."],
         multi=True,
         spiegazione="`express-session` realizza le sessioni web del capitolo 13: dati sul "
                     "server, identificatore firmato nel cookie `connect.sid` (il `secret` va "
                     "tenuto segreto). `cookie-parser` analizza l'header `Cookie` in "
                     "`req.cookies`: i valori viaggiano e restano sul client. "
                     "`saveUninitialized: false` non crea sessioni per chi non vi ha scritto "
                     "nulla.",
         rif=R % "express-session"))

d(chiusa("c15-flash", CAP, "sessioni e cookie",
         "Dopo aver cancellato un elemento, il server reindirizza l'utente alla lista e vuole "
         "mostrargli «Elemento cancellato». Perché servono i *messaggi flash*?",
         "Perché il reindirizzamento avvia un ciclo richiesta-risposta nuovo: il messaggio va "
         "conservato (nella sessione) fino alla richiesta successiva, che lo mostra e lo "
         "cancella.",
         ["Perché `res.redirect` non può inviare testo al client.",
          "Perché i messaggi flash vengono mostrati dal browser in una finestra di dialogo.",
          "Perché i messaggi flash si salvano nel database e restano visibili per sempre.",
          "Perché senza di essi il reindirizzamento non funziona.",
          "Perché HTTP non permette di inviare due risposte alla stessa richiesta."],
         spiegazione="È ancora l'assenza di stato di HTTP. `connect-flash` salva i messaggi nella "
                     "sessione (va registrato dopo `express-session`); `req.flash(chiave)` li "
                     "legge e li consuma, quindi ricaricando la pagina non compaiono più: è una "
                     "notifica «usa e getta».",
         rif=R % "Messaggi flash"))

d(chiusa("c15-express4", CAP, "routing",
         "Un'applicazione scritta per Express 4 dichiara la rotta `app.get(\"/web(-)?tech*\", ...)`. "
         "Che cosa succede eseguendola con Express 5?",
         "Il programma si ferma già all'avvio, quando la rotta viene dichiarata, con un errore "
         "sulla sintassi del percorso.",
         ["Funziona come in Express 4: corrisponde a `/webtech`, `/web-tech`, `/webtechs`...",
          "La rotta viene ignorata in silenzio e tutte le richieste ricevono `404`.",
          "La rotta corrisponde solo al percorso letterale `/web(-)?tech*`.",
          "Express 5 la converte automaticamente in un'espressione regolare.",
          "L'errore compare solo alla prima richiesta che corrisponde."],
         spiegazione="Express 5 non ammette più nei percorsi i caratteri speciali `?`, `+`, `*` e "
                     "le parentesi: la dichiarazione solleva un `PathError` all'avvio. Le parti "
                     "facoltative si scrivono con le graffe (`/web{-}tech`), una sequenza "
                     "qualsiasi con un jolly con nome (`{*resto}`), oppure si usa un'espressione "
                     "regolare.",
         rif=R % "Percorsi delle rotte"))

d(chiusa("c15-locals", CAP, "rispondere al client",
         "In un gestore Express, a che cosa serve assegnare `res.locals.items = [...]` prima di "
         "`res.render(\"lista\")`?",
         "A rendere disponibile `items` a tutte le viste generate per quella risposta.",
         ["A salvare `items` nella sessione dell'utente.",
          "A memorizzare `items` in un cookie.",
          "A inviare `items` al client in formato JSON.",
          "A rendere `items` disponibile a tutte le richieste successive.",
          "A salvare `items` nel file `views/lista.pug`."],
         spiegazione="`res.locals` vive per la sola risposta corrente: i suoi dati sono "
                     "disponibili ai template generati con `res.render` (che cerca la vista "
                     "nella cartella `views` con il motore impostato da `app.set(\"view "
                     "engine\", \"pug\")`). Un middleware può riempirlo per tutte le pagine.",
         rif=R % "Passare dati alla vista"))

# ----------------------------------------------------------------------
# Domande aperte
d(aperta("c15-a-framework", CAP, "framework",
         "Che differenza c'è fra una libreria e un framework? Si spieghi l'inversione del "
         "controllo e si descriva che cosa offre tipicamente un web framework, con riferimento "
         "a Express.",
         ["Libreria: funzioni che il nostro codice chiama, e che restituiscono il controllo; "
          "il flusso lo decide il nostro codice.",
          "Framework: progetto astratto in cui il nostro codice viene innestato; è il framework "
          "a controllare il flusso e a chiamare il nostro codice (IoC, «non chiamarci, ti "
          "chiamiamo noi»).",
          "Un web framework offre routing, analisi delle richieste, cookie e sessioni, un motore "
          "di template, spesso un ORM; può essere più o meno *opinionated*.",
          "Express: minimalista e unopinionated; rotte (`app.get(percorso, gestore)`, "
          "parametri, router), middleware, `res.render` con un motore di template."],
         rif=R % "Che cos'è un framework"))

d(aperta("c15-a-middleware", CAP, "middleware",
         "Si descriva il ciclo richiesta-risposta di Express e il ruolo dei middleware, con un "
         "esempio. Che cosa succede se un middleware non chiama `next()`?",
         ["Arrivata una richiesta, Express crea `req` e `res` e la fa passare per una sequenza "
          "di middleware e gestori, nell'ordine di dichiarazione, finché qualcuno non risponde.",
          "Un middleware è una funzione `(req, res, next)`: può modificare `req` e `res` (es. "
          "aggiungere `req.timestamp`), eseguire codice, rispondere, o passare al successivo "
          "con `next()`.",
          "Si montano con `app.use([percorso], fn)`; esempi: log, `express.static`, "
          "`express.urlencoded`, sessione, autenticazione.",
          "Senza `next()` e senza risposta la richiesta resta appesa fino al timeout del "
          "client, senza messaggi d'errore."],
         rif=R % "I middleware"))

d(aperta("c15-a-errori", CAP, "gestione degli errori",
         "Si descriva la gestione degli errori in Express: errori nel codice sincrono e "
         "asincrono, gestori personalizzati, differenze fra Express 4 ed Express 5.",
         ["Un errore sollevato nel codice sincrono di un gestore viene catturato da Express e "
          "passato al gestore degli errori (predefinito: `500`, traccia solo in sviluppo).",
          "Un errore nato in una callback asincrona va passato a mano con `next(err)`.",
          "Gestori personalizzati: middleware con quattro parametri `(err, req, res, next)`, "
          "dichiarati dopo le rotte; con tre parametri non vengono riconosciuti.",
          "Express 5: una Promise rifiutata da un gestore (es. `async` con `await`) invoca "
          "`next(err)` da sola; Express 4 la ignorava e il processo terminava."],
         rif=R % "Gestione degli errori"))

d(aperta("c15-a-sessioni", CAP, "sessioni e cookie",
         "Si confrontino `cookie-parser` ed `express-session`, e si spieghi a che cosa servono "
         "i messaggi flash e come funzionano.",
         ["`cookie-parser` analizza l'header `Cookie` in `req.cookies`; con `res.cookie` si "
          "impostano cookie i cui valori restano sul client, che può modificarli.",
          "`express-session` tiene i dati sul server e mette nel cookie solo l'identificatore, "
          "firmato con il `secret` (manomissioni riconosciute); archivio in memoria solo per lo "
          "sviluppo.",
          "Messaggi flash: dopo un'azione si reindirizza, e il messaggio va conservato fino "
          "alla richiesta successiva, che è un nuovo ciclo.",
          "`connect-flash` li salva nella sessione (dopo `express-session`): `req.flash(k, "
          "msg)` li aggiunge, `req.flash(k)` li legge e li consuma."],
         rif="cap. 15, «Middleware utili» e «Messaggi flash»"))
