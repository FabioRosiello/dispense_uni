"""Capitolo 6: JavaScript avanzato (prototipi, array, destrutturazione,
iterabili, Map e Set, classi, errori, moduli)."""

from generatore import Err, L, aperta, chiusa, famiglia, uscita_js

CAP = 6
R = "cap. 6, «%s»"

DOMANDE = []
d = DOMANDE.append

# ----------------------------------------------------------------------
# Famiglia: metodi degli array
OPERAZIONI = ["push", "pop", "shift", "unshift", "indexOf", "includes", "length"]


def _esegui(a, op):
    """Esegue `op` su `a` (modificandolo, come farebbe JavaScript) e restituisce
    il codice, il valore stampato e i valori che darebbero gli errori tipici."""
    if op == "push":
        a.append(9)
        return "a.push(9)", str(len(a)), ["9", str(len(a) - 1)]
    if op == "unshift":
        a.insert(0, 0)
        return "a.unshift(0)", str(len(a)), ["0", str(len(a) - 1)]
    if op == "pop":
        primo, tolto = a[0], a.pop()
        return "a.pop()", str(tolto), [str(len(a)), str(primo)]
    if op == "shift":
        ultimo, tolto = a[-1], a.pop(0)
        return "a.shift()", str(tolto), [str(len(a)), str(ultimo)]
    if op == "indexOf":
        if 4 in a:
            i = a.index(4)
            return "a.indexOf(4)", str(i), [str(i + 1), "true"]
        return "a.indexOf(4)", "-1", ["false", "undefined"]
    if op == "includes":
        if 7 in a:
            return "a.includes(7)", "true", [str(a.index(7)), "1"]
        return "a.includes(7)", "false", ["-1", "undefined"]
    return "a.length", str(len(a)), [str(len(a) - 1), str(len(a) + 1)]


@famiglia("c06-array-metodi", CAP, "array", varianti=4)
def _array(rng):
    iniziale = rng.sample([1, 2, 3, 4, 5, 7], 4)
    passi = rng.sample(OPERAZIONI, 3)
    a = list(iniziale)
    eseguiti = [_esegui(a, op) for op in passi]
    codice = "const a = [%s];\n%s\nconsole.log(a.join(\",\"));" % (
        ", ".join(map(str, iniziale)),
        "\n".join("console.log(%s);" % c for c, _, _ in eseguiti))
    risultati = [r for _, r, _ in eseguiti]
    finale = ",".join(map(str, a))
    giusta = risultati + [finale]

    # errori tipici: push/unshift che restituiscono l'elemento, pop/shift la
    # lunghezza o l'elemento all'altro capo, indici contati da 1, length sbagliata;
    # poi l'array finale non modificato o modificato dal lato sbagliato
    singoli = []
    for i, (_, giusto, alternative) in enumerate(eseguiti):
        for v in alternative:
            if v != giusto:
                alt = list(giusta)
                alt[i] = v
                singoli.append(alt)
    b = list(iniziale)          # lo stesso codice, confondendo la testa con la coda
    for op in passi:
        if op == "push":
            b.insert(0, 9)
        elif op == "unshift":
            b.append(0)
        elif op == "pop":
            b.pop(0)
        elif op == "shift":
            b.pop()
    finali = [",".join(map(str, x)) for x in (iniziale, b)]
    for f in finali:
        if f != finale:
            singoli.append(risultati + [f])
    # due errori insieme (uno per passo), per avere sempre abbastanza opzioni
    doppi = []
    for i in range(len(passi)):
        for j in range(i + 1, len(passi)):
            alt = list(giusta)
            alt[i], alt[j] = eseguiti[i][2][0], eseguiti[j][2][0]
            if alt[i] != giusta[i] and alt[j] != giusta[j]:
                doppi.append(alt)
    rng.shuffle(singoli)
    rng.shuffle(doppi)
    sbagliate = []
    for s in singoli[:4] + doppi + singoli[4:]:
        if s != giusta and s not in sbagliate:
            sbagliate.append(s)
    return uscita_js("c06-array-metodi", CAP, "array", codice, giusta, sbagliate[:5],
                     spiegazione="`push` e `unshift` aggiungono in fondo e in testa e "
                                 "restituiscono la **nuova lunghezza**; `pop` e `shift` "
                                 "rimuovono dall'ultimo e dal primo posto e restituiscono "
                                 "l'**elemento rimosso**. `indexOf` restituisce la posizione "
                                 "(o -1), `includes` un booleano. Tutti modificano l'array, "
                                 "tranne `indexOf`, `includes` e `length`.",
                     rif=R % "Metodi per aggiungere e rimuovere")


