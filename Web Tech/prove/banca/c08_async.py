"""Capitolo 8: asincronismo e richieste di rete (cookie e Web Storage, event
loop e callback, Promise, async e await, fetch)."""

from generatore import (FONTE_2024, Err, aperta, chiusa, combina_errori, famiglia,
                        uscita_browser, uscita_js)

CAP = 8
R = "cap. 8, «%s»"

DOMANDE = []
d = DOMANDE.append


def _unici(esiti):
    visti = []
    for e in esiti:
        if e not in visti:
            visti.append(e)
    return visti


# ----------------------------------------------------------------------
# Famiglia: l'ordine delle callback di setTimeout
def _ritardi(rng, forme):
    """Ritardi per i timer: tempi di scadenza tutti diversi, tranne
    eventuali timer di primo livello con lo stesso ritardo."""
    while True:
        ritardi = []
        for forma in forme:
            if forma == "timer":
                ritardi.append((rng.choice([0, 100, 200, 300]),))
            elif forma == "annidato":
                ritardi.append((rng.choice([0, 100, 200]), rng.choice([0, 100, 200])))
            else:
                ritardi.append(None)
        primo_livello = [r[0] for r in ritardi if r]
        interni = [r[0] + r[1] for r in ritardi if r and len(r) == 2]
        if all(t not in primo_livello for t in interni):
            return ritardi


@famiglia("c08-timer", CAP, "event loop e callback", varianti=4)
def _timer(rng):
    forme = ["log", "log", "timer", "timer", "annidato"]
    rng.shuffle(forme)
    nomi = iter("ABCDEFGH")
    righe, sincrone, scadenze, testuale = [], [], [], []
    # scadenze: (tempo, ordine di avvio, nome, è un timer interno, il suo ritardo)
    for seq, (forma, ritardo) in enumerate(zip(forme, _ritardi(rng, forme))):
        if forma == "log":
            n = next(nomi)
            righe.append('console.log("%s");' % n)
            sincrone.append(n)
            testuale.append(n)
        elif forma == "timer":
            n = next(nomi)
            righe.append('setTimeout(() => console.log("%s"), %d);' % (n, ritardo[0]))
            scadenze.append((ritardo[0], seq, n, False, ritardo[0]))
            testuale.append(n)
        else:
            esterno, interno = next(nomi), next(nomi)
            righe += ["setTimeout(() => {",
                      '  console.log("%s");' % esterno,
                      '  setTimeout(() => console.log("%s"), %d);' % (interno, ritardo[1]),
                      "}, %d);" % ritardo[0]]
            scadenze.append((ritardo[0], seq, esterno, False, ritardo[0]))
            # il timer interno viene avviato dopo tutti quelli del primo livello
            scadenze.append((ritardo[0] + ritardo[1], 100, interno, True, ritardo[1]))
            testuale += [esterno, interno]
    reale = sincrone + [s[2] for s in sorted(scadenze)]
    in_codice = [n for n in testuale if n not in sincrone]
    # ragionamenti sbagliati
    zero_subito = []                    # i timer da 0 ms eseguiti come codice sincrono
    for n in testuale:
        s = next((s for s in scadenze if s[2] == n), None)
        if s is None or s[4] == 0 and not s[3]:
            zero_subito.append(n)
    zero_subito += [s[2] for s in sorted(scadenze) if s[2] not in zero_subito]
    interni_in_coda = sincrone + [s[2] for s in sorted(scadenze, key=lambda s: (s[3], s[0], s[1]))]
    relativi = sincrone + [s[2] for s in sorted(scadenze, key=lambda s: (s[4], s[1], s[3]))]
    interno = next(s for s in scadenze if s[3])
    esterno = next(s for s in scadenze if not s[3] and s[1] == next(
        i for i, f in enumerate(forme) if f == "annidato"))
    senza_interno = [n for n in reale if n != interno[2]]
    interno_subito = []                 # il timer interno eseguito subito dopo l'esterno
    for n in senza_interno:
        interno_subito.append(n)
        if n == esterno[2]:
            interno_subito.append(interno[2])
    vicini = []                         # due callback consecutive scambiate
    for i in range(len(sincrone), len(reale) - 1):
        scambio = list(reale)
        scambio[i], scambio[i + 1] = scambio[i + 1], scambio[i]
        vicini.append(scambio)
    rng.shuffle(vicini)
    esiti = _unici([testuale, sincrone + in_codice, zero_subito, interni_in_coda, relativi,
                    interno_subito, senza_interno] + vicini)
    rng.shuffle(esiti)
    return uscita_js(
        "c08-timer", CAP, "event loop e callback", "\n".join(righe), reale,
        combina_errori(reale, [], rng, esiti=esiti),
        spiegazione="Il codice sincrono viene eseguito tutto per primo, nell'ordine. `setTimeout` "
                    "ritorna subito: allo scadere del timer il browser mette la callback nella "
                    "coda, e l'event loop la esegue quando lo stack è vuoto, anche con un "
                    "ritardo di 0 ms. Le callback partono quindi in ordine di scadenza (a parità "
                    "di ritardo, nell'ordine in cui i timer sono stati avviati); un timer avviato "
                    "dentro una callback comincia a contare solo quando quella callback viene "
                    "eseguita.",
        rif=R % "Sincronismo e asincronismo")


