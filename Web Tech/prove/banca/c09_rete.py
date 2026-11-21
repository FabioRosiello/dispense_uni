"""Capitolo 9: il Web sotto il cofano (applicazioni di rete, socket, IP e
porte, DNS, TCP, UDP e QUIC, versioni di HTTP, metodi sicuri e idempotenti,
codici di stato, HTTPS)."""

from generatore import FONTE_2026, L, aperta, chiusa, famiglia

CAP = 9
R = "cap. 9, «%s»"

DOMANDE = []
d = DOMANDE.append


# ----------------------------------------------------------------------
# Famiglia: il codice di stato giusto per la situazione
CODICI = {
    "200": "`200 OK`", "201": "`201 Created`", "204": "`204 No Content`",
    "301": "`301 Moved Permanently`", "302": "`302 Found`", "304": "`304 Not Modified`",
    "400": "`400 Bad Request`", "401": "`401 Unauthorized`", "403": "`403 Forbidden`",
    "404": "`404 Not Found`", "405": "`405 Method Not Allowed`",
    "500": "`500 Internal Server Error`", "502": "`502 Bad Gateway`",
    "503": "`503 Service Unavailable`",
}
SITUAZIONI = [
    ("401", "un utente **non autenticato** chiede una pagina riservata agli utenti registrati",
     ["403", "404", "400", "302"]),
    ("403", "un utente **autenticato**, ma senza i permessi necessari, chiede una pagina "
            "riservata agli amministratori", ["401", "404", "405", "400"]),
    ("301", "la risorsa è stata spostata **per sempre** a un nuovo indirizzo, e i link "
            "vanno aggiornati", ["302", "304", "404", "200"]),
    ("302", "la risorsa si trova **temporaneamente** a un altro indirizzo, e si deve "
            "continuare a usare quello vecchio", ["301", "304", "404", "200"]),
    ("304", "il client ha inviato `If-None-Match` con l'`ETag` della sua copia in cache, e "
            "la risorsa non è cambiata", ["200", "302", "204", "400"]),
    ("502", "un *proxy* ha ricevuto una risposta non valida dal server che sta dietro di lui",
     ["503", "500", "404", "400"]),
    ("503", "il server è momentaneamente non disponibile perché sovraccarico o in "
            "manutenzione", ["502", "500", "404", "401"]),
    ("201", "una `POST` ha creato una nuova risorsa", ["200", "204", "302", "304"]),
    ("204", "una `DELETE` è andata a buon fine e la risposta non ha corpo",
     ["200", "201", "404", "304"]),
    ("405", "il percorso richiesto esiste, ma il metodo usato non è previsto per esso",
     ["404", "400", "403", "500"]),
]


@famiglia("c09-codici", CAP, "codici di stato", varianti=5)
def _codici(rng):
    codice, situazione, vicini = rng.choice(SITUAZIONI)
    altri = [c for c in CODICI if c != codice and c not in vicini]
    sbagliate = vicini + rng.sample(altri, 1)
    return chiusa(
        "c09-codici", CAP, "codici di stato",
        "Quale codice di stato dovrebbe restituire il server nella seguente situazione: %s?"
        % situazione,
        CODICI[codice], [CODICI[c] for c in sbagliate],
        spiegazione="`401` vuol dire «non so chi sei» (manca l'autenticazione), `403` «so chi "
                    "sei, ma non puoi». `301` e `302` sono spostamenti definitivo e "
                    "temporaneo; `304` dice che la copia in cache è ancora buona. `502` "
                    "segnala una risposta non valida ricevuta da un server intermedio, `503` "
                    "un server momentaneamente non disponibile. `201` accompagna la creazione di "
                    "una risorsa, `204` un successo senza corpo, `405` un metodo non ammesso "
                    "su un percorso esistente.",
        rif=R % "La risposta")


d(_codici)


# ----------------------------------------------------------------------
# Famiglia: porte note
PORTE = [("80", "HTTP"), ("443", "HTTPS"), ("22", "SSH"), ("25", "SMTP (invio di posta)"),
         ("53", "DNS"), ("21", "FTP")]


@famiglia("c09-porte", CAP, "processi, socket e porte", varianti=3)
def _porte(rng):
    porta, servizio = rng.choice(PORTE)
    altri = [s for p, s in PORTE if p != porta]
    if rng.random() < 0.5:
        return chiusa(
            "c09-porte", CAP, "processi, socket e porte",
            "A quale servizio è assegnata, per convenzione, la porta `%s`?" % porta,
            servizio, altri,
            spiegazione="Alle applicazioni più diffuse sono assegnate porte note: 80 per HTTP, "
                        "443 per HTTPS, 22 per SSH, 25 per SMTP, 53 per il DNS, 21 per FTP. Per "
                        "questo nelle URL `http://` e `https://` la porta si può omettere.",
            rif=R % "Indirizzi IP e porte")
    return chiusa(
        "c09-porte", CAP, "processi, socket e porte",
        "Su quale porta è in ascolto, per convenzione, un server %s?" % servizio,
        "`%s`" % porta, ["`%s`" % p for p, _ in PORTE if p != porta],
        spiegazione="Alle applicazioni più diffuse sono assegnate porte note: 80 per HTTP, 443 "
                    "per HTTPS, 22 per SSH, 25 per SMTP, 53 per il DNS, 21 per FTP.",
        rif=R % "Indirizzi IP e porte")


