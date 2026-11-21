"""Capitolo 19: TypeScript (compilazione e type stripping, tipi primitivi,
any e unknown, inferenza, tipi oggetto, unioni, alias e interfacce,
tipizzazione strutturale, asserzioni, letterali ed enumerazioni, tipi
funzione, generici, livelli di severità).

Le domande con codice sono verificate compilando davvero con tsc
(TypeScript 7.0.2, impostazioni predefinite: modalità severa) ed eseguendo
con Node 22 il JavaScript prodotto o direttamente il file .ts.
"""

from generatore import aperta, chiusa, domanda_ts

CAP = 19
R = "cap. 19, «%s»"

DOMANDE = []
d = DOMANDE.append

# testi ricorrenti
TSC = ("Il file `prova.ts` seguente viene compilato con `tsc prova.ts` (TypeScript 7, "
       "impostazioni predefinite) e il file `prova.js` prodotto viene eseguito con "
       "`node prova.js`. Che cosa succede?")
RIGHE = ("Il file seguente viene compilato con `tsc` (TypeScript 7, impostazioni "
         "predefinite). Quali righe vengono segnalate come errori?")

# ----------------------------------------------------------------------
# Compilare, eseguire, togliere i tipi
d(domanda_ts("c19-strip", CAP, "compilare ed eseguire",
             "Il file `prova.ts` seguente viene eseguito **direttamente** con "
             "`node prova.ts` (Node 22.22, che accetta i file `.ts`). Che cosa succede?",
             """
let crediti: number = 6;
crediti = "9 CFU";
console.log(crediti);""",
             "Viene stampato `9 CFU`: Node toglie le annotazioni di tipo senza controllarle.",
             ["Node segnala l'errore `TS2322` alla riga 2 e non esegue nulla.",
              "Viene sollevato un `SyntaxError` sui due punti dell'annotazione `: number`.",
              "Viene stampato `6`: l'assegnamento di una stringa viene ignorato.",
              "Viene sollevato un `TypeError` alla riga 2."],
             errori=["2:TS2322"], ts=(["9 CFU"], None),
             spiegazione="Da Node 22.18 il comando `node` accetta i file `.ts`: ne **cancella** le "
                         "annotazioni di tipo (*type stripping*) e manda in esecuzione il "
                         "JavaScript che resta, senza verificare nulla. L'errore `TS2322` "
                         "(una stringa assegnata a un `number`) lo segnalano soltanto `tsc` e "
                         "l'editor. Il `SyntaxError` sui due punti è quello che dava Node 22.14, "
                         "prima di questa funzionalità.",
             rif=R % "Node e la rimozione dei tipi", trabocchetto=True))

d(domanda_ts("c19-emissione", CAP, "compilare ed eseguire", TSC,
             """
function doppio(n: number): number {
  return n * 2;
}
console.log(doppio("21"));""",
             "`tsc` segnala un errore alla riga 4, ma produce comunque `prova.js`, che stampa "
             "`42`.",
             ["`tsc` segnala un errore alla riga 4 e non produce `prova.js`.",
              "`tsc` non segnala errori e `prova.js` stampa `2121`.",
              "`tsc` segnala un errore alla riga 4; `prova.js` stampa `2121`.",
              "`tsc` segnala un errore alla riga 2: manca la conversione in numero."],
             errori=["4:TS2345"], js=(["42"], None),
             spiegazione="L'argomento `\"21\"` non è un `number`, e `tsc` lo segnala (`TS2345`). "
                         "Ma un errore di tipo **non blocca** la traduzione: senza l'opzione "
                         "`noEmitOnError` il file JavaScript viene generato lo stesso, con le "
                         "annotazioni tolte. Eseguito, `\"21\" * 2` converte la stringa in numero "
                         "e vale `42` (con `+` si sarebbe ottenuto `2121`).",
             rif=R % "Correggere e compilare", trabocchetto=True))

