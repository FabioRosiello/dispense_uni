# Generatore di prove di Tecnologie Web

Genera **simulazioni della prova intercorso** di Tecnologie Web, con lo stesso
aspetto delle prove del corso: intestazione con l'ID della prova, riquadro
delle istruzioni, **8 domande chiuse da 2 punti** con le opzioni A–F su due
colonne, **3 domande aperte da 5 punti** con le righe per la risposta, codice
con i numeri di riga, 45 minuti (come nel facsimile mostrato in aula).

Il programma è quello svolto finora: **dal Web agli strumenti di front-end**,
cioè i capitoli 1–20 della dispensa (REST, API in produzione, TypeScript, Sass
e Vite compresi). Per una prova sul programma della prima intercorso, fino a
Express, basta `--capitoli 1-16`. Ogni prova ha il suo PDF di **soluzioni**:
per le domande chiuse la lettera giusta, la spiegazione (anche del perché le
altre opzioni sono sbagliate) e la sezione della dispensa da ripassare; per le
aperte, la traccia di una risposta completa.

Per allenarsi **un argomento alla volta** c'è anche una pagina HTML,
`allenamento.html`: si scelgono i capitoli e si risponde alle domande una alla
volta, con la correzione subito, oppure si fa una simulazione d'esame a tempo
(vedi sotto).

Le prove sono marcate come *Simulazione non ufficiale* (filigrana e piè di
pagina): non sono materiale del docente.

## Allenarsi nel browser: `allenamento.html`

`allenamento.html` è un **unico file**, senza dipendenze esterne: si apre con un
doppio clic (anche senza connessione) e contiene l'intera banca. Da GitHub si
scarica con *Download raw file* dalla pagina del file.

1. **Si scelgono i capitoli**: uno solo per ripassare un argomento, più capitoli
   (o tutti) per un ripasso generale. Per ogni capitolo è indicato quante
   domande ci sono e quante ne sono già state viste.
2. **Si sceglie la modalità**:
   - *Allenamento*: una domanda alla volta; dopo «Verifica» le opzioni si
     colorano (giusta presa, giusta non presa, sbagliata), compare il punteggio
     con le regole d'esame, la spiegazione e la sezione della dispensa da
     rileggere. Si risponde anche da tastiera (A–F o 1–6, Invio per proseguire).
   - *Simulazione d'esame*: 8 chiuse e 3 aperte (modificabili) scelte come nel
     generatore di PDF (capitoli a rotazione secondo il loro peso, chiuse in
     ordine di capitolo, aperte da capitoli diversi), il tempo che scorre (45
     minuti) e la correzione alla consegna. Si può stampare.
3. **Filtri**: *solo domande a trabocchetto*, *solo domande delle prove del
   corso*, *prima quelle che non ho ancora visto* (le statistiche restano nel
   browser).

Le domande aperte non si correggono da sole: si scrive la risposta, poi si
confronta con la traccia e ci si assegna un punteggio da 0 a 5. A fine
sessione c'è il riepilogo per capitolo e il pulsante per **ripetere le domande
sbagliate**. Le domande fisse arrivano con sei estrazioni diverse delle opzioni,
quelle parametriche con dieci varianti dei dati.

Dopo aver modificato la banca la pagina si rigenera con:

```bash
python3 genera_allenamento.py
```

## Uso rapido

Serve solo **Python 3**; per avere i PDF serve anche **pdfLaTeX** (TeX Live o
MiKTeX). Dalla cartella `prove`:

```bash
python3 genera_prova.py                      # una prova a caso, con le soluzioni
python3 genera_prova.py --id 7               # la prova 00007 (è sempre la stessa)
python3 genera_prova.py --id 1 --quante 10   # le prove da 00001 a 00010
python3 genera_prova.py --capitoli 1-16      # il programma della prima intercorso
python3 genera_prova.py --capitoli 5-8       # solo JavaScript
python3 genera_prova.py --trabocchetti       # domande chiuse solo a trabocchetto
python3 genera_prova.py --raccolta           # tutte le domande in un PDF, con le soluzioni
python3 genera_prova.py --elenco             # che cosa contiene la banca
```

