# Dispensa di Tecnologie Web

Dispensa in italiano del corso di **Tecnologie Web** (prof. Bernardo Breve,
slide del prof. Luigi Libero Lucio Starace), Università degli Studi di Napoli
Federico II, corso di laurea in Informatica.

Copre **l'intero corso**: tutte le lezioni, più la lezione bonus su CMS e
GraphQL (inclusa come capitolo finale e segnalata come fuori programma).
26 capitoli, 456 pagine.

Il codice è quasi sempre accompagnato, **accanto**, da ciò che produce: il
rendering nel browser, l'output in console o nel terminale, oppure uno schema
(variabili e riferimenti in memoria, scope, alberi DOM, sequenze di richieste
e risposte, diagrammi di flusso, tabelle del database).

Ogni listato è disegnato come una piccola **finestra di Visual Studio Code** con
il tema scuro predefinito (Dark+): sfondo quasi nero, numeri di riga, colori
della sintassi del tema e, in alto, la scheda del file aperto con l'icona del
linguaggio.

La dispensa contiene **solo i contenuti tecnici** visti a lezione, cioè quelli
che possono essere oggetto d'esame. Le informazioni organizzative (crediti,
calendario, modalità d'esame, esercitazioni facoltative) sono deliberatamente
escluse: restano sulle slide e sul sito del docente, dove vengono aggiornate.

## Contenuto