d(chiusa("c19-superset", CAP, "compilare ed eseguire",
         "Quali delle seguenti affermazioni su TypeScript e sul compilatore `tsc` sono **vere**?",
         ["TypeScript è un superset di JavaScript: aggiunge i tipi alla sintassi del linguaggio.",
          "`tsc` controlla i tipi e traduce il codice in JavaScript, che è ciò che viene "
          "eseguito.",
          "Le annotazioni di tipo spariscono nel JavaScript prodotto."],
         ["I browser eseguono direttamente i file `.ts`.",
          "I tipi vengono controllati anche a runtime, a ogni assegnamento.",
          "Un errore di tipo impedisce sempre di generare il file `.js`.",
          "`tsc` produce codice macchina, più veloce del JavaScript."],
         multi=True,
         spiegazione="TypeScript estende JavaScript con un sistema di tipi statico e si compila "
                     "verso JavaScript: il controllo avviene **prima** dell'esecuzione, e nel "
                     "codice prodotto i tipi non ci sono più. Per impostazione predefinita `tsc` "
                     "genera il JavaScript anche quando segnala errori di tipo.",
         rif=R % "I transpiler"))

d(chiusa("c19-downleveling", CAP, "compilare ed eseguire",
         "Con TypeScript 7, senza indicare l'opzione `--target`, che cosa diventa nel file "
         "JavaScript prodotto l'istruzione `const nome = user?.name ?? \"anonimo\";`?",
         "Resta invariata: il bersaglio predefinito è ES2025, che conosce già `?.` e `??`.",
         ["Viene riscritta con confronti espliciti con `null` e `undefined`.",
          "Viene riscritta in ES5, con `var` al posto di `const`.",
          "`tsc` segnala un errore: `?.` e `??` richiedono `--target es2020`.",
          "Viene riscritta in ES3, il bersaglio più compatibile."],
         spiegazione="Il *downleveling* riscrive le funzionalità recenti con i mezzi di una "
                     "versione più vecchia del linguaggio, ma solo se il bersaglio lo richiede. "
                     "Dalla versione 6 il bersaglio predefinito è ES2025: `?.` e `??` (ES2020) "
                     "passano così come sono. Con `--target es2019` diventerebbero confronti con "
                     "`null` e `void 0`; ES3 ed ES5, in TypeScript 7, non esistono più.",
         rif=R % "Downleveling"))

d(chiusa("c19-target-es5", CAP, "compilare ed eseguire",
         "Un vecchio script di build compila con `tsc --target es5 app.ts`. Che cosa succede con "
         "TypeScript 7?",
         "`tsc` si ferma con un errore: il bersaglio ES5 è stato rimosso, e il minimo è ES6.",
         ["Produce codice ES5, con i template literal riscritti con `concat`.",
          "Ignora l'opzione e produce codice ES2025.",
          "Produce codice ES3, compatibile anche con ES5.",
          "Produce codice ES5 ma con un avviso di deprecazione."],
         spiegazione="Con TypeScript 7 i bersagli ES3 ed ES5 non esistono più: `--target es5` "
                     "produce l'errore `TS5108` (*Option 'target=ES5' has been removed*). Il "
                     "minimo è ES6 (o `es2015`); senza opzione il bersaglio è ES2025. Era "
                     "TypeScript 5 a produrre ES5 per impostazione predefinita, e a riscrivere i "
                     "template literal con `concat`.",
         rif=R % "Downleveling", trabocchetto=True))

# ----------------------------------------------------------------------
# Tipi: any, unknown, inferenza
d(domanda_ts("c19-any-impliciti", CAP, "any, unknown e inferenza", RIGHE,
             """
let x;
function saluta(nome) {
  console.log(`Ciao, ${nome}`);
}
saluta(x);""",
             "Solo la riga 2: il parametro `nome` è un `any` implicito.",
             ["Le righe 1 e 2: né `x` né `nome` hanno un tipo.",
              "Solo la riga 1: `x` non ha né tipo né valore.",
              "Nessuna: senza annotazioni TypeScript deduce `any` senza segnalare nulla.",
              "Solo la riga 5: si passa `undefined` a `saluta`."],
             errori=["2:TS7006"],
             spiegazione="Con TypeScript 7 la modalità severa è attiva di partenza, e con lei "
                     "`noImplicitAny`: il tipo di un parametro non si può dedurre, quindi `nome` "
                     "è un `any` implicito e viene segnalato (`TS7006`). `let x;` invece non è "
                     "un errore: a una variabile dichiarata senza valore TypeScript attribuisce, "
                     "punto per punto, il tipo dell'ultimo valore ricevuto. La risposta "
                     "«nessuna» valeva con TypeScript 5 senza opzioni.",
             rif=R % "Gli any impliciti", trabocchetto=True))

