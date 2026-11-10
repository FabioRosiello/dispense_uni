# Generatore di prove di Tecnologie Web

Genera **simulazioni della prova intercorso** di Tecnologie Web, con lo stesso
aspetto delle prove del corso: intestazione con l'ID della prova, riquadro
delle istruzioni, **8 domande chiuse da 2 punti** con le opzioni A–F su due
colonne, **3 domande aperte da 5 punti** con le righe per la risposta, codice
con i numeri di riga, 45 minuti (come nel facsimile mostrato in aula).

Il programma è quello della prova: **dal Web a Express incluso**, cioè i
capitoli 1–16 della dispensa. Ogni prova ha il suo PDF di **soluzioni**: per
le domande chiuse la lettera giusta, la spiegazione (anche del perché le altre
opzioni sono sbagliate) e la sezione della dispensa da ripassare; per le aperte,
la traccia di una risposta completa.

Le prove sono marcate come *Simulazione non ufficiale* (filigrana e piè di
pagina): non sono materiale del docente.

## Uso rapido

Serve solo **Python 3**; per avere i PDF serve anche **pdfLaTeX** (TeX Live o
MiKTeX). Dalla cartella `prove`:

```bash
python3 genera_prova.py                      # una prova a caso, con le soluzioni
python3 genera_prova.py --id 7               # la prova 00007 (è sempre la stessa)
python3 genera_prova.py --id 1 --quante 10   # le prove da 00001 a 00010
python3 genera_prova.py --capitoli 1-15      # senza il capitolo 16 (vedi sotto)
python3 genera_prova.py --capitoli 5-8       # solo JavaScript
python3 genera_prova.py --raccolta           # tutte le domande in un PDF, con le soluzioni
python3 genera_prova.py --elenco             # che cosa contiene la banca
```

| Opzione | Effetto |
|---|---|
| `--id N` | numero della prova (da 1); senza, un numero a caso |
| `--quante K` | genera K prove con ID consecutivi |
| `--capitoli 1-15` | capitoli della dispensa da cui pescare (anche `3,5-8`); predefinito `1-16` |
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

### Il capitolo 16

La lezione *Developing a Web App with Express* (capitolo 16: Sequelize,
organizzazione dell'applicazione, `dotenv`, autenticazione) chiude la parte su
Express, quindi è inclusa, ma con il peso più basso: compare in circa due prove
su cinque. Se il docente la escludesse dalla prova, basta `--capitoli 1-15`.

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
  Express escono più spesso (peso 3); CGI e capitolo 16 meno (peso 1); gli altri
  capitoli hanno peso 2. Per le aperte tutti i capitoli pesano uguale.
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

366 voci: **254 domande chiuse, 48 famiglie parametriche, 64 aperte**.

| Cap. | Argomento | Chiuse | Famiglie | Aperte |
|---:|---|---:|---:|---:|
| 1 | Introduzione al Web: Internet, ipertesti, HTTP, URL, codici di stato, statelessness | 17 | 3 | 5 |
| 2 | HTML: elementi, attributi, liste, tabelle, form, URL relative, tag semantici, DOM, DevTools | 29 | 2 | 4 |
| 3 | CSS: selettori, combinatori, pseudo-classi e pseudo-elementi, cascata, specificità, ereditarietà | 20 | 5 | 5 |
| 4 | Layout: unità di misura, box model, display, float, posizionamento, Flexbox, Grid, media query | 16 | 4 | 4 |
| 5 | JavaScript: scope e hoisting, tipi, uguaglianza, funzioni, closure, oggetti, `this` | 24 | 2 | 5 |
| 6 | JavaScript avanzato: prototipi, array, destrutturazione, Map e Set, classi, errori, moduli | 19 | 1 | 4 |
| 7 | JavaScript nel browser: DOM e BOM, ricerca e modifica dei nodi, eventi, propagazione, script | 22 | 7 | 5 |
| 8 | Asincronismo e rete: cookie e Web Storage, callback, Promise, `async`/`await`, `fetch` | 18 | 3 | 5 |
| 9 | Il Web sotto il cofano: socket e porte, DNS, versioni di HTTP, TCP/UDP/QUIC, metodi, HTTPS | 20 | 3 | 4 |
| 10 | Il lato server: pagine statiche e dinamiche, CGI, scripting lato server | 7 | 1 | 3 |
| 11 | Node.js: event loop, modello multi-thread, npm e `package.json`, server HTTP | 9 | 0 | 3 |
| 12 | Web app con Node.js: routing, template Pug, corpo delle richieste, Post/Redirect/Get | 10 | 5 | 3 |
| 13 | Sessioni: lo stato nei cookie, sessioni lato server | 10 | 0 | 3 |
| 14 | CSS moderno: `:is()`/`:where()`/`:has()`, custom property, `calc()` e `clamp()`, container query | 10 | 7 | 4 |
| 15 | Express: routing, risposte, middleware, errori, `express.static`, sessioni e cookie | 13 | 4 | 4 |
| 16 | Una web app con Express: ORM e Sequelize, configurazione, organizzazione, autenticazione | 10 | 1 | 3 |

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
  delle funzioni.

Alcune sono riprese così come sono, altre sono diventate famiglie che ne
generano varianti (i codici di stato, il selettore della lista: la variante
originale esce circa una volta su tre). Nelle soluzioni queste domande
riportano la fonte («Fonte: prima prova intercorso del 23 aprile 2024»).

Una correzione: nella domanda su `document.head.children` l'opzione giusta
della prova è scritta `<meta charset="UTF-8"/>`, ma il browser stampa
`<meta charset="UTF-8">` (`outerHTML` ricostruisce il codice dal DOM e la barra
finale non c'è più); la banca usa l'output reale.

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
| risposte di un server | il server (Express 5 o il modulo `http`) viene **avviato** e interrogato |

Per le famiglie vengono provate più varianti. L'ultima esecuzione completa:
**581 casi, 0 problemi**. Per ripeterla servono Node.js e Chromium per
Playwright:

```bash
cd verifica
npm install                       # Express, express-session, cookie-parser, Pug
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
`famiglia` (decoratore per le domande parametriche: una funzione che riceve un
generatore casuale e restituisce una `chiusa`) e `combina_errori` (distrattori
costruiti combinando gli errori tipici riga per riga). Le domande costruite con
questi aiuti vengono verificate automaticamente.

## Struttura della cartella

| Percorso | Contenuto |
|---|---|
| `genera_prova.py` | il programma da riga di comando |
| `generatore/modello.py` | domande chiuse, aperte e famiglie, con i controlli sulla banca |
| `generatore/selezione.py` | come vengono scelte le domande di una prova (ID, serie, pesi) |
| `generatore/latex.py` | l'impaginazione LaTeX, ricalcata sulle prove del corso |
| `generatore/markup.py` | il piccolo markup dei testi e la sua traduzione in LaTeX |
| `banca/` | le domande, un file per capitolo |
| `verifica/` | gli script di controllo: `verifica.py` esegue il codice delle domande (Node, Chromium, Pug, Express), `composizione.py` prova famiglie e prove in gran numero |
| `generate/` | prove d'esempio (00001–00010), soluzioni e raccolta |

Pacchetti LaTeX usati: `fontenc`, `inputenc`, `babel` (italiano), `lmodern`,
`libertine`, `textcomp`, `geometry`, `fancyhdr`, `enumitem`, `multicol`,
`xcolor`, `listings`, `eso-pic`, `graphicx`, `array` (tutti presenti in una
installazione completa di TeX Live o MiKTeX).