d(_porte)


# ----------------------------------------------------------------------
# Famiglia: le versioni di HTTP
VERSIONI = [
    ("HTTP/1.0", "usava di norma una connessione TCP **diversa** per ogni coppia "
                 "richiesta--risposta (connessioni non persistenti)"),
    ("HTTP/1.1", "ha reso **persistenti** le connessioni per impostazione predefinita"),
    ("HTTP/2", "invia più richieste in parallelo come **flussi multiplexati** su un'unica "
               "connessione TCP, con messaggi in formato binario"),
    ("HTTP/3", "viaggia su **QUIC**, che a sua volta usa UDP"),
]


@famiglia("c09-versioni", CAP, "versioni di HTTP", varianti=2)
def _versioni(rng):
    versione, descrizione = rng.choice(VERSIONI)
    return chiusa(
        "c09-versioni", CAP, "versioni di HTTP",
        "Quale versione di HTTP %s?" % descrizione,
        versione, [v for v, _ in VERSIONI if v != versione] + ["HTTPS"],
        spiegazione="HTTP/1.0 (1996) usava spesso connessioni non persistenti; HTTP/1.1 (1997) "
                    "le rende persistenti per impostazione predefinita; HTTP/2 (2015) "
                    "multiplexa più flussi su un'unica connessione TCP, con messaggi binari; "
                    "HTTP/3 (2022) usa QUIC, su UDP. HTTPS non è una versione: è HTTP dentro "
                    "un canale TLS.",
        rif=R % "HTTP più da vicino")


d(_versioni)

# ----------------------------------------------------------------------
d(chiusa("c09-architetture", CAP, "applicazioni di rete",
         "Quali delle seguenti affermazioni sulle architetture delle applicazioni di rete sono "
         "**vere**?",
         ["Nell'architettura client-server i client non comunicano direttamente fra loro.",
          "Nell'architettura client-server il server ha un indirizzo fisso e noto, ed è "
          "sempre acceso.",
          "In un'applicazione peer-to-peer lo stesso processo può fare da client in uno "
          "scambio e da server in un altro.",
          "Un servizio client-server può essere realizzato da molti server, che il client "
          "percepisce come uno solo."],
         ["Nell'architettura peer-to-peer c'è un host sempre acceso che coordina tutti gli "
          "scambi.",
          "Nell'architettura client-server ogni client inoltra le richieste degli altri client.",
          "Un'applicazione web è il tipico esempio di architettura peer-to-peer.",
          "Nell'architettura peer-to-peer i nodi sono eterogenei: uno fa sempre da server.",
          "Nell'architettura client-server è il server ad avviare la comunicazione."],
         multi=True,
         spiegazione="Nel modello client-server i nodi sono eterogenei: un server sempre acceso, "
                     "con indirizzo noto, serve le richieste dei client, che non parlano fra "
                     "loro (anche se dietro ci sono molti server o interi data center). Nel "
                     "peer-to-peer i nodi sono idealmente omogenei e comunicano direttamente; "
                     "il processo che avvia uno scambio fa da client, e i ruoli cambiano da uno "
                     "scambio all'altro.",
         rif=R % "Client-server e peer-to-peer"))

d(chiusa("c09-socket", CAP, "processi, socket e porte",
         "Che cos'è un *socket*?",
         "L'interfaccia software fra il livello applicativo e il livello di trasporto, "
         "attraverso cui un processo invia e riceve messaggi sulla rete.",
         ["Il cavo che collega un host al primo router della rete.",
          "Il protocollo di trasporto usato da HTTP al posto di TCP.",
          "Un file di configurazione che associa i nomi degli host agli indirizzi IP.",
          "Il processo del server web che resta in ascolto sulla porta 80.",
          "Un messaggio di controllo scambiato durante l'*handshake* di TCP."],
         spiegazione="Il socket è la «cassetta postale» del processo: l'applicazione vi imbuca i "
                     "messaggi, e l'infrastruttura di trasporto, controllata dal sistema "
                     "operativo, li consegna al socket del destinatario. Dal lato del trasporto "
                     "lo sviluppatore sceglie solo il protocollo (TCP o UDP) e pochi parametri.",
         rif=R % "Il socket"))

d(chiusa("c09-ip-porta", CAP, "processi, socket e porte",
         "Per inviare un messaggio a un processo in esecuzione su un altro host servono un "
         "indirizzo IP e un numero di porta. A che cosa servono, rispettivamente?",
         "L'indirizzo IP identifica l'host (livello di rete), la porta il processo su quell'host "
         "(livello di trasporto).",
         ["L'indirizzo IP identifica il processo, la porta l'host.",
          "L'indirizzo IP identifica l'utente, la porta il browser che usa.",
          "Entrambi identificano l'host: la porta serve solo quando l'indirizzo IP è privato.",
          "L'indirizzo IP identifica il sito, la porta la pagina richiesta.",
          "La porta identifica la scheda di rete dell'host, l'indirizzo IP il router."],
         spiegazione="Su un host girano molte applicazioni di rete: l'indirizzo IP (32 bit in "
                     "IPv4, 128 in IPv6) trova la macchina, il numero di porta (da 0 a 65535) "
                     "trova il processo. Anche il browser usa una porta, assegnata al momento "
                     "dal sistema operativo, per ricevere la risposta.",
         rif=R % "Indirizzi IP e porte"))