d(_timer)


# ----------------------------------------------------------------------
# Famiglia: una catena di Promise
OPERAZIONI = ["* 2", "+ 1", "* 3", "- 1"]


def _applica(v, op):
    if v is None or v != v:                     # undefined o NaN
        return float("nan")
    return {"*": v * int(op[2:]), "+": v + int(op[2:]), "-": v - int(op[2:])}[op[0]]


def _js(v):
    if v is None:
        return "undefined"
    if v != v:
        return "NaN"
    return str(v)


def _simula(inizio, passi, stesso_valore=False, finally_azzera=False, catch_ferma=False,
            valore_dopo=False):
    """Le righe stampate dalla catena (dopo il codice sincrono) e, per ognuna,
    gli sbagli tipici su quella riga."""
    stato, valore = inizio
    originale = valore
    righe, alternative = [], []
    for passo in passi:
        tipo = passo[0]
        if tipo == "then" and stato == "ok":
            nuovo = _applica(valore, passo[1])
            righe.append(_js(nuovo if valore_dopo else valore))
            alternative.append([_js(nuovo)])
            if not stesso_valore:
                valore = nuovo
            else:
                valore = originale
        elif tipo == "throw" and stato == "ok":
            righe.append(_js(valore))
            alternative.append([])
            stato, valore = "ko", "ko"
        elif tipo == "catch" and stato == "ko":
            righe.append(valore)
            alternative.append(["Error: " + valore, "undefined"])
            stato, valore = "ok", passo[1]
            originale = valore      # la catena riparte dal valore del catch
            if catch_ferma:
                break
        elif tipo == "finally":
            righe.append("finally")
            alternative.append([])
            if finally_azzera and stato == "ok":
                valore = None
        elif tipo == "fine" and stato == "ok":
            righe.append(_js(valore))
            alternative.append([])
    return righe, alternative


@famiglia("c08-catena", CAP, "Promise", varianti=4)
def _catena(rng):
    v0 = rng.choice([1, 2, 3, 5])
    rifiutata = rng.random() < 0.25
    con_timer = rng.random() < 0.6
    inizio = ("ko", "no") if rifiutata else ("ok", v0)
    esito = 'reject(new Error("no"))' if rifiutata else "resolve(%d)" % v0
    # una catena con soli catch e finally stampa il valore e basta: in quel caso
    # gli errori tipici coincidono con la risposta giusta e la catena si rifà
    for _ in range(100):
        passi = []
        for _ in range(rng.choice([3, 4])):
            tipo = rng.choice(["then", "then", "throw", "finally", "catch"])
            if tipo == "then":
                passi.append(("then", rng.choice(OPERAZIONI)))
            elif tipo == "catch":
                passi.append(("catch", rng.choice([0, 10, 100])))
            else:
                passi.append((tipo,))
        passi += [("catch", rng.choice([0, 10, 100])), ("fine",)]
        righe, alternative = _simula(inizio, passi)
        giusta = ["sync"] + righe
        esiti = [righe + ["sync"]]
        for opzioni in ({"stesso_valore": True}, {"finally_azzera": True},
                        {"catch_ferma": True}, {"valore_dopo": True}):
            esiti.append(["sync"] + _simula(inizio, passi, **opzioni)[0])
        esiti = _unici(esiti)
        rng.shuffle(esiti)
        sbagliate = combina_errori(giusta, [[]] + alternative, rng, esiti=esiti)
        if len(sbagliate) >= 3:
            break

    codice = ["const p = new Promise((resolve, reject) => {",
              ("  setTimeout(() => %s, 100);" % esito) if con_timer else "  %s;" % esito,
              "});"]
    anelli = []
    for passo in passi:
        if passo[0] == "then":
            anelli.append(".then((v) => { console.log(v); return v %s; })" % passo[1])
        elif passo[0] == "throw":
            anelli.append('.then((v) => { console.log(v); throw new Error("ko"); })')
        elif passo[0] == "catch":
            anelli.append(".catch((e) => { console.log(e.message); return %d; })" % passo[1])
        elif passo[0] == "finally":
            anelli.append('.finally(() => console.log("finally"))')
        else:
            anelli.append(".then((v) => console.log(v));")
    codice.append("p" + anelli[0])
    codice += ["  " + a for a in anelli[1:]]
    codice.append('console.log("sync");')

    return uscita_js(
        "c08-catena", CAP, "Promise", "\n".join(codice), giusta, sbagliate,
        spiegazione="I gestori registrati con `then`, `catch` e `finally` vengono eseguiti solo "
                    "dopo il codice sincrono, anche se la Promise è già risolta. Ogni anello "
                    "restituisce una nuova Promise: un `then` riceve il valore restituito "
                    "dall'anello precedente; un errore sollevato (o un rifiuto) salta i `then` "
                    "fino al primo `catch`, che con il suo valore di ritorno fa ripartire la "
                    "catena. `finally` esegue la sua callback in ogni caso e lascia passare "
                    "invariato il valore (o l'errore).",
        rif="cap. 8, «then, catch e finally» e «Concatenare le Promise»")


