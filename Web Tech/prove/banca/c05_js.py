"""Capitolo 5: JavaScript (variabili, scope, hoisting, tipi, operatori,
funzioni, closure, oggetti, this, costruttori, optional chaining)."""

from generatore import (FONTE_2024, FONTE_AULA, Err, L, aperta, chiusa, esito, famiglia,
                        uscita_js)

CAP = 5
R = "cap. 5, «%s»"

DOMANDE = []
d = DOMANDE.append

# ----------------------------------------------------------------------
# Famiglia: typeof
TYPEOF = [
    ("42", "number"), ("3.14", "number"), ("42 / 0", "number"), ("42 * \"Hello\"", "number"),
    ("NaN", "number"), ("\"42\"", "string"), ("'hello'", "string"), ("`${1 + 1}`", "string"),
    ("false", "boolean"), ("1 < 2", "boolean"), ("null", "object"), ("undefined", "undefined"),
    ("[1, 2, 3]", "object"), ("{ a: 1 }", "object"), ("function () {}", "function"),
    ("() => 1", "function"), ("10n", "bigint"), ("Symbol(\"id\")", "symbol"),
    ("new Date()", "object"), ("typeof 42", "string"),
]
NOMI_TIPI = ["number", "string", "boolean", "object", "undefined", "function", "null", "array",
             "bigint", "symbol", "NaN", "integer"]


@famiglia("c05-typeof", CAP, "tipi di dato e typeof", varianti=4)
def _typeof(rng):
    scelte = rng.sample(TYPEOF, 3)
    # typeof lega più forte degli operatori binari: le espressioni composte
    # vanno fra parentesi (typeof 1 < 2 sarebbe ("number" < 2), cioè false)
    codice = "\n".join("console.log(typeof %s);" % (
        "(%s)" % e if (" " in e and not e.startswith("typeof") and not e.startswith("new")
                       and not e.startswith("Symbol")) or e.startswith("{") else e)
        for e, _ in scelte)
    giusta = [t for _, t in scelte]
    sbagliate = set()
    errori = {"null": "null", "[1, 2, 3]": "array", "NaN": "NaN", "function () {}": "object",
              "() => 1": "object", "42 / 0": "Infinity", "10n": "number",
              "Symbol(\"id\")": "string", "typeof 42": "number", "new Date()": "date",
              "42 * \"Hello\"": "NaN", "`${1 + 1}`": "number", "1 < 2": "number"}
    for i, (e, t) in enumerate(scelte):
        alternativa = list(giusta)
        alternativa[i] = errori.get(e, rng.choice([x for x in NOMI_TIPI if x != t]))
        sbagliate.add(tuple(alternativa))
    while len(sbagliate) < 5:
        alternativa = [rng.choice([x for x in NOMI_TIPI if x != t]) if rng.random() < 0.5 else t
                       for t in giusta]
        if alternativa != giusta:
            sbagliate.add(tuple(alternativa))
    sbagliate = sorted(sbagliate)
    rng.shuffle(sbagliate)
    return uscita_js("c05-typeof", CAP, "tipi di dato e typeof", codice, giusta,
                     [list(s) for s in sbagliate[:5]], n=4,
                     spiegazione="`typeof` restituisce una stringa: i tipi primitivi `number` "
                                 "(anche `NaN` e `Infinity`), `string`, `boolean`, `undefined`, "
                                 "`bigint`, `symbol`; per gli oggetti (array e `null` compresi, "
                                 "una storica stranezza) `object`, e `function` per le funzioni.",
                     rif=R % "Tipi di dato primitivi")


d(_typeof)

# Famiglia: == e ===
CONFRONTI = [
    ('"1" == 1', True), ('"1" === 1', False), ("0 == false", True), ("0 === false", False),
    ("true == 1", True), ("true === 1", False), ('true == "1"', True), ("true == 42", False),
    ('"JS" === "JS"', True), ("42 === 42", True), ("null == undefined", True),
    ("null === undefined", False), ('"" == 0', True), ("NaN == NaN", False),
]