| Opzione | Effetto |
|---|---|
| `--id N` | numero della prova (da 1); senza, un numero a caso |
| `--quante K` | genera K prove con ID consecutivi |
| `--capitoli 1-16` | capitoli della dispensa da cui pescare (anche `3,5-8`); predefinito `1-20` |
| `--trabocchetti` | fra le domande chiuse, solo quelle a trabocchetto (le aperte restano tutte) |
| `--chiuse 8`, `--aperte 3` | quante domande di ciascun tipo |
| `--minuti 45` | il tempo scritto nelle istruzioni |
| `--titolo "..."` | il titolo in alto a sinistra |
| `--cartella DIR` | dove salvare i file (predefinito: `generate/`) |
| `--senza-soluzioni` | solo il testo della prova |
| `--solo-tex`, `--tieni-tex` | scrivere i sorgenti `.tex` invece dei PDF, o in aggiunta |
| `--raccolta` | un unico PDF con **tutte** le domande della banca e le soluzioni |
| `--elenco` | il contenuto della banca, capitolo per capitolo |

Per ogni prova escono due file: `prova-00007.pdf` e `prova-00007-soluzioni.pdf`.
Senza pdfLaTeX il programma scrive i `.tex`, che si compilano anche su
**Overleaf** (compilatore pdfLaTeX).

In `generate/` ci sono già le prove **da 00001 a 00010**, con le soluzioni, e
la **raccolta** di tutte le domande (`raccolta-domande.pdf`).

### I capitoli 16–20

Il capitolo 16 (Sequelize, organizzazione dell'applicazione, autenticazione) e
il 18 (API in produzione: versioni, sicurezza, rate limiting, osservabilità)
hanno il peso più basso; REST, TypeScript e gli strumenti di front-end (17, 19,
20) il peso normale. Per restare sul programma della prima intercorso basta
`--capitoli 1-16` (o `1-15`, senza Sequelize).

## Come viene composta una prova

- **L'ID decide tutto.** Lo stesso ID produce sempre la stessa prova (con la
  stessa banca e le stesse opzioni): si può rigenerare, o confrontare con un
  collega.
- **Serie di dieci prove.** Gli ID sono raggruppati a decine (1–10, 11–20, …).
  Dentro una serie le domande escono da un mazzo senza reinserimento: dieci
  prove consecutive non ripetono una domanda finché la banca lo consente.
- **Più argomenti possibili.** I capitoli ruotano: ogni prova pesca da capitoli
  diversi prima di tornare su uno già usato, e le domande aperte preferiscono i
  capitoli non toccati dalle chiuse. Risultato: in 99 prove su 100 le 11
  domande vengono da 11 capitoli diversi. Dentro un capitolo si alternano gli
  argomenti (per esempio, in JavaScript: hoisting, closure, `this`, ...), e una
  domanda non compare mai due volte nella stessa prova.
- **Pesi.** CSS, JavaScript (base, avanzato, nel browser), asincronismo ed
  Express escono più spesso (peso 3); CGI e capitoli 16 e 18 meno (peso 1); gli
  altri capitoli hanno peso 2. Per le aperte tutti i capitoli pesano uguale.
- **Domande parametriche** (*famiglie*): codici di stato, URL, specificità,
  `:nth-child`, selettori, unità di misura, metodi degli array, timer e Promise,
  rotte di Express, template Pug, ... Ogni variante ha dati diversi e la
  risposta calcolata, e le prove di una stessa serie non ricevono gli stessi
  dati.
- **Opzioni mescolate**, a volte con *Nessuna delle altre* (che può anche
  essere la risposta giusta). Nelle domande «Quali delle seguenti...» le
  risposte giuste sono di solito due, a volte una o tre, come nelle prove vere.
- Per le domande del tipo «qual è l'output?» i **distrattori** non sono casuali:
  vengono dagli errori tipici (ordine dei `console.log` con timer e Promise,
  `var` contro `let`, `this` perso, una regola CSS più specifica dimenticata,
  ...).

## La banca delle domande

533 voci: **394 domande chiuse, 49 famiglie parametriche, 90 aperte**; 123
domande chiuse sono marcate come *trabocchetto*.