d(_catena)


# ----------------------------------------------------------------------
# Famiglia: i metodi statici di Promise
@famiglia("c08-statici", CAP, "Promise", varianti=4)
def _statici(rng):
    metodo = rng.choice(["all", "allSettled", "race", "any"])
    while True:
        tempi = rng.sample([100, 200, 300, 400], 3)
        riuscite = [rng.random() < 0.65 for _ in range(3)]
        if metodo != "any" or any(riuscite):
            break
    valori = ["a", "b", "c"]
    ingressi = list(zip(tempi, valori, riuscite))
    per_tempo = sorted(ingressi)

    def risultato(m, ordine_arrivo=False):
        lista = per_tempo if ordine_arrivo else ingressi
        if m == "all":
            rifiuti = [x for x in per_tempo if not x[2]]
            if rifiuti:
                return "ko " + rifiuti[0][1]
            return "ok " + ",".join(x[1] for x in lista)
        if m == "allSettled":
            return "ok " + ",".join("fulfilled" if x[2] else "rejected" for x in lista)
        if m == "race":
            primo = per_tempo[0]
            return ("ok " if primo[2] else "ko ") + primo[1]
        riuscite_ = [x for x in per_tempo if x[2]]
        return "ok " + riuscite_[0][1] if riuscite_ else "ko AggregateError"

    if metodo == "allSettled":
        dopo = '  .then((r) => console.log("ok", r.map((x) => x.status).join(",")))'
    else:
        dopo = '  .then((r) => console.log("ok", String(r)))'
    codice = "\n".join([
        "const attesa = (ms, valore, ok) => new Promise((resolve, reject) => {",
        "  setTimeout(() => ok ? resolve(valore) : reject(new Error(valore)), ms);",
        "});",
        "Promise.%s([" % metodo] +
        ['  attesa(%d, "%s", %s),' % (t, v, "true" if ok else "false") for t, v, ok in ingressi] +
        ["])", dopo, '  .catch((e) => console.log("ko", e.message));'])
    giusta = [risultato(metodo)]
    if metodo == "allSettled":
        stati = ["fulfilled" if ok else "rejected" for _, _, ok in ingressi]
        altri = [risultato(metodo, ordine_arrivo=True), "ok " + ",".join(["fulfilled"] * 3)]
        for i in range(3):          # un esito sbagliato
            diverso = list(stati)
            diverso[i] = "rejected" if stati[i] == "fulfilled" else "fulfilled"
            altri.append("ok " + ",".join(diverso))
        altri.append("ok " + ",".join("resolved" if s == "fulfilled" else s for s in stati))
        if not all(riuscite):       # come se si comportasse come all
            altri.append(risultato("all"))
    else:
        altri = [risultato(m) for m in ("all", "race", "any") if m != metodo]
        altri += [risultato(metodo, ordine_arrivo=True), risultato("all", ordine_arrivo=True)]
        # chi confonde gli esiti o il primo arrivato con il primo dell'elenco
        altri += ["ok " + ",".join(valori), "ok " + valori[0], "ko " + valori[0],
                  "ok " + per_tempo[-1][1]]
    esiti = _unici([[a] for a in altri if a != giusta[0] and "AggregateError" not in a])
    rng.shuffle(esiti)
    return uscita_js(
        "c08-statici", CAP, "Promise", codice, giusta, esiti[:5],
        spiegazione="`Promise.all` si risolve con i risultati di tutte, nell'ordine dell'array "
                    "(non in quello di completamento), e rifiuta appena una rifiuta. "
                    "`Promise.allSettled` attende che tutte si sistemino e descrive l'esito di "
                    "ciascuna (`fulfilled` o `rejected`). `Promise.race` assume l'esito della "
                    "prima che si sistema, in un senso o nell'altro; `Promise.any` il valore "
                    "della prima che si risolve, ignorando i rifiuti.",
        rif=R % "I metodi statici della classe Promise")


d(_statici)


