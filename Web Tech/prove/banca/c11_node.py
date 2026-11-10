"""Capitolo 11: Node.js (modello multi-thread ed event loop, differenze con
il browser, npm e package.json, un server HTTP, strumenti di sviluppo)."""

from generatore import FONTE_2024, L, aperta, chiusa, uscita_js

CAP = 11
R = "cap. 11, «%s»"
NODE = "Qual è l'output dell'esecuzione del seguente modulo con Node.js?"

DOMANDE = []
d = DOMANDE.append

# ----------------------------------------------------------------------
d(uscita_js("c11-readfile", CAP, "il modello di Node.js",
            """
import fs from "fs";

console.log("inizio");
fs.readFile("dati.txt", "utf8", (err, testo) => console.log("asincrono:", testo));
const t = fs.readFileSync("dati.txt", "utf8");
console.log("sincrono:", t);
console.log("fine");""",
            ["inizio", "sincrono: ciao", "fine", "asincrono: ciao"],
            [["inizio", "asincrono: ciao", "sincrono: ciao", "fine"],
             ["inizio", "sincrono: ciao", "asincrono: ciao", "fine"],
             ["inizio", "fine", "asincrono: ciao", "sincrono: ciao"],
             ["inizio", "fine", "sincrono: ciao", "asincrono: ciao"],
             ["inizio", "sincrono: undefined", "fine", "asincrono: ciao"]],
            testo=NODE + " Il file `dati.txt` esiste e contiene la stringa `ciao`.",
            modulo=True, file={"dati.txt": "ciao"},
            spiegazione="`fs.readFile` è asincrona: avvia la lettura, che procede fuori dal thread "
                        "di JavaScript, e ritorna subito; la callback viene eseguita dall'event "
                        "loop dopo la fine del codice sincrono. `fs.readFileSync` invece blocca "
                        "l'esecuzione finché il file non è stato letto, e restituisce il "
                        "contenuto. In Node.js le operazioni sincrone sono l'eccezione.",
            rif=R % "Il modello di Node.js"))

d(uscita_js("c11-cpu", CAP, "il modello di Node.js",
            """
setTimeout(() => console.log("timer"), 0);
const fine = Date.now() + 300;
while (Date.now() < fine) { }      // un calcolo lungo e sincrono
console.log("calcolo finito");""",
            ["calcolo finito", "timer"],
            [["timer", "calcolo finito"], ["calcolo finito"], ["timer"], []],
            testo="Qual è l'output dell'esecuzione del seguente frammento con Node.js?",
            spiegazione="Il codice JavaScript gira in un solo thread: un calcolo lungo e sincrono "
                        "occupa l'event loop, e la callback del timer, pur scaduta, può essere "
                        "eseguita solo quando lo stack si svuota. Su un server, lo stesso calcolo "
                        "bloccherebbe **tutte** le richieste, non solo la propria.",
            rif=R % "Il modello di Node.js"))

d(chiusa("c11-node", CAP, "che cos'è Node.js",
         "Quali delle seguenti affermazioni su Node.js sono **vere**?",
         ["È un ambiente di esecuzione JavaScript basato sul motore V8 di Google.",
          "Adotta un modello di I/O basato sugli eventi e non bloccante.",
          "Il codice JavaScript di un'applicazione viene eseguito in un solo thread.",
          "Le operazioni di I/O vere e proprie sono affidate a worker interni al runtime."],
         ["Crea un nuovo thread per ogni richiesta HTTP che riceve.",
          "È un framework per scrivere applicazioni web, come Express.",
          "È un linguaggio di programmazione derivato da Java.",
          "Rende parallelo il codice JavaScript sui core della CPU.",
          "Mette a disposizione gli oggetti `window` e `document`."],
         multi=True,
         spiegazione="Node.js è un *runtime* JavaScript (motore V8) con I/O asincrono e non "
                     "bloccante. Il nostro codice gira in un unico thread, l'event loop; l'I/O "
                     "è delegato ai worker del runtime, e la sua callback torna all'event loop. "
                     "Express è un framework costruito su Node.js; DOM e BOM non esistono fuori "
                     "dal browser.",
         rif=R % "Che cos'è Node.js"))

