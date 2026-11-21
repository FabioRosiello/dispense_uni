"""Capitolo 20: strumenti di front-end (pre- e post-processori, Sass,
framework CSS, bundling, tree shaking, minificazione, Vite, fingerprinting).

Le domande su Sass sono verificate compilando davvero con Sass 1.108.2,
quella sul tree shaking impacchettando con esbuild 0.28.2, quella sugli
script e sul CSS scartato con Chromium.
"""

from generatore import aperta, chiusa, domanda_bundle, domanda_sass, uscita_browser

CAP = 20
R = "cap. 20, «%s»"

DOMANDE = []
d = DOMANDE.append

SASS = "Che cosa produce Sass compilando il foglio di stile seguente?"

# ----------------------------------------------------------------------
# Pre- e post-processori
d(chiusa("c20-pre-post", CAP, "pre- e post-processori",
         "Quali delle seguenti sono tipiche funzioni di un **post**-processore CSS come "
         "PostCSS?",
         ["Aggiungere i prefissi specifici dei browser.",
          "Riscrivere costrutti recenti in forme comprese dai browser più vecchi.",
          "Minificare il foglio di stile."],
         ["Introdurre variabili risolte alla compilazione e mixin.",
          "Compilare la sintassi indentata `.sass`.",
          "Generare famiglie di classi con un ciclo `@each`.",
          "Annidare le regole e risolvere il selettore `&`."],
         multi=True,
         spiegazione="Un **pre**-processore (Sass, LESS, Stylus) genera CSS da una sintassi "
                     "propria, che estende il CSS con variabili, annidamento, mixin, moduli e "
                     "cicli. Un **post**-processore (PostCSS, con i suoi plugin) trasforma CSS "
                     "già esistente: downleveling (`postcss-preset-env`), autoprefissatura "
                     "(Autoprefixer), ottimizzazioni come la minificazione, controllo delle "
                     "convenzioni.",
         rif=R % "Pre- e post-processori CSS"))

d(chiusa("c20-autoprefixer", CAP, "pre- e post-processori",
         "Si esegue `npx postcss transition.css --use autoprefixer` su un file che contiene "
         "soltanto `.example { transition: all .5s; }`, senza alcuna configurazione di "
         "Browserslist. Che cosa produce Autoprefixer?",
         "La regola invariata: i browser della query predefinita (`defaults`) non hanno bisogno "
         "di prefissi per `transition`.",
         ["La regola con in più `-webkit-transition` e `-o-transition`.",
          "La regola con i prefissi di tutti i browser esistenti, per sicurezza.",
          "Un errore: senza un file `.browserslistrc` Autoprefixer non sa che cosa fare.",
          "La regola con `transition` sostituita da `-webkit-transition`."],
         spiegazione="Autoprefixer aggiunge **solo** i prefissi che servono ai browser da "
                     "supportare, e li ricava da Browserslist: senza indicazioni vale la query "
                     "`defaults`, e `transition` senza prefisso funziona ovunque da anni. I "
                     "prefissi `-webkit-` e `-o-` compaiono solo chiedendo browser molto vecchi, "
                     "per esempio `BROWSERSLIST='Safari 6, Opera 12'`.",
         rif=R % "Post-processori", trabocchetto=True))

d(chiusa("c20-browserslist", CAP, "pre- e post-processori",
         "In un progetto si vuole indicare una volta per tutte quali browser supportare, in "
         "modo che Autoprefixer, `postcss-preset-env` e Vite usino la stessa lista. Dove la si "
         "scrive?",
         "Nella chiave `\"browserslist\"` del `package.json` (o in un file `.browserslistrc`).",
         ["In un commento in cima a ogni foglio di stile.",
          "Nel file `.env`, nella variabile `BROWSERS`.",
          "Nel tag `<meta name=\"viewport\">` della pagina.",
          "In ciascun plugin di PostCSS, con un'opzione separata."],
         spiegazione="Browserslist è una lista condivisa da molti strumenti: la si scrive una "
                     "volta nel `package.json` o in `.browserslistrc`, e tutti la leggono da lì. "
                     "La variabile d'ambiente `BROWSERSLIST` serve a sostituirla al volo, per "
                     "una singola esecuzione.",
         rif=R % "Post-processori"))

# ----------------------------------------------------------------------
# Sass
d(chiusa("c20-sintassi", CAP, "Sass",
         "Quali delle seguenti affermazioni sulle due sintassi di Sass sono **vere**?",
         ["La sintassi SCSS (`.scss`) è un superset del CSS: un CSS valido è anche SCSS "
          "valido.",
          "La sintassi indentata (`.sass`) usa l'indentazione al posto delle graffe.",
          "La sintassi indentata è quella originale di Sass."],
         ["La sintassi indentata è oggi la più diffusa.",
          "Un file `.scss` non può contenere CSS normale.",
          "Le due sintassi producono CSS diversi per lo stesso foglio di stile.",
          "Il browser carica direttamente i file `.scss`."],
         multi=True,
         spiegazione="SCSS (estensione `.scss`) estende il CSS ed è la sintassi più usata; la "
                     "sintassi indentata (`.sass`), basata sull'indentazione come Python, era "
                     "quella originale. Lo stesso foglio scritto nelle due sintassi produce lo "
                     "stesso CSS. In ogni caso il browser riceve CSS: il file Sass va compilato.",
         rif=R % "Due sintassi"))

