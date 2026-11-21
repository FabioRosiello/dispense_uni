"""Capitolo 17: il paradigma REST (risorse, verbi e URI, archetipi, filtri e
paginazione, autenticazione con token e JWT, funzioni di hash, una API REST
con Express 5, regole di progettazione, OpenAPI).

Le domande sulle applicazioni Express sono verificate avviando davvero il
server; quella su jsonwebtoken eseguendo il codice con il pacchetto vero.
"""

from generatore import aperta, chiusa, famiglia, risposte_server, uscita_js

CAP = 17
R = "cap. 17, «%s»"

DOMANDE = []
d = DOMANDE.append

# ----------------------------------------------------------------------
# REST, risorse, verbi
d(chiusa("c17-stato", CAP, "risorse, verbi e URI",
         "Nel nome *Representational State Transfer*, dove vive lo **stato dell'applicazione** "
         "(che cosa l'utente sta guardando, i dati già ricevuti)?",
         "Sul client, mentre il server conserva lo stato delle risorse.",
         ["Sul server, nella sessione dell'utente.",
          "Nel token JWT, firmato dal server a ogni richiesta.",
          "Nel database, insieme alle risorse.",
          "In un proxy intermedio, che lo ricorda fra una richiesta e l'altra."],
         spiegazione="Lo stato delle **risorse** vive sul server; lo stato dell'**applicazione** "
                     "vive sul client; i due comunicano trasferendo **rappresentazioni** (per "
                     "esempio in JSON). Il server non conserva sessioni: ogni richiesta porta con "
                     "sé ciò che serve per essere servita.",
         rif=R % "Representational State Transfer", trabocchetto=True))

d(chiusa("c17-stateless", CAP, "risorse, verbi e URI",
         "Perché una API REST stateless si scala più facilmente di una web app con le sessioni "
         "in memoria?",
         "Due richieste dello stesso client possono essere servite da macchine diverse: per "
         "reggere più traffico basta aggiungerne.",
         ["Perché JSON è più compatto dell'HTML.",
          "Perché il server salva il token nel database a ogni richiesta.",
          "Perché le richieste stateless non attraversano la rete.",
          "Perché HTTP/3 è disponibile solo per le API stateless."],
         spiegazione="Se il server non conserva nulla fra una richiesta e l'altra, qualunque "
                     "macchina può rispondere a qualunque richiesta. Con le sessioni in memoria, "
                     "invece, ogni client resta legato alla macchina che lo ha servito la prima "
                     "volta.",
         rif=R % "I fondamenti"))

d(chiusa("c17-put", CAP, "risorse, verbi e URI",
         "Il document `/todos/3` è `{\"todo\": \"Studiare\", \"done\": false, \"priorita\": 2}`. "
         "Un client invia `PUT /todos/3` con il corpo `{\"done\": true}`. Secondo la semantica "
         "di `PUT`, che cosa dovrebbe contenere la risorsa dopo la richiesta?",
         "`{\"done\": true}`: `PUT` sostituisce l'intera rappresentazione con quella inviata.",
         ["`{\"todo\": \"Studiare\", \"done\": true, \"priorita\": 2}`: cambia solo `done`.",
          "Niente: `PUT` si usa solo per creare risorse nuove.",
          "Due elementi: `PUT` aggiunge una nuova versione della risorsa accanto alla vecchia.",
          "Niente: la richiesta fallisce perché mancano dei campi."],
         spiegazione="`PUT /todos/<ID>` **sostituisce** (o crea) la risorsa con i dati del corpo: "
                     "i campi non inviati non sopravvivono. Per modificare solo alcuni campi "
                     "esiste `PATCH` (capitolo 9). Un'API reale può validare il corpo e rifiutare "
                     "rappresentazioni incomplete, ma non le «completa» con i vecchi valori.",
         rif=R % "Verbi e URI", trabocchetto=True))

