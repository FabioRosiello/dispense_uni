"""Capitolo 18: API pronte per la produzione (OpenAPI, evoluzione e
versionamento, deprecazione, OWASP API Security Top 10, rate limiting,
SSRF, configurazioni e risposte di errore, osservabilità e log).

Le domande sulle applicazioni Express (versioni con Accept, rate limiting
con express-rate-limit) sono verificate avviando davvero il server; quelle
sulla validazione degli URL eseguendo il codice con Node.
"""

from generatore import Err, aperta, chiusa, risposte_server, uscita_js

CAP = 18
R = "cap. 18, «%s»"

DOMANDE = []
d = DOMANDE.append

# ----------------------------------------------------------------------
# Evoluzione e versionamento
d(chiusa("c18-breaking", CAP, "evoluzione e versionamento",
         "Quali delle seguenti modifiche a una API sono potenzialmente **non retrocompatibili** "
         "(*breaking change*)?",
         ["Rinominare il campo `title` in `name`.",
          "Sostituire il booleano `completed` con un campo `status` di tipo stringa.",
          "Rispondere `200` invece di `201` alle creazioni.",
          "Cambiare il formato delle risposte di errore."],
         ["Aggiungere un nuovo endpoint.",
          "Aggiungere un campo facoltativo alla risposta, con client che ignorano i campi "
          "sconosciuti.",
          "Aggiungere un parametro di filtro facoltativo, con un valore predefinito.",
          "Riscrivere l'implementazione interna senza cambiarne il comportamento."],
         multi=True,
         spiegazione="L'API è un contratto: percorsi, formati, codici di stato, errori, "
                     "autenticazione. Rinominare o togliere campi, cambiarne il tipo, cambiare "
                     "codici di stato o formato degli errori rompe i client che ci contano. "
                     "Aggiungere (endpoint, campi facoltativi, filtri con un valore predefinito) "
                     "di solito è sicuro, come un refactoring che non cambia il comportamento.",
         rif=R % "Modifiche compatibili e modifiche che rompono"))

d(chiusa("c18-campo-in-piu", CAP, "evoluzione e versionamento",
         "Si aggiunge il campo `createdAt` alla risposta di `GET /tasks/1`: di solito è una "
         "modifica sicura. In quale caso **rompe** un client esistente?",
         "Se il client valida le risposte contro uno schema che non ammette campi aggiuntivi.",
         ["Se il client legge solo `title` e `completed`.",
          "Se il client usa `fetch` invece di `curl`.",
          "Se la nuova versione non cambia il prefisso `/api/v1`.",
          "Se il campo contiene una data in formato ISO."],
         spiegazione="Aggiungere un campo alla risposta è sicuro **purché i client ignorino i "
                     "campi che non conoscono**. Un client che rifiuta le risposte con campi in "
                     "più trasforma anche questa modifica in una rottura.",
         rif=R % "Modifiche compatibili e modifiche che rompono", trabocchetto=True))

d(chiusa("c18-quando-versionare", CAP, "evoluzione e versionamento",
         "Quale regola riassume quando conviene creare una nuova versione di una API?",
         "Aggiungere senza cambiare versione; togliere o ridefinire con una versione nuova.",
         ["Una versione nuova a ogni rilascio, così i client possono sempre scegliere.",
          "Mai versionare: sono i client a doversi adeguare.",
          "Versionare solo quando cambia l'implementazione interna.",
          "Versionare ogni endpoint separatamente, a ogni modifica."],
         spiegazione="Mantenere più versioni è un grande sforzo (correzioni, documentazione, "
                     "test e monitoraggio per ciascuna): si versiona solo per le modifiche che "
                     "rompono il contratto.",
         rif=R % "Quando versionare"))