# ----------------------------------------------------------------------
# Dalle prove del corso
d(uscita_js("c08-prova-promise", CAP, "Promise",
            """
let prom = new Promise(function(resolve, reject) { setTimeout(() => { resolve("A"); }, 1000); });
prom.finally(value => console.log("B")).then(val => console.log(val))
     .catch(value => console.log("X"));
console.log("Done");""",
            ["Done", "B", "A"],
            [["A", "B", "Done"], ["Done", "A", "B"], ["X", "B", "Done"], ["Done", "X"],
             ["B", "A", "Done"]],
            fisse=True,
            spiegazione="Il codice sincrono termina per primo: `Done`. Dopo un secondo la Promise "
                        "si risolve con `\"A\"`: `finally` esegue la sua callback (che non riceve "
                        "argomenti: `value` è `undefined`) e lascia passare il valore, che arriva "
                        "al `then` successivo. Il `catch` non viene eseguito, perché nessun passo "
                        "fallisce.",
            rif=R % "then, catch e finally", fonte=FONTE_2024))

# ----------------------------------------------------------------------
d(uscita_js("c08-executor", CAP, "Promise",
            """
console.log("1");
const p = new Promise((resolve) => {
  console.log("2");
  resolve("3");
  console.log("4");
});
p.then((v) => console.log(v));
console.log("5");""",
            ["1", "2", "4", "5", "3"],
            [["1", "2", "3", "4", "5"], ["1", "5", "2", "4", "3"], ["1", "2", "5", "3"],
             ["1", "2", "4", "3", "5"], ["1", "5", "2", "3", "4"]],
            spiegazione="L'executor viene invocato **subito**, dal costruttore: `2` e `4` sono "
                        "stampati durante la creazione della Promise. `resolve` sistema la Promise "
                        "ma non interrompe l'executor. Il gestore registrato con `then` viene "
                        "eseguito solo dopo la fine del codice sincrono, anche se la Promise è già "
                        "risolta.",
            rif=R % "Creare una Promise"))

d(uscita_js("c08-settled", CAP, "Promise",
            """
const p = new Promise((resolve, reject) => {
  resolve("primo");
  reject(new Error("errore"));
  resolve("secondo");
});
p.then((v) => console.log("ok", v))
  .catch((e) => console.log("ko", e.message));""",
            ["ok primo"],
            [["ok secondo"], ["ko errore"], ["ok primo", "ko errore"], Err("Error"),
             ["ok primo", "ok secondo"]],
            spiegazione="Una Promise che ha lasciato lo stato `pending` è *settled*, e da quel "
                        "momento il suo stato non cambia più: le chiamate successive a `reject` e "
                        "`resolve` vengono ignorate.",
            rif=R % "Creare una Promise"))

d(uscita_js("c08-resolve-metodo", CAP, "Promise",
            """
const p = new Promise((resolve) => resolve(1));
p.resolve(42);
p.then((v) => console.log("valore", v));
console.log("fine");""",
            Err("TypeError"),
            [["valore 42", "fine"], ["fine", "valore 42"], ["fine", "valore 1"],
             Err("TypeError", ["fine"]), ["valore 1", "fine"]],
            spiegazione="Un oggetto Promise **non ha** un metodo `resolve`: `p.resolve(42)` solleva "
                        "un `TypeError` (*p.resolve is not a function*) e lo script si ferma lì. "
                        "Il `resolve` che riceve l'executor è una funzione legata a quella Promise; "
                        "`Promise.resolve(valore)` è un metodo statico che crea una nuova Promise "
                        "già risolta.",
            rif=R % "Anatomia di una Promise: chi fa cosa"))

d(uscita_js("c08-stessa-promise", CAP, "Promise",
            """
const p = Promise.resolve(1);
p.then((r) => { console.log(r); return r * 2; });
p.then((r) => { console.log(r); return r * 2; });
p.then((r) => { console.log(r); return r * 2; });""",
            ["1", "1", "1"],
            [["1", "2", "4"], ["1"], ["2", "2", "2"], ["1", "2", "3"], ["2", "4", "8"]],
            spiegazione="I tre gestori sono registrati sulla **stessa** Promise: sono "
                        "indipendenti e ricevono tutti il suo valore, 1. Il valore restituito da "
                        "un gestore alimenta solo la Promise restituita da quel `then`, che qui "
                        "nessuno usa. Per passare il risultato da un passo al successivo bisogna "
                        "concatenare: `p.then(...).then(...)`.",
            rif=R % "Concatenare le Promise"))