d(chiusa("c17-ripetere", CAP, "risorse, verbi e URI",
         "Un client ripete una richiesta andata in timeout, che arriva quindi **due volte** "
         "all'API. Per quali delle seguenti richieste lo stato del server dopo la seconda è lo "
         "stesso che dopo la prima?",
         ["`PUT /todos/3`, con lo stesso corpo.",
          "`DELETE /todos/3` (anche se la seconda risponde `404`).",
          "`GET /todos?done=true`."],
         ["`POST /todos`, con lo stesso corpo.",
          "`POST /alerts/1234/resend`.",
          "`POST /todos/3/toggle`, che inverte il campo `done`."],
         multi=True,
         spiegazione="`PUT` e `DELETE` sono **idempotenti**: ripeterle lascia il server nello "
                     "stesso stato (la seconda `DELETE` trova la risorsa già eliminata, ma lo "
                     "stato non cambia). `GET` non modifica nulla. `POST` su una collection crea "
                     "un secondo elemento; un controller come `resend` rispedisce l'avviso; un "
                     "*toggle* ripetuto annulla l'effetto del primo.",
         rif=R % "Verbi e URI"))

d(chiusa("c17-una-uri", CAP, "risorse, verbi e URI",
         "La stessa recensione è raggiungibile sia come `/sellers/3/reviews/8` sia come "
         "`/reviews/8`. Qual è il problema principale?",
         "Per i client e per le cache sono due risorse diverse: una modifica inviata a un "
         "indirizzo non invalida la copia dell'altro.",
         ["Express non permette di collegare due rotte allo stesso controller.",
          "Le risorse annidate non sono ammesse in REST.",
          "`/reviews/8` viola la regola dei nomi al plurale.",
          "Il server deve conservare due copie della recensione nel database."],
         spiegazione="Ogni risorsa dovrebbe avere **una sola** URI. Con due indirizzi le cache "
                     "tengono due copie che invecchiano ciascuna per conto suo. Le risorse "
                     "annidate vanno benissimo, purché ogni risorsa abbia un solo indirizzo.",
         rif=R % "Risorse annidate"))

# ----------------------------------------------------------------------
# Archetipi e regole
d(chiusa("c17-store", CAP, "archetipi e regole",
         "Un client aggiunge il Napoli ai preferiti dell'utente 1234 inviando "
         "`PUT /users/1234/favourites/napoli`, e la risorsa nasce esattamente a quell'URI. Di "
         "quale archetipo è `/users/1234/favourites`?",
         "Uno store: è il client a scegliere l'URI delle nuove risorse.",
         ["Una collection: è al plurale e contiene più risorse.",
          "Un controller: modifica lo stato dell'utente.",
          "Un document: appartiene a un singolo utente.",
          "Una collection annidata: le collection accettano `PUT` per creare elementi."],
         spiegazione="Collection e store sono entrambi al plurale e contengono risorse; la "
                     "differenza sta in **chi sceglie l'URI** dei nuovi elementi. In una "
                     "collection il client propone con `POST` e il server sceglie "
                     "l'identificatore (comunicandolo con `Location`); in uno store il client "
                     "crea la risorsa con `PUT` all'URI che preferisce.",
         rif=R % "Store", trabocchetto=True))

d(chiusa("c17-coerenti", CAP, "archetipi e regole",
         "Quali delle seguenti richieste sono coerenti con le regole e gli archetipi del "
         "capitolo?",
         ["`POST /todos`, per aggiungere un elemento.",
          "`DELETE /todos/2`.",
          "`POST /alerts/1234/resend`.",
          "`PUT /users/1234/favourites/napoli`."],
         ["`GET /todos/2/delete`.",
          "`POST /deleteTodo?id=2`.",
          "`GET /reset-app`, per azzerare l'applicazione.",
          "`POST /My_Todos`."],
         multi=True,
         spiegazione="`POST` su una collection aggiunge un elemento, `DELETE` elimina un "
                     "document, `POST` esegue un controller (un verbo), `PUT` inserisce in uno "
                     "store. Le altre violano qualche regola: `GET` solo per leggere (anche "
                     "`/reset-app`, che pure ha un nome corretto, va invocato con `POST`), "
                     "niente operazioni CRUD nelle URI, URI in minuscolo e senza trattini "
                     "bassi.",
         rif=R % "Regole e linee guida", trabocchetto=True))

d(chiusa("c17-regole-uri", CAP, "archetipi e regole",
         "Quali delle seguenti URI rispettano **tutte** le regole di nomenclatura del capitolo?",
         ["`/leagues/serie-a/teams`", "`/users/1234/favourites`", "`/alerts/1234/resend`"],
         ["`/todos/`", "`/my_todos`", "`/resetApp`", "`/todo/2`", "`/Todos`"],
         multi=True,
         spiegazione="Collection e store al plurale, document al singolare (o con un "
                     "identificatore), controller con un verbo; niente barra finale, minuscolo, "
                     "trattini (`-`) al posto di trattini bassi e CamelCase. `/todo/2` usa il "
                     "singolare per una collection.",
         rif=R % "Regole e linee guida"))

