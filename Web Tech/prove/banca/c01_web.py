"""Capitolo 1: Introduzione al Web (Internet e Web, HTTP, URL, messaggi, stato)."""

from urllib.parse import urlsplit

from generatore import aperta, chiusa, famiglia

CAP = 1
R = "cap. 1, «%s»"

DOMANDE = []
d = DOMANDE.append

# ----------------------------------------------------------------------
# Codici di stato: le classi
CLASSI = {
    "1xx": "Risposta informativa: la richiesta è stata ricevuta e l'elaborazione continua.",
    "2xx": "La richiesta è stata ricevuta, compresa e soddisfatta con successo.",
    "3xx": "Reindirizzamento: per completare la richiesta servono ulteriori azioni del client.",
    "4xx": "Errore nella richiesta.",
    "5xx": "Errore nel processamento della richiesta.",
}
ALTRE = [
    "Errore nella trasmissione dei dati.",
    "Errore nella connessione.",
    "Errore nella risoluzione del nome di dominio.",
    "La risorsa è stata trovata nella cache del browser.",
]


@famiglia("c01-classi-stato", CAP, "codici di stato: le classi", varianti=4)
def _classi(rng):
    classe = rng.choice(["2xx", "3xx", "4xx", "4xx", "5xx", "5xx"])
    giusta = CLASSI[classe]
    sbagliate = [v for k, v in CLASSI.items() if k != classe] + ALTRE
    return chiusa(
        "c01-classi-stato", CAP, "codici di stato: le classi",
        "Qual è il significato degli status code della famiglia `%s` di HTTP?" % (classe[0] + "00"),
        giusta, sbagliate, n=4,
        spiegazione="La prima cifra del codice identifica la classe: 1xx informativi, 2xx "
                    "successo, 3xx reindirizzamento, 4xx errore del client (la richiesta è "
                    "sbagliata: ripeterla identica non serve), 5xx errore del server (la "
                    "richiesta era plausibile ma il server non è riuscito a elaborarla). "
                    "Problemi di connessione o di trasmissione non producono alcun codice: "
                    "la risposta non arriva proprio.",
        rif=R % "Codici di stato della risposta")


DOMANDE.append(_classi)

CODICI = [
    ("200", "La richiesta è andata a buon fine (`OK`)."),
    ("201", "È stata creata una nuova risorsa (`Created`)."),
    ("204", "La richiesta è andata a buon fine e la risposta non ha corpo (`No Content`)."),
    ("301", "La risorsa si è spostata in modo permanente a un altro indirizzo."),
    ("302", "La risorsa si trova temporaneamente a un altro indirizzo."),
    ("304", "La copia in cache del client è ancora valida (`Not Modified`)."),
    ("400", "La richiesta è malformata (`Bad Request`)."),
    ("401", "Manca l'autenticazione, o non è valida (`Unauthorized`)."),
    ("403", "Il client è identificato ma non ha i permessi (`Forbidden`)."),
    ("404", "La risorsa richiesta non esiste (`Not Found`)."),
    ("405", "Il metodo non è ammesso per quella risorsa (`Method Not Allowed`)."),
    ("500", "Si è verificato un errore interno del server (`Internal Server Error`)."),
    ("503", "Il server è momentaneamente non disponibile (`Service Unavailable`)."),
]


@famiglia("c01-codice", CAP, "codici di stato: i singoli codici", varianti=5)
def _codice(rng):
    codice, significato = rng.choice(CODICI)
    altri = [s for c, s in CODICI if c != codice and c[0] != codice[0]]
    vicini = [s for c, s in CODICI if c != codice and c[0] == codice[0]]
    sbagliate = vicini + rng.sample(altri, 4)
    return chiusa(
        "c01-codice", CAP, "codici di stato: i singoli codici",
        "Che cosa indica il codice di stato `%s` in una risposta HTTP?" % codice,
        significato, sbagliate, n=4,
        spiegazione="`%s` appartiene alla classe %sxx. Promemoria: 200 OK, 201 Created, 204 "
                    "No Content; 301 spostamento permanente, 302 temporaneo, 304 «la tua "
                    "copia in cache va ancora bene»; 400 richiesta malformata, 401 «non so "
                    "chi sei», 403 «so chi sei, ma non puoi», 404 risorsa inesistente, 405 "
                    "metodo non ammesso; 500 errore interno, 503 server non disponibile."
                    % (codice, codice[0]),
        rif="cap. 1, «Codici di stato della risposta»; cap. 9, «La risposta»")