d(_array)

# ----------------------------------------------------------------------
d(uscita_js("c06-prototipo-lettura", CAP, "prototipi ed ereditarietà",
            """
const animale = { zampe: 4, verso: "..." };
const gatto = { __proto__: animale, verso: "miao" };
gatto.zampe = 3;
console.log(gatto.zampe, animale.zampe, gatto.verso);
console.log(Object.keys(gatto).length);""",
            ["3 4 miao", "2"],
            [["3 3 miao", "2"], ["3 4 miao", "3"], ["4 4 miao", "1"], ["3 3 ...", "1"],
             ["3 4 ...", "2"]],
            spiegazione="Leggendo una proprietà che l'oggetto non ha, JavaScript la cerca lungo la "
                        "catena dei prototipi. Scrivendo, invece, la proprietà viene sempre "
                        "creata (o modificata) **sull'oggetto stesso**: `gatto.zampe = 3` non "
                        "tocca `animale`. Le proprietà proprie di `gatto` sono `verso` e "
                        "`zampe`.",
            rif=R % "I prototipi si usano solo in lettura"))

d(uscita_js("c06-prototipo-metodi", CAP, "prototipi ed ereditarietà",
            """
function Pet(nome) {
  this.nome = nome;
  this.corri = function () { return "corro"; };
}
Pet.prototype.saluta = function () { return "ciao " + this.nome; };
const a = new Pet("Fido");
const b = new Pet("Rex");
console.log(a.saluta === b.saluta, a.corri === b.corri);
console.log(b.saluta());""",
            ["true false", "ciao Rex"],
            [["false false", "ciao Rex"], ["true true", "ciao Rex"], ["false true", "ciao Rex"],
             ["true false", "ciao Fido"], ["true false", "ciao undefined"]],
            spiegazione="I metodi definiti su `Pet.prototype` esistono una sola volta e sono "
                        "condivisi da tutte le istanze tramite la catena dei prototipi. Una "
                        "funzione assegnata a `this` nel costruttore viene invece ricreata per "
                        "ogni oggetto. `this` dentro `saluta` è l'oggetto su cui la si chiama.",
            rif=R % "Due modi per aggiungere metodi"))

d(uscita_js("c06-sparsi", CAP, "array",
            """
const a = [10, 20, 30];
a[5] = 60;
console.log(a.length, a[4]);
a.length = 2;
console.log(a.join("-"));""",
            ["6 undefined", "10-20"],
            [["4 undefined", "10-20"], ["6 null", "10-20"], ["6 undefined", "10-20-30--60"],
             Err("RangeError"), ["4 60", "10-20"]],
            spiegazione="Assegnare a un indice oltre la fine allunga l'array: `length` diventa "
                        "l'ultimo indice più uno e le posizioni intermedie restano vuote "
                        "(leggerle dà `undefined`). Ridurre `length` tronca l'array.",
            rif=R % "La proprietà length"))

d(uscita_js("c06-slice-splice", CAP, "array",
            """
const a = [1, 2, 3, 4, 5];
const b = a.slice(1, 3);
const c = a.splice(1, 2);
console.log(b.join(","), c.join(","), a.join(","));""",
            ["2,3 2,3 1,4,5"],
            [["2,3 2,3 1,2,3,4,5"], ["2,3,4 2,3 1,4,5"], ["2,3 2,3,4 1,5"], ["2 2,3 1,4,5"],
             ["2,3 3,4 1,2,5"]],
            spiegazione="`slice(inizio, fine)` restituisce una copia della porzione (fine esclusa) "
                        "senza modificare l'array; `splice(inizio, quanti)` **rimuove** `quanti` "
                        "elementi dall'array originale e li restituisce.",
            rif=R % "Metodi per aggiungere e rimuovere"))