@famiglia("c05-uguaglianza", CAP, "uguaglianza debole e stretta", varianti=4)
def _uguaglianza(rng):
    scelte = rng.sample(CONFRONTI, 3)
    codice = "console.log(%s);" % ", ".join(e for e, _ in scelte)
    giusta = " ".join(str(v).lower() for _, v in scelte)
    sbagliate = []
    for maschera in range(8):
        valori = [v ^ bool(maschera >> i & 1) for i, (_, v) in enumerate(scelte)]
        t = " ".join(str(v).lower() for v in valori)
        if t != giusta:
            sbagliate.append([t])
    rng.shuffle(sbagliate)
    return uscita_js("c05-uguaglianza", CAP, "uguaglianza debole e stretta", codice, [giusta],
                     sbagliate[:5], n=4,
                     spiegazione="`===` confronta valore **e** tipo: con tipi diversi è sempre "
                                 "`false`. `==` invece converte gli operandi: stringhe e booleani "
                                 "diventano numeri (`\"1\" == 1`, `true == 1`, `0 == false` sono "
                                 "veri; `true == 42` è falso perché `true` diventa 1). `null == "
                                 "undefined` è vero, mentre `NaN` non è uguale a niente, nemmeno "
                                 "a se stesso. Per evitare sorprese si usa sempre `===`.",
                     rif=R % "Uguaglianza debole e uguaglianza stretta")


d(_uguaglianza)

# ----------------------------------------------------------------------
# Il ciclo di vita di let (prova intercorso 2024)
d(chiusa("c05-prova-let", CAP, "variabili, scope e hoisting",
         'Si consideri il seguente frammento di codice JavaScript (si assuma la presenza di '
         '`"use strict";`).',
         ["In Linea 3, `x` è dichiarata ma non inizializzata.",
          "In Linea 5, `x` ha valore `undefined`."],
         ["In Linea 3, `x` è inizializzata a `undefined`.",
          "In Linea 5, `x` ha valore `null`.",
          "Il codice esegue senza sollevare errori.",
          "In Linea 1, `x` è inizializzata ma non dichiarata."],
         codice=L("js", """
console.log(x);
if (true) {
  console.log(x);
  let x;
  console.log(x); }"""),
         dopo="Con riferimento al ciclo di vita di una variabile dichiarata con `let`, indicare "
              "quali delle seguenti affermazioni sono **vere**.",
         multi=True, fisse=True,
         spiegazione="Una variabile `let` viene dichiarata (sollevata) all'inizio del suo blocco, "
                     "ma resta non inizializzata fino alla riga della dichiarazione: dalla linea "
                     "2 alla 4 è nella *temporal dead zone*, e usarla solleva un "
                     "`ReferenceError`. Con `let x;` viene inizializzata a `undefined`. In Linea "
                     "1, fuori dal blocco, `x` non esiste affatto: l'esecuzione si ferma proprio "
                     "lì con un `ReferenceError`.",
         rif=R % "Il ciclo di vita di una variabile", fonte=FONTE_2024))

d(uscita_js("c05-prova-try", CAP, "variabili, scope e hoisting",
            """
try { console.log("A"); x = 1; console.log(x); }
catch(e) { console.log("X"); } finally { console.log("Z"); }""",
            ["A", "X", "Z"],
            [Err("ReferenceError"), ["X", "Z"], ["A", "1", "Z"], ["A", "1", "X", "Z"],
             Err("ReferenceError", ["A"])],
            spiegazione="In modalità strict assegnare a una variabile mai dichiarata solleva un "
                        "`ReferenceError` (senza strict creerebbe una variabile globale). "
                        "L'errore viene catturato dal `catch`, e il blocco `finally` viene "
                        "eseguito in ogni caso.",
            rif=R % "Prima di ECMAScript 6: var e dichiarazioni implicite",
            fonte=FONTE_2024))

d(chiusa("c05-primitivi", CAP, "tipi di dato e typeof",
         "Quali dei seguenti **non** sono tipi di dato primitivi in JavaScript?",
         ["`array`", "`Promise`", "`float`", "`object`", "`integer`"],
         ["`boolean`", "`number`", "`string`", "`undefined`", "`bigint`", "`symbol`"],
         multi=True,
         spiegazione="I tipi primitivi sono `number`, `string`, `boolean`, `undefined`, `null`, "
                     "`bigint` e `symbol`. Esiste un solo tipo numerico (`number`, a virgola "
                     "mobile): `float` e `integer` non esistono. Array, Promise e funzioni sono "
                     "oggetti.",
         rif=R % "Tipi di dato primitivi", fonte=FONTE_2024))