d(domanda_ts("c19-unknown", CAP, "any, unknown e inferenza", RIGHE,
             """
function a(x: any) { return x.nome; }
function b(x: unknown) { return x.nome; }
function c(x: unknown) { return (x as { nome: string }).nome; }
console.log(c({ nome: "ok" }));""",
             "Solo la riga 2.",
             ["Le righe 1 e 2.", "Le righe 2 e 3.", "Tutte e tre le funzioni.",
              "Nessuna: `any` e `unknown` sono equivalenti."],
             errori=["2:TS18046"], js=(["ok"], None),
             spiegazione="`any` disattiva i controlli: `x.nome` compila (riga 1). `unknown` "
                         "rappresenta anch'esso qualunque valore, ma non consente alcuna "
                         "operazione finché non se ne restringe il tipo: la riga 2 dà "
                         "`TS18046`. Alla riga 3 un'asserzione dice al compilatore che cosa "
                         "aspettarsi, e lui si fida (senza controllare nulla a runtime).",
             rif=R % "Altri tipi da conoscere", trabocchetto=True))

d(domanda_ts("c19-asserzione", CAP, "any, unknown e inferenza", TSC,
             """
const dato: unknown = "42";
const n = dato as number;
console.log(n + 1, typeof n);""",
             "`tsc` non segnala errori; il programma stampa `421 string`.",
             ["`tsc` non segnala errori; il programma stampa `43 number`.",
              "`tsc` non segnala errori; il programma stampa `43 string`.",
              "`tsc` segnala la riga 2: una stringa non si può convertire in `number`.",
              "Il programma solleva un `TypeError` alla riga 2: l'asserzione fallisce."],
             errori=[], js=(["421 string"], None),
             spiegazione="Un'asserzione di tipo è solo un'indicazione al compilatore: **non "
                         "converte** il valore e **non verifica** nulla a runtime. Nel JavaScript "
                         "prodotto `as number` sparisce, `n` resta la stringa `\"42\"`, quindi "
                         "`n + 1` concatena (`\"421\"`) e `typeof n` è `\"string\"`. Il compilatore "
                         "accetta l'asserzione perché da `unknown` si può asserire qualunque tipo.",
             rif=R % "Asserzioni di tipo", trabocchetto=True))

d(chiusa("c19-tipi-speciali", CAP, "any, unknown e inferenza",
         "Quali delle seguenti affermazioni sui tipi `any`, `unknown`, `void` e `never` sono "
         "**vere**?",
         ["Su un valore `unknown` non si può fare nulla senza prima restringerne il tipo.",
          "`never` è il tipo di ritorno di una funzione che solleva sempre un errore.",
          "`void` è il tipo dedotto per una funzione senza `return`.",
          "Un valore `any` si può assegnare a una variabile `number` senza errori."],
         ["`unknown` disattiva i controlli esattamente come `any`.",
          "`never` è il tipo di una funzione che restituisce `undefined`.",
          "Un'asserzione `as` verifica il tipo a runtime e solleva un errore se è sbagliato.",
          "`void` è un sinonimo di `null`."],
         multi=True,
         spiegazione="`any` disattiva i controlli (anche negli assegnamenti: un `any` va bene "
                     "ovunque); `unknown` accetta qualunque valore ma obbliga a restringerne il "
                     "tipo prima di usarlo. `void` è il tipo di ritorno delle funzioni che non "
                     "restituiscono nulla; `never` descrive valori che non si osservano mai, "
                     "come il risultato di una funzione che solleva sempre un'eccezione. Le "
                     "asserzioni non controllano nulla a runtime.",
         rif=R % "Altri tipi da conoscere"))

d(domanda_ts("c19-inizializzazione", CAP, "any, unknown e inferenza", TSC,
             """
class Animale { specie: string; }
const a = new Animale();
console.log(a.specie);""",
             "`tsc` segnala la riga 1 (proprietà senza valore iniziale); il JavaScript prodotto "
             "stampa `undefined`.",
             ["`tsc` non segnala errori; il programma stampa una stringa vuota.",
              "`tsc` non segnala errori; il programma stampa `undefined`.",
              "`tsc` segnala la riga 3: `specie` potrebbe essere `undefined`.",
              "`tsc` segnala la riga 1 e non produce il JavaScript."],
             errori=["1:TS2564"], js=(["undefined"], None),
             spiegazione="In modalità severa (predefinita da TypeScript 6) è attivo anche "
                         "`strictPropertyInitialization`: una proprietà dichiarata `string` senza "
                         "valore iniziale né assegnamento nel costruttore varrebbe `undefined`, e "
                         "`tsc` la segnala (`TS2564`). Il file viene comunque generato, ed "
                         "eseguito stampa proprio `undefined`. Si corregge con un valore iniziale "
                         "o con `specie!: string`.",
             rif=R % "Vincoli sui generici"))