d(risposte_server("c18-accept", CAP, "evoluzione e versionamento",
                  """
import express from "express";
const app = express();
const V2 = "application/vnd.academy.tasks.v2+json";
const task = { id: 1, title: "Lezione", status: "DONE" };
app.get("/api/tasks/1", (req, res) => {
  res.vary("Accept");
  if (req.accepts(["application/json", V2]) === V2) {
    res.type(V2).json(task);
  } else {
    res.json({ id: 1, title: "Lezione", completed: task.status === "DONE" });
  }
});
app.listen(3000);""",
                  [{"metodo": "GET", "percorso": "/api/tasks/1",
                    "intestazioni": {"Accept": "*/*"}},
                   {"metodo": "GET", "percorso": "/api/tasks/1",
                    "intestazioni": {"Accept": "application/vnd.academy.tasks.v2+json"}}],
                  ['200 {"id":1,"title":"Lezione","completed":true}',
                   '200 {"id":1,"title":"Lezione","status":"DONE"}'],
                  [['200 {"id":1,"title":"Lezione","status":"DONE"}',
                    '200 {"id":1,"title":"Lezione","status":"DONE"}'],
                   ['200 {"id":1,"title":"Lezione","completed":true}',
                    '200 {"id":1,"title":"Lezione","completed":true}'],
                   ['406 Not Acceptable', '200 {"id":1,"title":"Lezione","status":"DONE"}'],
                   ['200 {"id":1,"title":"Lezione","status":"DONE"}',
                    '200 {"id":1,"title":"Lezione","completed":true}']],
                  applicazione="Express",
                  spiegazione="`req.accepts` sceglie, fra i tipi che il server sa produrre, quello "
                              "preferito dal client. `Accept: */*` (quello che inviano di solito "
                              "curl e `fetch`) accetta tutto, e vince il **primo** della lista: "
                              "la v1. Chi chiede esplicitamente il tipo della v2 la ottiene. "
                              "`Vary: Accept` avverte le cache che la risposta dipende da quell'"
                              "header.",
                  rif=R % "Versionare", trabocchetto=True))

d(chiusa("c18-vary", CAP, "evoluzione e versionamento",
         "Una API sceglie la versione della risposta in base all'header `Accept`. Perché deve "
         "aggiungere alla risposta `Vary: Accept`?",
         "Perché una cache non serva a un client la versione chiesta da un altro.",
         ["Per dire al client quali versioni esistono.",
          "Perché senza, Express ignora l'header `Accept`.",
          "Per annunciare che la versione 1 è deprecata.",
          "Per permettere le richieste da altre origini."],
         spiegazione="Con una sola URI per tutte le versioni, la risposta dipende da un header "
                     "della richiesta. `Vary` lo dice alle cache (capitolo 2): senza, una cache "
                     "potrebbe riusare per tutti la prima rappresentazione ricevuta.",
         rif=R % "Versionare"))

d(chiusa("c18-strategie", CAP, "evoluzione e versionamento",
         "Quali delle seguenti affermazioni sulle strategie di versionamento sono **vere**?",
         ["La versione nell'URI (`/api/v1/tasks`) è facile da provare, documentare e "
          "instradare.",
          "Con la versione in un header, la stessa URI serve tutte le versioni.",
          "In Express, due versioni nell'URI si realizzano con due router montati su prefissi "
          "diversi."],
         ["La versione nell'URI richiede di duplicare il database.",
          "Il prefisso `vnd.` in `application/vnd.academy.tasks.v2+json` indica una versione "
          "deprecata.",
          "Con la versione in un header non si possono avere due versioni attive insieme.",
          "La versione nell'URI impedisce di usare il browser per provare l'API."],
         multi=True,
         spiegazione="La versione nell'URI è la strategia più immediata (un prezzo: qualche "
                     "duplicazione in router e controller, non nei dati). Con un header "
                     "(`X-API-Version` o il tipo richiesto in `Accept`, dove `vnd.` sta per "
                     "*vendor*, un tipo definito da chi fornisce l'API) l'URI resta unica.",
         rif=R % "Versionare"))