d(domanda_sass("c20-annidamento", CAP, "Sass",
               "Quale selettore genera Sass per la regola annidata alla riga 5?",
               """
.card {
  color: navy;
  &:hover { color: red; }
  & .titolo { font-weight: bold; }
  .scuro & { color: white; }
}""",
               "`.scuro .card`",
               ["`.card .scuro`", "`.card.scuro`", "`.scuro.card`", "`.card .scuro .card`"],
               css=""".card { color: navy; }
.card:hover { color: red; }
.card .titolo { font-weight: bold; }
.scuro .card { color: white; }""",
               spiegazione="Il simbolo `&` sta per il selettore della regola genitore **nel "
                           "punto in cui compare**: `&:hover` diventa `.card:hover`, `& .titolo` "
                           "diventa `.card .titolo` (come senza `&`), e `.scuro &` mette il "
                           "genitore dopo: una `.card` dentro un elemento `.scuro`.",
               rif=R % "Annidamento", trabocchetto=True))

d(domanda_sass("c20-default", CAP, "Sass",
               "Di che colore è il testo degli elementi `.a`, secondo il CSS prodotto da Sass?",
               """
$colore: red;
$colore: blue !default;
.a { color: $colore; }""",
               "`red`",
               ["`blue`", "Nessuno: Sass segnala che `$colore` è dichiarata due volte.",
                "Il CSS contiene due dichiarazioni, `color: red` e `color: blue`."],
               css=".a { color: red; }",
               spiegazione="`!default` assegna il valore **solo se la variabile non ne ha già "
                           "uno**: qui `$colore` vale già `red`, e la seconda riga non cambia "
                           "nulla. È il meccanismo con cui un framework come Bootstrap lascia "
                           "personalizzare le proprie variabili, assegnandole prima di "
                           "importarlo.",
               rif=R % "Personalizzare un framework", trabocchetto=True))

d(domanda_sass("c20-modulo", CAP, "Sass",
               "Si compila `stile.scss` (a destra), che usa il parziale `_base.scss` (a "
               "sinistra). Che cosa succede?",
               """
@use 'base';
.inverso { background: $primario; }""",
               "Sass si ferma con un errore: con `@use` le variabili del modulo si leggono con "
               "il prefisso, `base.$primario`.",
               ["Viene generato `.inverso { background: #333; }`, preceduto dalla regola di "
                "`body`.",
                "Viene generata solo la regola di `body`: `$primario` resta vuota.",
                "Vengono generati due file, `base.css` e `stile.css`.",
                "Viene generato `.inverso { background: $primario; }`, che il browser scarta."],
               file={"_base.scss": "$primario: #333;\nbody { color: $primario; }"},
               errore="Undefined variable",
               spiegazione="Con `@use` le variabili di un modulo non finiscono nello spazio dei "
                           "nomi di chi lo usa: si leggono con il prefisso del nome del modulo, "
                           "`base.$primario`. Senza, Sass non trova la variabile (*Undefined "
                           "variable*). Il parziale (nome che inizia con `_`) non produce mai un "
                           "file CSS autonomo; nella regola `@use` trattino basso ed estensione "
                           "si omettono.",
               rif=R % "Moduli e parziali", trabocchetto=True))

d(domanda_sass("c20-commenti", CAP, "Sass",
               "Quali commenti del foglio Sass seguente arrivano nel CSS prodotto?",
               """
// nota interna
/* nota pubblica */
.a { color: red; } // fine""",
               "Solo `/* nota pubblica */`.",
               ["Tutti e tre.", "Nessuno: Sass elimina tutti i commenti.",
                "Solo i due commenti con `//`.",
                "`/* nota pubblica */` e `// fine`, che sta sulla stessa riga di una regola."],
               css="/* nota pubblica */\n.a { color: red; }",
               spiegazione="I commenti con `//` sono *silenziosi*: restano nel sorgente ma non "
                           "arrivano nel CSS (nel CSS, del resto, non esistono). I commenti "
                           "`/* */` invece vengono copiati.",
               rif=R % "Annidamento"))

d(domanda_sass("c20-mixin", CAP, "Sass",
               "Quale selettore riceve la dichiarazione `display: inline-block` nel CSS "
               "prodotto?",
               """
@mixin clear-list {
  list-style-type: none;
  li { display: inline-block; }
}
nav ul {
  background-color: aliceblue;
  @include clear-list;
}""",
               "`nav ul li`",
               ["`li`", "`nav li`", "`nav ul`", "`clear-list li`"],
               css="""nav ul { background-color: aliceblue; list-style-type: none; }
nav ul li { display: inline-block; }""",
               spiegazione="Le dichiarazioni di un mixin vengono copiate dove lo si include, e "
                           "le regole annidate al suo interno seguono il selettore di chi lo "
                           "include: `li` diventa `nav ul li`.",
               rif=R % "Mixin"))

d(domanda_sass("c20-lista", CAP, "Sass", SASS,
               """
@use "sass:list";
$larghezze: (120px, 240px, 480px);
.a { width: list.nth($larghezze, 2); }""",
               "`.a { width: 240px; }`",
               ["`.a { width: 480px; }`", "`.a { width: 120px; }`",
                "Un errore: gli elementi di una lista si leggono solo con `@each`.",
                "`.a { width: 120px, 240px, 480px; }`"],
               css=".a { width: 240px; }",
               spiegazione="Gli elementi di una lista Sass si contano **da 1**, non da 0: il "
                           "secondo è `240px` (e `list.nth($larghezze, 0)` sarebbe un errore).",
               rif=R % "Liste e mappe", trabocchetto=True))