# ----------------------------------------------------------------------
# Tipi oggetto, strutturali, interfacce
d(domanda_ts("c19-eccesso", CAP, "tipizzazione strutturale e interfacce", RIGHE,
             """
interface Corso { nome: string }
function stampa(c: Corso) { console.log(c.nome); }
const algebra = { nome: "Algebra", anno: 1 };
stampa(algebra);
stampa({ nome: "Fisica", anno: 2 });""",
             "Solo la riga 5.",
             ["Solo la riga 4.", "Le righe 4 e 5.",
              "Nessuna: con la tipizzazione strutturale le proprietà in più sono sempre ammesse.",
              "La riga 3: `anno` non fa parte di `Corso`."],
             errori=["5:TS2353"], js=(["Algebra", "Fisica"], None),
             spiegazione="Per la tipizzazione strutturale `algebra` è un `Corso`: ha la proprietà "
                         "`nome` di tipo `string`, e le proprietà in più non contano (riga 4). Un "
                         "**oggetto letterale** scritto direttamente dove è atteso un tipo, "
                         "però, viene controllato in modo più severo: una proprietà che il tipo "
                         "non prevede è quasi sempre un errore di battitura, e `tsc` la segnala "
                         "(`TS2353`, come per `year` nell'esempio del capitolo).",
             rif=R % "Tipizzazione strutturale", trabocchetto=True))

d(domanda_ts("c19-classi-strutturali", CAP, "tipizzazione strutturale e interfacce", TSC,
             """
class Gatto { nome = "Tom"; }
class Cane { nome = "Rex"; }
const g: Gatto = new Cane();
console.log(g instanceof Gatto, g.nome);""",
             "`tsc` non segnala errori; il programma stampa `false Rex`.",
             ["`tsc` segnala la riga 3: un `Cane` non è un `Gatto`.",
              "`tsc` non segnala errori; il programma stampa `true Rex`.",
              "`tsc` non segnala errori; il programma stampa `false Tom`.",
              "`tsc` non segnala errori; il programma stampa `true Tom`."],
             errori=[], js=(["false Rex"], None),
             spiegazione="La tipizzazione strutturale vale anche per le classi: `Cane` ha la "
                         "stessa forma di `Gatto` (una proprietà `nome` di tipo `string`), quindi "
                         "un `Cane` si può assegnare a una variabile `Gatto`. Ma il tipo esiste "
                         "solo per il compilatore: a runtime l'oggetto è un `Cane`, e "
                         "`instanceof`, che guarda la catena dei prototipi, risponde `false`. In "
                         "Java, con i tipi nominativi, la riga 3 non compilerebbe.",
             rif=R % "Tipizzazione strutturale", trabocchetto=True))

d(domanda_ts("c19-riapertura", CAP, "tipizzazione strutturale e interfacce", RIGHE,
             """
interface Pet { nome: string }
interface Pet { anni: number }
const matt: Pet = { nome: "Matt", anni: 2 };
type Gatto = { nome: string };
type Gatto = { anni: number };""",
             "Le righe 4 e 5: un alias di tipo non si può dichiarare due volte.",
             ["Le righe 1, 2, 4 e 5: né le interfacce né gli alias si possono ridichiarare.",
              "Solo la riga 3: `matt` ha una proprietà in più rispetto alla prima interfaccia.",
              "Solo la riga 5.",
              "Nessuna: sia le interfacce sia gli alias si fondono."],
             errori=["4:TS2300", "5:TS2300"],
             spiegazione="Le interfacce si possono **riaprire**: le due dichiarazioni di `Pet` si "
                         "fondono in una sola con entrambe le proprietà, e `matt` è corretto. Un "
                         "alias di tipo invece non si riapre: il nome risulta dichiarato due volte "
                         "(`TS2300`, segnalato su tutte e due le dichiarazioni). Gli alias si "
                         "estendono con le intersezioni (`&`).",
             rif=R % "Estendere interfacce e tipi"))