d(chiusa("c09-protocollo", CAP, "applicazioni di rete",
         "Che cosa stabilisce un **protocollo di livello applicativo**?",
         ["I tipi di messaggio scambiati, per esempio richieste e risposte.",
          "La sintassi di ciascun tipo di messaggio: i campi e come sono delimitati.",
          "Il significato delle informazioni contenute nei campi.",
          "Le regole su quando e come un processo invia messaggi e risponde."],
         ["Il percorso dei pacchetti attraverso i router della rete.",
          "Il linguaggio di programmazione con cui scrivere client e server.",
          "La codifica elettrica dei bit sul cavo.",
          "L'indirizzo IP da assegnare a ciascun host."],
         multi=True,
         spiegazione="Un protocollo applicativo (HTTP, DNS, SMTP...) definisce tipi, sintassi e "
                     "semantica dei messaggi e le regole dello scambio. L'instradamento, la "
                     "trasmissione fisica e l'assegnazione degli indirizzi sono compito di altri "
                     "livelli e di altri protocolli (per esempio DHCP per gli indirizzi).",
         rif=R % "I protocolli applicativi"))

d(chiusa("c09-dns", CAP, "DNS",
         "Quali delle seguenti affermazioni sul DNS sono **vere**?",
         ["È un database distribuito su migliaia di server, non un unico server centrale.",
          "I nomi sono organizzati in un albero: dalla radice ai TLD come `.it`, poi ai domini "
          "di secondo livello come `unina.it`.",
          "Resolver e dispositivi tengono in cache le risposte per un tempo stabilito, il TTL.",
          "Il browser di norma interroga un *resolver*, che scende nell'albero per suo conto."],
         ["Tutte le richieste di risoluzione arrivano a un unico server centrale.",
          "Il server *root* conosce gli indirizzi IP di tutti gli host di Internet.",
          "Il DNS assegna gli indirizzi IP agli host quando si collegano alla rete.",
          "Un nome si legge da sinistra a destra, dalla radice verso l'host.",
          "Le risposte del DNS non vengono mai memorizzate, per essere sempre aggiornate."],
         multi=True,
         spiegazione="Il DNS è una rubrica distribuita e gerarchica: la radice sa chi gestisce "
                     "ciascun TLD, il server del TLD sa chi gestisce ciascun dominio, il server "
                     "autoritativo conosce gli indirizzi. Le risposte restano in cache per la "
                     "durata del TTL. Gli indirizzi agli host li assegna DHCP. Un nome si legge "
                     "da destra a sinistra risalendo verso la radice.",
         rif=R % "Dalla URL all'indirizzo: il DNS"))

d(chiusa("c09-dns-ordine", CAP, "DNS",
         "Il resolver deve trovare l'indirizzo di `www.unina.it` e non ha nulla in cache. A quali "
         "server chiede, nell'ordine?",
         "Al server *root*, al server del TLD `.it`, al server autoritativo di `unina.it`.",
         ["Al server autoritativo di `unina.it`, al server del TLD `.it`, al server *root*.",
          "Al server del TLD `.it`, al server *root*, al server autoritativo di `unina.it`.",
          "Soltanto al server *root*, che conosce tutti gli indirizzi.",
          "Al server autoritativo di `www.unina.it`, poi al server *root* per conferma.",
          "A un server DHCP, che gli assegna l'indirizzo di `www.unina.it`."],
         spiegazione="Il resolver scende nell'albero un livello alla volta: il server root non "
                     "conosce l'indirizzo, ma sa chi gestisce `.it`; il server del TLD sa chi "
                     "gestisce `unina.it`; il server autoritativo di `unina.it` conosce "
                     "l'indirizzo. La risposta resta poi in cache per la durata del TTL.",
         rif=R % "Dalla URL all'indirizzo: il DNS"))

d(chiusa("c09-tcp-udp", CAP, "TCP, UDP e QUIC",
         "Quali delle seguenti affermazioni su TCP e UDP sono **vere**?",
         ["TCP è orientato alla connessione: prima di scambiare dati i processi fanno un "
          "*handshake*.",
          "TCP offre un trasferimento affidabile: i dati arrivano integri e in ordine.",
          "UDP non garantisce che i messaggi arrivino, né in che ordine.",
          "HTTP/3 usa UDP, insieme al protocollo QUIC che aggiunge l'affidabilità."],
         ["UDP è più lento di TCP perché ritrasmette i pacchetti persi.",
          "TCP non richiede alcun *handshake* iniziale.",
          "HTTP ha sempre usato soltanto UDP.",
          "UDP garantisce la consegna in ordine, ma non l'integrità dei dati.",
          "Con TCP lo sviluppatore deve gestire a mano ritrasmissioni e perdite."],
         multi=True,
         spiegazione="TCP è orientato alla connessione e affidabile, al prezzo di handshake, "
                     "conferme e ritrasmissioni; UDP è leggero e senza garanzie. HTTP ha usato "
                     "storicamente TCP per l'affidabilità; HTTP/3 usa QUIC, che implementa "
                     "l'affidabilità sopra UDP. In entrambi i casi l'applicazione delega questi "
                     "problemi ai livelli inferiori.",
         rif=R % "TCP o UDP"))