d(risposte_server("c17-express-tollerante", CAP, "archetipi e regole",
                  """
import express from "express";
const app = express();
app.get("/todos", (req, res) => res.send("lista"));
app.listen(3000);""",
                  ["GET /todos/", "GET /TODOS", "GET /todos/1"],
                  ["200 lista", "200 lista", "404 Cannot GET /todos/1"],
                  [["404 Cannot GET /todos/", "404 Cannot GET /TODOS", "404 Cannot GET /todos/1"],
                   ["200 lista", "404 Cannot GET /TODOS", "404 Cannot GET /todos/1"],
                   ["404 Cannot GET /todos/", "200 lista", "404 Cannot GET /todos/1"],
                   ["200 lista", "200 lista", "200 lista"]],
                  applicazione="Express",
                  spiegazione="Per impostazione predefinita Express è tollerante: ignora la barra "
                              "finale e non distingue maiuscole e minuscole nei percorsi, quindi "
                              "`/todos/` e `/TODOS` portano alla stessa rotta. `/todos/1` invece "
                              "è un altro percorso. Proprio per questo un'API dovrebbe "
                              "documentare e usare una sola forma: una risorsa, una URI.",
                  rif=R % "Regole e linee guida", trabocchetto=True))

# ----------------------------------------------------------------------
# Filtri, paginazione, ricerche
d(risposte_server("c17-query-stringhe", CAP, "filtri, paginazione e ricerche",
                  """
import express from "express";
const app = express();
app.get("/users", (req, res) => {
  const { min } = req.query;
  res.json({ tipo: typeof min, doppio: min * 2, somma: min + 1 });
});
app.listen(3000);""",
                  ["GET /users?min=18"],
                  ['200 {"tipo":"string","doppio":36,"somma":"181"}'],
                  [['200 {"tipo":"number","doppio":36,"somma":19}'],
                   ['200 {"tipo":"string","doppio":"1818","somma":"181"}'],
                   ['200 {"tipo":"string","doppio":36,"somma":19}'],
                   ['200 {"tipo":"number","doppio":36,"somma":"181"}']],
                  applicazione="Express",
                  spiegazione="Express consegna i parametri della query in `req.query` così come "
                              "sono scritti, e i valori sono sempre **stringhe**. La "
                              "moltiplicazione converte la stringa in numero (`36`), ma `+` con "
                              "una stringa concatena (`\"181\"`). Convertire i numeri è compito "
                              "del codice dell'API.",
                  rif=R % "Filtrare", trabocchetto=True))

d(risposte_server("c17-query-nomi", CAP, "filtri, paginazione e ricerche",
                  """
import express from "express";
const app = express();
app.get("/users", (req, res) => res.json(req.query));
app.listen(3000);""",
                  ["GET /users?age.gt=18&age.lte=40", "GET /users?role=admin&role=user"],
                  ['200 {"age.gt":"18","age.lte":"40"}', '200 {"role":["admin","user"]}'],
                  [['200 {"age":{"gt":"18","lte":"40"}}', '200 {"role":["admin","user"]}'],
                   ['200 {"age":{"gt":18,"lte":40}}', '200 {"role":"user"}'],
                   ['200 {"age.gt":"18","age.lte":"40"}', '200 {"role":"user"}'],
                   ['200 {"age.gt":18,"age.lte":40}', '200 {"role":"admin"}']],
                  applicazione="Express",
                  spiegazione="I nomi dei parametri arrivano così come sono scritti, punto "
                              "compreso: `age.gt` non diventa un oggetto annidato, e tradurlo in "
                              "una condizione è compito dell'API (è una sua convenzione, non uno "
                              "standard). I valori sono stringhe; un parametro ripetuto diventa "
                              "un array.",
                  rif=R % "Filtrare"))