DOMANDE.append(_codice)

# ----------------------------------------------------------------------
# Le parti di una URL
URL_PROVA = [
    "https://www.example.org/corsi/web/index.html?anno=2025&lingua=it#programma",
    "http://localhost:3000/todo/12?modifica=true",
    "https://docenti.unina.it:8443/didattica/esami.php?corso=TW#appelli",
    "http://www.example.com/cerca?q=css+grid&pagina=2",
    "https://api.example.net/v2/utenti/42/preferiti",
    "http://192.168.1.10:8080/admin/login.html#form",
    "https://www.unina.it/ateneo/organizzazione",
]
PARTI = ["schema", "host", "porta", "percorso", "query", "ancora"]


def _parti(url):
    p = urlsplit(url)
    porta = str(p.port) if p.port else ("443" if p.scheme == "https" else "80")
    return {"schema": p.scheme, "host": p.hostname, "porta": porta, "percorso": p.path,
            "query": p.query or "(nessuna)", "ancora": p.fragment or "(nessuna)"}


@famiglia("c01-url", CAP, "anatomia di una URL", varianti=4)
def _url(rng):
    url = rng.choice(URL_PROVA)
    parti = _parti(url)
    parte = rng.choice(PARTI)
    domande = {
        "schema": "Qual è lo **schema** della URL `%s`?",
        "host": "Qual è il **nome dell'host** (dominio) nella URL `%s`?",
        "porta": "A quale **porta** del server si collega il browser per la URL `%s`?",
        "percorso": "Qual è il **percorso** della risorsa nella URL `%s`?",
        "query": "Qual è la **stringa di query** della URL `%s`?",
        "ancora": "Qual è l'**ancora** (frammento) della URL `%s`?",
    }
    giusta = parti[parte]
    candidati = set(v for v in parti.values()) | {"80", "443", "8080", "3000", "/", "http",
                                                   "https", "(nessuna)"}
    if parte == "porta":
        candidati |= {"80", "443", "21", "8443", "3000"}
    if parte in ("percorso", "query"):
        p = urlsplit(url)
        candidati |= {p.path.rsplit("/", 1)[-1] or "/", p.path + "?" + p.query if p.query else
                      p.path + "/", (p.hostname or "") + p.path}
    sbagliate = sorted(c for c in candidati if c != giusta and c)
    rng.shuffle(sbagliate)
    fmt = lambda v: v if v == "(nessuna)" else "`%s`" % v
    spiegazioni = {
        "schema": "Lo schema è la parte prima di `://` e dice quale protocollo usare.",
        "host": "Il nome dell'host sta fra `://` e la porta (o la prima `/`).",
        "porta": "Se la porta non è scritta si usa quella predefinita dello schema: 80 per "
                 "`http`, 443 per `https`. Una porta esplicita segue i due punti dopo l'host.",
        "percorso": "Il percorso va dalla prima `/` dopo l'host fino a `?` o `#` (esclusi).",
        "query": "La query è ciò che segue `?`, fino a `#`: coppie `chiave=valore` separate "
                 "da `&`.",
        "ancora": "L'ancora è ciò che segue `#`; non viene inviata al server, la usa il "
                  "browser per scorrere fino al punto indicato.",
    }
    return chiusa(
        "c01-url", CAP, "anatomia di una URL", domande[parte] % url,
        fmt(giusta), [fmt(s) for s in sbagliate[:5]], n=4,
        spiegazione="Scomposta, la URL ha schema `%s`, host `%s`, porta %s, percorso `%s`, "
                    "query %s e ancora %s. %s" % (
                        parti["schema"], parti["host"], parti["porta"], parti["percorso"],
                        fmt(parti["query"]), fmt(parti["ancora"]), spiegazioni[parte]),
        rif=R % "URL: individuare una risorsa",
        verifica=dict(tipo="node", strict=True, codice=(
            "const u = new URL(%r);\n"
            "const porta = u.port || (u.protocol === 'https:' ? '443' : '80');\n"
            "console.log([u.protocol.slice(0, -1), u.hostname, porta, u.pathname,\n"
            "  u.search.slice(1) || '(nessuna)', u.hash.slice(1) || '(nessuna)'].join(' | '));"
            % url).replace("'", '"'),
            righe=[" | ".join(parti[p] for p in PARTI)], errore=None))