d(chiusa("c09-quic", CAP, "TCP, UDP e QUIC",
         "Quali dei seguenti sono vantaggi di QUIC (e quindi di HTTP/3) rispetto a TCP?",
         ["Apertura della connessione e negoziazione crittografica avvengono insieme, di solito "
          "in un solo *round trip*.",
          "La perdita di un pacchetto blocca solo il flusso a cui appartiene, non le altre "
          "richieste.",
          "È implementato di solito nel software applicativo, quindi si aggiorna più facilmente."],
         ["Non usa conferme né ritrasmissioni, quindi non perde mai tempo.",
          "Non cifra i dati, e per questo è più veloce.",
          "Usa una connessione TCP separata per ogni richiesta.",
          "Elimina la necessità del DNS.",
          "Trasmette i messaggi HTTP come semplice testo ASCII."],
         multi=True,
         spiegazione="QUIC combina handshake di trasporto e TLS (un round trip, zero riprendendo "
                     "una connessione precedente), usa flussi separati evitando il "
                     "*head-of-line blocking* di TCP, e vive nel software applicativo invece che "
                     "nel kernel. Come TCP usa conferme e timer per ritrasmettere i dati persi, "
                     "e integra TLS.",
         rif=R % "QUIC"))

d(chiusa("c09-hol", CAP, "TCP, UDP e QUIC",
         "Con HTTP/2 tre richieste viaggiano in parallelo sulla stessa connessione TCP, e si "
         "perde un pacchetto della prima. Che cosa succede?",
         "Anche i dati delle altre due richieste che arrivano dopo restano fermi finché il "
         "pacchetto non viene ritrasmesso.",
         ["Si ferma solo la prima richiesta; le altre due vengono consegnate subito.",
          "La connessione viene chiusa e le tre richieste ripartono da capo.",
          "Il pacchetto perso viene ignorato e la prima risposta arriva incompleta.",
          "Il browser apre tre nuove connessioni, una per richiesta.",
          "Il server rimanda tutte e tre le risposte su UDP."],
         spiegazione="TCP vede un unico flusso di byte da consegnare in ordine: un pacchetto "
                     "perso blocca anche i dati che seguono, di qualunque richiesta siano. È il "
                     "*head-of-line blocking*. HTTP/3 lo evita con flussi QUIC separati: si "
                     "blocca solo il flusso a cui appartiene il pacchetto perso.",
         rif=R % "QUIC"))

d(chiusa("c09-persistenti", CAP, "TCP, UDP e QUIC",
         "Una pagina richiede tre oggetti allo stesso server. Che cosa si risparmia usando una "
         "connessione **persistente** invece di connessioni non persistenti?",
         "L'apertura di due connessioni: tutte le richieste e risposte viaggiano sulla stessa.",
         ["Due delle tre richieste: il server invia tutti gli oggetti con una sola risposta.",
          "La risoluzione DNS, che con le connessioni persistenti non serve.",
          "La cifratura TLS, che si applica solo alle connessioni non persistenti.",
          "Nulla: le connessioni persistenti servono solo a mantenere il login.",
          "Gli header delle risposte, che vengono inviati una volta sola."],
         spiegazione="Con connessioni non persistenti (HTTP/1.0) ogni coppia richiesta--risposta "
                     "apre una connessione nuova; con quelle persistenti, predefinite da HTTP/1.1 "
                     "(`Connection: keep-alive`), le richieste successive riusano la stessa, "
                     "risparmiando le aperture (e le negoziazioni TLS).",
         rif=R % "Connessioni persistenti e non persistenti"))

d(chiusa("c09-sicuri", CAP, "metodi HTTP",
         "Quali dei seguenti metodi HTTP sono **sicuri** (*safe*)?",
         ["`GET`", "`HEAD`", "`OPTIONS`", "`QUERY`"],
         ["`POST`", "`PUT`", "`DELETE`", "`PATCH`"],
         multi=True,
         spiegazione="Un metodo è sicuro se è di sola lettura: il client non chiede alcuna "
                     "modifica sul server. Lo sono `GET`, `HEAD`, `OPTIONS` e `QUERY`; `POST`, "
                     "`PUT`, `PATCH` e `DELETE` chiedono invece di modificare lo stato.",
         rif=R % "Metodi sicuri e idempotenti"))

d(chiusa("c09-idempotenti", CAP, "metodi HTTP",
         "Quali dei seguenti metodi HTTP sono **idempotenti ma non sicuri**?",
         ["`PUT`", "`DELETE`"],
         ["`POST`", "`GET`", "`HEAD`", "`OPTIONS`", "`QUERY`"],
         multi=True, quante_giuste=(1, 2),
         spiegazione="Un metodo è idempotente se l'effetto di più richieste identiche è lo "
                     "stesso di una sola. I metodi sicuri lo sono tutti; fra quelli che "
                     "modificano lo stato lo sono `PUT` (il nuovo stato completo) e `DELETE` (la "
                     "risorsa resta cancellata). `POST` non è né sicuro né idempotente.",
         rif=R % "Metodi sicuri e idempotenti"))