@famiglia("c17-paginazione", CAP, "filtri, paginazione e ricerche", varianti=3)
def _paginazione(rng):
    size = rng.choice([5, 10, 20, 25, 50])
    page = rng.randint(2, 6)
    primo = (page - 1) * size + 1
    giusta = "Dall'elemento %d al %d." % (primo, page * size)
    sbagliate = ["Dall'elemento %d al %d." % (page * size + 1, (page + 1) * size),
                 "Dall'elemento %d al %d." % (primo - 1, page * size - 1),
                 "Dall'elemento %d al %d." % (page, page + size - 1),
                 "Dall'elemento 1 al %d." % (page * size)]
    return chiusa("c17-paginazione", CAP, "filtri, paginazione e ricerche",
                  "Una API restituisce i risultati a pagine di `size` elementi, numerando le "
                  "pagine da 1. Quali elementi restituisce `GET /todos?size=%d&page=%d`?"
                  % (size, page),
                  giusta, sbagliate,
                  spiegazione="La pagina `page` comincia dopo `(page - 1) * size` elementi: qui "
                              "si saltano i primi %d e si restituiscono i %d successivi."
                              % (primo - 1, size),
                  rif=R % "Paginare")


d(_paginazione)

d(chiusa("c17-ricerca-post", CAP, "filtri, paginazione e ricerche",
         "Una ricerca con criteri complessi viene esposta come `POST /users/search`, con i "
         "criteri in un oggetto JSON nel corpo. Qual è il prezzo di questa scelta rispetto a "
         "una `GET` con la query string?",
         "La richiesta non è né sicura né idempotente, e non viene messa in cache.",
         ["Il server non può leggere un corpo JSON in una `POST`.",
          "`/users/search` viola la regola dei nomi al plurale.",
          "I criteri finiscono nell'URL, e quindi nei log.",
          "Il client deve autenticarsi due volte."],
         spiegazione="Una risorsa controller come `search` permette criteri strutturati "
                     "(alternative, liste, annidamenti) scomodi nella query string. Ma `POST` "
                     "non ha la semantica di sola lettura di `GET`: è proprio il vuoto che vuole "
                     "colmare il metodo `QUERY` (capitolo 9).",
         rif=R % "Ricerche complesse"))

# ----------------------------------------------------------------------
# Autenticazione e autorizzazione
d(chiusa("c17-403", CAP, "autenticazione e autorizzazione",
         "Un utente, con un token valido, invia `DELETE /todos/7`, ma l'elemento 7 appartiene a "
         "un altro utente. Secondo la distinzione fra autenticazione e autorizzazione, con quale "
         "codice dovrebbe rispondere l'API?",
         "`403 Forbidden`",
         ["`401 Unauthorized`", "`400 Bad Request`", "`405 Method Not Allowed`",
          "`409 Conflict`"],
         spiegazione="`401` vuol dire «non so chi sei» (token mancante o non valido); `403` «so "
                     "chi sei, ma non puoi». Qui l'utente è autenticato: mancano i permessi. Il "
                     "nome di `401`, *Unauthorized*, inganna. (Alcune API rispondono di "
                     "proposito `404` per non rivelare quali identificatori esistono: deve "
                     "essere una scelta, non un incidente.)",
         rif=R % "Autorizzazione", trabocchetto=True))

d(chiusa("c17-scaduto", CAP, "autenticazione e autorizzazione",
         "Una richiesta arriva all'API del capitolo con un JWT la cui firma è corretta, ma il "
         "cui campo `exp` è già passato. Che cosa risponde il middleware "
         "`enforceAuthentication`?",
         "`401`: `jwt.verify` rifiuta il token scaduto (`TokenExpiredError`).",
         ["`200`: la firma è valida, e il server non ricorda i token emessi.",
          "`403`: l'utente è identificato, ma il token non dà più permessi.",
          "`400`: la richiesta è malformata.",
          "`500`: il token scaduto solleva un'eccezione non gestita."],
         spiegazione="`jwt.verify` controlla la firma **e** la scadenza: un token scaduto ha "
                     "una firma valida ma viene rifiutato, e il middleware chiama `next` con "
                     "`status: 401`. Per questo i token hanno una durata limitata: il server non "
                     "può revocarli, e un token rubato vale fino alla scadenza.",
         rif=R % "Il middleware di autenticazione"))