d(chiusa("c18-deprecazione", CAP, "evoluzione e versionamento",
         "Una versione dell'API è **deprecata** ma ancora attiva. Quali delle seguenti "
         "affermazioni sono **vere**?",
         ["Continua a funzionare come prima, ma può aggiungere alle risposte gli header "
          "`Deprecation` e `Sunset`.",
          "La data di `Sunset` non deve essere precedente a quella di `Deprecation`.",
          "Un header `Link` con `rel=\"deprecation\"` può indicare dove trovare le istruzioni "
          "per migrare."],
         ["Risponde `410 Gone` a ogni richiesta.",
          "Secondo la RFC 9745, il valore dell'header `Deprecation` è `true`.",
          "Gli header di deprecazione fanno fallire i client che non li conoscono.",
          "Si deve creare una nuova versione anche per aggiungere un campo facoltativo."],
         multi=True,
         spiegazione="L'idea è non rompere i client in silenzio: una versione deprecata funziona "
                     "ancora, e lo annuncia con `Deprecation`, `Sunset` (la data di dismissione) "
                     "e `Link`. `Deprecation: true` è la forma delle prime bozze, molto diffusa; "
                     "la RFC 9745 (2025) prevede la **data**, scritta come `@` seguito dai "
                     "secondi dal 1970.",
         rif=R % "Deprecazione e dismissione", trabocchetto=True))

# ----------------------------------------------------------------------
# Sicurezza
d(chiusa("c18-bola", CAP, "sicurezza delle API",
         "Nell'API del capitolo 17 si toglie il middleware `ensureUsersModifyOnlyOwnTodos` dalla "
         "rotta `GET /todos/:id`. eric, con un token valido, chiede `/todos/1`, che appartiene "
         "a janet. Che cosa ottiene?",
         "`200` con l'elemento di janet: è una *Broken Object Level Authorization*.",
         ["`401`: il token di eric non vale per gli elementi di janet.",
          "`403`: Sequelize controlla il proprietario prima di restituire l'elemento.",
          "`404`: per eric l'elemento non esiste.",
          "`500`: l'elemento non appartiene all'utente del token."],
         spiegazione="L'autenticazione dice **chi** è eric, non che cosa può vedere: senza il "
                     "controllo, la rotta cerca l'elemento solo per identificatore. E con "
                     "identificatori consecutivi provarli tutti è banale. Il `404` sarebbe la "
                     "risposta della soluzione robusta, che cerca l'elemento fra quelli "
                     "dell'utente.",
         rif=R % "Autorizzazione a livello di oggetto", trabocchetto=True))

d(chiusa("c18-bola-difesa", CAP, "sicurezza delle API",
         "Qual è la difesa più robusta contro la *Broken Object Level Authorization* indicata "
         "nel capitolo?",
         "Cercare l'oggetto fra quelli dell'utente, mettendo il proprietario nella condizione "
         "della query.",
         ["Usare identificatori numerici consecutivi, più facili da controllare.",
          "Nascondere nel front-end i pulsanti per gli elementi altrui.",
          "Verificare con più attenzione che il token sia valido.",
          "Rispondere sempre `403`, anche per gli elementi che non esistono."],
         spiegazione="Con `Todo.findOne({ where: { id, UserUserName: req.username } })` gli "
                     "elementi altrui semplicemente non esistono per chi li chiede: le risposte "
                     "sono identiche a quelle per un identificatore inesistente, e il controllo "
                     "non si può dimenticare in una rotta, perché sta nella query.",
         rif=R % "Autorizzazione a livello di oggetto"))

d(chiusa("c18-owasp", CAP, "sicurezza delle API",
         "Solo il personale dovrebbe poter eseguire `DELETE /api/tags/5`, ma la rotta non "
         "controlla il ruolo (tanto nessun pulsante del front-end porta a quella richiesta). "
         "Quale rischio della OWASP API Security Top 10 è?",
         "Broken Function Level Authorization.",
         ["Broken Object Level Authorization.",
          "Broken Object Property Level Authorization.",
          "Security Misconfiguration.",
          "Unrestricted Access to Sensitive Business Flows."],
         spiegazione="Il problema riguarda una **funzionalità** riservata a un ruolo, non un "
                     "oggetto altrui (BOLA) né le singole proprietà di un oggetto (BOPLA). E "
                     "nascondere il pulsante non protegge nulla: `curl` non ha bisogno di "
                     "pulsanti. La difesa è un middleware che verifica il ruolo e risponde "
                     "`403`.",
         rif=R % "Autorizzazione a livello di funzione", trabocchetto=True))