d(uscita_js("c08-any-aggregate", CAP, "Promise",
            """
Promise.any([
  Promise.reject(new Error("a")),
  new Promise((res, rej) => setTimeout(() => rej(new Error("b")), 100)),
]).then((v) => console.log("ok", v))
  .catch((e) => console.log(e.name, e.errors.length));""",
            ["AggregateError 2"],
            [["Error 1"], ["Error 2"], ["ok undefined"], ["AggregateError 1"], ["ok a"]],
            spiegazione="`Promise.any` si risolve con la prima Promise **risolta**, ignorando i "
                        "rifiuti. Se tutte rifiutano, rifiuta con un `AggregateError`, che "
                        "raccoglie nella proprietà `errors` tutti gli errori (qui due).",
            rif=R % "I metodi statici della classe Promise"))

d(uscita_js("c08-callback", CAP, "event loop e callback",
            """
function primo(v, cb) { setTimeout(() => cb(v + 1), 100); }
function secondo(v, cb) { cb(v * 10); }
primo(1, (r1) => {
  secondo(r1, (r2) => console.log("risultato", r2));
});
secondo(5, (r) => console.log("subito", r));
console.log("fine");""",
            ["subito 50", "fine", "risultato 20"],
            [["risultato 20", "subito 50", "fine"], ["fine", "subito 50", "risultato 20"],
             ["subito 50", "risultato 20", "fine"], ["subito 50", "fine", "risultato 11"],
             ["fine", "risultato 20", "subito 50"]],
            spiegazione="Passare una callback non rende asincrona un'operazione: `secondo` la "
                        "chiama subito, quindi `subito 50` viene stampato durante l'esecuzione "
                        "del codice sincrono. `primo` invece la chiama dentro un `setTimeout`: il "
                        "risultato (`(1 + 1) * 10`) arriva dopo, quando il codice sincrono è "
                        "terminato.",
            rif=R % "Callback"))

d(uscita_js("c08-async-ritorno", CAP, "async e await",
            """
async function f() { return 1; }
const r = f();
console.log(typeof r, r instanceof Promise);
r.then((v) => console.log(v));
console.log("fine");""",
            ["object true", "fine", "1"],
            [["number false", "fine", "1"], ["object true", "1", "fine"],
             ["function false", "fine", "1"], ["number false", "1", "fine"],
             Err("TypeError", ["number false"])],
            spiegazione="Una funzione `async` restituisce **sempre** una Promise: il valore "
                        "restituito (qui 1) viene avvolto in una Promise risolta. Il gestore "
                        "registrato con `then` viene eseguito dopo la fine del codice sincrono.",
            rif=R % "async"))

d(uscita_js("c08-await-ordine", CAP, "async e await",
            """
async function f() {
  console.log("B");
  const v = await new Promise((res) => setTimeout(() => res("D"), 100));
  console.log(v);
  return "E";
}
console.log("A");
f().then((x) => console.log(x));
console.log("C");""",
            ["A", "B", "C", "D", "E"],
            [["A", "C", "B", "D", "E"], ["A", "B", "D", "E", "C"], ["A", "C", "D", "E", "B"],
             ["A", "B", "C", "E", "D"], ["A", "B", "D", "C", "E"]],
            spiegazione="La chiamata `f()` esegue subito il corpo della funzione fino al primo "
                        "`await` (quindi `B` viene stampato prima di `C`). `await` sospende "
                        "**solo** `f`: il resto del programma prosegue e stampa `C`. Quando la "
                        "Promise si risolve, `f` riprende (`D`) e il suo valore di ritorno "
                        "risolve la Promise restituita da `f()` (`E`).",
            rif=R % "await"))

d(uscita_js("c08-await-fuori", CAP, "async e await",
            """
function carica() {
  const dati = await Promise.resolve(42);
  return dati;
}
console.log("inizio");""",
            Err("SyntaxError"),
            [["inizio"], [], Err("ReferenceError"), Err("TypeError", ["inizio"]),
             Err("SyntaxError", ["inizio"])],
            spiegazione="`await` si può usare solo dentro le funzioni `async`: qui `carica` è una "
                        "funzione normale, e lo script non supera nemmeno l'analisi sintattica. "
                        "Un `SyntaxError` impedisce l'esecuzione dell'intero script, anche delle "
                        "righe che lo precedono o che non lo usano.",
            rif=R % "await"))

d(uscita_js("c08-async-errori", CAP, "async e await",
            """
async function leggi(ok) {
  if (!ok) throw new Error("rifiutata");
  return "dati";
}
async function main() {
  try {
    console.log(await leggi(true));
    console.log(await leggi(false));
    console.log("dopo");
  } catch (e) {
    console.log("errore:", e.message);
  }
}
main();""",
            ["dati", "errore: rifiutata"],
            [["dati", "errore: rifiutata", "dopo"], ["dati", "undefined", "dopo"],
             Err("Error", ["dati"]), ["errore: rifiutata"], ["dati", "rifiutata", "dopo"]],
            spiegazione="Un errore sollevato in una funzione `async` diventa una Promise "
                        "rifiutata; `await` su una Promise rifiutata **solleva** l'errore, che si "
                        "cattura con un normale `try/catch`. L'istruzione dopo l'`await` fallito "
                        "non viene eseguita.",
            rif=R % "async e await"))