d(chiusa("c09-ripetute", CAP, "metodi HTTP",
         "Per un doppio clic, la stessa richiesta arriva due volte al server. In quali dei "
         "seguenti casi lo stato del server, dopo la seconda, è lo stesso che dopo la prima?",
         ["`PUT /api/compiti/42` con lo stato completo del compito.",
          "`DELETE /api/compiti/42`.",
          "`PATCH /api/compiti/42` con `{\"scadenza\": \"2026-11-12\"}`, che imposta un valore.",
          "`GET /api/compiti/42`."],
         ["`POST /api/compiti` con i dati di un nuovo compito.",
          "`PATCH /api/compiti/42` che aggiunge un elemento alla lista degli allegati.",
          "`POST /api/ordini` con il contenuto del carrello.",
          "`PATCH /api/contatori/7` che incrementa un contatore."],
         multi=True,
         spiegazione="`PUT` e `DELETE` sono idempotenti (la seconda `DELETE` riceverà "
                     "probabilmente `404`, ma la risorsa resta cancellata), e `GET` non modifica "
                     "nulla. Una `POST` ripetuta crea un duplicato. Per `PATCH` dipende dal "
                     "documento di patch: impostare un valore è idempotente, aggiungere o "
                     "incrementare no.",
         rif=R % "I metodi, uno per uno"))

d(chiusa("c09-put-patch", CAP, "metodi HTTP",
         "Qual è la differenza fra `PUT` e `PATCH`?",
         "`PUT` invia lo stato completo che la risorsa deve assumere; `PATCH` applica una "
         "modifica parziale allo stato attuale.",
         ["`PUT` crea sempre una nuova risorsa; `PATCH` la cancella.",
          "`PUT` è sicuro; `PATCH` no.",
          "`PATCH` invia lo stato completo; `PUT` solo i campi da modificare.",
          "`PUT` si usa solo per i file; `PATCH` solo per i documenti JSON.",
          "Nessuna: sono due nomi dello stesso metodo."],
         spiegazione="Il corpo di una `PUT` contiene il nuovo stato completo della risorsa "
                     "all'URI indicato (che viene creata o sostituita): ripeterla non cambia "
                     "nulla, quindi è idempotente. `PATCH` descrive solo una modifica parziale, "
                     "e la sua idempotenza dipende dal tipo di modifica.",
         rif=R % "I metodi, uno per uno"))

d(chiusa("c09-etag", CAP, "codici di stato",
         "Un browser ha in cache una risorsa ricevuta con l'header `ETag: \"abc123\"`. Come può "
         "chiedere al server se è ancora valida, senza riscaricarla se non è cambiata?",
         "Inviando la richiesta con `If-None-Match: \"abc123\"`: se la risorsa non è cambiata il "
         "server risponde `304 Not Modified`, senza corpo.",
         ["Inviando `If-None-Match: \"abc123\"`: se la risorsa non è cambiata il server "
          "risponde `404 Not Found`.",
          "Inviando una `DELETE` della copia vecchia e poi una nuova `GET`.",
          "Inviando l'header `ETag: \"abc123\"`: il server risponde sempre `200 OK` con il "
          "corpo.",
          "Inviando `Cache-Control: no-store`: il server risponde `204 No Content`.",
          "Non può: deve sempre riscaricare la risorsa."],
         spiegazione="Il server associa a ogni versione di una risorsa un'etichetta, l'`ETag`. Il "
                     "client la rimanda con `If-None-Match`: se la risorsa non è cambiata, il "
                     "server risponde `304 Not Modified` senza ritrasmetterla (non è un errore: "
                     "«la tua copia è ancora buona»).",
         rif=R % "I metodi, uno per uno"))

d(chiusa("c09-query", CAP, "metodi HTTP",
         "Perché è stato introdotto il metodo HTTP `QUERY`?",
         "Per inviare un'interrogazione complessa nel corpo della richiesta mantenendo una "
         "semantica di sola lettura: sicura, idempotente e memorizzabile in cache.",
         ["Per sostituire `GET`, che è stato deprecato.",
          "Per modificare parzialmente una risorsa, come `PATCH` ma più veloce.",
          "Per interrogare il DNS direttamente da HTTP.",
          "Per permettere a `POST` di essere messa in cache.",
          "Per inviare query SQL direttamente al database del server."],
         spiegazione="Con `GET` l'interrogazione deve stare tutta nella query string, che ha "
                     "limiti di lunghezza e finisce nei log; con una `POST` si può usare il "
                     "corpo, ma la richiesta non è più né sicura né idempotente. `QUERY` unisce "
                     "le due cose: un corpo come la `POST`, la semantica di sola lettura della "
                     "`GET`.",
         rif=R % "I metodi, uno per uno"))