d(chiusa("c18-mass-assignment", CAP, "sicurezza delle API",
         "La rotta che aggiorna un elemento esegue `item.set(req.body)` e poi lo salva. Quale "
         "rischio introduce?",
         "Un client può cambiare proprietà riservate, per esempio il proprietario "
         "dell'elemento (*mass assignment*).",
         ["Un client può leggere le password degli altri utenti.",
          "L'API diventa vulnerabile alla *Server-Side Request Forgery*.",
          "La richiesta smette di essere idempotente.",
          "Il token dell'utente viene salvato nel database."],
         spiegazione="È il secondo aspetto della *Broken Object Property Level Authorization*: "
                     "copiando tutto il corpo, un client può inviare anche "
                     "`\"UserUserName\": \"eric\"` e regalare l'elemento a un altro. Si copiano "
                     "solo i campi previsti; e nelle risposte si restituiscono DTO, non i "
                     "modelli del database (che contengono, per esempio, la password).",
         rif=R % "Autorizzazione a livello di proprietà"))

d(risposte_server("c18-rate-limit", CAP, "sicurezza delle API",
                  """
import express from "express";
import { rateLimit } from "express-rate-limit";
const app = express();
app.use(rateLimit({ windowMs: 60000, limit: 4, message: "troppe" }));
const loginLimiter = rateLimit({ windowMs: 60000, limit: 2, message: "calma" });
app.post("/login", loginLimiter, (req, res) => res.status(401).send("no"));
app.get("/tasks", (req, res) => res.json([]));
app.listen(3000);""",
                  ["POST /login", "POST /login", "POST /login", "GET /tasks", "GET /tasks"],
                  ["401 no", "401 no", "429 calma", "200 []", "429 troppe"],
                  [["401 no", "401 no", "429 calma", "200 []", "200 []"],
                   ["401 no", "401 no", "401 no", "200 []", "200 []"],
                   ["401 no", "401 no", "429 calma", "429 troppe", "429 troppe"],
                   ["401 no", "401 no", "429 troppe", "200 []", "200 []"]],
                  applicazione="Express (con `express-rate-limit`)",
                  spiegazione="Il limite generale (4 richieste al minuto per IP) conta **tutte** "
                              "le richieste, login compresi; quello del login (2 al minuto) solo "
                              "le sue. Il terzo login supera il limite del login: `429` con il "
                              "suo messaggio. Il limite generale è a 3: la prima `GET` è la "
                              "quarta richiesta (passa), la seconda la quinta (`429`).",
                  rif=R % "Rate limiting", trabocchetto=True))

d(chiusa("c18-rate-limit-header", CAP, "sicurezza delle API",
         "Quali delle seguenti affermazioni sul rate limiting con `express-rate-limit` "
         "(configurato con `standardHeaders: \"draft-8\"`) sono **vere**?",
         ["Chi supera il limite riceve `429 Too Many Requests`.",
          "La risposta `429` contiene `Retry-After`, che dice quanti secondi aspettare.",
          "L'header `RateLimit` indica quante richieste restano nella finestra."],
         ["Chi supera il limite riceve `403 Forbidden`.",
          "Il limite si applica per utente autenticato, mai per indirizzo IP.",
          "`RateLimit-Policy` contiene l'indirizzo IP del client in chiaro.",
          "Il rate limiting rende superflua l'autenticazione."],
         multi=True,
         spiegazione="Il codice fatto apposta è `429`; `Retry-After` dice quando riprovare, "
                     "`RateLimit` quante richieste restano (`r`) e fra quanto la finestra "
                     "riparte (`t`), `RateLimit-Policy` la regola (quota e finestra) con "
                     "un'impronta del client, non l'IP in chiaro. Il conteggio è per IP (con gli "
                     "IPv6 raggruppati per prefisso).",
         rif=R % "Rate limiting"))