| Percorso | Descrizione |
|---|---|
| `main.tex` | Documento principale: copertina, estratto, indice, inclusione dei capitoli |
| `preamble/webtech-preamble.tex` | Font, linguaggi per i listati, riquadro "browser", stili TikZ, correzioni alla classe |
| `chapters/1. Introduzione al Web.tex` | Internet e Web, ipertesti, HTTP, URL, messaggi, status code, statelessness |
| `chapters/2. HTML.tex` | Server HTTP, tag ed elementi, head e favicon, testo, link, tabelle, liste, riferimenti a caratteri, immagini, form, divisioni e `span`, tag semantici, DOM, DevTools (ispezione, scheda Rete, cache HTTP) |
| `chapters/3. CSS.tex` | Regole e loro applicazione, inclusione, stile inline, selettori, combinatori, pseudo-classi (compreso `:nth-child()` senza selettore di tipo), pseudo-elementi, cascata, specificità, ereditarietà |
| `chapters/4. Layout e Responsive Design.tex` | Unità di misura, box model (anche come lo mostrano i DevTools), display, float, positioning, Flexbox, Grid, media query, responsive design, meta viewport |
| `chapters/5. JavaScript.tex` | Inclusione, strict mode, variabili e scope, hoisting e TDZ, tipi, operatori, `==` contro `===`, funzioni, closure, oggetti, `this`, costruttori, optional chaining, getter/setter |
| `chapters/6. JavaScript avanzato.tex` | Prototipi ed ereditarietà, array, destrutturazione, iterabili, Map e Set, classi, gestione degli errori, moduli |
| `chapters/7. JavaScript nel browser.tex` | `window`, DOM e BOM, ricerca e navigazione dei nodi, modifica del DOM, eventi, bubbling e delegazione, ordine di esecuzione degli script |
| `chapters/8. Asincronismo e rete.tex` | Cookie e Web Storage, callback, Promise e concatenazione, API statiche, `async`/`await`, `fetch` |
| `chapters/9. Il Web sotto il cofano.tex` | Applicazioni di rete, client-server e P2P, processi e socket, IP e porte, protocolli applicativi, DNS, versioni di HTTP, TCP/UDP e QUIC, connessioni persistenti, metodi sicuri e idempotenti (GET, HEAD, POST, PUT, PATCH, DELETE, OPTIONS, QUERY), risposte e codici di stato, HTTPS e TLS, dal clic alla pagina e tempistiche nei DevTools |
| `chapters/10. Web statico e dinamico.tex` | Limiti del web statico, programmazione lato server, CGI (flusso, interfaccia con variabili d'ambiente, stdin e stdout, lista di cose da fare), scripting lato server, PHP, NGINX e PHP-FPM |
| `chapters/11. Node.tex` | Diffusione dei runtime (State of JS), modello multi-thread e I/O bloccante, event loop, installazione con nvm (Node.js 22.14.0), REPL, npm e `package.json` (`npm run`), primo server HTTP, debug in VS Code (Auto Attach, breakpoint, azioni di debug), nodemon |
| `chapters/12. Web app con Node.tex` | L'applicazione to-do e le sue tre pagine, routing, motori di template e Pug (con l'HTML generato dalle inclusioni), analisi del corpo delle richieste, l'applicazione completa (router, controller, template con layout comune, prove con `curl`, Post/Redirect/Get), estensione con la cancellazione (routing sul `pathname`, parametri della query, perché una GET non deve modificare lo stato) |
| `chapters/13. Sessioni.tex` | HTTP stateless e tracciamento della sessione, approccio ingenuo con i cookie (schema con due utenti, login con reindirizzamento `302`, `parseCookies`, contesto passato ai controller), manomissione dei cookie con i DevTools e loro limiti, sessioni web lato server (schema con due utenti e i dati di sessione), classe `Session` con una `Map` di `Map` e identificatori generati con `randomUUID`, sessioni in memoria e produzione, altri metodi di tracciamento |
| `chapters/14. CSS moderno.tex` | CSS moderno e adattivo: pseudo-classi funzionali (`:is()`, `:where()`, `:not()`, `:has()`) e la loro specificità, custom properties (`var()`, ereditarietà, `:root`, valori di riserva, `@property`), `calc()`, `min()`, `max()` e `clamp()`, unità `svh`, `lvh` e `dvh`, `gap` e la scorciatoia `flex` (`flex-grow`, `flex-shrink`, `flex-basis`), container query, immagini responsive (`srcset`, `<picture>` e art direction), media query sulle preferenze dell'utente, `@supports`, annidamento nativo e selettore `&` |
| `chapters/15. Express.tex` | Framework e inversione del controllo (schema a passi numerati), opinionated e no, Express 5.3.0 con output reali (`curl -i`, log del server): routing, percorsi delle rotte e differenze fra Express 4 ed Express 5 (`PathError`, sintassi `{}` e `*nome`), parametri di rotta e gruppi con nome, più gestori, `app.route()` e router modulari, risposte e template Pug con `res.locals`, ciclo richiesta-risposta, middleware, errori sincroni e asincroni, gestori personalizzati, Promise in Express 5 e il crash di Express 4, `express.static`, `urlencoded`, `json`, `express-session` (cookie firmato), `cookie-parser` (cookie manomesso), messaggi flash con `connect-flash` |
| `chapters/16. Web app con Express.tex` | ORM (oggetti e tabelle) e Sequelize 6 con SQLite, tutto eseguito davvero e con i log SQL reali: connessione, modelli, sincronizzazione (`force`, `alter`), creazione di entità e query parametriche, modelli come classi e associazioni (chiave esterna `UserId`), dati collegati e annidati, `findAll` con `Op`, `include` e `findByPk`, modifica ed eliminazione, pro e contro degli ORM; organizzazione di un'app Express, configurazione con `.env` e `dotenv` (precedenza delle variabili d'ambiente); la lista di cose da fare con Express e Sequelize (modelli, middleware, rotte con `'/*splat'`, router, controller, autenticazione, una sessione di lavoro con il log di `morgan`, la trappola di `router.use` senza percorso e il rimedio). Quattro sviste delle slide segnalate (`firstName`/`name`, `console.err`, apici tipografici, `true`/`false`) |
| `chapters/17. REST.tex` | Limiti delle web app tradizionali e contesto architetturale (client di ogni tipo, server che interrogano altri server), API e stile REST, rappresentazioni JSON e XML, verbi e URI, risorse annidate; i quattro archetipi di risorse (document, collection, store, controller) con le loro regole di nomenclatura; filtri e paginazione nella query string (come li consegna Express) e ricerche complesse con un controller; autenticazione con token e JWT con prove reali (il token delle slide decodificato, la firma HMAC ricalcolata a mano, payload alterato, chiave sbagliata, token scaduto), HS256 e RS256, il logout senza sessione, funzioni di hash (i digest delle slide verificati con `sha256sum`); l'API REST della lista di cose da fare con Express 5.3.0, Sequelize, `jsonwebtoken` 9.0.3 e `cors`, eseguita davvero (`curl -i` e `-v`, log di `morgan`): `201` con `Location`, `204`, `401`, `403`, filtro e paginazione con la query SQL generata, e cinque ritocchi verificati (la password nella risposta di `/signup`, un `403` al posto del `404`, gli `undefined` nel log, il `Content-Type` dimenticato, il `404` in HTML); regole e linee guida (Massé, RESTRuler); OpenAPI con `swagger-jsdoc` 6.3.0 e `swagger-ui-express` 5.0.1 (la specifica generata dalle annotazioni, Swagger UI ridisegnata dal vero). Tre sviste delle slide segnalate (i dati «dell'esame», i campi `user`/`pws` e il `{"token": …}` del diagramma) |
| `chapters/18. API in produzione.tex` | Dalle API che funzionano alle API pronte per la produzione, con Express 5.3.0, Spring Boot 4.1.2 e Django Ninja 1.8.0 eseguiti davvero: la struttura degli oggetti di una specifica OpenAPI e la validazione con Redocly CLI; l'API come contratto, modifiche compatibili e non retrocompatibili, versionamento nell'URI e negli header (`Accept` con un tipo *vendor* e `Vary`), ciclo di vita delle versioni e header `Deprecation`, `Sunset` e `Link`; l'OWASP API Security Top 10 (2023), con la BOLA mostrata sull'API del capitolo 17, il rate limiting con `express-rate-limit` 8.7.4 (header `RateLimit` della bozza 8), il throttling di Django Ninja e Bucket4j, una SSRF che raggiunge davvero un servizio interno, le tracce degli errori in sviluppo e in produzione, un formato coerente per gli errori; osservabilità con Spring Boot Actuator (stato di salute, metriche, il conteggio dei `429`), un `/health` che risponde `503` e che cosa scrivere (e non scrivere) nei log. Sei sviste delle slide segnalate (`produces` di Swagger 2.0, `Deprecation: true` invece della data della RFC 9745, giovedì 31 dicembre 2026 scritto `Wed`, `create_response` senza `status`, che solleva `AssertionError`, il commento «100 richieste in 15 minuti» accanto a `limit: 10`, `Bandwidth.classic` e `Refill` deprecati in Bucket4j 8) |
| `chapters/19. TypeScript.tex` | Transpiler, tipi, unioni, interfacce, generici, livelli di severità |
| `chapters/20. Frontend Tooling.tex` | Sass, framework CSS, bundling, tree shaking, minificazione, Vite |
| `chapters/21. Single Page App.tex` | Routing lato client, componenti, Web Components API |
| `chapters/22. Angular.tex` | Componenti, template, eventi, `@Input`/`@Output`, Router |
| `chapters/23. Angular avanzato.tex` | Form, servizi e DI, guardie, HttpClient, Observable, signal, la SPA completa |
| `chapters/24. Sicurezza.tex` | XSS, CSRF, SQL injection, session hijacking, same-origin policy e CORS |
| `chapters/25. Testing.tex` | Piramide del testing, Jasmine, test double, E2E, fragilità e flakiness, Playwright |
| `chapters/26. CMS e GraphQL.tex` | *(fuori programma)* CMS tradizionali e headless, Strapi, GraphQL, siti statici |
| `unina_doc_class.cls` | Classe di documento (ripresa dalle *Dispense APA*, non modificata) |
| `fonts/` | Font usati dalla classe (Lato, Gobold, FiraCode, Lora, IcoMoon, …) |
| `sources/` | Logo dell'ateneo, risorse della copertina, immagine di Fu-Tzu (`fu-tzu.jpg`, dalle slide) |
| `build.ps1` | Script di compilazione |
| `DispensaWebTech.pdf` | PDF già compilato |
| `prove/` | Generatore di simulazioni della prova intercorso (capitoli 1–16, fino a Express incluso) nello stile delle prove del corso, con le soluzioni; prove d'esempio in `prove/generate/`. Vedi `prove/README.md` |

