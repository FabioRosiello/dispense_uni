"""Capitolo 13: gestione delle sessioni (tracciamento della sessione, stato
nei cookie e suoi problemi, sessioni web, implementazione da zero)."""

from generatore import L, aperta, chiusa, risposte_server, uscita_js

CAP = 13
R = "cap. 13, «%s»"

DOMANDE = []
d = DOMANDE.append

LETTURA_COOKIE = """
function cookie(request) {
  const lista = {};
  for (const c of (request.headers.cookie || "").split(";")) {
    const [nome, valore] = c.trim().split("=");
    if (nome) lista[nome] = valore;
  }
  return lista;
}
"""

# ----------------------------------------------------------------------
d(risposte_server("c13-fiducia-cookie", CAP, "lo stato nei cookie",
                  'import http from "http";\n' + LETTURA_COOKIE + """
http.createServer((request, response) => {
  const c = cookie(request);
  if (c.auth === "true") {
    response.writeHead(200);
    response.end("Lista di " + c.username);
  } else {
    response.writeHead(401);
    response.end("Non autorizzato");
  }
}).listen(3000);""",
                  ["GET /todo",
                   {"percorso": "/todo", "intestazioni": {"Cookie": "auth=true; username=bob"}},
                   {"percorso": "/todo", "intestazioni": {"Cookie": "username=luigi"}}],
                  ["401 Non autorizzato", "200 Lista di bob", "401 Non autorizzato"],
                  [["401 Non autorizzato", "401 Non autorizzato", "401 Non autorizzato"],
                   ["401 Non autorizzato", "401 Non autorizzato", "200 Lista di luigi"],
                   ["200 Lista di undefined", "200 Lista di bob", "200 Lista di luigi"],
                   ["401 Non autorizzato", "200 Lista di bob", "200 Lista di luigi"],
                   ["401 Non autorizzato", "403 Forbidden", "401 Non autorizzato"]],
                  testo="Si consideri la seguente applicazione Node.js, in ascolto sulla porta "
                        "3000, che memorizza lo stato di autenticazione nei cookie. Nessuno ha "
                        "mai effettuato il login. Quali risposte (codice di stato e corpo) "
                        "ottengono, nell'ordine, le richieste `GET /todo` (senza cookie), "
                        "`GET /todo` con l'header `Cookie: auth=true; username=bob` e "
                        "`GET /todo` con l'header `Cookie: username=luigi`?",
                  spiegazione="Il server si fida di ciò che il browser gli rimanda: chiunque può "
                              "impostarsi da solo i cookie `auth=true` e `username=bob` (bastano "
                              "i DevTools) e ottenere la lista di bob **senza mai passare dal "
                              "login**. È il difetto critico dell'approccio a cookie: i dati "
                              "sono interamente controllati dal client.",
                  rif=R % "I problemi dell'approccio a cookie"))

d(risposte_server("c13-sessione-server", CAP, "sessioni web",
                  """
import http from "http";

const sessioni = new Map();       // la sessione creata da un login di luigi
sessioni.set("9b1d6bcd-bbfd", new Map([["username", "luigi"]]));

function sessionId(request) {
  const m = (request.headers.cookie || "").match(/sessionId=([^;]+)/);
  return m ? m[1] : undefined;
}

http.createServer((request, response) => {
  const sessione = sessioni.get(sessionId(request));
  if (sessione) {
    response.writeHead(200);
    response.end("Lista di " + sessione.get("username"));
  } else {
    response.writeHead(401);
    response.end("Non autorizzato");
  }
}).listen(3000);""",
                  [{"percorso": "/todo", "intestazioni": {"Cookie": "sessionId=9b1d6bcd-bbfd"}},
                   {"percorso": "/todo", "intestazioni": {"Cookie": "auth=true; username=bob"}},
                   {"percorso": "/todo", "intestazioni": {"Cookie": "sessionId=42"}}],
                  ["200 Lista di luigi", "401 Non autorizzato", "401 Non autorizzato"],
                  [["200 Lista di luigi", "200 Lista di bob", "401 Non autorizzato"],
                   ["200 Lista di luigi", "200 Lista di bob", "200 Lista di luigi"],
                   ["200 Lista di luigi", "401 Non autorizzato", "200 Lista di undefined"],
                   ["401 Non autorizzato", "401 Non autorizzato", "401 Non autorizzato"],
                   ["200 Lista di 9b1d6bcd-bbfd", "401 Non autorizzato", "401 Non autorizzato"]],
                  testo="Si consideri la seguente applicazione Node.js, in ascolto sulla porta "
                        "3000, che conserva le sessioni sul server. Quali risposte (codice di "
                        "stato e corpo) ottengono, nell'ordine, tre richieste `GET /todo` con "
                        "gli header `Cookie: sessionId=9b1d6bcd-bbfd`, `Cookie: auth=true; "
                        "username=bob` e `Cookie: sessionId=42`?",
                  spiegazione="Con le sessioni i dati restano sul server: il client possiede solo "
                              "un identificatore opaco. Un cookie `username` inventato non conta "
                              "nulla, e un identificatore che non corrisponde a una sessione "
                              "esistente non trova alcun dato (`get` restituisce `undefined`).",
                  rif=R % "Implementare le sessioni da zero"))