d(uscita_js("c05-var-blocco", CAP, "variabili, scope e hoisting",
            """
if (true) {
  var a = 1;
  let b = 2;
}
console.log(typeof a, typeof b);""",
            ["number undefined"],
            [["number number"], ["undefined undefined"], ["undefined number"],
             Err("ReferenceError"), Err("ReferenceError", ["number"])],
            spiegazione="`var` ha visibilità di funzione (qui globale): `a` esiste anche fuori dal "
                        "blocco. `let` ha visibilità di blocco: fuori dall'`if` `b` non esiste. "
                        "`typeof` applicato a un nome non dichiarato restituisce `\"undefined\"` "
                        "invece di sollevare un errore.",
            rif=R % "Gli scope"))

d(uscita_js("c05-var-hoisting", CAP, "variabili, scope e hoisting",
            """
console.log(n);
var n = 5;
console.log(n);""",
            ["undefined", "5"],
            [Err("ReferenceError"), ["5", "5"], Err("TypeError"), ["null", "5"],
             Err("ReferenceError", ["undefined"])],
            spiegazione="Le dichiarazioni `var` vengono sollevate (*hoisting*) all'inizio dello "
                        "scope e inizializzate subito a `undefined`; l'assegnamento resta al suo "
                        "posto. Con `let` la prima riga solleverebbe invece un `ReferenceError` "
                        "(TDZ).",
            rif=R % "Hoisting"))

d(uscita_js("c05-let-tdz", CAP, "variabili, scope e hoisting",
            """
let x = "esterna";
function f() {
  console.log(x);
  let x = "interna";
}
f();""",
            Err("ReferenceError"),
            [["esterna"], ["undefined"], ["interna"], ["esterna", "interna"]],
            spiegazione="Dentro `f` la dichiarazione `let x` viene sollevata all'inizio della "
                        "funzione e **nasconde** la `x` esterna, ma fino alla sua riga è nella "
                        "*temporal dead zone*: leggerla solleva un `ReferenceError`, non stampa "
                        "la variabile esterna.",
            rif=R % "Hoisting"))

d(uscita_js("c05-const-oggetto", CAP, "variabili, scope e hoisting",
            """
const pet = { nome: "Fido" };
pet.nome = "Rex";
console.log(pet.nome);
pet = { nome: "Fufi" };
console.log(pet.nome);""",
            Err("TypeError", ["Rex"]),
            [["Rex", "Fufi"], Err("TypeError"), ["Fido", "Fufi"], ["Rex", "Rex"],
             Err("TypeError", ["Fido"])],
            spiegazione="`const` impedisce di **riassegnare la variabile**, non di modificare "
                        "l'oggetto a cui si riferisce: cambiare `pet.nome` è lecito, assegnare a "
                        "`pet` un altro oggetto solleva un `TypeError` (*Assignment to constant "
                        "variable*).",
            rif=R % "let e const"))

d(uscita_js("c05-asi", CAP, "funzioni",
            """
function risposta() {
  return
    42;
}
console.log(risposta());""",
            ["undefined"],
            [["42"], Err("SyntaxError"), ["null"], ["NaN"]],
            spiegazione="Per l'inserimento automatico dei punti e virgola, un `return` seguito da "
                        "un a capo diventa `return;`: la funzione restituisce `undefined` e "
                        "`42;` è codice irraggiungibile. Il valore va scritto sulla stessa riga "
                        "del `return`.",
            rif=R % "Il linguaggio"))

d(uscita_js("c05-default", CAP, "funzioni",
            """
function saluta(nome = "ospite") {
  console.log("Ciao " + nome);
}
saluta();
saluta(undefined);
saluta(null);""",
            ["Ciao ospite", "Ciao ospite", "Ciao null"],
            [["Ciao ospite", "Ciao undefined", "Ciao null"],
             ["Ciao ospite", "Ciao ospite", "Ciao ospite"],
             ["Ciao undefined", "Ciao undefined", "Ciao null"],
             ["Ciao ospite", "Ciao undefined", "Ciao ospite"]],
            spiegazione="Il valore predefinito di un parametro si usa quando l'argomento manca o "
                        "vale `undefined`; `null` è un valore a tutti gli effetti, quindi viene "
                        "usato così com'è.",
            rif=R % "Argomenti predefiniti"))