d(uscita_js("c06-map-filter", CAP, "array",
            """
const voti = [18, 24, 30, 27, 21];
const r = voti
  .filter(v => v >= 24)
  .map(v => v + 1)
  .reduce((somma, v) => somma + v, 0);
console.log(r, voti.length);""",
            ["84 5"],
            [["81 5"], ["84 3"], ["125 5"], ["81 3"], ["[ 25, 31, 28 ] 5"]],
            spiegazione="`filter` tiene 24, 30 e 27; `map` li trasforma in 25, 31 e 28; `reduce` "
                        "li somma a partire da 0: 84. Questi metodi restituiscono nuovi valori "
                        "senza modificare l'array originale, che resta di 5 elementi.",
            rif=R % "Iterazione"))

d(uscita_js("c06-for-in", CAP, "array",
            """
const a = ["x", "y"];
for (const i in a) console.log(typeof i, i);
for (const v of a) console.log(v);""",
            ["string 0", "string 1", "x", "y"],
            [["number 0", "number 1", "x", "y"], ["string x", "string y", "0", "1"],
             ["number 0", "number 1", "0", "1"], ["string 0", "string 1", "0", "1"]],
            spiegazione="`for...in` scorre i **nomi** delle proprietà enumerabili, che sono "
                        "stringhe anche per gli indici di un array (e includerebbe eventuali "
                        "proprietà aggiunte): per gli array non va usato. `for...of` scorre i "
                        "**valori** di un oggetto iterabile.",
            rif=R % "Iterazione"))

d(uscita_js("c06-destrutturazione", CAP, "destrutturazione e spread",
            """
const [a, , b = 5, ...resto] = [1, 2, undefined, 4, 6];
const { nome: n, anni = 18 } = { nome: "Ada", corso: "TW" };
console.log(a, b, resto.length, n, anni);""",
            ["1 5 2 Ada 18"],
            [["1 2 2 Ada 18"], ["1 5 3 Ada 18"], ["1 undefined 2 Ada 18"],
             ["1 5 2 undefined 18"], Err("ReferenceError")],
            spiegazione="Nella destrutturazione di array si può saltare una posizione con una "
                        "virgola, dare un valore predefinito (usato se l'elemento è "
                        "`undefined`) e raccogliere il resto con `...`. In quella di oggetti "
                        "`nome: n` copia la proprietà `nome` nella variabile `n`, e `anni = 18` "
                        "vale 18 perché la proprietà manca.",
            rif=R % "Assegnamenti destrutturanti"))

d(uscita_js("c06-spread", CAP, "destrutturazione e spread",
            """
function conta(primo, ...altri) {
  return altri.length;
}
const v = [1, 2];
console.log(conta(...v, 3, ...v));
const o = { a: 1, b: 2 };
const p = { ...o, b: 3, c: 4 };
console.log(Object.values(p).join(","));""",
            ["4", "1,3,4"],
            [["5", "1,3,4"], ["4", "1,2,3,4"], ["2", "1,3,4"], ["4", "1,2,4"], ["3", "1,3,4"]],
            spiegazione="Nella chiamata lo spread espande gli array: gli argomenti sono 1, 2, 3, "
                        "1, 2; il parametro *rest* `...altri` raccoglie tutti quelli dopo il "
                        "primo (4). Negli oggetti lo spread copia le proprietà, e quelle scritte "
                        "dopo sovrascrivono quelle con lo stesso nome.",
            rif=R % "Assegnamenti destrutturanti"))

d(uscita_js("c06-map-chiavi", CAP, "Map e Set",
            """
const o = {};
o[1] = "numero";
o["1"] = "stringa";
const m = new Map();
m.set(1, "numero");
m.set("1", "stringa");
console.log(Object.keys(o).length, m.size, m.get(1));""",
            ["1 2 numero"],
            [["2 2 numero"], ["1 1 stringa"], ["1 2 stringa"], ["2 1 numero"],
             ["1 2 undefined"]],
            spiegazione="Le chiavi delle proprietà di un oggetto sono stringhe: `o[1]` e `o[\"1\"]` "
                        "sono la stessa proprietà. Una `Map` accetta chiavi di qualunque tipo "
                        "e le distingue: il numero 1 e la stringa `\"1\"` sono due chiavi "
                        "diverse.",
            rif=R % "Mappe"))