d(chiusa("c17-jwt", CAP, "autenticazione e autorizzazione",
         "Quali delle seguenti affermazioni su un JWT firmato con `HS256` sono **vere**?",
         ["Chiunque intercetti il token può leggerne il payload senza conoscere la chiave.",
          "Modificare il payload invalida la firma, a meno di conoscere la chiave segreta.",
          "La stessa chiave segreta serve sia a firmare sia a verificare.",
          "Un token rubato resta valido fino alla scadenza, anche dopo il «logout» del client."],
         ["Il payload è cifrato con la chiave segreta, quindi può contenere la password.",
          "La firma è un hash del payload calcolato senza chiave, che chiunque può rifare.",
          "Il server conserva l'elenco dei token emessi per poterli verificare.",
          "Base64Url garantisce la riservatezza dell'header."],
         multi=True,
         spiegazione="Header e payload sono solo **codificati** in Base64Url: si leggono senza "
                     "chiave, e non vanno mai usati per dati riservati. La firma (un HMAC-SHA256 "
                     "di `header.payload` calcolato **con** la chiave) garantisce l'integrità: "
                     "senza la chiave non si ricalcola. Con `HS256` chi verifica può anche "
                     "firmare (con `RS256` no). Il server non ricorda i token: il logout è il "
                     "client che dimentica il token.",
         rif=R % "JSON Web Token"))

d(uscita_js("c17-jwt-decode", CAP, "autenticazione e autorizzazione",
            """
import jwt from "jsonwebtoken";
const segreto = "una-chiave-lunga-e-casuale";
const token = jwt.sign({ user: "eric", role: "user" }, segreto);
const [h, p, s] = token.split(".");
const dati = JSON.parse(Buffer.from(p, "base64url").toString());
dati.role = "admin";
const falso = [h, Buffer.from(JSON.stringify(dati)).toString("base64url"), s].join(".");
console.log(jwt.decode(falso).role);
try { console.log(jwt.verify(falso, segreto).role); }
catch (e) { console.log(e.message); }""",
            ["admin", "invalid signature"],
            [["user", "invalid signature"], ["admin", "admin"],
             ["invalid signature", "invalid signature"], ["user", "user"]],
            testo="Il modulo seguente, eseguito con Node, usa il pacchetto `jsonwebtoken` "
                  "(quello del capitolo). Qual è il risultato dell'esecuzione?",
            modulo=True, pacchetti=True,
            spiegazione="Il payload si legge e si riscrive senza chiave: è solo Base64Url. "
                        "`jwt.decode` **decodifica senza verificare**, quindi restituisce il "
                        "payload alterato (`admin`). `jwt.verify` invece ricalcola la firma con "
                        "la chiave: non corrisponde più, e solleva `invalid signature`. "
                        "Un'API deve fidarsi solo di ciò che restituisce `verify`.",
            rif=R % "JSON Web Token", trabocchetto=True))

d(risposte_server("c17-ordine-router", CAP, "autenticazione e autorizzazione",
                  """
import express from "express";
const app = express();
const auth = (req, res, next) => {
  if (req.get("Authorization") === "Bearer ok") next();
  else res.status(401).json({ code: 401 });
};
app.post("/auth", (req, res) => res.json("ok"));
app.use(auth);
app.get("/todos", (req, res) => res.json([]));
app.use((req, res) => res.status(404).json({ code: 404 }));
app.listen(3000);""",
                  ["GET /nonesiste", "POST /auth",
                   {"metodo": "GET", "percorso": "/todos",
                    "intestazioni": {"Authorization": "Bearer ok"}}],
                  ['401 {"code":401}', '200 "ok"', "200 []"],
                  [['404 {"code":404}', '200 "ok"', "200 []"],
                   ['401 {"code":401}', '401 {"code":401}', "200 []"],
                   ['404 {"code":404}', '401 {"code":401}', "200 []"],
                   ['401 {"code":401}', '200 "ok"', '401 {"code":401}']],
                  applicazione="Express",
                  spiegazione="I middleware si eseguono nell'ordine di dichiarazione. `/auth` "
                              "viene prima di `auth`, quindi si raggiunge senza token (altrimenti "
                              "nessuno potrebbe ottenerne uno). `auth`, montato senza percorso, "
                              "intercetta **tutte** le richieste successive: anche quella per un "
                              "percorso inesistente riceve `401`, prima di arrivare al "
                              "*catch-all* `404`. Per un'API è un comportamento ragionevole: chi "
                              "non è autenticato non scopre nemmeno quali risorse esistono.",
                  rif=R % "Cinque ritocchi", trabocchetto=True))