d(uscita_js("c05-hoisting-fn", CAP, "funzioni",
            """
console.log(quadrato(3));
console.log(cubo(2));
function quadrato(n) { return n * n; }
var cubo = function (n) { return n * n * n; };""",
            Err("TypeError", ["9"]),
            [["9", "8"], Err("ReferenceError", ["9"]), Err("TypeError"), ["9", "undefined"],
             Err("ReferenceError")],
            spiegazione="Le dichiarazioni di funzione vengono sollevate per intero: `quadrato` si "
                        "può chiamare prima della sua definizione. `cubo` invece è una variabile "
                        "`var` a cui viene assegnata un'espressione di funzione: durante "
                        "l'hoisting vale `undefined`, e chiamarla solleva un `TypeError` (*cubo "
                        "is not a function*). Con `let` o `const` si avrebbe un "
                        "`ReferenceError`.",
            rif=R % "Hoisting delle funzioni"))

d(uscita_js("c05-prova-hoisting", CAP, "funzioni",
            """
foo();
function foo() { console.log("Hello!"); }
foo();""",
            ["Hello!", "Hello!"],
            [["undefined", "Hello!", "Hello!"], Err("ReferenceError"),
             ["Hello!", "Hello!", "Hello!"]],
            testo="Qual è l'output dell'esecuzione del seguente frammento di codice JavaScript "
                  "(si assuma la presenza di `\"use strict\";`)?",
            fisse=True,
            spiegazione="Le dichiarazioni di funzione vengono sollevate per intero (nome e corpo) "
                        "all'inizio dello scope: la prima chiamata, che precede la definizione, "
                        "funziona già. La definizione da sola non esegue nulla: le chiamate sono "
                        "due, quindi `Hello!` compare due volte. Non compare `undefined`, perché "
                        "il valore restituito dalle chiamate non viene stampato.",
            rif=R % "Hoisting delle funzioni", fonte=FONTE_AULA))

d(uscita_js("c05-closure", CAP, "closure",
            """
function contatore() {
  let n = 0;
  return () => ++n;
}
const a = contatore();
const b = contatore();
a(); a();
console.log(a(), b());""",
            ["3 1"],
            [["3 3"], ["1 1"], ["2 1"], ["3 4"], Err("ReferenceError")],
            spiegazione="Ogni chiamata di `contatore` crea un nuovo ambiente con la propria "
                        "variabile `n`, e la funzione restituita lo ricorda (*closure*). `a` e "
                        "`b` hanno contatori indipendenti: `a` arriva a 3, `b` a 1.",
            rif=R % "Funzioni annidate restituite"))

d(uscita_js("c05-riferimenti", CAP, "oggetti",
            """
let a = { x: 1, dati: { y: 1 } };
let b = a;
let c = { ...a };
b.x = 2;
c.dati.y = 3;
console.log(a.x, a.dati.y);""",
            ["2 3"],
            [["1 1"], ["2 1"], ["1 3"], ["2 undefined"], Err("TypeError")],
            spiegazione="Gli oggetti si assegnano **per riferimento**: `b` è lo stesso oggetto di "
                        "`a`. La sintassi `{ ...a }` crea una copia **superficiale**: `c.x` è "
                        "indipendente, ma `c.dati` punta allo stesso oggetto interno di "
                        "`a.dati`.",
            rif=R % "Clonare un oggetto"))

d(uscita_js("c05-this", CAP, "this e costruttori",
            """
const pet = {
  nome: "Fido",
  saluta() { console.log("Ciao, sono " + this.nome); }
};
pet.saluta();
const f = pet.saluta;
f();""",
            Err("TypeError", ["Ciao, sono Fido"]),
            [["Ciao, sono Fido", "Ciao, sono Fido"], ["Ciao, sono Fido", "Ciao, sono undefined"],
             Err("TypeError"), ["Ciao, sono Fido", "Ciao, sono "]],
            spiegazione="`this` dipende da **come** si chiama la funzione: in `pet.saluta()` vale "
                        "`pet`. `f` è la stessa funzione chiamata da sola: in modalità strict "
                        "`this` vale `undefined`, e leggere `this.nome` solleva un `TypeError`.",
            rif=R % "La parola chiave this"))