d(uscita_js("c06-set", CAP, "Map e Set",
            """
const s = new Set([3, 1, 3, "3", 1]);
s.add(1);
console.log(s.size, [...s].join(" "));""",
            ["3 3 1 3"],
            [["2 1 3"], ["5 3 1 3 3 1"], ["4 3 1 3 1"], ["3 1 3 3"], ["2 3 1"]],
            spiegazione="Un `Set` contiene valori senza ripetizioni (il numero 3 e la stringa "
                        "`\"3\"` sono diversi) e ricorda l'ordine di inserimento; aggiungere un "
                        "valore già presente non ha effetto.",
            rif=R % "Insiemi"))

d(uscita_js("c06-map-iterazione", CAP, "Map e Set",
            """
const voti = new Map([["web", 30], ["reti", 27]]);
voti.set("web", 28);
for (const [esame, voto] of voti) {
  console.log(esame + ": " + voto);
}""",
            ["web: 28", "reti: 27"],
            [["web: 30", "reti: 27", "web: 28"], ["reti: 27", "web: 28"], ["web: 30", "reti: 27"],
             ["0: web,28", "1: reti,27"]],
            spiegazione="Iterando una `Map` con `for...of` si ottengono coppie `[chiave, valore]`, "
                        "che si possono destrutturare. Le chiavi restano nell'ordine di "
                        "inserimento; `set` su una chiave esistente ne aggiorna il valore senza "
                        "spostarla.",
            rif=R % "Iterare su una mappa"))

d(uscita_js("c06-classe-hoisting", CAP, "classi",
            """
console.log(typeof Pet);
const p = new Pet("Fido");
class Pet {
  constructor(nome) { this.nome = nome; }
}""",
            Err("ReferenceError"),
            [["function"], ["class"], Err("ReferenceError", ["function"]),
             Err("TypeError", ["undefined"]), ["undefined"]],
            spiegazione="Le dichiarazioni di classe vengono sollevate come `let`: fino alla "
                        "dichiarazione la classe è nella *temporal dead zone*. Già `typeof Pet` "
                        "solleva un `ReferenceError` (lo stesso `typeof` che, per un nome mai "
                        "dichiarato, restituirebbe `\"undefined\"`).",
            rif=R % "Non solo zucchero sintattico"))

d(uscita_js("c06-classe", CAP, "classi",
            """
class Pet {
  constructor(nome) { this.nome = nome; }
  verso() { return "..."; }
  presentati() { return this.nome + " fa " + this.verso(); }
}
class Cane extends Pet {
  verso() { return "bau"; }
}
const c = new Cane("Fido");
console.log(typeof Pet, c.presentati(), c instanceof Pet);""",
            ["function Fido fa bau true"],
            [["class Fido fa bau true"], ["function Fido fa ... true"],
             ["function Fido fa bau false"], ["object Fido fa bau true"],
             ["class Fido fa ... false"]],
            spiegazione="Una classe è, sotto sotto, una funzione costruttrice (`typeof` dà "
                        "`function`). `Cane` eredita costruttore e `presentati` da `Pet` e "
                        "ridefinisce `verso`: `this.verso()` chiama il metodo dell'oggetto "
                        "reale, quindi quello di `Cane`. Un `Cane` è anche un `Pet`.",
            rif=R % "Ereditarietà fra classi"))

d(uscita_js("c06-classe-new", CAP, "classi",
            """
class Punto {
  constructor(x) { this.x = x; }
  static origine() { return new Punto(0); }
}
console.log(Punto.origine().x);
const p = Punto(5);
console.log(p.x);""",
            Err("TypeError", ["0"]),
            [["0", "5"], ["0", "undefined"], Err("TypeError"), Err("ReferenceError", ["0"])],
            spiegazione="I metodi `static` si chiamano sulla classe, non sulle istanze. A "
                        "differenza delle vecchie funzioni costruttrici, una classe non si può "
                        "chiamare senza `new`: `Punto(5)` solleva un `TypeError` (*Class "
                        "constructor Punto cannot be invoked without 'new'*).",
            rif=R % "Non solo zucchero sintattico"))