DOMANDE.append(_url)

# ----------------------------------------------------------------------
d(chiusa("c01-internet-web", CAP, "Internet e il Web",
         "Quali delle seguenti affermazioni su Internet e il World Wide Web sono **vere**?",
         ["Il Web è un servizio che funziona *sopra* Internet, insieme ad altri (posta "
          "elettronica, trasferimento di file, ...).",
          "Internet è la rete di reti che collega i dispositivi; il Web è un insieme di "
          "documenti ipertestuali collegati fra loro.",
          "Le risorse del Web sono identificate da URL e trasferite con il protocollo HTTP."],
         ["Internet e il World Wide Web sono due nomi della stessa cosa.",
          "Il Web esisteva prima di Internet, che ne è un'estensione.",
          "La posta elettronica è una parte del World Wide Web.",
          "Il Web usa un protocollo di rete alternativo a TCP/IP.",
          "Un documento è nel Web solo se è scritto in HTML5."],
         multi=True,
         spiegazione="Internet è l'infrastruttura (la rete di reti basata su TCP/IP); il World "
                     "Wide Web è uno dei servizi che la usano: documenti ipertestuali "
                     "identificati da URL e trasferiti con HTTP. Anche la posta elettronica "
                     "usa Internet, ma non fa parte del Web.",
         rif=R % "Internet e il World Wide Web"))

d(chiusa("c01-ipertesto", CAP, "ipertesti",
         "Che cos'è un **ipertesto**?",
         "Un testo con collegamenti ad altri testi, che si può leggere in ordine non lineare.",
         ["Un documento HTML che contiene almeno un'immagine o un video.",
          "Un testo che viaggia cifrato durante il trasferimento con HTTPS.",
          "Un documento troppo grande per essere inviato in una sola risposta.",
          "Un file di testo che il server genera dinamicamente a ogni richiesta.",
          "Il corpo di una risposta HTTP, separato dalle intestazioni."],
         spiegazione="L'ipertesto è un testo con collegamenti ad altri testi: il lettore non è "
                     "costretto a una lettura sequenziale ma segue i riferimenti. Il Web è un "
                     "enorme ipertesto, in cui i collegamenti sono URL.",
         rif=R % "Documenti ipertestuali"))

d(chiusa("c01-chi-inizia", CAP, "HTTP: richiesta e risposta",
         "Nel protocollo HTTP, come si svolge la comunicazione fra client e server?",
         "Il client invia una richiesta e il server risponde; il server non inizia mai.",
         ["Il server invia periodicamente le pagine aggiornate ai client collegati.",
          "Client e server possono iniziare la comunicazione indifferentemente.",
          "Il server apre la comunicazione inviando l'elenco delle risorse disponibili.",
          "Il client si collega e attende che il server scelga quale pagina inviare.",
          "Il server risponde solo ai client che hanno già una sessione aperta."],
         spiegazione="HTTP è un protocollo di tipo richiesta-risposta: il client parla per primo, "
                     "sempre. Il server si limita a rispondere alle richieste che riceve.",
         rif=R % "HTTP: il protocollo del Web"))

d(chiusa("c01-stateless", CAP, "statelessness",
         "Che cosa significa che HTTP è un protocollo *stateless*?",
         "Il server non conserva memoria delle richieste precedenti di un client.",
         ["Il server non può salvare in modo permanente i dati in un database.",
          "Le risposte del server non possono mai essere conservate in una cache.",
          "Il client non può inviare dati al server, ma solo riceverne.",
          "La connessione viene chiusa e riaperta dopo ogni pacchetto trasmesso.",
          "Le pagine restituite dal server sono sempre documenti statici."],
         nessuna=True,
         spiegazione="Senza stato vuol dire che il protocollo non ricorda nulla fra una "
                     "richiesta e l'altra. Il vantaggio è la scalabilità (due richieste dello "
                     "stesso utente possono essere servite da macchine diverse); lo svantaggio "
                     "è che il concetto di «utente collegato» va costruito sopra HTTP, per "
                     "esempio con i cookie.",
         rif=R % "HTTP è un protocollo stateless"))