d(chiusa("c18-risorse", CAP, "sicurezza delle API",
         "L'API del capitolo 17 legge la dimensione della pagina da `?size=` senza alcun "
         "massimo. Quale rischio della OWASP API Security Top 10 introduce, e come si corregge?",
         "*Unrestricted Resource Consumption*: con `?size=1000000` un client ottiene tutto in "
         "una volta; si impone un massimo, come `Math.min(Number(req.query.size) || 10, 100)`.",
         ["*Broken Authentication*: si corregge chiedendo di nuovo la password.",
          "*Server-Side Request Forgery*: si corregge validando l'URL.",
          "*Improper Inventory Management*: si corregge documentando `size` in OpenAPI.",
          "Nessuno: la paginazione protegge già da sola dagli abusi."],
         spiegazione="Ogni limite che manca (tempo di esecuzione, richieste per client, memoria, "
                     "dimensione dei file, **elementi per risposta**, spesa per servizi esterni) "
                     "è un'occasione per un attacco DoS o per far salire i costi.",
         rif=R % "Consumo di risorse senza limiti"))

d(uscita_js("c18-ssrf-includes", CAP, "sicurezza delle API",
            """
const ammessi = ["images.example.com"];
const prove = ["https://images.example.com.evil.it/a.jpg",
               "https://evil.it/images.example.com/a.jpg",
               "https://images.example.com/a.jpg"];
for (const u of prove) {
  console.log(u.includes("images.example.com"),
              ammessi.includes(new URL(u).hostname));
}""",
            ["true false", "true false", "true true"],
            [["false false", "false false", "true true"],
             ["true true", "false false", "true true"],
             ["true true", "true true", "true true"],
             ["true false", "false false", "true true"]],
            testo="Un endpoint che scarica immagini da URL ricevuti dal client vuole accettare "
                  "solo il server `images.example.com`. Si confrontano due controlli: «l'URL "
                  "contiene il nome» e «il nome dell'host è nella lista». Che cosa stampa il "
                  "frammento seguente?",
            spiegazione="`includes` sulla stringa dell'URL si aggira facilmente: il nome "
                        "ammesso può comparire come inizio di un dominio dell'attaccante "
                        "(`images.example.com.evil.it`) o nel percorso. Confrontando "
                        "`url.hostname` per intero con una **lista di ammessi** passa solo il "
                        "server giusto. Contro la SSRF servono anche lo schema `https`, nessun "
                        "reindirizzamento seguito (`redirect: \"error\"`) e un timeout.",
            rif=R % "Server-Side Request Forgery", trabocchetto=True))

d(uscita_js("c18-url-schema", CAP, "sicurezza delle API",
            """
const u = new URL("localhost:8080");
console.log(u.protocol, u.hostname === "", u.pathname);""",
            ["localhost: true 8080"],
            [Err("TypeError"), ["http: false /"], ["localhost: false 8080"],
             ["http: true 8080"]],
            testo="Un attaccante invia come URL dell'immagine la stringa `localhost:8080`, senza "
                  "schema. Qual è il risultato dell'esecuzione del frammento seguente?",
            spiegazione="Senza `http://`, `localhost:` viene letto come lo **schema** dell'URL e "
                        "`8080` come il percorso, senza host: per questo `fetch(\"localhost:8080\")` "
                        "fallisce (*unknown scheme*) e l'attacco SSRF richiede l'URL completo, "
                        "`http://localhost:8080/`. Interpretare l'input con `new URL` e "
                        "controllarne le parti è anche il primo passo della difesa.",
            rif=R % "Server-Side Request Forgery", trabocchetto=True))

d(chiusa("c18-ssrf", CAP, "sicurezza delle API",
         "Un endpoint scarica l'immagine del profilo da `req.body.picture_url` con `fetch`, "
         "senza controlli. Che cosa può fare un attaccante?",
         "Far fare al server richieste verso servizi della rete interna, che dall'esterno non "
         "si raggiungono (SSRF).",
         ["Leggere i token degli altri utenti dal loro `localStorage`.",
          "Far eseguire uno script nel browser degli altri utenti.",
          "Superare il rate limiting cambiando indirizzo IP.",
          "Scaricare il codice sorgente del front-end."],
         spiegazione="Il server può raggiungere ciò che il client non vede: servizi su "
                     "`127.0.0.1`, la rete interna, l'indirizzo dei metadati del cloud "
                     "(`169.254.169.254`). Anche i tempi di risposta e i messaggi d'errore "
                     "rivelano quali porte sono aperte.",
         rif=R % "Server-Side Request Forgery"))