| Cap. | Argomento | Chiuse | Famiglie | Aperte | Trabocchetti |
|---:|---|---:|---:|---:|---:|
| 1 | Introduzione al Web: Internet, ipertesti, HTTP, URL, codici di stato, statelessness | 18 | 3 | 5 | 1 |
| 2 | HTML: elementi, attributi, liste, tabelle, form, URL relative, tag semantici, DOM, DevTools | 30 | 2 | 4 | 3 |
| 3 | CSS: selettori, combinatori, pseudo-classi e pseudo-elementi, cascata, specificità, ereditarietà | 22 | 5 | 5 | 6 |
| 4 | Layout: unità di misura, box model, display, float, posizionamento, Flexbox, Grid, media query | 17 | 4 | 4 | 2 |
| 5 | JavaScript: scope e hoisting, tipi, uguaglianza, funzioni, closure, oggetti, `this` | 30 | 2 | 5 | 14 |
| 6 | JavaScript avanzato: prototipi, array, destrutturazione, Map e Set, classi, errori, moduli | 26 | 1 | 4 | 12 |
| 7 | JavaScript nel browser: DOM e BOM, ricerca e modifica dei nodi, eventi, propagazione, script | 26 | 7 | 5 | 7 |
| 8 | Asincronismo e rete: cookie e Web Storage, callback, Promise, `async`/`await`, `fetch` | 22 | 3 | 5 | 10 |
| 9 | Il Web sotto il cofano: socket e porte, DNS, versioni di HTTP, TCP/UDP/QUIC, metodi, HTTPS | 27 | 3 | 4 | 5 |
| 10 | Il lato server: pagine statiche e dinamiche, CGI, scripting lato server | 7 | 1 | 3 | 0 |
| 11 | Node.js: event loop, modello multi-thread, npm e `package.json`, server HTTP | 9 | 0 | 4 | 1 |
| 12 | Web app con Node.js: routing, template Pug, corpo delle richieste, Post/Redirect/Get | 11 | 5 | 3 | 2 |
| 13 | Sessioni: lo stato nei cookie, sessioni lato server | 10 | 0 | 3 | 1 |
| 14 | CSS moderno: `:is()`/`:where()`/`:has()`, custom property, `calc()` e `clamp()`, container query | 12 | 7 | 5 | 3 |
| 15 | Express: routing, risposte, middleware, errori, `express.static`, sessioni e cookie | 14 | 4 | 5 | 3 |
| 16 | Una web app con Express: ORM e Sequelize, configurazione, organizzazione, autenticazione | 10 | 1 | 3 | 0 |
| 17 | REST: risorse e verbi, archetipi, filtri e paginazione, token e JWT, hash, API con Express 5, OpenAPI | 20 | 1 | 5 | 11 |
| 18 | API in produzione: breaking change e versioni, deprecazione, OWASP API Top 10, rate limiting, SSRF, errori, osservabilità | 24 | 0 | 6 | 11 |
| 19 | TypeScript: `tsc` e type stripping, `any`/`unknown`, inferenza, tipizzazione strutturale, unioni, enum, generici, severità | 23 | 0 | 6 | 13 |
| 20 | Strumenti di front-end: PostCSS e Autoprefixer, Sass, Bootstrap, bundling, tree shaking, minificazione, Vite | 36 | 0 | 6 | 18 |

Con `python3 genera_prova.py --elenco` si vedono anche gli argomenti di ogni
capitolo.

### Le domande delle prove vere

Ci sono **tutte le domande** delle prove fornite:

- le 11 della **prima prova intercorso del 23 aprile 2024** (le stesse del
  facsimile in PDF): significato dei codici `4xx`, il selettore dei link nelle
  voci pari di `ul.lst`, il colore finale dell'`h1`, il ciclo di vita di `let`,
  i tipi non primitivi, `try`/`catch`/`finally` in modalità strict, `finally`
  e `then` su una Promise, `document.head.children`, e le aperte sul modello
  multi-thread, su `async` e `defer`, sulle origini delle regole CSS;