d(domanda_ts("c19-interfaccia-valore", CAP, "tipizzazione strutturale e interfacce", TSC,
             """
interface Persona { nome: string }
const p: Persona = { nome: "Ada" };
console.log(p instanceof Persona);""",
             "`tsc` segnala la riga 3: un'interfaccia esiste solo per il compilatore e non si può "
             "usare come valore; il JavaScript prodotto solleva un `ReferenceError`.",
             ["`tsc` non segnala errori; il programma stampa `true`.",
              "`tsc` non segnala errori; il programma stampa `false`.",
              "`tsc` segnala la riga 2: un oggetto letterale non è una `Persona`.",
              "`tsc` segnala la riga 3; il JavaScript prodotto stampa `false`."],
             errori=["3:TS2693"], js=([], "ReferenceError"),
             spiegazione="Le interfacce (come gli alias) spariscono nella traduzione: nel "
                         "JavaScript non resta nulla che si chiami `Persona`. `instanceof` vuole "
                         "a destra un valore, un costruttore, e `tsc` lo segnala (`TS2693`: "
                         "*only refers to a type, but is being used as a value*). Il file "
                         "prodotto, eseguito, solleva un `ReferenceError`.",
             rif=R % "Alias di tipo e interfacce", trabocchetto=True))

d(chiusa("c19-strutturale", CAP, "tipizzazione strutturale e interfacce",
         "Le interfacce `Person` e `Pet` hanno entrambe le proprietà `name: string` e "
         "`age: number`. Una funzione dichiara un parametro di tipo `Person`. Che cosa succede "
         "passandole un oggetto dichiarato di tipo `Pet`?",
         "Compila: per la tipizzazione strutturale contano solo le proprietà, non i nomi dei "
         "tipi.",
         ["Errore di compilazione: `Pet` e `Person` sono tipi diversi.",
          "Compila solo se `Pet` dichiara `extends Person`.",
          "Compila, ma a runtime viene sollevato un `TypeError`.",
          "Compila solo con un'asserzione esplicita `as Person`."],
         spiegazione="TypeScript ha un sistema di tipi **strutturale**: due tipi con la stessa "
                     "forma sono compatibili, qualunque nome abbiano. Java, con un sistema "
                     "**nominativo**, rifiuterebbe la chiamata.",
         rif=R % "Tipizzazione strutturale"))

# ----------------------------------------------------------------------
# Unioni, letterali, enumerazioni
d(domanda_ts("c19-restringimento", CAP, "unioni, letterali ed enumerazioni", RIGHE,
             """
function f(x: string | number | boolean) {
  if (typeof x === "string") return x.toUpperCase();
  if (typeof x === "number") return x.toFixed(1);
  return x.length;
}""",
             "Solo la riga 4: lì `x` può essere soltanto un `boolean`.",
             ["Le righe 2 e 3: su un tipo unione non si possono chiamare metodi specifici.",
              "Nessuna: dopo i due `if` il tipo di `x` è `never`.",
              "Solo la riga 1: un'unione di tre tipi non è ammessa.",
              "Le righe 2, 3 e 4."],
             errori=["4:TS2339"],
             spiegazione="Dentro ogni ramo TypeScript **restringe** il tipo: dopo "
                         "`typeof x === \"string\"` `x` è una stringa, dopo il secondo controllo "
                         "un numero. Alla riga 4 restano solo i `boolean`, che non hanno "
                         "`length`: errore `TS2339`. Sarebbe `never` solo se fossero stati "
                         "esclusi tutti i tipi dell'unione.",
             rif=R % "Tipi unione"))

d(domanda_ts("c19-letterali", CAP, "unioni, letterali ed enumerazioni", RIGHE,
             """
type Allineamento = "center" | "left" | "right";
let a: Allineamento = "left";
let b = "center";
a = b;
const c = "right";
a = c;""",
             "Solo la riga 4.",
             ["Le righe 4 e 6.", "Solo la riga 6.",
              "Nessuna: `\"center\"` e `\"right\"` sono valori ammessi.",
              "Le righe 3 e 4."],
             errori=["4:TS2322"],
             spiegazione="Per una variabile `let` inizializzata con `\"center\"` il tipo dedotto è "
                         "`string` (potrà cambiare valore), e una `string` qualunque non è "
                         "assegnabile al tipo letterale `Allineamento`: errore alla riga 4. Una "
                         "costante non può cambiare, quindi per `c` TypeScript deduce il tipo "
                         "letterale `\"right\"`, che è uno dei valori ammessi.",
             rif=R % "Tipi letterali ed enumerazioni", trabocchetto=True))