d(chiusa("c09-options", CAP, "metodi HTTP",
         "Prima di inviare una `POST` con corpo JSON a un altro dominio, il browser invia "
         "automaticamente una richiesta `OPTIONS`. A che cosa serve?",
         "È il *preflight* CORS: il browser chiede al server se quella richiesta è permessa "
         "dall'origine della pagina.",
         ["A scaricare l'elenco delle opzioni del form da inviare.",
          "A cifrare il corpo della richiesta prima dell'invio.",
          "A chiedere al server di creare la risorsa in anticipo.",
          "A misurare il tempo di risposta del server.",
          "A cancellare i cookie del dominio di destinazione."],
         spiegazione="`OPTIONS` chiede quali opzioni di comunicazione sono disponibili per una "
                     "risorsa; è sicuro e idempotente. I browser lo usano per il *preflight* "
                     "CORS: prima di una richiesta da un'altra origine chiedono al server se "
                     "metodo e header sono permessi.",
         rif=R % "I metodi, uno per uno"))

d(chiusa("c09-tls", CAP, "HTTPS",
         "Quali garanzie offre TLS a una comunicazione HTTPS?",
         ["Riservatezza: chi intercetta i dati lungo il percorso vede solo byte cifrati.",
          "Autenticazione del server, tramite un certificato firmato da un'autorità di cui il "
          "browser si fida.",
          "Integrità: il destinatario si accorge se i dati sono stati modificati in transito."],
         ["Che il gestore del sito sia onesto e affidabile.",
          "L'anonimato del client nei confronti del server.",
          "Che il server non subisca mai attacchi.",
          "Che la comunicazione sia più veloce di HTTP.",
          "Che i dati siano compressi."],
         multi=True,
         spiegazione="HTTPS è lo stesso HTTP dentro un canale TLS, che garantisce riservatezza, "
                     "autenticazione del server e integrità. Non dice nulla sull'onestà di chi "
                     "gestisce il sito: anche i siti di *phishing* hanno certificati validi e "
                     "mostrano il lucchetto.",
         rif=R % "HTTPS: HTTP dentro un canale TLS"))

d(chiusa("c09-ttfb", CAP, "HTTPS",
         "Nella sezione *Tempistiche* della scheda *Rete* dei DevTools, una richiesta ha una "
         "fase *In attesa* molto lunga. Che cosa indica?",
         "Che il server ha impiegato molto tempo a elaborare la richiesta prima di inviare il "
         "primo byte della risposta.",
         ["Che la risoluzione DNS è stata lenta.",
          "Che la negoziazione TLS è fallita.",
          "Che la risposta era molto grande da scaricare.",
          "Che la richiesta è rimasta in coda nel browser perché non c'era connessione.",
          "Che il browser ha impiegato molto tempo a disegnare la pagina."],
         spiegazione="*In attesa* è il tempo fra l'invio della richiesta e l'arrivo del primo "
                     "byte della risposta (*Time To First Byte*): il tempo di elaborazione del "
                     "server. DNS, connessione e TLS hanno barre proprie, e il tempo per "
                     "scaricare il corpo è la *Ricezione*.",
         rif=R % "Dal clic alla pagina: il viaggio completo"))

d(chiusa("c09-viaggio", CAP, "HTTPS",
         "Quando si fa clic su un link `https://` verso un sito mai visitato, in che ordine "
         "avvengono i passi seguenti?",
         "Analisi della URL, DNS, connessione (TCP o QUIC), TLS, richiesta, risposta.",
         ["DNS, analisi della URL, TLS, connessione, richiesta, risposta.",
          "Analisi della URL, connessione, DNS, richiesta, TLS, risposta.",
          "Analisi della URL, TLS, DNS, connessione, richiesta, risposta.",
          "Connessione, DNS, analisi della URL, richiesta, TLS, risposta.",
          "Analisi della URL, DNS, richiesta, connessione, TLS, risposta."],
         spiegazione="Dalla URL il browser ricava schema, host, porta e percorso; il DNS traduce "
                     "il nome in un indirizzo IP; solo allora può aprire la connessione verso "
                     "IP e porta, negoziare TLS (certificato e chiavi di sessione) e infine "
                     "inviare la richiesta e ricevere la risposta.",
         rif=R % "Dal clic alla pagina: il viaggio completo"))

# ----------------------------------------------------------------------
# Domande aperte
d(aperta("c09-a-trasporto", CAP, "TCP, UDP e QUIC",
         "Si confrontino TCP e UDP e si spieghi perché le versioni recenti di HTTP usano QUIC. "
         "Quali problemi di TCP risolve?",
         ["TCP: orientato alla connessione (handshake), affidabile (dati integri e in ordine), "
          "più lento per conferme e ritrasmissioni. UDP: senza connessione e senza garanzie, "
          "leggero.",
          "HTTP ha usato TCP per l'affidabilità; HTTP/3 usa QUIC, che implementa "
          "l'affidabilità sopra UDP.",
          "QUIC combina apertura della connessione e TLS (un round trip, zero riprendendo una "
          "connessione) ed evita l'*head-of-line blocking* con flussi separati.",
          "È implementato nel software applicativo, non nel kernel: si aggiorna più "
          "facilmente. Il modo di scrivere le richieste HTTP non cambia."],
         rif=R % "HTTP più da vicino"))