d(uscita_js("c13-cookie-parse", CAP, "lo stato nei cookie",
            """
function parseCookies(header) {
  const list = {};
  header.split(";").forEach((cookie) => {
    let [name, ...rest] = cookie.split("=");
    name = name.trim();
    const value = rest.join("=").trim();
    if (!name || !value) return;
    list[name] = decodeURIComponent(value);
  });
  return list;
}
const c = parseCookies("auth=true; username=luigi; tema=a=b; vuoto=");
console.log(Object.keys(c).length, c.username, c.tema, typeof c.auth);""",
            ["3 luigi a=b string"],
            [["4 luigi a=b string"], ["3 luigi a string"], ["3 luigi a=b boolean"],
             ["4 luigi a boolean"], ["3 luigi b string"]],
            spiegazione="L'header `Cookie` contiene coppie `nome=valore` separate da `;`. Il cookie "
                        "`vuoto` non ha valore e viene scartato. Ricomponendo con `join(\"=\")` "
                        "tutto ciò che segue il primo `=`, il valore di `tema` resta `a=b`. I "
                        "valori dei cookie sono stringhe: `auth` vale `\"true\"`, non il booleano "
                        "`true`.",
            rif=R % "Recuperare le informazioni di sessione"))

# ----------------------------------------------------------------------
d(chiusa("c13-tracciamento", CAP, "sessioni web",
         "Perché un'applicazione web ha bisogno di un meccanismo di *tracciamento della "
         "sessione*?",
         "Perché HTTP è *stateless*: una richiesta non contiene informazioni sulle precedenti, e "
         "il server non saprebbe, per esempio, che l'utente ha già effettuato il login.",
         ["Perché HTTP chiude la connessione TCP dopo ogni risposta.",
          "Perché i browser non possono inviare due richieste allo stesso server.",
          "Perché senza sessione le risposte non possono essere cifrate.",
          "Perché il DNS deve sapere quale utente sta usando il sito.",
          "Perché HTTP/1.1 non permette di inviare form con il metodo `POST`."],
         spiegazione="Il tracciamento della sessione mantiene informazioni con stato sulle "
                     "interazioni di un utente attraverso più richieste HTTP, così il server può "
                     "riconoscerlo e adattare le risposte.",
         rif=R % "Il problema"))

d(chiusa("c13-set-cookie", CAP, "lo stato nei cookie",
         "Dopo il login, il server risponde con la risposta seguente. Che cosa fa il browser?",
         "Memorizza due cookie distinti, validi per un'ora, poi segue il reindirizzamento con una "
         "`GET /` che li include nell'header `Cookie`.",
         ["Memorizza un solo cookie, perché ogni risposta può impostarne uno.",
          "Ignora i cookie, perché una risposta `302` non può impostarne.",
          "Memorizza i cookie per 3600 giorni.",
          "Rimanda subito i cookie al server con una `POST /`.",
          "Mostra all'utente una pagina con i cookie ricevuti."],
         codice=L("http", """
HTTP/1.1 302 Found
Location: /
Set-Cookie: auth=true; max-age=3600
Set-Cookie: username=luigi; max-age=3600"""),
         spiegazione="Ogni header `Set-Cookie` imposta un cookie (`max-age` è in secondi: 3600 è "
                     "un'ora). Il browser memorizza i cookie qualunque sia il codice di stato, "
                     "poi segue il `Location` con una `GET` e li allega, come a ogni richiesta "
                     "successiva allo stesso sito. Il reindirizzamento dopo la `POST` di login "
                     "evita di reinviare le credenziali aggiornando la pagina.",
         rif=R % "Gestire il login"))