d(chiusa("c18-produzione", CAP, "sicurezza delle API",
         "Una rotta Express ha un bug che solleva un `TypeError`, gestito dal gestore degli "
         "errori predefinito. Che cosa cambia avviando il server con `NODE_ENV=production`?",
         "La risposta `500` non contiene più la traccia dell'errore, che resta nel log del "
         "server.",
         ["In produzione l'errore termina il processo del server.",
          "La risposta diventa `400`: in produzione gli errori sono attribuiti al client.",
          "Express smette di registrare l'errore nel log.",
          "L'errore viene ignorato e la rotta risponde `200`."],
         spiegazione="In modalità di sviluppo (quella predefinita) la pagina d'errore mostra la "
                     "traccia completa: file, riga, percorsi, pacchetti, tutte informazioni "
                     "utili a un attaccante. Con `NODE_ENV=production` il corpo dice solo "
                     "*Internal Server Error*; la traccia, che serve a chi corregge il bug, "
                     "finisce in entrambi i casi nel log.",
         rif=R % "Configurazioni insicure"))

d(chiusa("c18-errori", CAP, "sicurezza delle API",
         "Quali delle seguenti pratiche sulle risposte di errore di una API sono corrette?",
         ["Usare un solo formato per tutti gli errori dell'API.",
          "Trasformare i bug in un `500` generico, lasciando i dettagli nel log.",
          "Restituire al client gli errori previsti (per esempio di validazione) con il "
          "codice e i dettagli utili."],
         ["Inserire nel corpo il nome della classe e la riga in cui è avvenuto l'errore.",
          "Rispondere `200` con un campo `error` nel corpo, per non allarmare i client.",
          "Cambiare formato a seconda dell'endpoint, per descrivere meglio ogni errore.",
          "Includere la traccia dello stack, che aiuta i client a segnalare il problema."],
         multi=True,
         spiegazione="Gli errori fanno parte del contratto: prevedibili, coerenti, sempre nello "
                     "stesso formato (esiste anche uno standard, i *Problem Details* della RFC "
                     "9457), e con il codice di stato giusto. I dettagli interni "
                     "(`NullPointerException at TaskService.java:47`) non devono mai trapelare.",
         rif=R % "Le risposte di errore"))

# ----------------------------------------------------------------------
# Osservabilità
d(chiusa("c18-health", CAP, "osservabilità",
         "Il controllo di salute `GET /health` scopre che il database non risponde. Come "
         "dovrebbe rispondere, secondo il capitolo?",
         "Con `503 Service Unavailable`, e il motivo preciso nel log.",
         ["Con `200` e `\"status\": \"error\"` nel corpo.",
          "Con `500 Internal Server Error`, lasciando passare l'eccezione.",
          "Con `404 Not Found`, perché il database non c'è.",
          "Con `401 Unauthorized`, perché il database ha rifiutato le credenziali."],
         spiegazione="Un sistema di monitoraggio o un bilanciatore di carico interroga "
                     "`/health` ogni pochi secondi e guarda il codice di stato: `503` dice "
                     "esattamente che il servizio non è disponibile, mentre un `500` qualunque "
                     "sembra un bug. Un `200` con un errore nel corpo verrebbe preso per buono.",
         rif=R % "Il controllo in Express", trabocchetto=True))

d(chiusa("c18-health-sqlite", CAP, "osservabilità",
         "Per provare il controllo di salute con un guasto, si configura Sequelize con un "
         "database SQLite in una cartella inesistente (`sqlite:/non/esiste/database.db`). Che "
         "cosa risponde `/health`?",
         "`200` con `database: \"ok\"`: Sequelize crea file e cartelle, e la query riesce su un "
         "database nuovo e vuoto.",
         ["`503`: la cartella del database non esiste.",
          "`500`: l'eccezione non viene intercettata.",
          "`404`: il file del database non esiste.",
          "Il server non parte."],
         spiegazione="Un controllo di salute verifica solo quello che controlla davvero: qui "
                     "che il database **risponda** a `SELECT 1`, non che sia quello giusto. Per "
                     "simulare il guasto serve un database che davvero non risponde, come un "
                     "PostgreSQL spento (`ECONNREFUSED`).",
         rif=R % "Il controllo in Express", trabocchetto=True))