d(aperta("c09-a-metodi", CAP, "metodi HTTP",
         "Che cosa vuol dire che un metodo HTTP è *sicuro* e che è *idempotente*? Si "
         "classifichino i metodi principali e si spieghi perché queste proprietà sono utili.",
         ["Sicuro: di sola lettura, non chiede modifiche (`GET`, `HEAD`, `OPTIONS`, `QUERY`).",
          "Idempotente: più richieste identiche hanno lo stesso effetto di una sola (tutti i "
          "sicuri, più `PUT` e `DELETE`); conta lo stato del server, non la risposta.",
          "`POST` non è né sicuro né idempotente; per `PATCH` dipende dal tipo di modifica.",
          "Browser, proxy e librerie possono ripetere da soli le richieste idempotenti e mettere "
          "in cache le risposte alle richieste sicure; una `POST` ripetuta può creare un "
          "duplicato (e una `GET` non deve mai modificare lo stato)."],
         rif=R % "Metodi sicuri e idempotenti"))

d(aperta("c09-a-dns", CAP, "DNS",
         "Si descriva il funzionamento del DNS: com'è organizzato lo spazio dei nomi, chi "
         "risponde a una richiesta di risoluzione e come si evita di sovraccaricare la rete.",
         ["Traduce i nomi degli host in indirizzi IP: le persone ricordano nomi, la rete "
          "instrada verso indirizzi.",
          "Database distribuito e gerarchico: radice, TLD (`.it`, `.com`), domini di secondo "
          "livello e sottodomini; nessun server centrale.",
          "Il browser chiede a un resolver, che interroga il server root, poi quello del TLD, "
          "poi l'autoritativo del dominio, che conosce l'indirizzo.",
          "I risultati restano in cache (resolver e dispositivi) per la durata del TTL."],
         rif=R % "Dalla URL all'indirizzo: il DNS"))

d(aperta("c09-a-viaggio", CAP, "HTTPS",
         "Si descrivano i passi che il browser compie dal clic su un link `https://` alla "
         "visualizzazione della risposta, indicando quali si possono evitare nelle visite "
         "successive.",
         ["Analisi della URL (schema, host, porta, percorso); risoluzione DNS del nome in "
          "indirizzo IP.",
          "Apertura della connessione (TCP o QUIC) verso IP e porta; negoziazione TLS "
          "(certificato, chiavi di sessione).",
          "Invio della richiesta (metodo, destinazione, header, corpo); attesa ed elaborazione "
          "del server; ricezione della risposta (stato, header, corpo).",
          "Visite successive: DNS in cache, connessione persistente già aperta (niente "
          "connessione né TLS), risorse in cache verificate con `ETag` e `304`."],
         rif=R % "Dal clic alla pagina: il viaggio completo"))

# ----------------------------------------------------------------------
# Dalla prima prova intercorso del 2026
d(chiusa("c09-prova-http3", CAP, "TCP, UDP e QUIC",
         "Quale protocollo di trasporto viene utilizzato da HTTP/3?",
         "UDP, tramite il protocollo QUIC.",
         ["TCP, come nelle versioni precedenti di HTTP.",
          "ICMP, per ridurre la latenza delle comunicazioni.",
          "SCTP, per garantire la consegna ordinata dei pacchetti."],
         fisse=True,
         spiegazione="HTTP/3 viaggia su **QUIC**, che a sua volta usa UDP e implementa da sé "
                     "affidabilità, controllo di congestione e cifratura TLS, con flussi "
                     "indipendenti (niente *head-of-line blocking* fra un flusso e l'altro). "
                     "Le versioni precedenti usavano TCP; ICMP serve ai messaggi di controllo "
                     "della rete (come `ping`), SCTP non è usato dal Web.",
         rif=R % "QUIC", fonte=FONTE_2026))

d(chiusa("c09-prova-host", CAP, "messaggi HTTP",
         "In una richiesta HTTP/1.1 verso un origin server, quale header identifica l'host di "
         "destinazione?",
         "`Host`",
         ["`Origin`", "`User-Agent`", "`Referer`"],
         fisse=True,
         spiegazione="`Host` è obbligatorio in HTTP/1.1: contiene il nome (ed eventualmente la "
                     "porta) del server a cui è diretta la richiesta, e permette a un solo "
                     "indirizzo IP di ospitare molti siti. `Origin` indica l'origine della "
                     "pagina che ha avviato la richiesta, `Referer` la pagina da cui si arriva, "
                     "`User-Agent` il software del client.",
         rif=R % "La richiesta", fonte=FONTE_2026))

# ----------------------------------------------------------------------
# Domande a trabocchetto
_HEAD = """
import express from "express";
const app = express();
app.get("/pagina", (req, res) => {
  res.send("<html><head><title>T</title></head><body>Ciao</body></html>");
});
app.listen(3000);"""