d(chiusa("c01-stateless-vantaggio", CAP, "statelessness",
         "Qual è il principale **vantaggio** del fatto che HTTP sia stateless?",
         "La scalabilità: ogni richiesta può essere servita da un server diverso.",
         ["La sicurezza: senza stato le richieste non si possono intercettare.",
          "Il login degli utenti è gestito automaticamente dal protocollo.",
          "La velocità: le richieste non hanno bisogno di intestazioni.",
          "Il server può inviare dati al client senza attendere una richiesta.",
          "Il browser non ha più bisogno di conservare le pagine in cache."],
         spiegazione="Se il server non deve ricordare nulla, qualunque macchina può rispondere a "
                     "qualunque richiesta: è ciò che permette di scalare aggiungendo server. Il "
                     "prezzo è che lo stato (per esempio il login) va gestito con meccanismi "
                     "costruiti sopra HTTP.",
         rif=R % "HTTP è un protocollo stateless"))

d(chiusa("c01-riga-richiesta", CAP, "messaggi HTTP",
         "Quali elementi compaiono nella **prima riga** di una richiesta HTTP/1.1?",
         "Il metodo, il percorso della risorsa e la versione del protocollo (es. `GET "
         "/index.html HTTP/1.1`).",
         ["Il codice di stato e la sua descrizione (es. `200 OK`).",
          "L'indirizzo IP del client e la porta sorgente.",
          "Il nome di dominio e il tipo di contenuto richiesto.",
          "Il metodo e il corpo della richiesta.",
          "La versione del protocollo e la data della richiesta."],
         spiegazione="La riga di richiesta contiene metodo, percorso e versione; seguono le "
                     "intestazioni (fra cui `Host`), una riga vuota e l'eventuale corpo. Il "
                     "codice di stato compare nella prima riga della *risposta*.",
         rif=R % "I messaggi HTTP"))

d(chiusa("c01-riga-risposta", CAP, "messaggi HTTP",
         "Quale fra le seguenti è una prima riga valida di una **risposta** HTTP/1.1?",
         "`HTTP/1.1 404 Not Found`",
         ["`GET /index.html HTTP/1.1`",
          "`404 Not Found HTTP/1.1`",
          "`HTTP/1.1 GET 200`",
          "`Status: 404 /index.html`",
          "`Host: www.example.org`"],
         spiegazione="La riga di stato della risposta è formata da versione del protocollo, "
                     "codice di stato e frase descrittiva. `GET /index.html HTTP/1.1` è la "
                     "prima riga di una richiesta; `Host:` è un'intestazione.",
         rif=R % "Esempio di risposta"))

d(chiusa("c01-header-host", CAP, "messaggi HTTP",
         "Quale intestazione di una richiesta HTTP/1.1 indica il nome di dominio del server a "
         "cui la richiesta è destinata?",
         "`Host`", ["`Server`", "`Origin`", "`Location`", "`Domain`", "`Referer`"],
         spiegazione="`Host` è obbligatoria in HTTP/1.1: permette a un solo server (un solo "
                     "indirizzo IP) di ospitare più siti. `Location` compare nelle risposte di "
                     "reindirizzamento; `Server` descrive il software del server.",
         rif=R % "Header"))

d(chiusa("c01-header-tipo", CAP, "messaggi HTTP",
         "In una risposta HTTP, quale intestazione indica il **tipo** di dati contenuto nel "
         "corpo (per esempio una pagina HTML o un oggetto JSON)?",
         "`Content-Type`", ["`Content-Length`", "`Accept`", "`Media-Type`", "`Content-Format`",
                            "`User-Agent`"],
         spiegazione="`Content-Type` dichiara il tipo del corpo (es. `text/html; "
                     "charset=utf-8`); `Content-Length` ne indica la lunghezza in byte. "
                     "`Accept` è un'intestazione di *richiesta*, con cui il client dice quali "
                     "tipi preferisce ricevere.",
         rif=R % "Header"))