## Simulazioni della prova intercorso

La cartella `prove/` contiene un generatore di prove nello stile della prova
intercorso (8 domande chiuse da 2 punti e 3 aperte da 5, 45 minuti), con il
programma fino a Express incluso. Ogni prova ha il suo PDF di soluzioni, con le
spiegazioni e il rimando alla sezione della dispensa. Le domande con codice sono
verificate eseguendolo davvero (Node.js, Chromium, Pug, Express). In
`prove/generate/` ci sono già dieci prove con le soluzioni e la raccolta di
tutte le domande; per generarne altre:

```bash
cd prove
python3 genera_prova.py --id 11 --quante 10
```

## Come compilare

Serve **LuaLaTeX** (la classe usa `fontspec` e `luacode`, quindi `pdflatex` non
funziona). Da PowerShell, nella cartella del progetto:

```bash
powershell -ExecutionPolicy Bypass -File build.ps1
```

Lo script esegue tre passate (contenuto → indice → riferimenti incrociati) e
cerca automaticamente `lualatex` nelle posizioni tipiche di MiKTeX e TeX Live se
non è nel `PATH`.

Su Linux, se l'archivio è stato estratto con i nomi di Windows (file chiamati
letteralmente `chapters\2. HTML.tex` invece di una cartella `chapters`),
occorre prima ricreare le cartelle `chapters`, `preamble`, `fonts` e `sources`,
per esempio con dei collegamenti simbolici in una cartella di compilazione.