d(chiusa("c13-problemi-cookie", CAP, "lo stato nei cookie",
         "Un'applicazione memorizza nei cookie `auth=true` e `username=luigi` dopo il login, e "
         "controlla quei cookie a ogni richiesta. Quali delle seguenti affermazioni sono "
         "**vere**?",
         ["Un utente può impostarsi da solo `auth=true` senza mai passare dal login.",
          "Un utente può cambiare `username` e farsi riconoscere come un altro utente.",
          "Con i cookie firmati dal server la manomissione si riconosce, ma i dati restano sul "
          "client.",
          "I browser limitano la dimensione e il numero dei cookie per dominio."],
         ["I cookie non sono modificabili, perché li ha impostati il server.",
          "Il problema si risolve rendendo i valori più lunghi.",
          "I cookie possono contenere una quantità illimitata di dati.",
          "Il browser invia i cookie solo alla pagina di login.",
          "Il problema riguarda solo i cookie impostati da JavaScript."],
         multi=True,
         spiegazione="I cookie sono interamente controllati dal client: dai DevTools si leggono e "
                     "si modificano con un doppio clic. In più sono limitati (di solito 4096 byte "
                     "ciascuno, da 20 a 50 per dominio). La soluzione sono le sessioni: i dati "
                     "restano sul server, il cookie porta solo un identificatore.",
         rif=R % "I problemi dell'approccio a cookie"))

d(chiusa("c13-sessione", CAP, "sessioni web",
         "Quali delle seguenti affermazioni sulle sessioni web sono **vere**?",
         ["I dati della sessione sono conservati sul server.",
          "Il client riceve solo un identificatore di sessione, di solito in un cookie.",
          "Uno stesso utente può avere più sessioni, per esempio da due browser diversi.",
          "Un identificatore che non corrisponde a una sessione esistente non dà accesso a "
          "nessun dato."],
         ["Il browser conserva in un cookie tutti i dati della sessione, cifrati.",
          "L'identificatore di sessione può essere un contatore, perché il server lo controlla.",
          "Le sessioni rendono HTTP un protocollo con stato.",
          "Per ogni sessione il server apre una connessione TCP dedicata che resta aperta.",
          "Ogni utente può avere una sola sessione alla volta."],
         multi=True,
         spiegazione="Una sessione è una struttura di coppie chiave-valore gestita sul server e "
                     "identificata da un token univoco e imprevedibile, passato al client come "
                     "cookie. HTTP resta *stateless*: è l'applicazione a ricollegare le richieste "
                     "alla sessione. Ogni login crea una sessione nuova.",
         rif=R % "Le sessioni web"))

d(chiusa("c13-id", CAP, "sessioni web",
         "Perché l'identificatore di sessione va generato con un generatore crittograficamente "
         "sicuro, come `randomUUID` del modulo `crypto`, e non con un contatore o con "
         "`Math.random()`?",
         "Perché chi conosce un identificatore valido è, per il server, il proprietario della "
         "sessione: un identificatore prevedibile si indovina, e permette di rubare la sessione "
         "di un altro.",
         ["Perché un contatore non può essere memorizzato in un cookie.",
          "Perché `Math.random()` restituisce numeri troppo lunghi per un cookie.",
          "Perché `randomUUID` cifra i dati della sessione.",
          "Perché un identificatore casuale rende la sessione più veloce da trovare nella "
          "`Map`.",
          "Perché i browser rifiutano i cookie con valori numerici."],
         spiegazione="Con identificatori progressivi basterebbe provare il valore successivo. "
                     "`Math.random()` non è pensato per la sicurezza; `randomUUID` produce 122 bit "
                     "casuali, e indovinarne uno valido è praticamente impossibile.",
         rif=R % "Implementare le sessioni da zero"))

d(chiusa("c13-memoria", CAP, "sessioni web",
         "Un'applicazione conserva le sessioni in una `Map` in memoria. Quali problemi può avere "
         "in produzione?",
         ["Al riavvio del server tutte le sessioni spariscono, e gli utenti devono rifare il "
          "login.",
          "Con più macchine dietro un bilanciatore di carico, una richiesta servita da una "
          "macchina non trova la sessione creata su un'altra."],
         ["I dati della sessione diventano visibili al client.",
          "Una `Map` non può contenere più di 20 sessioni.",
          "Le sessioni scadono dopo ogni richiesta.",
          "Gli utenti possono modificare i dati della sessione dai DevTools."],
         multi=True, quante_giuste=(1, 2),
         spiegazione="La memoria del processo non sopravvive ai riavvii e non è condivisa fra "
                     "più macchine. In produzione le sessioni si conservano in un archivio "
                     "condiviso (Redis, un database), oppure si usano token autoconsistenti e "
                     "firmati.",
         rif=R % "Usare le sessioni"))