d(chiusa("c01-4xx-5xx", CAP, "codici di stato: le classi",
         "Un server risponde `503` a una richiesta. Che cosa conviene fare al client?",
         "Riprovare più tardi: il problema è del server, non della richiesta.",
         ["Correggere la richiesta: è stata inviata in un formato non valido.",
          "Autenticarsi e ripetere la richiesta con le credenziali.",
          "Seguire l'indirizzo indicato nell'intestazione `Location`.",
          "Nulla: la richiesta è andata a buon fine.",
          "Cancellare la cache, che contiene una copia non più valida."],
         spiegazione="I codici 5xx segnalano un problema del server: riprovare più tardi ha "
                     "senso (`503` indica proprio un'indisponibilità momentanea). I 4xx dicono "
                     "invece che la colpa è della richiesta, e ripeterla identica non serve.",
         rif=R % "Codici di stato della risposta"))

d(chiusa("c01-dns", CAP, "DNS e caricamento di una pagina",
         "Qual è il compito del **DNS**?",
         "Tradurre un nome di dominio (es. `www.unina.it`) nell'indirizzo IP del server.",
         ["Instradare i pacchetti IP fino al server di destinazione.",
          "Cifrare le richieste HTTP prima che lascino il browser.",
          "Assegnare un indirizzo IP al computer quando si collega alla rete.",
          "Memorizzare in cache le pagine visitate di recente.",
          "Trasformare una URL relativa in una URL assoluta."],
         spiegazione="Il DNS è una «rubrica»: dato un nome restituisce un indirizzo. Una volta "
                     "ottenuto l'indirizzo IP, il browser apre la connessione e invia la "
                     "richiesta HTTP; il DNS non interviene nel trasferimento dei dati.",
         rif=R % "Cosa succede quando si apre una pagina"))

d(chiusa("c01-sequenza", CAP, "DNS e caricamento di una pagina",
         "L'utente digita `https://www.example.org/` nella barra degli indirizzi e preme "
         "Invio. In quale ordine avvengono le operazioni?",
         "Risoluzione DNS, connessione al server, richiesta HTTP, risposta, visualizzazione.",
         ["Richiesta HTTP al DNS, che la inoltra al server e restituisce la pagina.",
          "Connessione al server, risoluzione DNS, richiesta HTTP, risposta, visualizzazione.",
          "Richiesta HTTP, risoluzione DNS della risposta, visualizzazione della pagina.",
          "Download delle immagini, poi richiesta del documento HTML che le contiene.",
          "Risoluzione DNS, poi visualizzazione della pagina conservata dal server DNS."],
         spiegazione="Prima serve l'indirizzo IP (DNS), poi la connessione (TCP, e TLS per "
                     "HTTPS), poi la richiesta. Le risorse incluse nella pagina (immagini, "
                     "fogli di stile, script) vengono richieste dopo, man mano che il browser "
                     "analizza l'HTML.",
         rif=R % "Cosa succede quando si apre una pagina"))

d(chiusa("c01-tld", CAP, "anatomia di una URL",
         "Nel nome di dominio `www.docenti.unina.it`, qual è il dominio di **primo livello** "
         "(TLD)?",
         "`it`", ["`www`", "`unina`", "`docenti`", "`unina.it`", "`www.docenti`"],
         spiegazione="I nomi di dominio si leggono da destra verso sinistra: `it` è il dominio "
                     "di primo livello, `unina` il secondo livello, `docenti` e `www` sono "
                     "sottodomini.",
         rif="cap. 1, «Nome di dominio»"))