d(domanda_sass("c20-barra", CAP, "Sass",
               "Che cosa produce Sass (versione 1.108) per le regole `.a` e `.b`?",
               """
$w: 100px;
.a { width: 100px / 2; }
.b { width: $w / 2; }
.c { font: 16px/1.5 serif; }""",
               "`.a { width: 100px/2; }` e `.b { width: 50px; }`, con un avviso di "
               "deprecazione per `.b`.",
               ["`.a { width: 50px; }` e `.b { width: 50px; }`.",
                "`.a { width: 100px/2; }` e `.b { width: 100px/2; }`.",
                "Un errore: la divisione si scrive solo con `math.div()`.",
                "`.a { width: 50px; }` e `.b { width: 100px/2; }`."],
               css=""".a { width: 100px/2; }
.b { width: 50px; }
.c { font: 16px/1.5 serif; }""",
               spiegazione="In Sass la barra è anche un **separatore**, come in "
                           "`font: 16px/1.5`: fra due numeri scritti direttamente resta tale, e "
                           "il CSS contiene `100px/2`, che il browser scarta per `width`. Con una "
                           "variabile Sass esegue la divisione (`50px`), ma avvisa che usare `/` "
                           "per dividere è deprecato. Il modo corretto è "
                           "`math.div(100px, 2)`, dal modulo `sass:math`.",
               rif=R % "Regole di controllo del flusso", trabocchetto=True))

d(domanda_sass("c20-unita", CAP, "Sass", "Che cosa succede compilando il foglio seguente?",
               """
.a { margin: 2 * 0.5rem; }
.b { width: 10px + 2em; }""",
               "Sass si ferma con un errore: `10px` e `2em` hanno unità incompatibili.",
               ["Viene generato `.b { width: 12px; }`.",
                "Viene generato `.b { width: calc(10px + 2em); }`.",
                "Viene generato `.b { width: 10px + 2em; }`, che il browser scarta.",
                "La regola `.b` viene omessa, senza errori."],
               errore="incompatible units",
               spiegazione="Sass fa i conti con le unità di misura: `2 * 0.5rem` è `1rem`. Ma "
                           "non può sommare pixel ed em, il cui rapporto dipende dalla pagina: "
                           "la compilazione si ferma. Per un'espressione da risolvere nel "
                           "browser si scrive `calc(10px + 2em)`.",
               rif=R % "Regole di controllo del flusso"))

d(domanda_sass("c20-interpolazione", CAP, "Sass", "Che cosa succede compilando il foglio seguente?",
               """
$nome: "xs";
.hidden-$nome { display: none; }""",
               "Sass si ferma con un errore: in un selettore il valore di una variabile si "
               "inserisce con l'interpolazione, `.hidden-#{$nome}`.",
               ["Viene generato `.hidden-xs { display: none; }`.",
                "Viene generato `.hidden-$nome { display: none; }`.",
                "Viene generato `.hidden-\"xs\" { display: none; }`.",
                "La regola viene omessa, senza errori."],
               errore="expected selector",
               spiegazione="Le variabili si sostituiscono da sole solo nei **valori** delle "
                           "proprietà. Per inserire un valore in un selettore (o nel nome di una "
                           "proprietà) serve l'interpolazione `#{...}`, come nel ciclo `@each` "
                           "che genera `.hidden-xs`, `.hidden-md`…",
               rif=R % "Regole di controllo del flusso", trabocchetto=True))

d(domanda_sass("c20-import-ordine", CAP, "Sass",
               "Il parziale `_framework.scss` (a sinistra) imita il modo in cui Bootstrap "
               "dichiara le proprie variabili; `stile.scss` (a destra) lo importa e **poi** "
               "cambia `$primary`. Quale colore di sfondo hanno i pulsanti `.btn-primary` nel "
               "CSS prodotto?",
               """
@import "framework";
$primary: red;""",
               "`blue`: quando si assegna `$primary` la regola è già stata generata.",
               ["`red`: l'assegnamento viene per ultimo e vince.",
                "`red`: `!default` cede il passo a qualunque altro assegnamento.",
                "Nessuno: Sass segnala un errore perché `$primary` viene assegnata due volte."],
               file={"_framework.scss": "$primary: blue !default;\n"
                                        ".btn-primary { background: $primary; }"},
               css=".btn-primary { background: blue; }",
               spiegazione="Sass esegue il foglio dall'alto in basso: quando `@import` include il "
                           "framework, `$primary` non ha un valore, `!default` assegna `blue` e "
                           "la regola viene emessa così. Riassegnare la variabile dopo non tocca "
                           "il CSS già generato. Per questo le variabili di Bootstrap vanno "
                           "assegnate **prima** dell'importazione.",
               rif=R % "Personalizzare un framework", trabocchetto=True))

d(chiusa("c20-font", CAP, "Sass",
         "Sass compila `body { font: $font-stack; }`, con `$font-stack: Helvetica, sans-serif;`, "
         "e produce `body { font: Helvetica, sans-serif; }` senza avvisi. Che cosa ne fa il "
         "browser?",
         "Scarta la dichiarazione: la scorciatoia `font` richiede almeno dimensione e famiglia, "
         "e la regola resta vuota.",
         ["Applica Helvetica, con la dimensione predefinita.",
          "Applica Helvetica e ignora solo la parte mancante.",
          "Il CSS non arriva al browser: Sass avrebbe segnalato l'errore.",
          "Usa `sans-serif`, l'ultima famiglia della lista."],
         spiegazione="Sass non controlla il significato delle proprietà: copia il valore così "
                     "com'è. La proprietà abbreviata `font` vuole almeno la dimensione e la "
                     "famiglia (`font: 100% $font-stack`); una dichiarazione non valida viene "
                     "scartata per intero, e il testo resta nel carattere predefinito. In "
                     "alternativa si scrive `font-family: $font-stack`.",
         rif=R % "Variabili", trabocchetto=True,
         verifica=dict(tipo="dom",
                       html="<!DOCTYPE html><html><head><style>body { font: Helvetica, "
                            "sans-serif; }</style></head><body><p>Ciao</p></body></html>",
                       espressione="String(document.styleSheets[0].cssRules[0].style.length)",
                       atteso="0")))