d(uscita_js("c05-arrow-this", CAP, "this e costruttori",
            """
function Timer() {
  this.secondi = 0;
  this.avanza = () => { this.secondi++; };
}
const t = new Timer();
const avanza = t.avanza;
avanza(); avanza();
console.log(t.secondi);""",
            ["2"],
            [["0"], Err("TypeError"), ["NaN"], ["undefined"]],
            spiegazione="Le arrow function non hanno un proprio `this`: usano quello dello scope "
                        "in cui sono definite, qui l'oggetto creato da `new Timer()`. Per questo "
                        "`avanza` funziona anche chiamata da sola. Con una funzione normale "
                        "`this` sarebbe `undefined` e si avrebbe un `TypeError`.",
            rif=R % "La parola chiave this"))

d(uscita_js("c05-costruttore", CAP, "this e costruttori",
            """
function Persona(nome) {
  this.nome = nome;
}
const p = new Persona("Ada");
console.log(p.nome);
const q = Persona("Alan");
console.log(q);""",
            Err("TypeError", ["Ada"]),
            [["Ada", "undefined"], ["Ada", "Alan"], Err("TypeError"), ["Ada", "[object Object]"]],
            spiegazione="Con `new` viene creato un nuovo oggetto e `this` si riferisce a esso. "
                        "Senza `new` la funzione viene chiamata normalmente: in modalità strict "
                        "`this` vale `undefined` e `this.nome = ...` solleva un `TypeError`.",
            rif=R % "Costruttori"))

d(uscita_js("c05-optional", CAP, "oggetti",
            """
const pet = { nome: "Fido" };
console.log(pet.razza);
console.log(pet.padrone?.nome);
console.log(pet.padrone.nome);""",
            Err("TypeError", ["undefined", "undefined"]),
            [Err("ReferenceError", ["undefined", "undefined"]), ["undefined", "undefined", "undefined"],
             Err("TypeError", ["undefined"]), Err("TypeError")],
            spiegazione="Leggere una proprietà inesistente restituisce `undefined`. L'optional "
                        "chaining `?.` si ferma se ciò che sta a sinistra è `null` o `undefined` "
                        "e restituisce `undefined`. Senza, leggere `.nome` da `undefined` "
                        "solleva un `TypeError` (non un `ReferenceError`: la variabile `pet` "
                        "esiste).",
            rif=R % "Optional chaining"))

d(uscita_js("c05-readonly", CAP, "oggetti",
            """
const conto = { saldo: 100 };
Object.defineProperty(conto, "saldo", { writable: false });
console.log(conto.saldo);
conto.saldo = 0;
console.log(conto.saldo);""",
            Err("TypeError", ["100"]),
            [["100", "0"], ["100", "100"], Err("TypeError"), ["0", "0"]],
            spiegazione="Con `writable: false` la proprietà diventa di sola lettura. In modalità "
                        "strict assegnarle un valore solleva un `TypeError`; senza strict "
                        "l'assegnamento verrebbe ignorato in silenzio (e si stamperebbe di "
                        "nuovo 100).",
            rif=R % "Configurare le proprietà"))

d(uscita_js("c05-getter", CAP, "oggetti",
            """
const r = {
  base: 3, altezza: 4,
  get area() { return this.base * this.altezza; },
  set lato(v) { this.base = v; this.altezza = v; }
};
r.lato = 5;
console.log(r.area);""",
            ["25"],
            [["12"], Err("TypeError"), ["undefined"], ["[Function: get area]"]],
            spiegazione="Un getter si legge come una proprietà (`r.area`, senza parentesi) ma "
                        "esegue la funzione; un setter si attiva con un assegnamento. `r.lato = "
                        "5` imposta base e altezza a 5, quindi l'area vale 25.",
            rif=R % "Getter e setter"))

