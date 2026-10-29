# Dispensa di Tecnologie Web

Dispensa in italiano del corso di **Tecnologie Web** (prof. Bernardo Breve,
slide del prof. Luigi Libero Lucio Starace), Università degli Studi di Napoli
Federico II, corso di laurea in Informatica.

Copre **l'intero corso**: tutte le lezioni, più la lezione bonus su CMS e
GraphQL (inclusa come capitolo finale e segnalata come fuori programma).
25 capitoli, 391 pagine.

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
| `chapters/15. Express.tex` | Framework e inversione del controllo, routing, middleware, gestione errori, messaggi flash |
| `chapters/16. Web app con Express.tex` | ORM e Sequelize, organizzazione del progetto, file di configurazione |
| `chapters/17. REST.tex` | Stile REST, verbi e risorse, JWT, hash crittografici, OpenAPI |
| `chapters/18. TypeScript.tex` | Transpiler, tipi, unioni, interfacce, generici, livelli di severità |
| `chapters/19. Frontend Tooling.tex` | Sass, framework CSS, bundling, tree shaking, minificazione, Vite |
| `chapters/20. Single Page App.tex` | Routing lato client, componenti, Web Components API |
| `chapters/21. Angular.tex` | Componenti, template, eventi, `@Input`/`@Output`, Router |
| `chapters/22. Angular avanzato.tex` | Form, servizi e DI, guardie, HttpClient, Observable, signal, la SPA completa |
| `chapters/23. Sicurezza.tex` | XSS, CSRF, SQL injection, session hijacking, same-origin policy e CORS |
| `chapters/24. Testing.tex` | Piramide del testing, Jasmine, test double, E2E, fragilità e flakiness, Playwright |
| `chapters/25. CMS e GraphQL.tex` | *(fuori programma)* CMS tradizionali e headless, Strapi, GraphQL, siti statici |
| `unina_doc_class.cls` | Classe di documento (ripresa dalle *Dispense APA*, non modificata) |
| `fonts/` | Font usati dalla classe (Lato, Gobold, FiraCode, Lora, IcoMoon, …) |
| `sources/` | Logo dell'ateneo, risorse della copertina, immagine di Fu-Tzu (`fu-tzu.jpg`, dalle slide) |
| `build.ps1` | Script di compilazione |
| `DispensaWebTech.pdf` | PDF già compilato |

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
disponibili sono `html`, `css`, `js`, `ts`, `pug`, `php`, `json`, `shell`,
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