d(chiusa("c20-parziali", CAP, "Sass",
         "La cartella `scss` contiene `_variables.scss` e `style.scss`, che usa il primo con "
         "`@use 'variables'`. Si esegue `sass scss:css`. Quali file CSS compaiono nella "
         "cartella `css`?",
         "Solo `style.css` (con la sua source map).",
         ["`style.css` e `_variables.css`.", "`style.css` e `variables.css`.",
          "Nessuno: un parziale impedisce di compilare l'intera cartella.",
          "Solo `variables.css`, che contiene anche le regole di `style.scss`."],
         spiegazione="I file il cui nome inizia con un trattino basso sono **parziali**: "
                     "servono solo a essere inclusi da altri file, e Sass non genera per essi un "
                     "CSS autonomo. Compilando la cartella si ottiene `style.css`, che contiene "
                     "già ciò che serve del parziale, più la source map `style.css.map`.",
         rif=R % "Moduli e parziali"))

d(chiusa("c20-source-map", CAP, "Sass",
         "Compilando `sass file.scss file.css`, Sass scrive anche `file.css.map`. A che cosa "
         "serve?",
         "A far mostrare agli strumenti per sviluppatori del browser il file Sass e la riga da "
         "cui viene ogni regola del CSS.",
         ["A comprimere il CSS prima di inviarlo al browser.",
          "A elencare le variabili Sass, perché i framework possano riusarle.",
          "A indicare al browser quale foglio di stile caricare per ogni pagina.",
          "A conservare una copia del CSS precedente, per annullare le modifiche."],
         spiegazione="Una *source map* codifica da quale riga e colonna del sorgente viene ogni "
                     "pezzo del file generato. Il CSS la richiama con il commento finale "
                     "`sourceMappingURL`, e i DevTools la usano per mostrare il sorgente Sass "
                     "invece del CSS prodotto. Con `--no-source-map` non viene generata.",
         rif=R % "Variabili"))

d(chiusa("c20-annidamento-profondo", CAP, "Sass",
         "Perché annidare molti livelli di regole in Sass è considerata una cattiva pratica?",
         "Ogni livello aggiunge un elemento al selettore generato e ne aumenta la "
         "specificità: il foglio diventa difficile da sovrascrivere.",
         ["Sass supporta al massimo tre livelli di annidamento.",
          "I browser non accettano selettori con più di tre parti.",
          "Ogni livello genera un file CSS separato da scaricare.",
          "L'annidamento disattiva le source map."],
         spiegazione="Il CSS generato da regole molto annidate contiene selettori lunghi e "
                     "molto specifici, difficili da battere nella cascata (capitolo 3). La "
                     "regola pratica è non superare i tre livelli: è un consiglio, non un limite "
                     "dello strumento.",
         rif=R % "Annidamento"))

# ----------------------------------------------------------------------
# Framework CSS
d(chiusa("c20-framework", CAP, "framework CSS",
         "Bootstrap, Tailwind e Bulma si chiamano «framework CSS». Perché non sono framework "
         "nel senso del capitolo 15?",
         "Non c'è inversione del controllo: sono insiemi di fogli di stile da importare, con "
         "classi da applicare agli elementi.",
         ["Perché sono scritti in Sass invece che in JavaScript.",
          "Perché non si possono installare con npm.",
          "Perché non offrono componenti pronti, solo variabili.",
          "Perché funzionano solo se serviti da una CDN."],
         spiegazione="Un framework nel senso del capitolo 15 chiama il nostro codice (inversione "
                     "del controllo). Un framework CSS è invece una raccolta di stili di uso "
                     "generale (griglia, tipografia, componenti) che si importa e si usa "
                     "applicando le sue classi; si può servire dal proprio server o da una CDN.",
         rif=R % "Framework CSS"))

d(chiusa("c20-contrasto", CAP, "framework CSS",
         "Si ricompila Bootstrap con `$secondary: rgb(254, 203, 110)` (un giallo chiaro), e "
         "nei pulsanti `btn-secondary` il testo diventa nero invece che bianco. Perché?",
         "Bootstrap sceglie, compilando, il colore del testo con un contrasto sufficiente "
         "rispetto allo sfondo.",
         ["Perché `$secondary` è stata assegnata dopo l'importazione del framework.",
          "Perché il browser inverte da sé i colori troppo chiari.",
          "Perché `!default` imposta il testo nero per tutte le variabili modificate.",
          "Perché le classi `btn-*` hanno sempre il testo nero."],
         spiegazione="È il vantaggio di **ricompilare** il framework invece di sovrascriverne i "
                     "colori a mano: le sue funzioni Sass ricalcolano i valori derivati, fra cui "
                     "il colore del testo con il contrasto giusto. Se `$secondary` fosse stata "
                     "assegnata dopo l'importazione, il colore non sarebbe cambiato affatto.",
         rif=R % "Personalizzare un framework", trabocchetto=True))