d(domanda_ts("c19-enum", CAP, "unioni, letterali ed enumerazioni",
             TSC.replace("Che cosa succede?", "Che cosa stampa?"),
             """
enum Colore { Rosso, Verde = 5, Blu }
console.log(Colore.Blu, Colore[5], Object.keys(Colore).length);""",
             "`6 Verde 6`",
             ["`2 Verde 3`", "`6 Blu 3`", "`2 undefined 3`", "`6 Verde 3`",
              "`6 undefined 6`"],
             errori=[], js=(["6 Verde 6"], None), n=4,
             spiegazione="Senza valore esplicito una costante vale la precedente più uno: dopo "
                         "`Verde = 5`, `Blu` vale 6. Un'enumerazione numerica non sparisce: "
                         "diventa un oggetto con la corrispondenza **nei due sensi**, quindi "
                         "`Colore[5]` è `\"Verde\"` e l'oggetto ha sei chiavi: `Rosso`, `Verde`, "
                         "`Blu` e le stringhe `\"0\"`, `\"5\"`, `\"6\"`.",
             rif=R % "Tipi letterali ed enumerazioni", trabocchetto=True))

d(domanda_ts("c19-enum-node", CAP, "unioni, letterali ed enumerazioni",
             "Il file `prova.ts` seguente viene eseguito in due modi: (1) `tsc prova.ts` e poi "
             "`node prova.js`; (2) direttamente `node prova.ts` (Node 22.22). Che cosa succede?",
             """
enum Priorita { Bassa, Media, Alta }
console.log(Priorita.Media);""",
             "(1) stampa `1`; (2) viene sollevato un `SyntaxError`: un'enumerazione non si può "
             "eseguire togliendo soltanto i tipi.",
             ["(1) e (2) stampano entrambi `1`.",
              "(1) e (2) stampano entrambi `Media`.",
              "(1) stampa `1`; (2) stampa `undefined`, perché Node toglie la dichiarazione.",
              "(1) `tsc` segnala un errore: servono valori espliciti; (2) stampa `1`."],
             errori=[], js=(["1"], None), ts=([], "SyntaxError"),
             spiegazione="A differenza delle annotazioni, un'enumerazione **non sparisce** nella "
                         "traduzione: `tsc` la trasforma in un oggetto (con `Media` che vale 1). "
                         "Node, che si limita a cancellare la sintassi dei tipi, non sa che cosa "
                         "farne: *TypeScript enum is not supported in strip-only mode*, un "
                         "`SyntaxError`.",
             rif=R % "Tipi letterali ed enumerazioni", trabocchetto=True))

# ----------------------------------------------------------------------
# Funzioni e generici
d(domanda_ts("c19-tipi-funzione", CAP, "tipi funzione e generici", RIGHE,
             """
let f: (x: string, y: number) => void;
f = (x: string) => {};
f = () => {};
f = (x: string, y: number, z: boolean) => {};""",
             "Solo la riga 4.",
             ["Le righe 2, 3 e 4: il numero di parametri deve coincidere.",
              "Le righe 2 e 3: mancano dei parametri.",
              "Solo la riga 3.", "Nessuna."],
             errori=["4:TS2322"],
             spiegazione="Una funzione che usa **meno** parametri può prendere il posto di una "
                         "che ne riceve di più: ignorerà gli argomenti in più (righe 2 e 3). Il "
                         "contrario no: chi chiama `f` passerà solo due argomenti, e `z` "
                         "resterebbe senza valore. È lo stesso errore dell'esempio del capitolo: "
                         "*Target signature provides too few arguments*.",
             rif=R % "Tipi funzione", trabocchetto=True))

d(domanda_ts("c19-generici", CAP, "tipi funzione e generici", TSC,
             """
function primo<T>(a: T[]): T { return a[0]; }
const x = primo([1, 2, 3]);
const y: string = primo([1, 2, 3]);
console.log(x, y);""",
             "`tsc` segnala la riga 3; il JavaScript prodotto stampa `1 1`.",
             ["`tsc` non segnala errori: `T` diventa `any`.",
              "`tsc` segnala le righe 2 e 3.",
              "`tsc` segnala la riga 3 e non produce il JavaScript.",
              "`tsc` segnala la riga 3; il JavaScript prodotto solleva un `TypeError`."],
             errori=["3:TS2322"], js=(["1 1"], None),
             spiegazione="La variabile di tipo `T` viene dedotta dall'argomento: con "
                         "`[1, 2, 3]` è `number`, e il risultato è un `number`, che non si può "
                         "assegnare a una variabile `string`. È la differenza con `any`: "
                         "l'informazione sul tipo **si conserva**. Il file viene comunque "
                         "generato, e a runtime i tipi non ci sono: stampa `1 1`.",
             rif=R % "Generici"))