d(chiusa("c13-altri-metodi", CAP, "sessioni web",
         "Oltre ai cookie, con quali altri metodi si può trasmettere l'identificatore di "
         "sessione?",
         ["Con l'*URL rewriting*: l'identificatore viene aggiunto a ogni URL come parametro.",
          "Con campi nascosti nei form, inviati insieme agli altri dati."],
         ["Nell'header `Host` della richiesta.",
          "Nel codice di stato della risposta.",
          "Nell'indirizzo IP del client.",
          "Nel nome del file HTML richiesto."],
         multi=True, quante_giuste=(1, 2),
         spiegazione="I cookie sono l'approccio più diffuso. URL rewriting e campi nascosti "
                     "funzionano anche senza cookie, ma espongono l'identificatore in luoghi "
                     "(URL, log, link condivisi) dove è facile che venga copiato.",
         rif=R % "Altri metodi di tracciamento"))

# ----------------------------------------------------------------------
# Domande aperte
d(aperta("c13-a-sessioni", CAP, "sessioni web",
         "Si spieghi il problema del tracciamento della sessione in HTTP e si confrontino "
         "l'approccio che memorizza lo stato nei cookie e quello basato sulle sessioni web.",
         ["HTTP è *stateless*: per riconoscere un utente fra più richieste (es. dopo il login) "
          "serve uno stato mantenuto dall'applicazione.",
          "Stato nei cookie (`Set-Cookie: auth=true`, `username=...`): semplice, ma i cookie "
          "sono controllati dal client e si manomettono facilmente; limiti di dimensione e "
          "numero. I cookie firmati riconoscono la manomissione ma lasciano i dati al client.",
          "Sessioni: i dati restano sul server, in una struttura chiave-valore; il client "
          "riceve solo un identificatore opaco (di solito un cookie) che il server usa per "
          "ritrovarli.",
          "L'identificatore deve essere imprevedibile (generatore crittograficamente sicuro): "
          "chi lo conosce è il proprietario della sessione."],
         rif=R % "Le sessioni web"))

d(aperta("c13-a-implementazione", CAP, "sessioni web",
         "Si descriva come implementare da zero un meccanismo di sessione in Node.js: strutture "
         "dati, che cosa avviene al login e a ogni richiesta successiva, e quali accorgimenti "
         "servono in produzione.",
         ["Una `Map` dagli identificatori alle sessioni, ciascuna a sua volta una `Map` di "
          "coppie chiave-valore.",
          "Al login: si crea una sessione con un identificatore casuale (`randomUUID`), vi si "
          "salvano i dati (es. `username`) e si invia l'identificatore con `Set-Cookie`, di "
          "solito con un reindirizzamento.",
          "A ogni richiesta: si legge il cookie dall'header `Cookie`, si cerca la sessione; se "
          "non esiste l'utente non è autenticato (`401` o reindirizzamento al login).",
          "In produzione: sessioni in un archivio condiviso (Redis, database), che sopravvive ai "
          "riavvii ed è comune a più macchine; scadenza delle sessioni."],
         rif=R % "Implementare le sessioni da zero"))

d(aperta("c13-a-cookie-login", CAP, "lo stato nei cookie",
         "Un'applicazione memorizza lo stato nei cookie `auth` e `username`. Si descriva quali "
         "header si scambiano browser e server al login e nelle richieste successive, e si "
         "spieghi perché questo approccio non è sicuro.",
         ["Il form invia le credenziali con una `POST`; se sono giuste il server risponde con "
          "un reindirizzamento (`302 Found`, `Location: /`) e due header `Set-Cookie` "
          "(`auth=true; max-age=3600` e `username=luigi; max-age=3600`), altrimenti "
          "ripropone il login con `401`.",
          "Il browser memorizza i cookie e da quel momento li allega a ogni richiesta allo "
          "stesso sito in un unico header `Cookie: auth=true; username=luigi`, che il server "
          "deve analizzare (coppie separate da `;`, nome e valore da `=`).",
          "Le pagine protette controllano `auth`: se manca rispondono `401` o reindirizzano al "
          "login.",
          "I cookie sono controllati dal client: con i DevTools si cambia `username` o ci si "
          "imposta `auth=true` senza login. I cookie firmati rivelano la manomissione, ma i "
          "dati restano sul client: la soluzione sono le sessioni web."],
         rif="cap. 13, «Un approccio ingenuo: i cookie» e «I problemi dell'approccio a "
             "cookie»"))