# ----------------------------------------------------------------------
# Bundling, tree shaking, minificazione
d(domanda_bundle("c20-tree-shaking", CAP, "bundling e minificazione",
                 "esbuild impacchetta i due moduli seguenti partendo da `index.js` (a destra), "
                 "con il tree shaking attivo. Che cosa contiene il bundle, oltre al codice di "
                 "`index.js`?",
                 {"matematica.js": """
export function somma(a, b) { return a + b; }
export function prodotto(a, b) { return a * b; }
console.log("matematica caricata");""",
                  "index.js": """
import { somma, prodotto } from "./matematica.js";
console.log(somma(2, 3));"""},
                 "La funzione `somma` e la chiamata `console.log(\"matematica caricata\")`; "
                 "`prodotto` viene eliminata.",
                 ["Tutto `matematica.js`: `prodotto` viene importata, quindi resta.",
                  "Solo `somma`: le istruzioni di primo livello dei moduli importati vengono "
                  "eliminate.",
                  "`somma` e `prodotto`, senza il `console.log`.",
                  "Niente: gli `import` vengono lasciati al browser."],
                 funzioni=["somma"], righe=["matematica caricata", "5"],
                 spiegazione="Il tree shaking elimina il codice **mai usato**: `prodotto` è "
                             "importata ma nessuno la chiama, quindi non serve. Il `console.log` "
                             "al primo livello del modulo, invece, è un effetto collaterale che "
                             "avviene quando il modulo viene caricato: va conservato, e il "
                             "bundle eseguito stampa `matematica caricata` e poi `5`. "
                             "L'analisi è possibile perché `import` ed `export` sono statici.",
                 rif=R % "Tree shaking", trabocchetto=True))

d(chiusa("c20-statico", CAP, "bundling e minificazione",
         "Perché il tree shaking funziona bene con i moduli ES?",
         "Perché `import` ed `export` sono statici: si possono analizzare senza eseguire il "
         "programma.",
         ["Perché i moduli ES sono sempre minificati.",
          "Perché il browser scarica solo le funzioni effettivamente chiamate.",
          "Perché ogni modulo può esportare una sola funzione.",
          "Perché i moduli ES vengono eseguiti dal bundler durante la build."],
         spiegazione="Un bundler può stabilire quali esportazioni vengono importate (e usate) "
                     "guardando soltanto il testo del programma, perché le istruzioni `import` "
                     "ed `export` non dipendono dall'esecuzione: si trovano al primo livello e "
                     "nominano esplicitamente ciò che collegano.",
         rif=R % "Tree shaking"))

d(chiusa("c20-bundling", CAP, "bundling e minificazione",
         "Quali delle seguenti affermazioni sul bundling sono **vere**?",
         ["Riduce il numero di richieste HTTP necessarie al primo caricamento di una pagina.",
          "L'ordine in cui i file vengono accodati nel bundle conta, sia per il CSS sia per "
          "JavaScript.",
          "Strumenti come Webpack e Rollup sono nati quando i browser non supportavano ancora "
          "i moduli ES."],
         ["Il bundler riordina le regole CSS per specificità, così l'ordine non conta.",
          "Il bundling rende inutile la cache del browser.",
          "Un bundle si può usare solo con il server di sviluppo di Vite.",
          "Il bundling elimina sempre i commenti e gli spazi del codice."],
         multi=True,
         spiegazione="Il bundling unisce più file in uno per fare meno richieste (la cache aiuta "
                     "nelle visite successive, non nella prima). L'ordine conta: nel CSS decide "
                     "chi vince a parità di specificità, in JavaScript quali definizioni sono "
                     "pronte quando servono. Togliere spazi e commenti è la minificazione, "
                     "un'operazione distinta (anche se spesso fatta insieme).",
         rif=R % "Bundling"))

d(uscita_browser("c20-type-script", CAP, "bundling e minificazione",
                 """
<script type="javascript">console.log("A");</script>
<script type="text/javascript">console.log("B");</script>
<script>console.log("C");</script>
<script type="module">console.log("D");</script>""",
                 ["B", "C", "D"],
                 [["A", "B", "C", "D"], ["B", "C"], ["C", "D"], ["A", "B", "C"],
                  ["D", "B", "C"]],
                 spiegazione="`javascript` non è un valore valido per l'attributo `type`: il "
                             "browser considera il contenuto un blocco di dati e **non lo "
                             "esegue**. Sono validi un tipo MIME JavaScript come "
                             "`text/javascript` (che per gli script classici si omette) e "
                             "`module`. Lo script di tipo modulo è differito, ma qui è comunque "
                             "l'ultimo: l'ordine resta `B`, `C`, `D`.",
                 rif=R % "Bundling", trabocchetto=True))

d(chiusa("c20-toplevel", CAP, "bundling e minificazione",
         "Uno script classico dichiara al livello più esterno `let msg = \"Hello\";` e "
         "`let name = \"Web Technologies\";`. Minificato con `terser --compress --mangle`, "
         "i nomi `msg` e `name` restano invariati. Perché?",
         "Sono variabili globali: altri script della pagina potrebbero usarle, e accorciarle "
         "romperebbe quegli script.",
         ["Perché sono dichiarate con `let`, che Terser non sa rinominare.",
          "Perché `--mangle` agisce solo sui nomi delle funzioni.",
          "Perché i template literal impediscono la rinomina.",
          "Perché Terser accorcia solo i nomi più lunghi di dieci caratteri."],
         spiegazione="Le dichiarazioni al livello più esterno di uno script classico sono "
                     "**globali**, condivise con tutti gli script della pagina: il minificatore "
                     "non può sapere se altri le usano. Con `--toplevel` gli si dice che non è "
                     "così, e Terser arriva a eliminare del tutto le variabili, calcolando in "
                     "anticipo la stringa. Nei bundle i nomi non sono più globali, e si possono "
                     "accorciare.",
         rif=R % "Minificazione", trabocchetto=True))