d(domanda_ts("c19-find", CAP, "tipi funzione e generici", TSC,
             """
const nomi = ["Sam", "Cliff"];
const trovato = nomi.find((n) => n === "Amelie");
console.log(trovato.toUpperCase());""",
             "`tsc` segnala alla riga 3 che `trovato` potrebbe essere `undefined`; il JavaScript "
             "prodotto solleva un `TypeError`.",
             ["`tsc` non segnala errori; il programma stampa `undefined`.",
              "`tsc` non segnala errori; il programma solleva un `TypeError`.",
              "`tsc` segnala alla riga 2 che `find` non esiste sugli array.",
              "`tsc` segnala la riga 3 e non produce il JavaScript."],
             errori=["3:TS18048"], js=([], "TypeError"),
             spiegazione="`find` restituisce il primo elemento che soddisfa la condizione oppure "
                         "`undefined`: il tipo di `trovato` è `string | undefined`. Con "
                         "`strictNullChecks`, attivo di partenza da TypeScript 6, chiamare un "
                         "metodo senza controllare è un errore (`TS18048`). Il file viene "
                         "generato comunque, ed eseguito solleva proprio il `TypeError` che il "
                         "compilatore aveva previsto. (L'errore su `find` era quello di "
                         "TypeScript 5 con il bersaglio ES5.)",
             rif=R % "Livelli di severità"))

d(chiusa("c19-severita", CAP, "tipi funzione e generici",
         "Quali delle seguenti affermazioni sulle impostazioni predefinite di `tsc` sono "
         "**vere**?",
         ["Da TypeScript 6 l'opzione `strict` è attiva di partenza, con `noImplicitAny` e "
          "`strictNullChecks`.",
          "Con TypeScript 5 senza opzioni, `null` e `undefined` si potevano assegnare a "
          "qualunque tipo.",
          "Con TypeScript 7 il bersaglio predefinito è ES2025."],
         ["Con TypeScript 7 i controlli severi vanno attivati uno per uno con le opzioni.",
          "`strictNullChecks` vieta di usare `null` e `undefined` nei programmi.",
          "`noImplicitAny` vieta di scrivere `any` anche in modo esplicito.",
          "Con TypeScript 5 il bersaglio predefinito era ES2025."],
         multi=True,
         spiegazione="Fino a TypeScript 5 l'esperienza predefinita era permissiva: bersaglio "
                     "ES5, niente modalità severa, `null` assegnabile a ogni tipo. Da TypeScript "
                     "6 `strict` è attiva di partenza (`noImplicitAny`, `strictNullChecks`, "
                     "`strictPropertyInitialization`…) e il bersaglio è ES2025. "
                     "`strictNullChecks` non vieta `null`: obbliga a gestirlo; `noImplicitAny` "
                     "segnala solo gli `any` **impliciti**.",
         rif=R % "Livelli di severità"))

# ----------------------------------------------------------------------
# Domande aperte
d(aperta("c19-a-perche", CAP, "compilare ed eseguire",
         "Che cos'è TypeScript e quali problemi di JavaScript intende risolvere? Si spieghi che "
         "cosa fa il compilatore `tsc` e in che cosa differisce dall'eseguire un file `.ts` "
         "direttamente con Node.",
         ["Superset di JavaScript con tipizzazione statica (Microsoft, 2012): gli errori di tipo "
          "emergono prima dell'esecuzione, e l'editor può aiutare (completamento, refactoring).",
          "`tsc` controlla i tipi e traduce in JavaScript (le annotazioni spariscono); può fare "
          "*downleveling* verso versioni più vecchie del linguaggio (`--target`).",
          "Un errore di tipo non blocca la generazione del file (salvo `noEmitOnError`).",
          "Node 22.18+ esegue i `.ts` togliendo i tipi senza controllarli (*type stripping*); "
          "non funziona con sintassi che va tradotta, come le enumerazioni."],
         rif=R % "I transpiler"))