d(chiusa("c01-porta-default", CAP, "anatomia di una URL",
         "Quali delle seguenti affermazioni sulle porte nelle URL sono **vere**?",
         ["Se la URL non indica la porta, per `http` si usa la porta 80.",
          "Se la URL non indica la porta, per `https` si usa la porta 443.",
          "In `http://localhost:3000/`, il server è in ascolto sulla porta 3000.",
          "Una porta scritta esplicitamente segue i due punti dopo il nome dell'host."],
         ["La porta è obbligatoria in tutte le URL.",
          "La porta 80 è riservata ai server HTTPS.",
          "La porta viene indicata dopo il percorso, come `/index.html:8080`.",
          "La porta identifica la scheda del browser che ha inviato la richiesta.",
          "Il numero di porta fa parte del nome di dominio e viene risolto dal DNS."],
         multi=True,
         spiegazione="La porta identifica il processo server sulla macchina di destinazione. "
                     "Si può omettere quando è quella predefinita dello schema (80 per HTTP, "
                     "443 per HTTPS). In sviluppo si usano spesso porte come 3000 perché le "
                     "porte sotto la 1024 richiedono privilegi di amministratore.",
         rif="cap. 1, «Porta»"))

d(chiusa("c01-path-traversal", CAP, "anatomia di una URL",
         "Un server statico mappa i percorsi delle URL sui file di una cartella. Perché deve "
         "rifiutare una richiesta come `GET /../../etc/passwd`?",
         "Perché `..` farebbe uscire dalla cartella pubblicata (*path traversal*).",
         ["Perché i percorsi non possono contenere più di due barre.",
          "Perché i file senza estensione non possono essere inviati con HTTP.",
          "Perché la sequenza `..` non è ammessa nelle URL e la rende malformata.",
          "Perché le richieste `GET` non possono riferirsi a file di sistema.",
          "Perché il browser non sa visualizzare un file di testo semplice."],
         spiegazione="È l'attacco di *path traversal*: risalendo con `..` si arriva fuori dalla "
                     "radice dei documenti. Un server deve servire solo ciò che sta nella "
                     "*document root*.",
         rif="cap. 1, «Percorso»; cap. 2, «Dentro un server HTTP»"))

d(chiusa("c01-https", CAP, "anatomia di una URL",
         "Che cosa aggiunge HTTPS rispetto a HTTP?",
         "La cifratura della comunicazione e l'autenticazione del server, grazie a TLS.",
         ["Un formato diverso per i messaggi, non compatibile con HTTP.",
          "La garanzia che il sito sia affidabile e non malevolo.",
          "La compressione obbligatoria delle risposte.",
          "La possibilità di inviare richieste senza intestazioni.",
          "Il supporto ai metodi `PUT` e `DELETE`, che HTTP non prevede."],
         spiegazione="HTTPS è HTTP trasportato dentro un canale TLS: i messaggi sono gli stessi, "
                     "ma viaggiano cifrati e il certificato garantisce l'identità del server. "
                     "Il lucchetto non dice nulla sulle intenzioni di chi gestisce il sito.",
         rif="cap. 1, «Schema»; cap. 9, «HTTPS: HTTP dentro un canale TLS»"))

d(chiusa("c01-verbo-promessa", CAP, "messaggi HTTP",
         "Quale fra le seguenti affermazioni sui metodi (verbi) HTTP è corretta?",
         "Il metodo dichiara un'intenzione, ma è il server a decidere come gestirla.",
         ["Il protocollo impedisce a una `GET` di modificare dati sul server.",
          "Il metodo `POST` può essere usato solo per caricare file sul server.",
          "Il metodo viene scelto dal server e comunicato al client nella risposta.",
          "Una richiesta `GET` non può contenere alcun parametro.",
          "I metodi definiti da HTTP sono soltanto due: `GET` e `POST`."],
         spiegazione="Il verbo è una promessa, non un obbligo: nulla impedisce tecnicamente a un "
                     "server di modificare dati in risposta a una `GET`, ma violare la "
                     "semantica dei metodi rende l'applicazione imprevedibile (browser, proxy "
                     "e motori di ricerca ripetono le `GET` liberamente).",
         rif="cap. 1, «Metodi (o verbi) di richiesta»"))