In alternativa, manualmente:

```bash
lualatex main.tex && lualatex main.tex && lualatex main.tex
```

### Su Overleaf

Caricare l'intero contenuto della cartella, poi in *Menu → Compiler*
selezionare **LuaLaTeX**. Nessuna altra configurazione è necessaria.

## Convenzioni tipografiche

- riquadri **verdi** (`\info`): approfondimenti e osservazioni;
- riquadri **gialli** (`\warning`): avvertenze ed errori tipici;
- riquadri **rossi** (`\error`): anti-pattern da evitare;
- riquadri **Definizione** (`\dfn`): definizioni formali;
- blocchi **Esempio** (`esempio`): numerati per capitolo, con codice commentato;
- ambiente `browser`: finestra stilizzata che mostra il rendering approssimato
  del codice HTML appena presentato;
- ambiente `affianco`: codice a sinistra e risultato a destra, in un blocco che
  non si divide mai fra due pagine (vedi sotto);
- ambiente `devtools`: finestra dei DevTools, con i pannelli *Regole* e *Rete*
  (e *Archiviazione*, la scheda dei cookie, che compare solo quando è attiva);
- ambiente `console`: console dei DevTools, per l'output di uno script. Ogni
  riga del sorgente è una riga di output (niente `\\` da scrivere a mano);
- ambiente `immagine`: uno schema TikZ nella colonna del risultato, centrato e
  ridotto alla larghezza della colonna se serve, con una didascalia breve
  facoltativa (`\begin{immagine}[didascalia]`).