d(chiusa("c20-template-spazio", CAP, "bundling e minificazione",
         "Nella versione minificata di un programma il template literal "
         "`` `${msg}, ${name}!` `` compare come `` `${msg},${name}!` ``. È un risultato "
         "corretto della minificazione?",
         "No: lo spazio fa parte della stringa, e un minificatore non lo toglierebbe mai.",
         ["Sì: i minificatori tolgono tutti gli spazi non necessari.",
          "Sì, ma solo con l'opzione `--compress`.",
          "Sì, perché i template literal vengono valutati durante la build.",
          "Sì, ma solo se la variabile `name` non contiene spazi."],
         spiegazione="La minificazione toglie solo ciò che non cambia il comportamento: spazi "
                     "e a capo **fra** i simboli del codice, commenti, nomi locali lunghi. Uno "
                     "spazio dentro una stringa è un dato: toglierlo cambierebbe il testo "
                     "mostrato («Hello,Web Technologies!»).",
         rif=R % "Minificazione", trabocchetto=True))

d(chiusa("c20-minificazione", CAP, "bundling e minificazione",
         "Quali delle seguenti affermazioni su minificazione e compressione sono **vere**?",
         ["La minificazione non sostituisce la compressione gzip o Brotli del server: le due "
          "si sommano.",
          "Nella minificazione di JavaScript il guadagno maggiore viene di solito dal "
          "*mangling* dei nomi locali.",
          "Il CSS si minifica con risultati più modesti del JavaScript."],
         ["Un file minificato non si può più comprimere con gzip.",
          "La compressione di una risposta è segnalata dall'header `Content-Type`.",
          "La minificazione cambia il comportamento del codice, quindi va evitata in "
          "produzione.",
          "La minificazione serve soprattutto a rendere il codice illeggibile."],
         multi=True,
         spiegazione="Minificare riscrive il codice in forma più breve con lo stesso "
                     "comportamento; la compressione (segnalata da `Content-Encoding`) agisce poi "
                     "sui byte trasferiti, anche di un file già minificato. Per Moment.js il "
                     "*mangling* da solo porta il risparmio dal 38% (solo spazi e commenti) al "
                     "59%. Nel CSS non ci sono variabili locali da rinominare: Bootstrap "
                     "minificato pesa il 17% in meno.",
         rif=R % "Minificazione"))

# ----------------------------------------------------------------------
# Vite
d(chiusa("c20-vite-dev", CAP, "Vite",
         "Il server di sviluppo di Vite è pronto in poco più di un decimo di secondo, anche in "
         "un progetto con molti file. Perché?",
         "In sviluppo non impacchetta il codice: il browser carica i sorgenti come moduli ES, "
         "e Vite trasforma ogni file quando viene richiesto.",
         ["Perché riusa i bundle prodotti dall'ultima build.",
          "Perché compila tutto con `tsc` in parallelo all'avvio.",
          "Perché serve i file già pronti della cartella `dist`.",
          "Perché scarica il codice compilato da una CDN."],
         spiegazione="Il server di sviluppo sfrutta il supporto nativo dei moduli ES: niente "
                     "bundle all'avvio, ogni file (TypeScript, Sass…) viene trasformato al volo "
                     "quando il browser lo chiede. Il bundle ottimizzato si produce solo con "
                     "`npm run build`.",
         rif=R % "Il server di sviluppo"))

d(chiusa("c20-vite-tipi", CAP, "Vite",
         "Con il server di sviluppo di Vite attivo, si salva in `counter.ts` un assegnamento "
         "che viola un tipo dichiarato. Che cosa succede nella pagina?",
         "Funziona come prima: Vite toglie le annotazioni di tipo senza controllarle; il "
         "controllo resta a `tsc`.",
         ["Vite mostra l'errore di tipo nella pagina e blocca il caricamento.",
          "Il browser solleva un `TypeError` al caricamento del modulo.",
          "Vite invia al browser il file `.ts` così com'è, e il browser lo rifiuta.",
          "Vite esegue `tsc` e, trovato l'errore, ricarica la versione precedente."],
         spiegazione="Come il *type stripping* di Node (capitolo 19), Vite in sviluppo si limita "
                     "a togliere i tipi: il file arriva al browser già trasformato in "
                     "JavaScript. Gli errori di tipo li segnalano l'editor e `tsc`, che lo script "
                     "`build` esegue prima di `vite build`.",
         rif=R % "Il server di sviluppo", trabocchetto=True))

d(chiusa("c20-hmr", CAP, "Vite",
         "Che cos'è la *Hot Module Replacement* (HMR) del server di sviluppo di Vite?",
         "Quando si salva un file, Vite invia al browser (via WebSocket) solo il modulo "
         "modificato, che viene sostituito senza ricaricare la pagina.",
         ["Il ricaricamento completo della pagina a ogni salvataggio.",
          "La ricostruzione dell'intero bundle a ogni modifica.",
          "La sostituzione dei moduli sul server, senza coinvolgere il browser.",
          "Il caricamento dei moduli da una CDN quando il server locale non risponde."],
         spiegazione="Con la HMR la pagina cambia senza ricaricarsi e, quando possibile, senza "
                     "perdere lo stato dell'applicazione. Anche un file Sass diventa un modulo "
                     "JavaScript, che inserisce il CSS compilato in un elemento `<style>` e "
                     "viene sostituito a caldo.",
         rif=R % "Il server di sviluppo"))