d(aperta("c19-a-strutturale", CAP, "tipizzazione strutturale e interfacce",
         "Che cosa si intende per **tipizzazione strutturale**? Si confronti con la "
         "tipizzazione nominativa di Java, con un esempio, e si indichi un caso in cui "
         "TypeScript segnala comunque le proprietà in più.",
         ["Strutturale: la compatibilità dipende dalla forma (proprietà e tipi), non dal nome "
          "del tipo.",
          "Esempio: `Person` e `Pet` con le stesse proprietà sono intercambiabili; in Java "
          "servirebbe una relazione dichiarata (`extends`/`implements`).",
          "Un oggetto con proprietà in più è compatibile (se ha almeno quelle richieste).",
          "Eccezione: un oggetto letterale scritto direttamente dove è atteso un tipo non può "
          "avere proprietà sconosciute (`TS2353`)."],
         rif=R % "Tipizzazione strutturale"))

d(aperta("c19-a-any-unknown", CAP, "any, unknown e inferenza",
         "Si confrontino i tipi `any` e `unknown`. Che cosa sono le asserzioni di tipo e che "
         "cosa garantiscono?",
         ["`any`: qualunque valore, nessun controllo (si può usare e assegnare ovunque): "
          "rinuncia ai vantaggi di TypeScript.",
          "`unknown`: qualunque valore, ma nessuna operazione finché non si restringe il tipo "
          "(`typeof`, `Array.isArray`…): più sicuro.",
          "Asserzione (`valore as Tipo`): indicazione al compilatore quando ne sappiamo più di "
          "lui (es. `getElementById(...) as HTMLInputElement`).",
          "Non verifica né converte nulla a runtime: se è sbagliata l'errore emerge "
          "durante l'esecuzione."],
         rif=R % "Asserzioni di tipo"))

d(aperta("c19-a-generici", CAP, "tipi funzione e generici",
         "A che cosa servono i **generici** in TypeScript? Si mostri l'esempio della funzione "
         "identità e si spieghi perché è preferibile ad `any`; che cosa aggiunge un vincolo "
         "con `extends`?",
         ["Servono a scrivere codice riusabile con tipi diversi, conservando l'informazione "
          "sul tipo.",
          "`function identity<T>(x: T): T { return x; }`: il tipo in uscita è quello in "
          "ingresso (dedotto o esplicito, `identity<string>(...)`).",
          "Con `any` il risultato sarebbe `any`: si perde il tipo e i controlli.",
          "`<T extends Animal>`: `T` deve avere almeno la forma di `Animal`, e dentro la "
          "funzione se ne possono usare le proprietà."],
         rif=R % "Generici"))

d(aperta("c19-a-severita", CAP, "tipi funzione e generici",
         "Che cosa controllano le opzioni `noImplicitAny` e `strictNullChecks`? Come sono "
         "cambiate le impostazioni predefinite di `tsc` fra TypeScript 5 e TypeScript 6/7?",
         ["`noImplicitAny`: errore quando un tipo non si può dedurre e diventerebbe `any` "
          "(tipicamente i parametri senza annotazione).",
          "`strictNullChecks`: `null` e `undefined` non sono assegnabili agli altri tipi e "
          "vanno gestiti esplicitamente (es. il risultato di `find`).",
          "TypeScript 5: controlli severi spenti, bersaglio ES5 (ES3 fino alla 4.9).",
          "TypeScript 6/7: `strict` attiva di partenza (con anche "
          "`strictPropertyInitialization`), bersaglio ES2025."],
         rif=R % "Livelli di severità"))

d(aperta("c19-a-type-interface", CAP, "tipizzazione strutturale e interfacce",
         "Si confrontino alias di tipo (`type`) e interfacce (`interface`): come si definiscono, "
         "come si estendono e quale differenza fondamentale li distingue.",
         ["Entrambi danno un nome a un tipo oggetto (codice DRY); gli alias possono nominare "
          "anche unioni e letterali.",
          "Interfacce: si estendono con `extends`; alias: con le intersezioni `&`.",
          "Differenza chiave: un'interfaccia si può riaprire (le dichiarazioni con lo stesso "
          "nome si fondono), un alias no (`TS2300`).",
          "Esistono solo a tempo di compilazione: nel JavaScript non resta nulla."],
         rif=R % "Alias di tipo e interfacce"))