d(chiusa("c11-multithread", CAP, "il modello multi-thread",
         "In un application server che dedica un thread del pool a ogni richiesta, perché il "
         "modello è inefficiente quando le richieste fanno molto I/O (database, file, API "
         "esterne)?",
         "Perché i thread passano gran parte del tempo bloccati ad aspettare la fine delle "
         "operazioni di I/O, e il pool limita il numero di richieste servibili insieme.",
         ["Perché i thread non possono accedere al database contemporaneamente.",
          "Perché ogni thread deve compilare di nuovo il codice dell'applicazione.",
          "Perché i thread condividono un unico socket e devono fare a turno.",
          "Perché il sistema operativo esegue un solo thread per volta su ogni processore.",
          "Perché ogni thread apre una nuova connessione TCP verso il client."],
         spiegazione="Nel modello multi-thread un thread resta legato alla sua richiesta anche "
                     "mentre aspetta l'I/O (il cameriere fermo al tavolo). Il pool ha dimensione "
                     "fissa: le richieste concorrenti non possono superarla. Node.js usa invece "
                     "un solo thread che non aspetta mai: l'I/O procede altrove e la callback "
                     "arriva come evento.",
         rif=R % "Il modello multi-thread"))

d(chiusa("c11-differenze", CAP, "che cos'è Node.js",
         "Quali dei seguenti oggetti e moduli sono disponibili in un programma Node.js?",
         ["Il modulo `fs`, per leggere e scrivere file.",
          "Il modulo `http`, per creare un server.",
          "La funzione `setTimeout`.",
          "L'oggetto `console`."],
         ["L'oggetto `document`.", "L'oggetto `window`.", "L'oggetto `localStorage`.",
          "La funzione `alert`."],
         multi=True,
         spiegazione="Node.js e il browser condividono il linguaggio, non l'ambiente: in Node "
                     "mancano il DOM, il BOM e le API della piattaforma web (`document`, "
                     "`window`, `localStorage`, `alert`), ma c'è una libreria standard con "
                     "moduli per il filesystem e la rete. Timer e console esistono in entrambi.",
         rif=R % "Differenze rispetto all'ambiente browser"))

d(chiusa("c11-npm-run", CAP, "npm e package.json",
         "Nel `package.json` di un progetto la proprietà `scripts` contiene l'attività "
         "`\"build\": \"node build.js\"`. Con quale comando la si esegue?",
         "`npm run build`",
         ["`npm build`", "`node build`", "`npm install build`", "`npm start build`",
          "`node package.json build`"],
         spiegazione="Le attività definite in `scripts` si eseguono con `npm run <nome>`; solo "
                     "per quelle standard, come `start` e `test`, basta `npm <nome>`.",
         rif=R % "Creare un pacchetto"))

d(chiusa("c11-package", CAP, "npm e package.json",
         "Quali delle seguenti affermazioni su npm e sul file `package.json` sono **vere**?",
         ["`npm install <pacchetto>` aggiunge il pacchetto alla sezione `dependencies`.",
          "Le dipendenze vengono scaricate nella cartella `node_modules`, insieme alle loro "
          "dipendenze.",
          "`\"type\": \"module\"` abilita la sintassi `import`/`export` dei moduli ES.",
          "La cartella `node_modules` non va messa sotto controllo di versione: si ricostruisce "
          "con `npm install`."],
         ["`node_modules` va versionata, perché senza non si può ricostruire il progetto.",
          "`npm install` scarica solo il pacchetto richiesto, non le sue dipendenze.",
          "`package.json` contiene il codice dell'applicazione.",
          "`\"main\"` indica il comando da eseguire con `npm start`.",
          "Le dipendenze vengono installate nella cartella del sistema, comune a tutti i "
          "progetti."],
         multi=True,
         spiegazione="`package.json` descrive il pacchetto (come il `pom.xml` di Maven): nome, "
                     "versione, file principale (`main`), tipo di moduli, attività (`scripts`) e "
                     "dipendenze. npm scarica le dipendenze, ricorsivamente, in `node_modules`, "
                     "che si ricostruisce da `package.json` e per questo resta fuori dal "
                     "controllo di versione.",
         rif=R % "npm: il gestore di pacchetti"))

d(chiusa("c11-server", CAP, "un server HTTP con Node.js",
         "Si consideri il seguente server. Quando viene eseguita la funzione passata a "
         "`createServer`?",
         "Ogni volta che arriva una richiesta: è una callback, invocata dall'event loop.",
         ["Una sola volta, all'avvio del server.",
          "Una volta al secondo, finché il server resta acceso.",
          "Solo per la prima richiesta: le successive ricevono la stessa risposta.",
          "Quando viene chiamata `listen`, per ciascuna porta.",
          "Solo per le richieste `POST`."],
         codice=L("js", """
import http from 'http';

let server = http.createServer(function (request, response) {
  response.writeHead(200, { "Content-Type": "text/html" });
  response.end(`<p>Sono le ${new Date().toTimeString()}</p>`);
});
server.listen(3000);"""),
         spiegazione="`createServer` registra la funzione come gestore delle richieste: "
                     "l'event loop la invoca a ogni richiesta, e la pagina viene costruita ogni "
                     "volta (qui con l'ora corrente). Non c'è alcun file HTML sul disco.",
         rif=R % "Una prima applicazione web con Node.js"))