d(chiusa("c20-build-tsc", CAP, "Vite",
         "Nel modello `vanilla-ts` di Vite lo script `build` è `tsc && vite build`, e il "
         "`tsconfig.json` contiene `\"noEmit\": true`. Che ruolo ha `tsc`?",
         "Controlla i tipi senza produrre file; grazie a `&&`, `vite build` parte solo se il "
         "controllo riesce.",
         ["Compila i file `.ts` in `.js`, che Vite poi impacchetta.",
          "Esegue i test dell'applicazione prima della build.",
          "Avvia `vite build` in parallelo, per guadagnare tempo.",
          "Minifica il JavaScript prodotto da Vite."],
         spiegazione="Vite traduce TypeScript da sé, senza controllare i tipi; il controllo lo "
                     "fa `tsc`, che con `noEmit` non scrive nulla. `&&` esegue il secondo comando "
                     "solo se il primo termina con successo: un errore di tipo blocca la build.",
         rif=R % "La build", trabocchetto=True))

d(chiusa("c20-public", CAP, "Vite",
         "Nella build di Vite, che differenza c'è fra un'immagine importata in `main.ts` e un "
         "file della cartella `public`?",
         "L'immagine importata riceve un nome con l'impronta (o finisce incorporata nel "
         "JavaScript, se piccola); i file di `public` vengono copiati con il loro nome.",
         ["I file di `public` vengono minificati e rinominati con l'impronta.",
          "Le immagini importate vengono copiate in `public` con il loro nome.",
          "Nessuna: tutto finisce in `dist/assets` con l'impronta nel nome.",
          "I file di `public` non vengono copiati in `dist`."],
         spiegazione="Vite analizza quali risorse l'applicazione importa davvero: le impacchetta "
                     "con un hash nel nome (le piccole le incorpora). I file di `public` sono "
                     "invece copiati in `dist` così come sono, con il loro nome (come "
                     "`favicon.svg`), perché vi si fa riferimento da fuori del codice.",
         rif=R % "La build"))

d(chiusa("c20-impronta", CAP, "Vite",
         "In un progetto Vite si cambia **solo** un colore nel file Sass importato da "
         "`main.ts`, e si rifà la build. Che cosa succede ai nomi dei bundle in `dist/assets`?",
         "Cambiano sia il CSS sia il JavaScript, anche se il contenuto del JavaScript è "
         "identico: l'hash tiene conto anche dei moduli importati.",
         ["Cambia solo il nome del CSS, l'unico file con un contenuto diverso.",
          "Non cambia nessun nome: l'impronta dipende solo dal nome del progetto.",
          "Cambiano i nomi di tutti i file, immagini comprese.",
          "Cambia solo il nome del JavaScript, che importa il file Sass."],
         spiegazione="Nell'esperimento del capitolo il CSS cambia contenuto e nome; il "
                     "JavaScript ha la stessa impronta MD5, cioè è identico byte per byte, ma "
                     "cambia nome lo stesso, perché in Vite l'hash di un bundle dipende anche "
                     "dai moduli che importa, CSS compreso. Le immagini, invariate, conservano "
                     "il nome; ripristinando il colore tornano i nomi di prima.",
         rif=R % "Fingerprinting dei nomi", trabocchetto=True))

d(chiusa("c20-cache-impronta", CAP, "Vite",
         "Perché i file con l'impronta nel nome si possono servire con "
         "`Cache-Control: max-age=31536000, immutable`, mentre `index.html` va ricontrollato a "
         "ogni visita?",
         "Ogni modifica produce un nome nuovo, quindi una copia vecchia non viene più richiesta; "
         "`index.html` contiene i nomi aggiornati.",
         ["Perché l'impronta nel nome impedisce al browser di metterli in cache.",
          "Perché `index.html` è più grande dei bundle.",
          "Perché Vite firma i bundle con una chiave segreta.",
          "Perché `immutable` vale solo per i file minificati."],
         spiegazione="Con nomi fissi (`index.js`), un browser potrebbe continuare a usare una "
                     "copia vecchia e mescolarla con l'HTML nuovo. Con l'impronta, una versione "
                     "nuova ha un nome nuovo: la copia vecchia resta valida ma nessuno la chiede "
                     "più. L'unico file da ricontrollare è quello che contiene i nomi, "
                     "`index.html`.",
         rif=R % "Fingerprinting dei nomi"))

d(chiusa("c20-dev-dependencies", CAP, "Vite",
         "Nel `package.json` di un progetto Vite, `vite` e `typescript` compaiono in "
         "`devDependencies`. Perché?",
         "Servono a costruire l'applicazione, non a eseguirla: nel browser arriva solo il "
         "risultato della build.",
         ["Perché sono installati globalmente sul sistema.",
          "Perché in produzione si usa una versione diversa di Vite.",
          "Perché `npm install` non installa mai le `devDependencies`.",
          "Perché servono solo al server di anteprima `vite preview`."],
         spiegazione="Le dipendenze di sviluppo sono gli strumenti del flusso di lavoro "
                     "(compilatori, bundler, linter). L'applicazione pubblicata è la cartella "
                     "`dist`, fatta di file statici che non hanno bisogno né di Vite né di "
                     "TypeScript.",
         rif=R % "Creare un progetto"))