> **Attenzione:** `\info`, `\warning` e `\error` sono **macro**, quindi non
> possono contenere un `lstlisting` (un ambiente verbatim non sopravvive
> dentro l'argomento di una macro). Quando in un riquadro serve del codice,
> si usa la forma ambiente: `\begin{warningbox}{{Titolo}} ... \end{warningbox}`
> (doppie graffe per proteggere eventuali virgole nel titolo).

Macro utili definite nel preambolo:

| Macro | Effetto |
|---|---|
| `\code{...}` | codice inline non spezzabile |
| `\tg{p}` | rende `<p>` |
| `\attr{href}` | nome di attributo |
| `\term{...}` | termine tecnico evidenziato |
| `\urlx{...}` | URL spezzabile in stile codice |

### Codice e risultato affiancati

```latex
\begin{affianco}[0.55]          % frazione della riga per il codice
\begin{lstlisting}[style=html, name=index.html]
...
\end{lstlisting}
\risultato                       % da qui in poi: colonna destra
\begin{browser}[index.html]
...
\end{browser}
\wtnota{Nota breve sotto il risultato}
\end{affianco}
```

Nella colonna del codice possono stare più listati; `\codicepiccolo` (subito
dopo `\begin{affianco}`) riduce il carattere per le righe lunghe. Per disegnare
il risultato ci sono i controlli dei form come li mostra un browser
(`\wtcampo`, `\wtbottone`, `\wtcasella`, `\wtradio`, `\wttendina`,
l'ambiente `wtfieldset`), `\wtlink` e `\wtsopra` per i link, e i colori CSS
con il loro valore esatto (`css-red`, `css-blue`, `css-hotpink`, …), da usare
al posto degli omonimi di xcolor, ridefiniti dalla classe.

Con il secondo argomento facoltativo, `\begin{affianco}[0.5][c]`, le due
colonne sono centrate in verticale invece che allineate in alto: è la forma
usata quando a destra c'è uno schema più basso del codice.

### Schemi accanto al codice

Nel preambolo c'è un piccolo vocabolario TikZ per gli schemi, usato in tutta la
dispensa perché abbiano lo stesso aspetto:

| Macro / stile | Disegna |
|---|---|
| `\variabile{id}{(pos)}{nome}{valore}` | una variabile: nome e casella del valore |
| `\oggetto{id}{(pos)}{larghezza}{titolo}{chiave/valore, ...}` | un oggetto in memoria, con le sue proprietà (la colonna delle chiavi si allarga da sé) |
| `\riferimento{da}{percorso}` | un riferimento: pallino e freccia verso l'oggetto |
| `\scopo{livello}{nome}{etichetta}{(nodi)}` | il riquadro di uno scope, annidabile su tre livelli |
| `\celle{id}{(pos)}{v0, v1, ...}` | le caselle consecutive di un array, con gli indici (`\mvuota` per un buco) |
| `\dbtabella{id}{(pos)}{nome}{colonne}{righe}` | una tabella del database |
| `\wtdialogo[campo]{messaggio}{pulsanti}` | una finestra `alert`/`confirm`/`prompt` |
| `\wttoast[tipo]{titolo}{messaggio}` | una notifica di ngx-toastr (`success`, `error`, `warning`, `info`) |
| `\ctabella{...}` | il risultato di `console.table` nei DevTools |
| `\pic {utente=colore}`, `wtserver`, `wtrotta`, `wtdatabase`, `wtreq`, `wtrisp`, `wtmsg` | gli scambi numerati di richieste e risposte: utenti, application server con le sue rotte, database, frecce e testo dei messaggi |
| `mdom`, `mtesto`, `mcommento`, `mnuovo`, `mramo` | nodi e rami di un albero DOM |
| `mfun`, `mvar`, `mnota`, `mcod`, `mrif`, `mcerca` | funzioni, caselle, note, codice e frecce negli schemi |

`\mok` e `\merr` sono il segno di spunta verde e la croce rossa.

Per i listati: `\begin{lstlisting}[style=html, name=file.html]`. Gli stili
disponibili sono `html`, `css`, `js`, `ts`, `pug`, `php`, `json`, `shell`, `java`, `python`, `xml`,
`sql`, `http` e `plain`. Il `name` compare nella scheda in alto, accanto
all'icona del linguaggio scelta dallo stile; se omesso, la finestra non ha la
barra delle schede.

## Note

- Le figure sono ridisegnate in **TikZ**, quindi vettoriali e in italiano; non
  sono ritagli dalle slide originali.
- Autore e anno accademico si cambiano nelle prime righe di `main.tex`.

### Modifiche alla configurazione dei listati

Tutte in `preamble/webtech-preamble.tex`, la classe non è stata toccata.

- **Legature FiraCode disattivate.** Senza questa modifica `<!--` verrebbe reso
  come `<!—` e `-->` come `—>`, cioè non quello che va effettivamente digitato.
- **`mathescape` disattivato.** La classe lo abilita, ma in un listato CSS il
  `$` è un carattere legittimo (per esempio nel selettore `[href$='.it/']`) e
  non deve aprire la modalità matematica.
- **Aspetto `html` di listings caricato** con `\lstloadaspects{html}`: senza,
  le chiavi `tag`, `tagstyle`, `markfirstintag` e `usekeywordsintag` non
  esistono.
- **Listati come finestre di VS Code (tema Dark+).** Sfondo `#1E1E1E`, numeri
  di riga grigi, cornice di spessore nullo che allarga lo sfondo attorno al
  codice; i margini sono calcolati da `\wtvscmargini{sinistro}{destro}` perché
  la finestra occupi esattamente la riga (o la colonna di `affianco`).
  Il titolo del listato (`captionpos=t`) è ridisegnato in TikZ come barra delle
  schede: `\lst@maketitle` è sostituito a inizio documento, dopo che il
  pacchetto caption ha messo il suo. L'icona viene dalla chiave `vscicon`,
  impostata da ciascuno stile.
- **Colori della sintassi per classi di parole chiave.** Listings non conosce
  la grammatica dei linguaggi, quindi le categorie del tema sono elenchi fissi:
  blu per dichiarazioni e valori (`const`, `this`, `true`), viola per il
  controllo del flusso (`if`, `return`, `await`), giallo per le funzioni,
  verde acqua per classi e tipi, azzurro chiaro per tutti gli altri
  identificatori. VS Code colora di giallo ogni nome seguito da `(`: l'elenco
  delle funzioni contiene i nomi che negli esempi sono (quasi) sempre chiamate.
- **Codice in corpo 7,5** (6,6 con `\codicepiccolo`). La colonna dei numeri
  toglie spazio orizzontale: con il corpo un po' ridotto nessuna riga va a capo,
  come prima dell'introduzione dei numeri, e la dispensa ha lo stesso numero di
  pagine.
- **Ogni listato riparte dalla riga 1** (`firstnumber=1`): altrimenti listings
  prosegue la numerazione dei listati precedenti con lo stesso `name`.
- **Barra delle schede solo quando c'è `name`.** La chiave `title` rende la
  didascalia non vuota per tutti i listati; `everydisplay`, che listings esegue
  appena prima di disegnare il titolo, la svuota quando manca il nome. (Un hook
  `InitVars` non va bene: arriva dopo il titolo in alto.)
- **Titoli dei riquadri protetti** (`\info`, `\warning`, `\error`): la classe
  passa il titolo a tcolorbox come `title=#1`, quindi una virgola nel titolo
  verrebbe letta come separatore di chiavi.
- **Numerazione di esempi ed esercizi** riagganciata al capitolo: con
  `secnumdepth=0` il contatore di sezione non avanza mai, e le etichette
  sarebbero uscite come "Esempio 1.0.3".

- **Sostituzioni «legatura» disattivate in tutti i listati** (`literate={}`).
  Lo stile `FiraCodeStyle` del pacchetto `lstfiracode`, caricato dalla classe,
  tiene unite le coppie di caratteri che Fira Code disegna come legature
  (`</`, `-->`, `--`, `#!`...): così listings non riconosceva i tag di
  chiusura HTML, i commenti `--` di SQL e la riga `#!/bin/bash` degli script.
  Nel linguaggio `HTML5`, inoltre, il commento va dichiarato *dopo* il tag,
  altrimenti `<!--` apre un tag.
- **Prima classe di parole chiave predisposta nel preambolo**
  (`\lstset{keywords={}}`): il nome del tag HTML prende il suo stile, che
  listings crea solo al primo listato con parole chiave; se il primo listato
  del documento fosse HTML la compilazione si fermerebbe.
- **Il codice non si spezza fra due pagine.** Ogni `lstlisting` è chiuso in
  una minipage tramite gli hook `env/lstlisting/before` e `after`: se non entra
  in fondo alla pagina, passa per intero alla successiva. Il listato più lungo
  della dispensa ha 38 righe, quindi sta sempre in una pagina.
- **Titolo degli esempi attaccato al contenuto** (`\nopagebreak` nell'ambiente
  `esempio`), perché non resti da solo in fondo alla pagina.
- **I riquadri di spiegazione non si spezzano fra due pagine.** La classe li
  dichiara `breakable`, e così venivano tagliati a metà frase, senza bordo
  inferiore e senza titolo nella pagina successiva. Nel preambolo la chiave
  `breakable` di tcolorbox è ridefinita perché equivalga a `unbreakable`: un
  riquadro che non entra passa intero alla pagina dopo, come i listati.
- **Il codice inline non esce dal margine.** `\code` è chiuso in un `\mbox`
  e non si spezza: `\emergencystretch=3em` lascia a TeX un po' di spazio in
  più nelle righe che altrimenti sforerebbero. Per i frammenti lunghi con
  spazi interni (header HTTP, firme di metodi) si usa `\codel`, che può andare
  a capo.

- **Nessun concetto si divide fra due pagine** (in fondo al preambolo):
  - la frase che introduce un listato, una figura, una tabella, una lista o un
    risultato (`console`, `browser`, `devtools`, `affianco`) resta attaccata a
    ciò che introduce;
  - paragrafi e liste non si spezzano mai;
  - un titolo va a pagina nuova se sotto non c'è spazio per qualche riga
    (`\Needspace`);
  - ogni `esempio`/`esercizio` viene composto in una scatola e, se sta in una
    pagina, non si spezza (se fosse più lungo di una pagina si spezzerebbe
    normalmente).

  - ogni blocco da un titolo di sezione o sottosezione al successivo, se sta
    in una pagina, non si spezza: le posizioni di inizio e fine vengono
    salvate nel file `.aux` e alla compilazione successiva il blocco, se non
    entra, passa intero alla pagina dopo. Le altezze misurate restano
    memorizzate (`\wtmem` nel `.aux`) perché l'impaginazione non oscilli:
    servono **più compilazioni** (5-6 partendo da zero) perché si stabilizzi.
    Dopo modifiche importanti alla struttura dei capitoli conviene cancellare
    `main.aux` e ricompilare da capo;
  - il titolo di una sezione seguito subito da una sottosezione viaggia
    insieme a essa (`\wtsegue` nel `.aux`), così non resta da solo in fondo
    alla pagina quando la sottosezione passa alla pagina successiva.

  Il prezzo è qualche spazio bianco in più in fondo alle pagine.

### Una trappola da conoscere

In una colonna `p{...}` di `tabular`, una cella che **inizia** direttamente con
`\code{...}` fa scendere la prima riga rispetto alla colonna accanto. Basta
anteporre un `\mbox{}` (vedi la tabella `em`/`rem` nel capitolo 4).