d(chiusa("c18-log", CAP, "osservabilità",
         "Quali delle seguenti informazioni **non** vanno registrate nel log di una API?",
         ["Le password e i token.",
          "Gli header `Authorization` completi.",
          "I corpi completi delle richieste, per impostazione predefinita."],
         ["I fallimenti dell'autenticazione e dell'autorizzazione.",
          "Le violazioni dei limiti di richieste.",
          "L'uso delle versioni deprecate dell'API.",
          "Gli errori inattesi del server."],
         multi=True,
         spiegazione="I log sono strumenti operativi ma anche un rischio: vengono copiati, "
                     "conservati a lungo e letti da molti. Vanno registrati gli eventi utili "
                     "(fallimenti di accesso, limiti superati, uso di API deprecate, errori, "
                     "azioni degli amministratori), non i segreti né i dati personali; il corpo "
                     "di `POST /auth`, per esempio, contiene una password.",
         rif=R % "Il log"))

d(chiusa("c18-token-query", CAP, "osservabilità",
         "Perché è meglio inviare il token nell'header `Authorization` piuttosto che nella "
         "query string, come `GET /todos?token=...`?",
         "Perché il log (il formato `dev` di morgan, per esempio) registra l'URL completo, "
         "query compresa: il token finirebbe nei log.",
         ["Perché la query string non può contenere punti.",
          "Perché `jwt.verify` accetta solo token letti dagli header.",
          "Perché con HTTPS la query string viaggia in chiaro.",
          "Perché i token nella query string scadono prima."],
         spiegazione="morgan nel formato `dev` registra metodo, URL, stato e tempo: niente header "
                     "né corpi, ma l'URL sì, query compresa. Con HTTPS anche la query è cifrata "
                     "in rete: il problema è dove l'URL viene scritto dopo (log, cronologia, "
                     "intestazione `Referer`).",
         rif=R % "Il log", trabocchetto=True))

d(chiusa("c18-openapi-struttura", CAP, "OpenAPI",
         "In una specifica OpenAPI 3, quali delle seguenti affermazioni sono **vere**?",
         ["Le chiavi principali sono `openapi`, `info` e `paths`.",
          "Ogni path elenca i metodi supportati, e ciascuno descrive parametri, corpo della "
          "richiesta e risposte.",
          "Le chiavi delle risposte sono i codici di stato, fra virgolette."],
         ["Il tipo del contenuto si dichiara con la chiave `produces` di ogni operazione.",
          "In una specifica JSON si possono usare commenti con `//`.",
          "Una specifica descrive solo gli endpoint `GET`.",
          "Le risposte si elencano per nome, non per codice di stato."],
         multi=True,
         spiegazione="La struttura scende per livelli: OpenAPI Object → Paths → Path Item (i "
                     "metodi) → Operation (parametri, `requestBody`, `responses`) → Responses "
                     "(una per codice, fra virgolette per la compatibilità fra JSON e YAML). "
                     "`produces` è di Swagger 2.0: in OpenAPI 3 il tipo sta sotto `content`. "
                     "JSON non ha commenti.",
         rif=R % "Com'è fatta una specifica"))

# ----------------------------------------------------------------------
# Domande aperte
d(aperta("c18-a-versioni", CAP, "evoluzione e versionamento",
         "Che cos'è una *breaking change*? Si descrivano le principali strategie di "
         "versionamento di una API, con pro e contro, e si dica quando conviene creare una "
         "nuova versione.",
         ["L'API è un contratto (percorsi, formati, codici, errori, autenticazione); una "
          "breaking change rompe i client esistenti (rinominare/togliere campi, cambiare tipi, "
          "codici o formato degli errori).",
          "Versione nell'URI (`/api/v1/...`): immediata da provare, documentare e instradare; "
          "un po' di duplicazione.",
          "Versione in un header (`X-API-Version`, o `Accept` con un tipo `vnd.`): URI unica, "
          "serve `Vary: Accept` per le cache.",
          "Versionare solo per le modifiche che rompono: aggiungere senza versione, togliere o "
          "ridefinire con una versione nuova."],
         rif=R % "Versionare"))