d(chiusa("c20-trattino", CAP, "Vite",
         "Copiando da una slide il comando `npm install –D sass`, scritto con un trattino "
         "tipografico (–) al posto del trattino normale, che cosa succede?",
         "npm rifiuta il comando: `–D` non è un'opzione, ma un nome di pacchetto non valido.",
         ["Installa `sass` fra le dipendenze di sviluppo, come con `-D`.",
          "Installa `sass` fra le dipendenze normali, ignorando `–D`.",
          "Installa due pacchetti, `–D` e `sass`.",
          "Installa `sass` globalmente."],
         spiegazione="Per il terminale il trattino tipografico è un carattere qualunque: `–D` "
                     "non comincia con `-`, quindi npm lo prende per il nome di un pacchetto e "
                     "si ferma (*Argument starts with non-ascii dash*). Lo stesso succede a "
                     "`tsc –target es6`, letto come due file da compilare.",
         rif=R % "Aggiungere Sass", trabocchetto=True))

# ----------------------------------------------------------------------
# Domande aperte
d(aperta("c20-a-pre-post", CAP, "pre- e post-processori",
         "Che differenza c'è fra pre-processori e post-processori CSS? Si facciano esempi di "
         "strumenti e di funzionalità per ciascuna categoria.",
         ["Pre-processori (Sass, LESS, Stylus): «compilatori» da una sintassi propria che "
          "estende il CSS (variabili, annidamento, mixin, moduli, cicli) a CSS.",
          "Post-processori (PostCSS con i plugin): trasformano CSS esistente.",
          "Usi tipici dei post-processori: downleveling (`postcss-preset-env`), prefissi "
          "(Autoprefixer, guidato da Browserslist), minificazione, convenzioni ed errori.",
          "Catena tipica: sorgente Sass → pre-processore → CSS → post-processore → browser."],
         rif=R % "Pre- e post-processori CSS"))

d(aperta("c20-a-sass", CAP, "Sass",
         "Si descrivano almeno tre funzionalità di Sass, ciascuna con un piccolo esempio di "
         "codice SCSS e del CSS che ne risulta.",
         ["Variabili: `$primario: #333;` sostituite dal valore alla compilazione.",
          "Annidamento: `nav { a { ... } }` diventa `nav a { ... }`; `&` richiama il "
          "genitore (`&:hover`). Attenzione alla specificità.",
          "Mixin (`@mixin`/`@include`, anche con parametri e valori predefiniti), moduli "
          "(`@use` con prefisso) e parziali (`_file.scss`).",
          "Liste, mappe e controllo del flusso (`@if`, `@each`, `@for`) con interpolazione "
          "`#{}` per generare famiglie di regole."],
         rif=R % "Sass"))

d(aperta("c20-a-bundling", CAP, "bundling e minificazione",
         "Che cosa sono bundling, tree shaking e minificazione? Per ciascuno si spieghi perché "
         "si usa e che cosa guadagna l'utente finale.",
         ["Bundling: più file CSS/JS riuniti in uno, meno richieste HTTP al primo caricamento; "
          "l'ordine dei file conta.",
          "Tree shaking: eliminazione del codice mai usato, possibile perché `import`/`export` "
          "sono statici; bundle più piccoli.",
          "Minificazione: spazi, commenti e nomi locali accorciati senza cambiare il "
          "comportamento (Terser, esbuild); si somma alla compressione gzip/Brotli.",
          "Si fanno di solito insieme, con strumenti come esbuild o Vite."],
         rif=R % "Bundling e minificazione"))

d(aperta("c20-a-fingerprinting", CAP, "Vite",
         "Che cos'è il *fingerprinting* dei nomi dei file prodotti da una build? Quale problema "
         "risolve e come si combina con le intestazioni di cache HTTP?",
         ["Il nome del file contiene un hash del contenuto (es. `index-Dqtoo5RJ.js`): cambia "
          "solo se cambia il contenuto (in Vite anche se cambiano i moduli importati).",
          "Problema: con nomi fissi il browser può usare copie vecchie in cache e mescolarle con "
          "l'HTML nuovo.",
          "I file con l'impronta si mettono in cache «per sempre» (`max-age` lungo, "
          "`immutable`); `index.html`, che contiene i nomi, va ricontrollato a ogni visita."],
         rif=R % "Fingerprinting dei nomi"))

d(aperta("c20-a-vite", CAP, "Vite",
         "Che cos'è Vite? Si descrivano il server di sviluppo e la build di produzione, "
         "indicando che cosa fa ciascuno.",
         ["Strumento per lo sviluppo e il rilascio del front-end (`npm create vite@latest`; "
          "script `dev`, `build`, `preview`).",
          "Server di sviluppo: niente bundle, i sorgenti arrivano come moduli ES trasformati al "
          "volo (TypeScript, Sass); Hot Module Replacement via WebSocket.",
          "Build: `tsc` controlla i tipi, poi Vite (Rolldown) compila, unisce, minifica, applica "
          "il fingerprinting e scrive tutto in `dist` aggiornando `index.html`.",
          "`preview` serve `dist` per una prova locale; in produzione va un server statico."],
         rif=R % "Vite"))

d(aperta("c20-a-framework", CAP, "framework CSS",
         "Che cosa sono i framework CSS? Si descrivano vantaggi e limiti, e i due modi per "
         "personalizzare un framework come Bootstrap.",
         ["Insiemi di fogli di stile di uso generale (griglia, tipografia, componenti, reset): "
          "Bootstrap, Tailwind, Bulma…; si importano e si usano con le loro classi.",
          "Vantaggi: niente da riscrivere ogni volta, aspetto coerente; limiti: siti simili fra "
          "loro, CSS in più da scaricare.",
          "Personalizzazione 1: cambiare le variabili Sass (dichiarate con `!default`) **prima** "
          "dell'importazione e ricompilare.",
          "Personalizzazione 2: regole proprie che sovrascrivono quelle del framework."],
         rif=R % "Framework CSS"))