d(uscita_js("c05-template", CAP, "funzioni",
            """
const nome = "Ada";
const anni = 36;
console.log(`${nome} ha ${anni + 1} anni`);
console.log('${nome} ha ${anni + 1} anni');""",
            ["Ada ha 37 anni", "${nome} ha ${anni + 1} anni"],
            [["Ada ha 37 anni", "Ada ha 37 anni"], ["Ada ha 361 anni", "${nome} ha ${anni + 1} anni"],
             ["Ada ha 37 anni", "Ada ha 361 anni"], Err("SyntaxError")],
            spiegazione="Solo i *template literal*, delimitati dagli accenti gravi, interpretano "
                        "le espressioni `${...}`; fra apici singoli o doppi il testo resta "
                        "letterale. Dentro `${}` si valuta un'espressione: `anni + 1` è 37.",
            rif=R % "Funzioni"))

d(uscita_js("c05-truthy", CAP, "uguaglianza debole e stretta",
            """
const valori = [0, "0", "", [], null, NaN];
for (const v of valori) {
  if (v) console.log(JSON.stringify(v));
}""",
            ['"0"', "[]"],
            [['"0"'], ["0", '"0"', "[]"], ["[]"], ['"0"', '""', "[]"], []],
            spiegazione="Sono *falsy* `false`, `0`, `\"\"`, `null`, `undefined` e `NaN`: tutto il "
                        "resto è *truthy*, compresa la stringa `\"0\"` (non vuota) e l'array vuoto "
                        "(un oggetto).",
            rif=R % "Operatori"))

d(chiusa("c05-let-const-var", CAP, "variabili, scope e hoisting",
         "Quali delle seguenti affermazioni su `var`, `let` e `const` sono **vere**?",
         ["`let` e `const` hanno visibilità di blocco.",
          "`var` ha visibilità di funzione.",
          "Una variabile `const` va inizializzata nella dichiarazione.",
          "Le variabili `var` vengono sollevate e inizializzate a `undefined`."],
         ["`const` rende immutabile l'oggetto a cui la variabile si riferisce.",
          "Le variabili `let` non vengono sollevate affatto.",
          "Con `let` si può ridichiarare una variabile nello stesso blocco.",
          "`var` ha visibilità di blocco, come `let`.",
          "Leggere una variabile `let` prima della dichiarazione restituisce `undefined`."],
         multi=True,
         spiegazione="`let`/`const` sono visibili nel blocco e vengono sollevate ma restano non "
                     "inizializzate fino alla dichiarazione (TDZ: leggerle prima solleva un "
                     "`ReferenceError`). `var` è visibile nella funzione e viene inizializzata "
                     "subito a `undefined`. `const` impedisce la riassegnazione, non la "
                     "modifica dell'oggetto.",
         rif=R % "Variabili"))

d(chiusa("c05-script", CAP, "includere JavaScript",
         "Quale dei seguenti modi di includere uno script esterno è corretto?",
         '``<script src="app.js"></script>``',
         ['``<script src="app.js" />``', '``<link rel="script" href="app.js">``',
          '``<script href="app.js"></script>``', '``<js src="app.js"></js>``',
          '``<script>app.js</script>``'],
         spiegazione="Il tag `script` non è mai auto-chiudente: anche con `src` va chiuso con "
                     "`</script>`. `<script src=\"app.js\" />` viene letto come un tag aperto, e "
                     "il resto della pagina finisce dentro lo script.",
         rif=R % "Includere JavaScript in una pagina"))

d(chiusa("c05-strict", CAP, "variabili, scope e hoisting",
         "Quali effetti ha la direttiva `\"use strict\";`?",
         ["Assegnare a una variabile non dichiarata solleva un `ReferenceError`.",
          "In una funzione chiamata da sola `this` vale `undefined`.",
          "Assegnare a una proprietà di sola lettura solleva un `TypeError`."],
         ["Rende obbligatorio dichiarare il tipo delle variabili.",
          "Impedisce di usare le arrow function.",
          "Trasforma `==` in `===` in tutto lo script.",
          "Vieta l'uso di `var` e di `function`.",
          "Fa eseguire lo script solo dopo il caricamento della pagina."],
         multi=True,
         spiegazione="La modalità strict trasforma in errori alcuni comportamenti silenziosi "
                     "della versione «sciatta» del linguaggio: dichiarazioni implicite, `this` "
                     "globale nelle funzioni chiamate da sole, scritture su proprietà non "
                     "scrivibili. I moduli e le classi sono sempre in modalità strict.",
         rif=R % "JavaScript moderno"))