# ----------------------------------------------------------------------
# Domande aperte
d(aperta("c01-a-stateless", CAP, "statelessness",
         "Si spieghi che cosa significa che HTTP è un protocollo **stateless**, quali vantaggi "
         "e svantaggi comporta, e come si può comunque realizzare un'interazione con stato "
         "(per esempio il login).",
         ["Ogni richiesta è indipendente: il server non conserva memoria delle richieste "
          "precedenti dello stesso client.",
          "Vantaggio: scalabilità. Qualunque server può rispondere a qualunque richiesta, "
          "quindi basta aggiungere macchine.",
          "Svantaggio: non esiste il concetto di utente collegato; dopo il login la richiesta "
          "successiva è di uno sconosciuto.",
          "Lo stato si costruisce sopra HTTP: cookie inviati a ogni richiesta, che contengono "
          "i dati (approccio ingenuo, manipolabile) o, meglio, un identificatore di sessione "
          "con i dati conservati sul server."],
         rif="cap. 1, «HTTP è un protocollo stateless»; cap. 13"))

d(aperta("c01-a-messaggi", CAP, "messaggi HTTP",
         "Si descriva la struttura di una **richiesta** e di una **risposta** HTTP, indicando "
         "le parti che le compongono e facendo un esempio per ciascuna.",
         ["Richiesta: riga di richiesta (metodo, percorso, versione), intestazioni (`Host`, "
          "`User-Agent`, `Accept`, ...), riga vuota, corpo facoltativo (es. dati di un form "
          "inviato con `POST`).",
          "Risposta: riga di stato (versione, codice, frase), intestazioni (`Content-Type`, "
          "`Content-Length`, ...), riga vuota, corpo (es. il documento HTML).",
          "Esempio: `GET /index.html HTTP/1.1` con `Host: www.example.org`; risposta "
          "`HTTP/1.1 200 OK` con `Content-Type: text/html`.",
          "I codici di stato si raggruppano in classi (2xx successo, 3xx reindirizzamento, "
          "4xx errore del client, 5xx errore del server)."],
         rif="cap. 1, «I messaggi HTTP»"))

d(aperta("c01-a-url", CAP, "anatomia di una URL",
         "Si descrivano le parti di una URL, usando come esempio "
         "`https://www.example.org:8443/corsi/web?anno=2025#esami`.",
         ["Schema `https`: il protocollo (HTTP dentro TLS).",
          "Host `www.example.org`: il nome di dominio, tradotto dal DNS in un indirizzo IP.",
          "Porta `8443`: il processo server sulla macchina; se omessa vale 443 per https e 80 "
          "per http.",
          "Percorso `/corsi/web`: la risorsa sul server.",
          "Query `anno=2025`: parametri `chiave=valore` separati da `&`; ancora `esami`: "
          "usata solo dal browser, non viene inviata al server."],
         rif="cap. 1, «URL: individuare una risorsa»"))

d(aperta("c01-a-pagina", CAP, "DNS e caricamento di una pagina",
         "Si descriva che cosa accade, dal momento in cui l'utente digita una URL e preme "
         "Invio, fino alla visualizzazione completa della pagina.",
         ["Il browser estrae l'host dalla URL e lo risolve in un indirizzo IP con il DNS.",
          "Apre una connessione con il server sulla porta indicata (TCP, più TLS per HTTPS).",
          "Invia la richiesta HTTP (es. `GET /`) e riceve la risposta con il documento HTML.",
          "Analizza l'HTML, costruisce il DOM e invia nuove richieste per le risorse incluse "
          "(CSS, script, immagini), poi visualizza la pagina."],
         rif="cap. 1, «Cosa succede quando si apre una pagina»; cap. 9, «Dal clic alla pagina»"))

d(aperta("c01-a-4xx5xx", CAP, "codici di stato: le classi",
         "Si spieghi la differenza fra i codici di stato della famiglia `4xx` e quelli della "
         "famiglia `5xx`, con almeno due esempi per ciascuna.",
         ["4xx: errore del client. La richiesta è sbagliata e ripeterla identica non serve.",
          "Esempi 4xx: 400 richiesta malformata, 401 manca l'autenticazione, 403 permessi "
          "insufficienti, 404 risorsa inesistente, 405 metodo non ammesso.",
          "5xx: errore del server. La richiesta era plausibile ma il server non è riuscito a "
          "elaborarla; riprovare più tardi può avere senso.",
          "Esempi 5xx: 500 errore interno (es. un'eccezione non gestita), 502 risposta non "
          "valida da un server a monte, 503 servizio momentaneamente non disponibile."],
         rif="cap. 1, «Codici di stato della risposta»"))