d(risposte_server("c17-content-type", CAP, "autenticazione e autorizzazione",
                  """
import express from "express";
const app = express();
app.use(express.json());
app.post("/auth", (req, res) => {
  res.json({ utente: req.body.usr });
});
app.use((err, req, res, next) => {
  res.status(err.status || 500).json({ errore: err.status || 500 });
});
app.listen(3000);""",
                  [{"metodo": "POST", "percorso": "/auth", "corpo": '{"usr": "janet"}'},
                   {"metodo": "POST", "percorso": "/auth", "corpo": '{"usr": "janet"}',
                    "intestazioni": {"Content-Type": "application/json"}},
                   {"metodo": "POST", "percorso": "/auth", "corpo": "{'usr': 'janet'}",
                    "intestazioni": {"Content-Type": "application/json"}}],
                  ['500 {"errore":500}', '200 {"utente":"janet"}', '400 {"errore":400}'],
                  [['200 {"utente":"janet"}', '200 {"utente":"janet"}', '400 {"errore":400}'],
                   ['200 {}', '200 {"utente":"janet"}', '200 {"utente":"janet"}'],
                   ['400 {"errore":400}', '200 {"utente":"janet"}', '500 {"errore":500}'],
                   ['500 {"errore":500}', '200 {"utente":"janet"}', '200 {"utente":"janet"}']],
                  testo="Si consideri la seguente applicazione Express 5, in ascolto sulla porta "
                        "3000. Le si inviano tre richieste `POST /auth`: (1) con il corpo "
                        "`{\"usr\": \"janet\"}` dichiarato come dati di un form, come fa "
                        "`curl -d` senza altre opzioni; (2) con lo stesso corpo e l'header "
                        "`Content-Type: application/json`; (3) con il corpo `{'usr': 'janet'}` "
                        "e l'header `Content-Type: application/json`. Quali risposte ottengono, "
                        "nell'ordine?",
                  spiegazione="`express.json` analizza solo i corpi dichiarati come JSON. Nella "
                              "prima richiesta lo ignora, e in Express 5 `req.body` resta "
                              "`undefined`: leggere `req.body.usr` solleva un `TypeError`, che "
                              "arriva al gestore senza `status` e diventa `500` (l'API dà la "
                              "colpa a sé stessa per un errore del client). La terza ha "
                              "apici singoli, che JSON non ammette: è `express.json` a "
                              "segnalare l'errore, con `status` 400.",
                  rif=R % "Cinque ritocchi", trabocchetto=True))

d(chiusa("c17-hash", CAP, "autenticazione e autorizzazione",
         "Quali delle seguenti affermazioni su una funzione di hash crittografica come SHA-256 "
         "sono **vere**?",
         ["Il digest ha sempre la stessa lunghezza, qualunque sia l'input.",
          "Dato un digest, è impraticabile risalire all'input che lo ha generato.",
          "Cambiare un solo carattere dell'input produce un digest completamente diverso."],
         ["Con la chiave giusta il digest si può invertire.",
          "Input più lunghi producono digest più lunghi.",
          "`echo 'abc' | sha256sum` e `printf 'abc' | sha256sum` stampano lo stesso digest.",
          "Due input diversi producono sempre, per costruzione, digest diversi."],
         multi=True,
         spiegazione="SHA-256 produce sempre 256 bit, è facile da calcolare ma non invertibile, "
                     "e una minima differenza nell'input cambia tutto (anche l'a capo che "
                     "`echo` aggiunge in fondo). Le collisioni esistono per forza, perché gli "
                     "input possibili sono infiniti: una funzione sicura rende solo "
                     "**impraticabile** trovarne una.",
         rif=R % "Funzioni di hash crittografiche", trabocchetto=True))

# ----------------------------------------------------------------------
# OpenAPI
d(chiusa("c17-openapi", CAP, "OpenAPI",
         "Quali delle seguenti affermazioni su OpenAPI sono **vere**?",
         ["È uno standard per **descrivere** le API HTTP, già noto come Swagger.",
          "Una specifica si può scrivere indifferentemente in JSON o in YAML.",
          "Da una specifica si possono generare documentazione interattiva, SDK per i client e "
          "scheletri di server."],
         ["È un framework per implementare API REST in Node.js.",
          "Sostituisce HTTP con un protocollo binario più efficiente.",
          "Genera automaticamente l'implementazione completa del server.",
          "Si può scrivere soltanto dopo aver implementato l'API."],
         multi=True,
         spiegazione="OpenAPI è una descrizione formale, leggibile da persone e macchine "
                     "(versione `openapi`, `info`, `paths`…). Serve alla progettazione, alla "
                     "generazione di codice (solo **scheletri** lato server) e alla "
                     "documentazione (Swagger UI). Spesso la si scrive per prima "
                     "(*OpenAPI-driven development*).",
         rif=R % "OpenAPI"))