d(chiusa("c09-head", CAP, "metodi HTTP",
         "L'applicazione Express seguente definisce soltanto una rotta `GET`. Che cosa riceve "
         "un client che invia `HEAD /pagina`?",
         "Lo stesso codice di stato e gli stessi header di `GET /pagina`, ma senza corpo.",
         ["Solo l'elemento `<head>` della pagina.",
          "`404`: la rotta gestisce soltanto `GET`.",
          "Il corpo della pagina, ma senza header.",
          "`405 Method Not Allowed`: il metodo non è previsto."],
         codice=L("js", _HEAD),
         spiegazione="`HEAD` chiede la stessa risposta di `GET` **senza il corpo**: serve, per "
                     "esempio, a sapere se una risorsa è cambiata o quanto è grande, senza "
                     "scaricarla. Non ha nulla a che vedere con l'elemento `<head>` dell'HTML. "
                     "Express risponde da sé alle richieste `HEAD` con le rotte `GET`.",
         rif=R % "I metodi, uno per uno", trabocchetto=True,
         verifica=dict(tipo="express", codice=L("js", _HEAD).sorgente,
                       richieste=[{"metodo": "HEAD", "percorso": "/pagina"},
                                  {"metodo": "GET", "percorso": "/pagina"}],
                       atteso=["200 ", "200 <html><head><title>T</title></head>"
                                       "<body>Ciao</body></html>"])))

d(chiusa("c09-dns-porta", CAP, "DNS",
         "Il browser apre `https://www.unina.it:8443/corsi/web`. Che cosa chiede al DNS?",
         "Solo l'indirizzo IP di `www.unina.it`: porta e percorso non riguardano il DNS.",
         ["L'indirizzo IP e la porta del servizio.",
          "L'indirizzo IP di `www.unina.it:8443`.",
          "L'indirizzo IP del server che ospita `/corsi/web`.",
          "Il certificato TLS del sito."],
         spiegazione="Il DNS traduce **nomi di host** in indirizzi IP, e basta: la porta è "
                     "scritta nella URL (o è quella predefinita dello schema), e il percorso "
                     "viene inviato al server nella richiesta HTTP. Il certificato arriva dal "
                     "server durante la negoziazione TLS.",
         rif=R % "Dalla URL all'indirizzo: il DNS", trabocchetto=True))

d(chiusa("c09-socket-client", CAP, "processi, socket e porte",
         "Un server web gestisce contemporaneamente le connessioni di due browser, entrambe "
         "sulla sua porta 443. Come distingue le due connessioni?",
         "Dall'indirizzo IP e dalla porta del client: ogni connessione ha il proprio socket.",
         ["Assegnando a ogni client una porta diversa del server.",
          "Non può: una porta accetta un solo client per volta.",
          "Dall'header `Host` delle richieste.",
          "Dal nome del browser nell'header `User-Agent`."],
         spiegazione="Una connessione TCP è identificata dalla coppia di estremi: indirizzo e "
                     "porta del server **e** indirizzo e porta del client (la porta del client "
                     "è scelta dal suo sistema operativo). Due browser, anche sullo stesso "
                     "computer, usano porte di origine diverse: il server ha un socket per "
                     "ciascuna connessione, tutte sulla stessa porta 443.",
         rif=R % "Il socket", trabocchetto=True))

d(chiusa("c09-https-visibile", CAP, "HTTPS",
         "Un utente visita `https://www.example.org/esami?matricola=123` da una rete Wi-Fi "
         "pubblica. Che cosa può vedere chi osserva il traffico della rete?",
         ["L'indirizzo IP e la porta del server.",
          "Quanti dati vengono scambiati, e quando."],
         ["Il percorso `/esami` e la query `matricola=123`.",
          "I cookie inviati con la richiesta.",
          "Il corpo della risposta.",
          "Gli header della risposta, come `Content-Type`."],
         multi=True,
         spiegazione="Con HTTPS l'intero messaggio HTTP viaggia dentro il canale TLS: riga di "
                     "richiesta (quindi percorso e query), header, cookie e corpo sono cifrati. "
                     "Restano visibili le informazioni necessarie a instradare i pacchetti "
                     "(indirizzi e porte) e la quantità e i tempi del traffico.",
         rif=R % "HTTPS: HTTP dentro un canale TLS", trabocchetto=True))

d(chiusa("c09-sicuro-idempotente", CAP, "metodi HTTP",
         "Quali delle seguenti affermazioni sui metodi HTTP sono **vere**?",
         ["Ogni metodo sicuro è anche idempotente.",
          "`DELETE` resta idempotente anche se la seconda richiesta risponde `404`.",
          "Un server può scrivere nel log una richiesta `GET` senza violarne la sicurezza."],
         ["Un metodo idempotente restituisce sempre la stessa risposta.",
          "`POST` diventa idempotente se il corpo è identico.",
          "`PUT` è sicuro, perché ripeterlo non cambia nulla.",
          "Un metodo sicuro non può mai modificare nulla sul server, nemmeno un contatore "
          "di visite."],
         multi=True,
         spiegazione="Sicuro vuol dire che il client **non chiede** modifiche: log e contatori "
                     "sono effetti collaterali di cui il client non è responsabile. Idempotente "
                     "vuol dire che ripetere la richiesta lascia il server nello **stesso "
                     "stato**, non che la risposta sia la stessa (la seconda `DELETE` risponde "
                     "`404`). Chi non modifica nulla è anche idempotente; `PUT` è idempotente "
                     "ma non sicuro.",
         rif=R % "Metodi sicuri e idempotenti", trabocchetto=True))