d(uscita_js("c06-try-finally", CAP, "gestione degli errori",
            """
function f() {
  try {
    console.log("A");
    null.x;
    console.log("B");
  } catch (e) {
    console.log(e instanceof TypeError, e instanceof Error);
    return "C";
  } finally {
    console.log("D");
  }
}
console.log(f());""",
            ["A", "true true", "D", "C"],
            [["A", "true true", "C", "D"], ["A", "B", "D", "C"], ["A", "true false", "D", "C"],
             ["A", "true true", "C"], ["A", "false true", "D", "C"]],
            spiegazione="Leggere una proprietà di `null` solleva un `TypeError`, quindi `B` non "
                        "viene stampata. Ogni errore predefinito eredita da `Error`. Il "
                        "`return` nel `catch` viene eseguito, ma prima che la funzione "
                        "restituisca davvero il valore viene eseguito il blocco `finally`.",
            rif=R % "try / catch / finally"))

d(uscita_js("c06-throw", CAP, "gestione degli errori",
            """
class VotoNonValido extends Error {}
function registra(v) {
  if (v < 18 || v > 30) throw new VotoNonValido("voto " + v);
  return "ok " + v;
}
for (const v of [28, 31, 18]) {
  try { console.log(registra(v)); }
  catch (e) { console.log(e.name, e.message, e instanceof VotoNonValido); }
}""",
            ["ok 28", "Error voto 31 true", "ok 18"],
            [["ok 28", "VotoNonValido voto 31 true", "ok 18"], ["ok 28", "Error voto 31 true"],
             ["ok 28", "Error voto 31 false", "ok 18"], ["ok 28", "voto 31", "ok 18"],
             Err("VotoNonValido", ["ok 28"])],
            spiegazione="Si possono sollevare errori con `throw` e definire nuovi tipi di errore "
                        "estendendo `Error`. Un errore catturato non interrompe il ciclo. "
                        "Attenzione: `name` resta `\"Error\"` finché la sottoclasse non lo "
                        "imposta (per esempio con `this.name = \"VotoNonValido\"` nel "
                        "costruttore), mentre `instanceof` riconosce comunque la classe.",
            rif=R % "Sollevare errori"))

d(chiusa("c06-moduli", CAP, "moduli",
         "Quali delle seguenti affermazioni sui moduli JavaScript (``<script type=\"module\">``) "
         "sono **vere**?",
         ["Ogni modulo ha un proprio scope: le variabili non diventano globali.",
          "Il codice di un modulo è sempre in modalità strict.",
          "Gli script di tipo modulo si comportano come `defer` per impostazione predefinita.",
          "Aprendo la pagina con un doppio clic (URL `file://`) i moduli non vengono caricati."],
         ["Un modulo può importare solo ciò che è stato esportato con `export default`.",
          "Le variabili dichiarate in un modulo sono visibili in tutti gli altri script.",
          "Per usare i moduli serve Node.js anche nel browser.",
          "Un modulo viene eseguito di nuovo ogni volta che viene importato.",
          "L'istruzione `import` può comparire solo dentro una funzione."],
         multi=True,
         spiegazione="I moduli hanno uno scope proprio e condividono solo ciò che esportano; "
                     "sono in strict mode e differiti. Il browser li carica come risorse "
                     "soggette alle regole di sicurezza (CORS), quindi serve un server, anche "
                     "locale. Un modulo viene valutato una sola volta, anche se importato più "
                     "volte.",
         rif=R % "Cose da sapere sui moduli"))

d(chiusa("c06-export", CAP, "moduli",
         "Il modulo `cerchio.js` contiene `export default class Cerchio { ... }` ed `export "
         "const PI = 3.14;`. Quale istruzione importa correttamente entrambi?",
         "`import Cerchio, { PI } from './cerchio.js';`",
         ["`import { Cerchio, PI } from './cerchio.js';`",
          "`import Cerchio, PI from './cerchio.js';`",
          "`import default Cerchio, PI from './cerchio.js';`",
          "`import * from './cerchio.js';`",
          "`require('./cerchio.js').Cerchio, PI;`"],
         spiegazione="L'export predefinito (al più uno per modulo) si importa senza graffe e con "
                     "un nome a scelta; gli export con nome si importano fra graffe con il loro "
                     "nome (rinominabile con `as`).",
         rif=R % "Altre forme di export e import"))