# ----------------------------------------------------------------------
# Domande aperte
d(aperta("c17-a-rest", CAP, "risorse, verbi e URI",
         "Che cos'è REST? Se ne descrivano i principi fondamentali e si spieghi il significato "
         "del nome *Representational State Transfer*.",
         ["Uno stile architetturale (non uno standard né un protocollo) per le API web, basato "
          "su HTTP e sulle URI.",
          "Risorse identificate da URI univoche; verbi HTTP per leggerle e modificarle (GET, "
          "POST, PUT, DELETE).",
          "Stateless: niente sessioni lato server, ogni richiesta porta con sé ciò che serve "
          "(scalabilità).",
          "Stato dell'applicazione sul client, stato delle risorse sul server; si scambiano "
          "rappresentazioni (JSON, XML)."],
         rif=R % "REST"))

d(aperta("c17-a-archetipi", CAP, "archetipi e regole",
         "Si descrivano i quattro archetipi di risorse di una API REST, con un esempio di URI e "
         "i metodi tipici per ciascuno.",
         ["Document: un singolo oggetto, nome al singolare o identificatore "
          "(`/leagues/serie-a`); GET, PUT, DELETE.",
          "Collection: directory gestita dal server, plurale (`/leagues`); GET e POST (il "
          "server sceglie l'URI e risponde 201 con Location).",
          "Store: directory gestita dal client, plurale (`/users/1234/favourites`); PUT "
          "all'URI scelto dal client, GET, DELETE.",
          "Controller: una procedura, nome verbale (`/alerts/1234/resend`); POST."],
         rif=R % "Quattro archetipi di risorse"))

d(aperta("c17-a-token", CAP, "autenticazione e autorizzazione",
         "Si descriva lo schema di autenticazione basato su token per una API REST e la "
         "struttura di un JSON Web Token. Che cosa garantisce la firma, e che cosa no?",
         ["Login con credenziali, l'API risponde con un token; il client lo rimanda a ogni "
          "richiesta in `Authorization: Bearer ...`; l'API lo verifica (stateless).",
          "JWT: `header.payload.signature`, header e payload in JSON codificati in Base64Url; "
          "asserzioni come `exp` e `iat`.",
          "La firma (HMAC con chiave segreta, HS256) garantisce l'integrità: un payload "
          "alterato non supera la verifica.",
          "Non garantisce la riservatezza (il payload si legge senza chiave) e non permette la "
          "revoca: un token rubato vale fino alla scadenza."],
         rif=R % "Autenticazione con token"))

d(aperta("c17-a-401-403", CAP, "autenticazione e autorizzazione",
         "Si spieghi la differenza fra autenticazione e autorizzazione in una API REST, e fra i "
         "codici `401` e `403`, con un esempio per ciascuno. Come si realizzano in Express?",
         ["Autenticazione: chi sei (token valido); autorizzazione: che cosa puoi fare (es. "
          "modificare solo i propri elementi).",
          "`401 Unauthorized`: credenziali mancanti, scadute o alterate.",
          "`403 Forbidden`: utente autenticato senza permessi sulla risorsa.",
          "In Express: un middleware che verifica il token e salva l'utente in `req`, poi un "
          "middleware sulla rotta che controlla i permessi (l'ordine conta)."],
         rif=R % "Autorizzazione"))

d(aperta("c17-a-openapi", CAP, "OpenAPI",
         "Che cos'è lo standard OpenAPI, perché è stato introdotto e a che cosa può servire?",
         ["Standard aperto e formale (già Swagger) per descrivere le API HTTP, in JSON o YAML.",
          "Introdotto per standardizzare la documentazione e renderla leggibile anche dalle "
          "macchine.",
          "Usi: supporto alla progettazione (errori e incoerenze prima del codice), "
          "generazione di codice (SDK, scheletri di server, test), documentazione interattiva "
          "(Swagger UI)."],
         rif=R % "OpenAPI"))