d(uscita_browser("c08-localstorage", CAP, "memorizzare dati nel browser",
                 """
<script>
  localStorage.setItem("visite", 1);
  localStorage.visite = Number(localStorage.getItem("visite")) + 1;
  const v = localStorage.getItem("visite");
  console.log(typeof v, v + 1, localStorage.getItem("utente"));
</script>""",
                 ["string 21 null"],
                 [["number 3 null"], ["string 21 undefined"], ["number 3 undefined"],
                  ["string 11 null"], ["number 2 null"]],
                 spiegazione="`localStorage` memorizza **solo stringhe**: il numero viene convertito "
                             "in stringa al salvataggio, e `getItem` restituisce `\"2\"`, per cui "
                             "`v + 1` concatena. Le proprietà dell'oggetto sono un'alternativa a "
                             "`getItem` e `setItem`. Per una chiave assente `getItem` restituisce "
                             "`null`.",
                 rif=R % "localStorage"))

d(chiusa("c08-storage", CAP, "memorizzare dati nel browser",
         "Quali delle seguenti affermazioni sui meccanismi di memorizzazione nel browser sono "
         "**vere**?",
         ["I cookie vengono inviati al server in tutte le richieste verso lo stesso dominio, "
          "tramite l'header `Cookie`.",
          "`localStorage` memorizza solo valori stringa.",
          "I dati in `sessionStorage` sopravvivono a un aggiornamento della pagina, ma non alla "
          "chiusura della scheda.",
          "Esiste un `localStorage` distinto per ogni combinazione di dominio, protocollo e "
          "porta."],
         ["I dati in `localStorage` vengono inviati al server a ogni richiesta.",
          "I dati in `localStorage` vengono cancellati alla chiusura del browser.",
          "I dati memorizzati nel browser non sono modificabili dall'utente, quindi il server "
          "può fidarsene.",
          "`sessionStorage` è condiviso fra tutte le schede aperte sullo stesso sito.",
          "IndexedDB può memorizzare soltanto coppie di stringhe."],
         multi=True,
         spiegazione="I cookie fanno parte di HTTP e viaggiano con le richieste; `localStorage` e "
                     "`sessionStorage` no, e possono quindi contenere molti più dati (solo "
                     "stringhe). `localStorage` sopravvive anche al riavvio del browser, "
                     "`sessionStorage` è legato alla singola scheda. IndexedDB è un vero database. "
                     "Tutti questi dati sono sul computer dell'utente, che può leggerli e "
                     "modificarli: il server non deve fidarsene.",
         rif=R % "Memorizzare dati nel browser"))

d(chiusa("c08-cookie", CAP, "memorizzare dati nel browser",
         "Come vengono tipicamente impostati i cookie, e come tornano al server?",
         "Il server li imposta con l'header `Set-Cookie` di una risposta; il browser li rimanda "
         "con l'header `Cookie` nelle richieste successive allo stesso dominio.",
         ["Il server li imposta con l'header `Cookie` di una risposta; il browser li rimanda con "
          "l'header `Set-Cookie`.",
          "Il browser li invia al server solo quando uno script legge `document.cookie`.",
          "Il server li legge direttamente dal disco dell'utente quando gli servono.",
          "Il browser li invia solo nella prima richiesta di ogni sessione di navigazione.",
          "Il browser li aggiunge come parametri alla query string di ogni URL."],
         spiegazione="I cookie servono a superare l'assenza di stato di HTTP: il server li "
                     "imposta con `Set-Cookie`, il browser li memorizza e li allega, con l'header "
                     "`Cookie`, a tutte le richieste successive verso lo stesso dominio. Da "
                     "JavaScript si leggono e scrivono con `document.cookie`.",
         rif=R % "Cookie"))

d(chiusa("c08-thread", CAP, "event loop e callback",
         "Quali delle seguenti affermazioni sull'esecuzione asincrona del codice JavaScript di "
         "una pagina web sono **vere**?",
         ["Il codice JavaScript della pagina viene eseguito su un solo thread.",
          "Una callback di `setTimeout` viene eseguita solo quando lo stack delle chiamate è "
          "vuoto.",
          "Un calcolo sincrono molto lungo blocca la pagina anche se si trova dentro una "
          "callback.",
          "Mentre il timer di un `setTimeout` scorre, il thread di JavaScript può eseguire altro "
          "codice."],
         ["Allo scadere del timer, la callback interrompe il codice in esecuzione.",
          "`setTimeout(f, 0)` esegue `f` immediatamente, prima dell'istruzione successiva.",
          "Le callback asincrone vengono eseguite in parallelo, su thread diversi.",
          "Il timer di `setTimeout` viene contato dal thread di JavaScript, che resta occupato "
          "fino alla scadenza."],
         multi=True,
         spiegazione="C'è un solo thread: le attese (timer, rete) sono gestite dal browser, che "
                     "allo scadere mette la callback nella coda; l'event loop la esegue quando lo "
                     "stack è vuoto. Una callback non interrompe mai il codice in esecuzione, e "
                     "asincrono non vuol dire parallelo: un calcolo lungo blocca comunque tutto.",
         rif=R % "Sincronismo e asincronismo"))