d(chiusa("c11-nodemon", CAP, "strumenti di sviluppo",
         "A che cosa serve `nodemon`?",
         "A riavviare automaticamente il server quando cambia il codice sorgente.",
         ["A installare e cambiare le versioni di Node.js.",
          "A monitorare il traffico di rete del server.",
          "A eseguire il server in più processi paralleli.",
          "A scaricare le dipendenze mancanti all'avvio.",
          "A mostrare le variabili in scope durante il debug."],
         spiegazione="Durante lo sviluppo, `nodemon app.js` al posto di `node app.js` sorveglia i "
                     "file (`js`, `mjs`, `cjs`, `json`) e riavvia il processo a ogni modifica "
                     "(*live reloading*). Per le versioni di Node si usano gestori come `nvm`.",
         rif=R % "Ricaricamento automatico"))

# ----------------------------------------------------------------------
# Domande aperte
d(aperta("c11-a-multithread", CAP, "il modello multi-thread",
         "Quali sono gli svantaggi (se ve ne sono) dell'utilizzo di un approccio "
         "*multi-threaded request handling* per un'applicazione web che effettua frequenti "
         "accessi in lettura/scrittura a un database? Motivare la risposta.",
         ["Ogni richiesta occupa un thread (o processo) del pool per tutta la sua durata, anche "
          "mentre attende le operazioni di I/O sul database.",
          "Con accessi frequenti i thread passano la maggior parte del tempo bloccati: "
          "inefficienza (memoria e risorse spese per aspettare).",
          "Scalabilità limitata: il pool ha dimensione fissa, e non si servono più richieste "
          "concorrenti di quanti sono i thread (il ristorante con un cameriere per tavolo).",
          "Alternativa: modello a eventi con I/O non bloccante (Node.js): un thread non aspetta "
          "mai, l'I/O procede altrove e la sua callback torna all'event loop."],
         rif=R % "Il modello multi-thread", fonte=FONTE_2024))

d(aperta("c11-a-event-loop", CAP, "il modello di Node.js",
         "Si descriva il modello di esecuzione di Node.js, spiegando per quali applicazioni è "
         "adatto e per quali no.",
         ["Un unico processo: il codice JavaScript gira in un solo thread, l'event loop, che "
          "preleva un evento alla volta dalla coda e ne esegue il gestore.",
          "Le operazioni di I/O sono asincrone: vengono affidate ai worker del runtime, e "
          "l'event loop passa subito all'evento successivo; a operazione conclusa la callback "
          "torna in coda.",
          "Adatto ai carichi dominati dall'I/O (molte richieste che aspettano database, file, "
          "rete): un solo thread ne serve moltissime.",
          "Poco adatto ai carichi dominati dalla CPU: un calcolo lungo e sincrono blocca "
          "l'event loop e quindi tutte le richieste."],
         rif=R % "Il modello di Node.js"))

d(aperta("c11-a-npm", CAP, "npm e package.json",
         "Che cos'è npm? Si descrivano il ruolo del file `package.json` e della cartella "
         "`node_modules`, e si spieghi perché `node_modules` non va aggiunta al controllo di "
         "versione.",
         ["npm è il gestore di pacchetti di Node.js, installato insieme al runtime, con il più "
          "grande repository di pacchetti per un singolo linguaggio.",
          "`package.json` (creato da `npm init`) descrive il pacchetto: nome, versione, file "
          "principale (`main`), `\"type\": \"module\"` per usare `import`/`export`, gli "
          "`scripts` eseguibili con `npm run <nome>` (`npm start`, `npm test`) e le "
          "dipendenze.",
          "`npm install <pacchetto>` aggiunge la dipendenza a `dependencies` e la scarica in "
          "`node_modules`, insieme alle sue dipendenze (ricorsivamente).",
          "`node_modules` si ricostruisce con `npm install` a partire da `package.json`: "
          "basta versionare il proprio codice e il descrittore."],
         rif=R % "npm: il gestore di pacchetti"))