- le 6 del **facsimile mostrato in aula** (foto): codici `5xx`, colore
  dell'`h1` con due regole di pari specificità, API del BOM, `querySelector`
  prima che l'`h1` esista, il clic che risale da `button` a `div`, l'hoisting
  delle funzioni;
- le 11 della **prima prova intercorso del 2026** (foto): il trasporto di
  HTTP/3, uno script `async`, l'header `Host`, la specificità di `:is()` con un
  argomento che non seleziona nulla, `instanceof` con due costruttori che
  condividono il prototipo, la arrow function restituita da un metodo,
  `Object.setPrototypeOf` sul costruttore invece che su `F.prototype`, `await`
  in una funzione non `async`, e le aperte su `node_modules`, sui middleware e
  sulle container query. Escono con le stesse quattro opzioni della prova.

Alcune sono riprese così come sono, altre sono diventate famiglie che ne
generano varianti (i codici di stato, il selettore della lista: la variante
originale esce circa una volta su tre). Nelle soluzioni queste domande
riportano la fonte («Fonte: prima prova intercorso del 23 aprile 2024»), e
nella pagina di allenamento si possono chiedere da sole.

Una correzione: nella domanda su `document.head.children` l'opzione giusta
della prova è scritta `<meta charset="UTF-8"/>`, ma il browser stampa
`<meta charset="UTF-8">` (`outerHTML` ricostruisce il codice dal DOM e la barra
finale non c'è più); la banca usa l'output reale.

### Domande a trabocchetto

Le domande della prova del 2026 non chiedono definizioni: sono costruite
attorno a un dettaglio che sfugge a una lettura veloce (la specificità di
`:is()` che conta anche l'argomento assente, due costruttori che condividono lo
stesso prototipo). La banca contiene **123 domande di questo tipo**, marcate
con `trabocchetto=True`, tutte risolvibili ragionando su quanto spiega la
dispensa.
Qualche esempio:

- **Web e HTML**: quali URL individuano la stessa risorsa (maiuscole nell'host,
  `:443`, `/./`, la barra finale); un link relativo da una pagina senza barra
  finale; l'HTML che il parser corregge (`<p>Uno<div>Due</div>Tre</p>`).
- **CSS**: `[id="menu"]` che conta come una classe; un link dentro un paragrafo
  verde che resta blu; una media query vera che perde con una regola successiva;
  una container query che non si applica al contenitore stesso.
- **JavaScript**: `null >= 0` vero ma `null == 0` falso; `typeof` nella
  temporal dead zone; il valore predefinito di un parametro valutato a ogni
  chiamata; un oggetto ereditato modificato attraverso il prototipo;
  `for..in` che vede i metodi aggiunti al prototipo ma non quelli di una
  classe; gli `import` in sola lettura; `forEach` con funzioni `async`;
  `return` contro `return await` dentro un `try`; un `<script>` inserito con
  `innerHTML` che non viene eseguito (mentre `onerror` sì); `defer` ignorato
  sugli script in linea.
- **Rete e server**: `HEAD` su una rotta `GET` di Express; che cosa resta
  visibile con HTTPS; il frammento che non arriva mai al server; un gestore di
  errori con tre parametri che Express non riconosce.
- **REST e API**: `req.query` che contiene sempre stringhe (`min * 2` è 36,
  `min + 1` è `"181"`); il `401` che precede il `404` del catch-all; il corpo
  JSON ignorato senza `Content-Type` (in Express 5 `req.body` è `undefined`);
  `jwt.decode` che non verifica la firma; `Accept: */*` che sceglie la v1; due
  limiti di `express-rate-limit` che contano le stesse richieste; il controllo
  `includes` aggirato da `images.example.com.evil.it`.
- **TypeScript**: `node prova.ts` che toglie i tipi senza controllarli (ma non
  sa eseguire un `enum`); `tsc` che genera il JavaScript anche con errori; un
  oggetto letterale con una proprietà in più rifiutato, la stessa variabile
  accettata; due classi con la stessa forma intercambiabili (ma `instanceof`
  risponde `false`); `let b = "center"` che non è un tipo letterale.
- **Strumenti di front-end**: `.scuro &`, `!default`, il prefisso di `@use`,
  `width: 100px / 2` che resta `100px/2`, le variabili di Bootstrap assegnate
  dopo l'`@import`, il tree shaking che conserva il `console.log` di un modulo,
  `type="javascript"` che non esegue lo script, l'impronta di Vite che cambia
  anche per un JavaScript identico.

Nella pagina di allenamento c'è il filtro *solo domande a trabocchetto*; con il
generatore di PDF, `--trabocchetti`.

## Ogni risposta è verificata eseguendo il codice

Le risposte delle domande con codice non sono scritte «a memoria»: lo script
`verifica/verifica.py` esegue davvero ogni frammento e confronta il risultato
con l'opzione marcata come giusta.

| Tipo di domanda | Come viene verificata |
|---|---|
| output di un frammento JavaScript | eseguito con **Node.js** (righe stampate ed eventuale eccezione) |
| output di una pagina HTML (anche dopo clic) | aperta in **Chromium** con Playwright: console ed errori della pagina |
| colore finale di un elemento | stile calcolato da Chromium, e nessun'altra opzione deve corrispondere |
| selettori, DOM | espressione valutata nella pagina (per i selettori: solo l'opzione giusta seleziona gli elementi richiesti) |
| HTML prodotto da un template | reso con **Pug** 3 |
| risposte di un server | il server (Express 5, anche con `express-rate-limit`, o il modulo `http`) viene **avviato** e interrogato |
| frammenti TypeScript | compilati con **`tsc`** (TypeScript 7.0.2, impostazioni predefinite): righe e codici degli errori segnalati, poi il JavaScript prodotto e/o il file `.ts` eseguiti con Node |
| fogli di stile Sass | compilati con **Sass** 1.108.2: il CSS prodotto (a meno degli spazi) o il messaggio d'errore |
| tree shaking | moduli impacchettati con **esbuild** 0.28.2: le funzioni rimaste nel bundle e il suo output |
| frammenti con pacchetti npm | eseguiti con Node accanto ai pacchetti veri (per esempio `jsonwebtoken` 9.0.3) |

Per le famiglie vengono provate più varianti. L'ultima esecuzione completa:
**651 casi, 0 problemi** (browser 99, CSS 83, DOM 134, Express 89, Node 180,
Pug 38, Sass 10, TypeScript 17, bundle 1). Per ripeterla servono Node.js e
Chromium per Playwright:

```bash
cd verifica
npm install                       # Express, Pug, TypeScript, Sass, esbuild, jsonwebtoken, ...
npm install --no-save playwright  # se Playwright non è già installato
npx playwright install chromium
cd ..
python3 verifica/verifica.py                  # tutte le domande verificabili
python3 verifica/verifica.py --solo c07       # solo un capitolo (o un id)
python3 verifica/verifica.py --varianti 30    # più varianti per le famiglie
```

Ogni domanda viene anche controllata al caricamento della banca: almeno tre
distrattori, nessuna opzione ripetuta, la spiegazione presente, il markup
valido, nessuna riga di codice troppo lunga per la pagina. Un secondo script,
che non esegue codice e richiede solo Python, prova le famiglie con migliaia di
semi (una combinazione di parametri sfortunata farebbe fallire proprio la prova
che la pesca) e compone migliaia di prove, controllando che nessuna contenga
due volte la stessa domanda e che una serie non ripeta le domande fisse:

```bash
python3 verifica/composizione.py     # 2000 varianti per famiglia, oltre 3000 prove
```

## Aggiungere domande

La banca è in `banca/`, un file per capitolo (`c05_js.py`, `c15_express.py`,
...). Ogni file definisce la lista `DOMANDE`; un file nuovo con lo stesso
schema di nome viene raccolto da solo. Nei testi vale un piccolo markup:
`` `codice` ``, ``` `` co`dice `` ``` (codice con un apice inverso dentro),
`**grassetto**`, `*corsivo*`.

```python
from generatore import Err, aperta, chiusa, famiglia, uscita_js

CAP = 5
R = "cap. 5, «%s»"
DOMANDE = []
d = DOMANDE.append

d(chiusa("c05-typeof-null", CAP, "tipi di dato e typeof",
         "Che cosa restituisce `typeof null`?",
         '`"object"`',                                           # la risposta giusta
         ['`"null"`', '`"undefined"`', '`null`', '`"number"`'],  # almeno tre distrattori
         spiegazione="È un errore storico del linguaggio, mai corretto per compatibilità.",
         rif=R % "Tipi di dato primitivi"))

d(uscita_js("c05-closure-valore", CAP, "closure",
            """
let x = 1;
const f = () => x;
x = 2;
console.log(f());""",
            ["2"],                                         # le righe stampate
            [["1"], ["undefined"], Err("ReferenceError")],  # esiti sbagliati
            spiegazione="La closure legge il valore attuale di `x`, non una copia.",
            rif=R % "Closure"))

d(aperta("c05-a-esempio", CAP, "closure",
         "Che cos'è una closure? Si mostri un esempio.",
         ["Una funzione insieme all'ambiente in cui è stata creata.",
          "Continua a vedere le variabili esterne anche dopo che la funzione "
          "che le conteneva è terminata."],                # traccia della risposta
         rif=R % "Closure"))
```

Altri aiuti, tutti in `generatore/__init__.py`: `uscita_browser` (output di
una pagina HTML, anche dopo dei clic), `colore_css` («di che colore è
l'elemento?»), `uscita_pug` (l'HTML generato da un template), `risposte_server`
(che cosa risponde un server Node o Express a una serie di richieste),
`domanda_ts` (un frammento TypeScript: errori di `tsc` attesi, nella forma
`"5:TS2322"`, e output del JavaScript prodotto o del `.ts` eseguito da Node),
`domanda_sass` (il CSS atteso, o l'errore, per un foglio SCSS ed eventuali
parziali), `domanda_bundle` (le funzioni che restano dopo il tree shaking),
`famiglia` (decoratore per le domande parametriche: una funzione che riceve un
generatore casuale e restituisce una `chiusa`) e `combina_errori` (distrattori
costruiti combinando gli errori tipici riga per riga). Le domande costruite con
questi aiuti vengono verificate automaticamente.

Le domande costruite su un dettaglio insidioso si marcano con
`trabocchetto=True` (anche nelle famiglie: `@famiglia(..., trabocchetto=True)`);
quelle riprese da una prova del corso con `fonte=` (per esempio `FONTE_2026`).
Dopo aver modificato la banca si rigenera la pagina di allenamento con
`python3 genera_allenamento.py`.

## Struttura della cartella

| Percorso | Contenuto |
|---|---|
| `genera_prova.py` | il programma da riga di comando |
| `genera_allenamento.py` | scrive `allenamento.html` a partire dalla banca |
| `allenamento.html` | la pagina per allenarsi nel browser (file unico, si apre con un doppio clic) |
| `generatore/modello.py` | domande chiuse, aperte e famiglie, con i controlli sulla banca |
| `generatore/selezione.py` | come vengono scelte le domande di una prova (ID, serie, pesi) |
| `generatore/latex.py` | l'impaginazione LaTeX, ricalcata sulle prove del corso |
| `generatore/markup.py` | il piccolo markup dei testi e la sua traduzione in LaTeX |
| `generatore/html.py` | il markup e i listati (colorati, con i numeri di riga) in HTML, ed esportazione della banca per l'allenamento |
| `generatore/allenamento.html` | il modello della pagina di allenamento (HTML, CSS e JavaScript, senza dipendenze) |
| `banca/` | le domande, un file per capitolo |
| `verifica/` | gli script di controllo: `verifica.py` esegue il codice delle domande (Node, Chromium, Pug, Express, TypeScript, Sass, esbuild), `composizione.py` prova famiglie e prove in gran numero |
| `generate/` | prove d'esempio (00001–00010), soluzioni e raccolta |

Pacchetti LaTeX usati: `fontenc`, `inputenc`, `babel` (italiano), `lmodern`,
`libertine`, `textcomp`, `geometry`, `fancyhdr`, `enumitem`, `multicol`,
`xcolor`, `listings`, `eso-pic`, `graphicx`, `array` (tutti presenti in una
installazione completa di TeX Live o MiKTeX).