d(aperta("c18-a-deprecazione", CAP, "evoluzione e versionamento",
         "Si descriva il ciclo di vita di una versione di una API e come lo si comunica ai "
         "client.",
         ["Fasi: active, deprecated (funziona ma si invita a migrare), sunset (data di "
          "rimozione annunciata), removed.",
          "Non rompere i client in silenzio: avvisarli per tempo.",
          "Header: `Deprecation` (dalla RFC 9745 una data, `@` e i secondi dal 1970), `Sunset` "
          "(la data di dismissione, non prima della deprecazione), `Link` con "
          "`rel=\"deprecation\"`.",
          "Un client ben scritto registra questi header; il log dell'API mostra chi usa ancora "
          "la versione vecchia."],
         rif=R % "Deprecazione e dismissione"))

d(aperta("c18-a-rate-limiting", CAP, "sicurezza delle API",
         "Che cos'è il rate limiting di una API? A che cosa serve, come si realizza in Express "
         "e quali codici di stato e header sono coinvolti?",
         ["Limite al numero di richieste per client (per IP o utente, per funzionalità) "
          "nell'unità di tempo.",
          "Serve contro gli abusi e i tentativi di password a raffica, per i costi, per l'uso "
          "equo e contro i sovraccarichi accidentali.",
          "In Express: il middleware `express-rate-limit` (`windowMs`, `limit`), generale e più "
          "stretto sul login.",
          "Superato il limite: `429 Too Many Requests` con `Retry-After`; header `RateLimit` e "
          "`RateLimit-Policy`."],
         rif=R % "Rate limiting"))

d(aperta("c18-a-bola", CAP, "sicurezza delle API",
         "Che cos'è la *Broken Object Level Authorization*? Se ne mostri un esempio in una API "
         "REST e si descrivano le contromisure.",
         ["Primo rischio della OWASP API Security Top 10: si accede agli oggetti altrui "
          "cambiando un identificatore (`GET /todos/1` di un altro utente).",
          "Nasce dall'affidarsi alla sola autenticazione («ha un token valido, quindi può»).",
          "Contromisure: un middleware che verifica il proprietario (`403`), o meglio cercare "
          "l'oggetto fra quelli dell'utente (proprietario nella query, `404` per gli altri).",
          "Identificatori consecutivi rendono l'attacco banale; le risposte non devono rivelare "
          "quali identificatori esistono."],
         rif=R % "Autorizzazione a livello di oggetto"))

d(aperta("c18-a-osservabilita", CAP, "osservabilità",
         "Che cosa si intende per osservabilità di una API in produzione? Si descrivano un "
         "controllo di salute e le buone pratiche per i log.",
         ["Sapere (automaticamente) se l'API è in esecuzione, se il database risponde, quante "
          "richieste falliscono, quali endpoint sono lenti, se scattano i limiti, chi usa le "
          "versioni vecchie.",
          "Controllo di salute: `/health` che verifica davvero le dipendenze (`SELECT 1`), "
          "risponde `200` o `503` (Spring Boot Actuator lo offre già).",
          "Log: fallimenti di accesso, limiti superati, errori, uso di API deprecate, azioni "
          "degli amministratori.",
          "Mai password, token, header `Authorization`, dati personali, corpi completi."],
         rif=R % "Osservabilità"))

d(aperta("c18-a-errori", CAP, "sicurezza delle API",
         "Perché le risposte di errore fanno parte del contratto di una API? Come vanno "
         "progettate e che cosa non devono contenere? Come si realizza in Express?",
         ["I client devono poter gestire gli errori senza indovinare: formato unico e codici "
          "di stato corretti (es. `{error, message, details}`, o i Problem Details, RFC 9457).",
          "Mai dettagli interni: tracce, nomi di classi e file, righe di codice.",
          "In Express: una classe per gli errori previsti (con stato e codice) e un gestore "
          "degli errori a quattro parametri che li restituisce; i bug diventano un `500` "
          "generico e i dettagli vanno nel log.",
          "In produzione `NODE_ENV=production` (o `DEBUG = False` in Django)."],
         rif=R % "Le risposte di errore"))