d(chiusa("c08-fetch-404", CAP, "fetch",
         "Uno script esegue `const r = await fetch(\"/non-esiste\");` e il server risponde con "
         "stato `404`. Che cosa succede?",
         "La Promise si risolve con un oggetto `Response` in cui `r.ok` vale `false` e "
         "`r.status` vale `404`.",
         ["La Promise viene rifiutata, e l'`await` solleva un errore.",
          "La Promise si risolve con `null`, perché la risorsa non esiste.",
          "La Promise si risolve, e `r.ok` vale `true` perché il server ha risposto.",
          "La Promise resta per sempre nello stato `pending`.",
          "`fetch` solleva subito un `TypeError`, prima di inviare la richiesta."],
         spiegazione="La Promise di `fetch` viene rifiutata solo se la risposta non arriva "
                     "affatto (rete assente, server irraggiungibile). Un `404` o un `500` sono "
                     "risposte HTTP a tutti gli effetti: si riconoscono controllando "
                     "`response.ok` (vero solo per gli stati da 200 a 299) o `response.status`.",
         rif=R % "Lavorare con la risposta"))

d(chiusa("c08-fetch-corpo", CAP, "fetch",
         "Quali delle seguenti affermazioni sull'oggetto `Response` restituito da `fetch` sono "
         "**vere**?",
         ["La Promise di `fetch` si risolve appena arrivano gli header: il corpo può non essere "
          "ancora disponibile.",
          "`response.json()` restituisce una Promise, che si risolve con il corpo interpretato "
          "come JSON.",
          "Il corpo si può leggere una sola volta: dopo `response.text()`, `response.json()` non "
          "funziona.",
          "`response.ok` vale `true` solo per gli stati da 200 a 299."],
         ["`response.json()` restituisce direttamente l'oggetto, senza Promise.",
          "`response.ok` vale `true` per qualunque risposta del server.",
          "Per leggere gli header bisogna prima aver letto il corpo.",
          "`fetch` restituisce direttamente l'oggetto `Response`, senza Promise.",
          "Il corpo si legge come stringa dalla proprietà `response.text`."],
         multi=True,
         spiegazione="`fetch` restituisce una Promise che si risolve con la `Response` quando "
                     "arrivano gli header (`status`, `ok`, `headers`). Il corpo si legge dopo, "
                     "con metodi che restituiscono a loro volta Promise (`text()`, `json()`, "
                     "`blob()`...), e una volta sola, perché leggerlo lo consuma.",
         rif=R % "Lavorare con la risposta"))

d(chiusa("c08-fetch-post", CAP, "fetch",
         "Quale delle seguenti chiamate invia una richiesta `POST` con un corpo JSON?",
         "``fetch(\"/api\", { method: \"POST\", headers: { \"Content-Type\": \"application/json\" "
         "}, body: JSON.stringify(dati) })``",
         ["`fetch.post(\"/api\", dati)`",
          "`fetch(\"/api\", \"POST\", JSON.stringify(dati))`",
          "`fetch(\"POST /api\", { body: dati })`",
          "`fetch(\"/api\", { type: \"POST\", data: dati })`",
          "`fetch(\"/api\").post(JSON.stringify(dati))`"],
         spiegazione="Il secondo argomento di `fetch` è un oggetto di opzioni: `method` per il "
                     "metodo HTTP, `headers` per gli header della richiesta e `body` per il "
                     "corpo, che va serializzato (qui con `JSON.stringify`) e descritto con "
                     "l'header `Content-Type`.",
         rif=R % "L'API fetch"))

# ----------------------------------------------------------------------
# Domande aperte
d(aperta("c08-a-event-loop", CAP, "event loop e callback",
         "Si descriva il modello di esecuzione di JavaScript nel browser (thread, Web API, coda "
         "dei callback, event loop), spiegando con un esempio perché `setTimeout(f, 0)` non "
         "esegue `f` immediatamente.",
         ["Il codice della pagina gira su un solo thread, che esegue script, gestori di eventi e "
          "aggiornamento della pagina: un'attesa sincrona blocca tutto.",
          "Le operazioni lente (timer, richieste di rete, eventi) sono gestite dal browser "
          "tramite le Web API: la chiamata ritorna subito e l'attesa procede fuori dal thread.",
          "Al termine il browser mette la callback nella coda dei callback; l'event loop la "
          "esegue quando lo stack delle chiamate è vuoto.",
          "Es.: `console.log(\"A\"); setTimeout(() => console.log(\"B\"), 0); "
          "console.log(\"C\");` stampa A, C, B. Asincrono non vuol dire parallelo."],
         rif=R % "Sincronismo e asincronismo"))