# ----------------------------------------------------------------------
# Domande aperte
d(aperta("c05-a-variabili", CAP, "variabili, scope e hoisting",
         "Si confrontino le dichiarazioni `var`, `let` e `const` in JavaScript rispetto a "
         "visibilità (scope), hoisting e possibilità di riassegnazione, con un esempio.",
         ["`var`: visibilità di funzione; sollevata e inizializzata a `undefined` (leggerla "
          "prima dà `undefined`); ridichiarabile.",
          "`let`: visibilità di blocco; sollevata ma non inizializzata fino alla dichiarazione "
          "(TDZ, `ReferenceError`); riassegnabile.",
          "`const`: come `let`, ma va inizializzata e non si può riassegnare (`TypeError`); "
          "l'oggetto a cui punta resta modificabile.",
          "Esempio: `var` dentro un `if` è visibile fuori, `let` no."],
         rif=R % "Variabili"))

d(aperta("c05-a-uguaglianza", CAP, "uguaglianza debole e stretta",
         "Si spieghi la differenza fra gli operatori `==` e `===` in JavaScript, con almeno "
         "tre esempi in cui danno risultati diversi.",
         ["`===` (uguaglianza stretta): vero solo se tipo e valore coincidono, senza "
          "conversioni.",
          "`==` (uguaglianza debole): se i tipi differiscono converte gli operandi (di solito "
          "in numeri) prima di confrontarli.",
          "Esempi: `\"1\" == 1` vero e `\"1\" === 1` falso; `0 == false` vero, `0 === false` "
          "falso; `null == undefined` vero, `null === undefined` falso.",
          "Le conversioni producono sorprese (es. `true == \"1\"` vero, `true == 42` falso): si "
          "usa sempre `===`."],
         rif=R % "Uguaglianza debole e uguaglianza stretta"))

d(aperta("c05-a-this", CAP, "this e costruttori",
         "Si spieghi come viene determinato il valore di `this` in JavaScript, distinguendo "
         "chiamata come metodo, chiamata semplice, chiamata con `new` e arrow function.",
         ["Come metodo (`obj.m()`): `this` è l'oggetto prima del punto.",
          "Chiamata semplice (`f()`): in modalità strict `this` è `undefined` (anche se `f` "
          "era un metodo estratto dall'oggetto).",
          "Con `new`: `this` è il nuovo oggetto in costruzione.",
          "Arrow function: non hanno un proprio `this`, usano quello dello scope in cui sono "
          "definite (utile nelle callback, inadatte come metodi)."],
         rif=R % "La parola chiave this"))

d(aperta("c05-a-closure", CAP, "closure",
         "Che cos'è una **closure** in JavaScript? Si illustri il concetto con un esempio e "
         "si indichi a che cosa serve.",
         ["Una funzione che ricorda le variabili dello scope in cui è stata creata, anche dopo "
          "che la funzione esterna è terminata.",
          "Esempio: `function contatore() { let n = 0; return () => ++n; }`: ogni contatore "
          "ha la propria `n`.",
          "Serve a mantenere uno stato privato (non accessibile dall'esterno) e a creare "
          "funzioni configurate (fabbriche di funzioni, gestori di eventi)."],
         rif=R % "Funzioni annidate restituite"))

d(aperta("c05-a-hoisting", CAP, "variabili, scope e hoisting",
         "Che cos'è l'**hoisting** in JavaScript? Si spieghi come si comportano le "
         "dichiarazioni `var`, `let`, le dichiarazioni di funzione e le espressioni di "
         "funzione.",
         ["Le dichiarazioni vengono elaborate prima di eseguire il codice dello scope, come se "
          "fossero spostate in cima.",
          "`var`: sollevata e inizializzata a `undefined`; `let`/`const`: sollevate ma nella "
          "TDZ fino alla dichiarazione (`ReferenceError`).",
          "Dichiarazioni di funzione: sollevate per intero, si possono chiamare prima della "
          "definizione.",
          "Espressioni di funzione: si comportano come la variabile che le contiene (con `var` "
          "`TypeError` *is not a function*, con `let`/`const` `ReferenceError`)."],
         rif=R % "Hoisting"))