d(chiusa("c06-prototipo-def", CAP, "prototipi ed ereditarietà",
         "Che cosa succede quando si accede a una proprietà che un oggetto non possiede?",
         "JavaScript la cerca nel prototipo, poi nel prototipo del prototipo, e così via.",
         ["Viene sollevato un `ReferenceError`.",
          "Viene creata automaticamente con valore `undefined`.",
          "JavaScript la cerca fra le variabili globali.",
          "Viene sollevato un `TypeError`, perché l'oggetto non è estensibile.",
          "JavaScript la cerca negli oggetti creati con lo stesso costruttore."],
         spiegazione="Ogni oggetto ha un prototipo (accessibile con `Object.getPrototypeOf` o "
                     "`__proto__`). La ricerca risale la catena dei prototipi fino a "
                     "`Object.prototype`; se la proprietà non si trova si ottiene `undefined`.",
         rif=R % "Prototipi ed ereditarietà"))

# ----------------------------------------------------------------------
# Domande aperte
d(aperta("c06-a-prototipi", CAP, "prototipi ed ereditarietà",
         "Si spieghi il meccanismo dei **prototipi** in JavaScript e il suo rapporto con le "
         "funzioni costruttrici e con le classi.",
         ["Ogni oggetto ha un prototipo; le proprietà mancanti si cercano lungo la catena dei "
          "prototipi (in lettura; le scritture avvengono sull'oggetto stesso).",
          "Un oggetto creato con `new F()` ha come prototipo `F.prototype`: i metodi definiti "
          "lì sono condivisi da tutte le istanze.",
          "Le classi sono costruite sullo stesso meccanismo: i metodi stanno nel prototipo "
          "della classe, `extends` collega i prototipi.",
          "Le classi aggiungono vincoli: non si possono chiamare senza `new`, sono in strict "
          "mode, non vengono inizializzate prima della dichiarazione."],
         rif=R % "Prototipi ed ereditarietà"))

d(aperta("c06-a-map", CAP, "Map e Set",
         "Si spieghino le differenze fra un oggetto usato come dizionario e una `Map`, e si "
         "descriva a che cosa serve un `Set`, con un esempio.",
         ["In un oggetto le chiavi sono stringhe (o simboli); in una `Map` qualunque valore, "
          "anche oggetti, e `1` e `\"1\"` restano distinte.",
          "La `Map` ha `size`, metodi dedicati (`set`, `get`, `has`, `delete`), conserva "
          "l'ordine di inserimento ed è iterabile con `for...of` (coppie chiave-valore).",
          "Un oggetto eredita proprietà dal prototipo, che possono confondersi con le chiavi.",
          "Un `Set` è una collezione di valori senza duplicati: es. `new Set(lista)` per "
          "eliminare le ripetizioni, `has` per l'appartenenza."],
         rif="cap. 6, «Mappe» e «Insiemi»"))

d(aperta("c06-a-errori", CAP, "gestione degli errori",
         "Si descriva il meccanismo di gestione degli errori in JavaScript (`try`, `catch`, "
         "`finally`, `throw`), indicando come si possono definire e riconoscere errori "
         "specifici.",
         ["`try` racchiude il codice che può fallire; se viene sollevata un'eccezione "
          "l'esecuzione passa al `catch`, che riceve l'oggetto errore.",
          "`finally` viene eseguito sempre, con o senza errore (anche dopo un `return`).",
          "`throw` solleva un errore: di solito un oggetto `Error` o di una sottoclasse "
          "(`TypeError`, `ReferenceError`, o classi proprie con `extends Error`).",
          "Nel `catch` si distingue il tipo con `instanceof` e si rilancia ciò che non si sa "
          "gestire; un errore non gestito interrompe lo script."],
         rif=R % "Gestione degli errori"))

d(aperta("c06-a-moduli", CAP, "moduli",
         "Perché sono stati introdotti i **moduli** in JavaScript? Si descrivano le forme di "
         "`export` e `import` e il comportamento degli script di tipo modulo nel browser.",
         ["Senza moduli tutti gli script condividono lo scope globale: conflitti di nomi e "
          "dipendenze implicite fra file.",
          "Un modulo ha un proprio scope ed esporta esplicitamente ciò che vuole condividere: "
          "export con nome (`export const x`) ed export predefinito (`export default`).",
          "`import { x, y as z } from './m.js'` per gli export con nome, `import M from "
          "'./m.js'` per quello predefinito.",
          "Nel browser: `<script type=\"module\">`, strict mode, esecuzione differita, una "
          "sola valutazione per modulo; servono un server (no `file://`)."],
         rif=R % "Moduli"))