d(aperta("c08-a-promise", CAP, "Promise",
         "Che cos'è una Promise in JavaScript? Se ne descrivano gli stati, il ruolo "
         "dell'executor e delle funzioni `resolve` e `reject`, i metodi `then`, `catch` e "
         "`finally`, e il motivo per cui sono preferibili alle callback annidate.",
         ["Un oggetto che collega un codice produttore (che richiede tempo) a un codice "
          "consumatore: rappresenta un risultato disponibile in futuro.",
          "Stati: `pending`, poi `fulfilled` (con un valore) o `rejected` (con un errore); una "
          "volta *settled* non cambia più. Stato e risultato non sono leggibili direttamente.",
          "L'executor, passato al costruttore, viene eseguito subito e chiama `resolve(valore)` "
          "o `reject(errore)`; il consumatore registra i gestori con `then`, `catch` e `finally` "
          "(eseguito in ogni caso, senza argomenti).",
          "Ogni `then` restituisce una nuova Promise (*chaining*): passi in sequenza senza "
          "annidamento, e un errore salta i `then` fino al primo `catch`, mentre con le callback "
          "annidate si arriva al *Callback Hell*."],
         rif=R % "Promise"))

d(aperta("c08-a-async-await", CAP, "async e await",
         "A che cosa servono le parole chiave `async` e `await`? Si spieghi il loro rapporto con "
         "le Promise e come si gestiscono gli errori.",
         ["`async` davanti a una funzione fa sì che restituisca sempre una Promise: il valore "
          "restituito viene avvolto in una Promise risolta, un errore in una rifiutata.",
          "`await`, solo dentro le funzioni `async`, sospende la funzione finché la Promise non "
          "è sistemata, e ne restituisce il valore (o ne solleva l'errore).",
          "Non blocca il browser: sospende solo la funzione `async`, mentre il resto del "
          "programma prosegue.",
          "Gli errori si gestiscono con i normali `try/catch`; il codice asincrono si legge come "
          "codice sincrono, senza catene di `then`: è zucchero sintattico sulle Promise."],
         rif=R % "async e await"))

d(aperta("c08-a-storage", CAP, "memorizzare dati nel browser",
         "Si confrontino cookie, `localStorage`, `sessionStorage` e IndexedDB. Quali dati non vi "
         "andrebbero mai memorizzati, e perché?",
         ["Cookie: piccole stringhe impostate di solito dal server con `Set-Cookie` e rimandate "
          "dal browser in tutte le richieste verso lo stesso dominio; da JavaScript con "
          "`document.cookie`.",
          "`localStorage`: coppie chiave/valore (solo stringhe) non inviate al server, una per "
          "combinazione di dominio, protocollo e porta; sopravvivono al riavvio del browser.",
          "`sessionStorage`: stessa interfaccia, ma legato alla scheda (sopravvive "
          "all'aggiornamento, non alla chiusura). IndexedDB: un database nel browser, per le "
          "applicazioni offline.",
          "Sono sul computer dell'utente, ispezionabili e modificabili: niente segreti, e il "
          "server non deve fidarsi di questi dati (es. i prezzi di un carrello)."],
         rif=R % "Memorizzare dati nel browser"))

d(aperta("c08-a-fetch", CAP, "fetch",
         "Si descriva l'API `fetch`: che cosa restituisce, quando la sua Promise viene risolta o "
         "rifiutata, e come si legge il corpo della risposta. Si scriva una funzione `async` "
         "che scarica un documento JSON gestendo gli errori.",
         ["`fetch(url, opzioni)` avvia una richiesta HTTP (opzioni: metodo, header, corpo) e "
          "restituisce una Promise che si risolve in un oggetto `Response`.",
          "Si risolve appena arrivano gli header (`status`, `ok`, `headers`); viene rifiutata "
          "solo se la risposta non arriva: un 404 o un 500 la risolvono, con `ok` falso.",
          "Il corpo si legge con metodi che restituiscono Promise (`text()`, `json()`, "
          "`blob()`...), una volta sola.",
          "Es.: `const r = await fetch(url); if (!r.ok) throw new Error(r.status); return await "
          "r.json();`, dentro un `try/catch` per gli errori di rete."],
         rif=R % "Richieste di rete"))
