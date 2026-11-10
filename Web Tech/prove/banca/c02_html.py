"""Capitolo 2: HTML (elementi, head, link e URL, tabelle, liste, entità,
immagini, form, tag semantici, DOM, DevTools)."""

from urllib.parse import urljoin, urlencode

from generatore import L, aperta, chiusa, famiglia

CAP = 2
R = "cap. 2, «%s»"

DOMANDE = []
d = DOMANDE.append

# ----------------------------------------------------------------------
# Famiglia: risoluzione delle URL relative
PAGINE = ["https://www.example.org/a/b/c/hello.html",
          "http://localhost:3000/corsi/web/lezioni/index.html",
          "https://docenti.unina.it/didattica/tw/programma.html"]
RIFERIMENTI = ["./index.html", "../foo.html", "../../pic.jpg", "./../../pic.jpg", "pic.jpg",
               "/img/logo.png", "../css/stile.css", "?pagina=2", "#esami", "sub/../x.html"]


@famiglia("c02-url-relativa", CAP, "URL relative e assolute", varianti=4)
def _url_relativa(rng):
    pagina = rng.choice(PAGINE)
    href = rng.choice(RIFERIMENTI)
    giusta = urljoin(pagina, href)
    base = pagina.rsplit("/", 1)[0]
    radice = "/".join(pagina.split("/")[:3])
    # le directory della pagina, dalla radice alla più interna
    segmenti = pagina.split("/")[3:-1]
    cartelle = [radice + "".join("/" + x for x in segmenti[:k]) for k in range(len(segmenti) + 1)]
    resto = href
    while resto.startswith(("./", "../")):
        resto = resto.split("/", 1)[1]
    resto = resto.lstrip("/")
    pulito = resto.replace("../", "").replace("./", "")
    candidati = set()
    if href[0] in "?#":
        candidati |= {c + "/" + href for c in cartelle}
        candidati |= {c + "/" + href[1:].split("=")[0] for c in cartelle}
        candidati.add(pagina + "/" + href)
    else:
        candidati |= {c + "/" + pulito for c in cartelle}
        candidati |= {c + "/" + pulito.split("/")[-1] for c in cartelle}
        # l'errore tipico: trattare la pagina come se fosse una directory
        candidati.add(pagina + "/" + pulito)
    sbagliate = sorted(c for c in candidati if c != giusta and "/./" not in c and "/../" not in c)
    rng.shuffle(sbagliate)
    return chiusa(
        "c02-url-relativa", CAP, "URL relative e assolute",
        "Una pagina all'indirizzo `%s` contiene il collegamento ``<a href=\"%s\">``. A quale "
        "URL porta il collegamento?" % (pagina, href),
        "`%s`" % giusta, ["`%s`" % s for s in sbagliate[:5]], n=4,
        spiegazione="Una URL relativa si risolve rispetto alla directory della pagina corrente "
                    "(`%s/`). Se comincia con `/` si parte invece dalla radice del sito; `.` "
                    "indica la directory corrente e `..` la directory padre; `?` e `#` "
                    "sostituiscono solo la query o l'ancora della pagina corrente." % base,
        rif=R % "URL relative e assolute",
        verifica=dict(tipo="node", strict=True,
                      codice="console.log(new URL(%s, %s).href);" % (
                          '"%s"' % href, '"%s"' % pagina),
                      righe=[giusta], errore=None))


d(_url_relativa)

# ----------------------------------------------------------------------
# Famiglia: che cosa invia un form con il metodo GET
NOMI = ["Mario Rossi", "Ada Lovelace", "Alan Turing", "Grace Hopper"]
ESAMI = [("web", "Tecnologie Web"), ("pl2", "Linguaggi di Programmazione II"),
         ("net", "Reti di Calcolatori")]
CORSI = [("tw", "Tecnologie Web"), ("igsw", "Ingegneria del Software"), ("rpd", "Reti")]


@famiglia("c02-form-get", CAP, "form: invio e codifica", varianti=4)
def _form_get(rng):
    nome = rng.choice(NOMI)
    spuntati = [v for v, _ in ESAMI if rng.random() < 0.5]
    anno = rng.choice(["1", "2", "3", None])
    corso_sel = rng.choice([None, "igsw", "rpd"])
    righe = ['<form action="/iscrizione" method="GET">',
             '  <input type="text" name="nome" id="n" value="%s">' % nome]
    for valore, _etichetta in ESAMI:
        righe.append('  <input type="checkbox" name="esami" value="%s"%s>' % (
            valore, " checked" if valore in spuntati else ""))
    for a in ("1", "2", "3"):
        righe.append('  <input type="radio" name="anno" value="%s"%s>' % (
            a, " checked" if a == anno else ""))
    righe.append('  <select name="corso">')
    for v, etichetta in CORSI:
        righe.append('    <option value="%s"%s>%s</option>' % (
            v, " selected" if v == corso_sel else "", etichetta))
    righe.append('  </select>')
    righe.append('  <input type="text" id="note" value="nessuna">')
    righe.append('  <button type="submit">Invia</button>')
    righe.append('</form>')
    html = "\n".join(righe)

    coppie = [("nome", nome)] + [("esami", v) for v in spuntati]
    if anno:
        coppie.append(("anno", anno))
    corso = corso_sel or "tw"
    coppie.append(("corso", corso))
    giusta = "/iscrizione?" + urlencode(coppie)
    sbagliate = set()
    # errori tipici: checkbox non spuntate, spazi non codificati, id al posto
    # di name, valori uniti con la virgola, select dimenticata, campo senza name
    tutte = [("nome", nome)] + [("esami", v) for v, _ in ESAMI] + (
        [("anno", anno)] if anno else []) + [("corso", corso)]
    sbagliate.add("/iscrizione?" + urlencode(tutte))
    sbagliate.add(giusta.replace("+", " ").replace("%20", " "))
    sbagliate.add("/iscrizione?" + urlencode([("n", nome)] + coppie[1:]))
    sbagliate.add("/iscrizione?" + urlencode(coppie + [("note", "nessuna")]))
    if len(spuntati) > 1:
        unite = [("nome", nome), ("esami", ",".join(spuntati))] + coppie[1 + len(spuntati):]
        sbagliate.add("/iscrizione?" + urlencode(unite).replace("%2C", ","))
    sbagliate.add("/iscrizione?" + urlencode([c for c in coppie if c[0] != "corso"]))
    if not anno:
        sbagliate.add("/iscrizione?" + urlencode(coppie[:-1] + [("anno", ""), coppie[-1]]))
    sbagliate.discard(giusta)
    sbagliate = sorted(sbagliate)
    rng.shuffle(sbagliate)
    return chiusa(
        "c02-form-get", CAP, "form: invio e codifica",
        "Si consideri il seguente form, inviato senza che l'utente abbia modificato alcun "
        "campo. Quale URL viene richiesta all'invio?",
        "`%s`" % giusta, ["`%s`" % s for s in sbagliate[:5]], n=4,
        codice=L("html", html),
        spiegazione="Con `GET` i dati diventano la query della URL indicata da `action`, come "
                    "coppie `name=valore` nell'ordine del documento. Si inviano solo i campi "
                    "con un attributo `name` (l'`id` non conta): le checkbox spuntate "
                    "ripetono il nome, quelle non spuntate non compaiono; un gruppo di radio "
                    "senza scelta non compare; la `select` invia l'opzione `selected`, o la "
                    "prima. Gli spazi diventano `+` (codifica delle URL).",
        rif=R % "Form",
        verifica=dict(tipo="dom", html="<!DOCTYPE html><html><body>\n%s\n</body></html>" % html,
                      espressione="(() => { const f = document.querySelector('form'); return "
                                  "f.getAttribute('action') + '?' + new URLSearchParams(new "
                                  "FormData(f)).toString(); })()",
                      atteso=giusta))


d(_form_get)

# ----------------------------------------------------------------------
d(chiusa("c02-void", CAP, "tag, elementi e attributi",
         "Quali dei seguenti elementi HTML sono **elementi vuoti** (*void*), cioè non hanno "
         "contenuto né tag di chiusura?",
         ["`<br>`", "`<img>`", "`<input>`", "`<meta>`", "`<link>`"],
         ["`<p>`", "`<script>`", "`<a>`", "`<li>`", "`<title>`", "`<span>`"],
         multi=True,
         spiegazione="Gli elementi vuoti hanno solo il tag di apertura (con eventuali "
                     "attributi): `br`, `img`, `input`, `meta`, `link`, `hr`, ... `<script>` "
                     "invece va sempre chiuso con `</script>`, anche quando usa l'attributo "
                     "`src`.",
         rif=R % "Tag, elementi e attributi"))

d(chiusa("c02-head", CAP, "l'elemento head",
         "Quali dei seguenti elementi si collocano normalmente nell'elemento `<head>` di un "
         "documento HTML?",
         ["`<title>`", '``<meta charset="utf-8">``', '``<link rel="stylesheet" href="s.css">``',
          '``<link rel="icon" href="favicon.ico">``'],
         ["`<h1>`", "`<main>`", "`<footer>`", "`<p>`", "`<table>`"],
         multi=True,
         spiegazione="L'`head` contiene i metadati del documento: titolo (mostrato nella "
                     "scheda), codifica dei caratteri, fogli di stile, icona, script. Il "
                     "contenuto visibile (titoli, paragrafi, tabelle, sezioni) va nel `body`.",
         rif=R % "L'elemento head"))

d(chiusa("c02-charset", CAP, "l'elemento head",
         "Una pagina scritta in UTF-8 non dichiara la codifica dei caratteri e il server non "
         "la indica nella risposta. Che cosa può succedere?",
         "Le lettere accentate possono comparire come sequenze di simboli senza senso.",
         ["Il browser rifiuta di visualizzare la pagina e mostra un errore.",
          "Il server risponde con il codice di stato `415 Unsupported Media Type`.",
          "Il browser mostra il codice sorgente della pagina invece del contenuto.",
          "Gli elementi della pagina vengono visualizzati senza alcuno stile.",
          "Le immagini non vengono caricate perché il percorso non è valido."],
         spiegazione="Senza `<meta charset=\"utf-8\">` (o l'intestazione `Content-Type` con il "
                     "charset) il browser deve indovinare la codifica: se sbaglia, i caratteri "
                     "non ASCII come «è» diventano sequenze di simboli (*mojibake*).",
         rif=R % "L'elemento head"))

d(chiusa("c02-intestazioni", CAP, "elementi fondamentali",
         "Quale fra le seguenti affermazioni sugli elementi `<h1>`...`<h6>` è corretta?",
         "Indicano titoli di sezione e la loro gerarchia, non la dimensione del testo.",
         ["Servono a ingrandire il testo: `<h1>` è il carattere più piccolo.",
          "Ogni pagina può contenere al massimo un elemento per ciascun livello.",
          "Devono comparire nell'`head`, prima del `title`.",
          "Sono elementi in linea e vanno sempre racchiusi in un paragrafo.",
          "Si possono usare solo all'interno di una tabella."],
         spiegazione="Le intestazioni esprimono la struttura del documento (titolo, "
                     "sottosezioni, ...): motori di ricerca e lettori di schermo le usano per "
                     "capirne l'organizzazione. L'aspetto si controlla con il CSS.",
         rif=R % "Elementi fondamentali"))

d(chiusa("c02-semantica-testo", CAP, "elementi fondamentali",
         "Che differenza c'è fra `<strong>` e `<b>`?",
         "`<strong>` indica un contenuto importante; `<b>` lo evidenzia senza dargli "
         "importanza.",
         ["Nessuna: sono sinonimi e i browser li trattano allo stesso modo in ogni contesto.",
          "`<strong>` è deprecato in HTML5 e va sostituito con `<b>`.",
          "`<b>` è un elemento di blocco, `<strong>` un elemento in linea.",
          "`<strong>` rende il testo rosso, `<b>` lo rende in grassetto.",
          "`<b>` si può usare solo nei titoli, `<strong>` solo nei paragrafi."],
         spiegazione="HTML descrive il significato, non l'aspetto: `<strong>` ed `<em>` "
                     "portano semantica (importanza, enfasi), mentre `<b>` e `<i>` sono "
                     "semplici evidenziazioni tipografiche. Che entrambi appaiano in grassetto "
                     "è solo lo stile predefinito del browser.",
         rif=R % "Semantica del testo"))

d(chiusa("c02-commenti", CAP, "elementi fondamentali",
         "Uno sviluppatore commenta in una pagina HTML la password del database di prova, "
         "``<!-- password: s3cr3t -->``. Che cosa succede?",
         "Il commento non è visibile nella pagina, ma chiunque può leggerlo nel sorgente.",
         ["Il server rimuove i commenti prima di inviare la pagina, quindi è al sicuro.",
          "Il browser cifra i commenti, che sono leggibili solo dallo sviluppatore.",
          "La pagina non viene visualizzata perché i commenti non possono contenere `:`.",
          "Il commento viene mostrato in un riquadro grigio nella pagina.",
          "Il commento è leggibile solo nei DevTools, non nel sorgente della pagina."],
         spiegazione="I commenti HTML viaggiano nella risposta come il resto del documento: "
                     "non vengono visualizzati, ma basta «Visualizza sorgente» o l'ispettore "
                     "per leggerli. Non sono un nascondiglio.",
         rif=R % "Commenti"))

d(chiusa("c02-target", CAP, "collegamenti ipertestuali",
         "Che effetto ha l'attributo ``target=\"_blank\"`` su un elemento `<a>`?",
         "Il collegamento si apre in una nuova scheda (o finestra) del browser.",
         ["Il collegamento si apre nella stessa scheda, sostituendo la pagina.",
          "Il collegamento viene disattivato e il testo appare grigio.",
          "La risorsa collegata viene scaricata invece che visualizzata.",
          "La pagina collegata viene aperta senza stili.",
          "Il collegamento viene seguito solo con un doppio clic."],
         spiegazione="`target` indica dove aprire la risorsa collegata: `_blank` in un nuovo "
                     "contesto di navigazione (nuova scheda o finestra); il valore predefinito "
                     "`_self` la apre nella scheda corrente.",
         rif=R % "L'attributo target"))

d(chiusa("c02-relative-assolute", CAP, "URL relative e assolute",
         "Perché per collegare le pagine **interne** di un sito conviene usare URL relative?",
         "Perché non cambiano se il sito viene spostato su un altro host, per esempio dallo "
         "sviluppo alla produzione.",
         ["Perché le URL assolute non funzionano con il protocollo HTTPS.",
          "Perché i browser caricano più velocemente le URL relative.",
          "Perché le URL assolute non possono contenere parametri di query.",
          "Perché le URL relative vengono risolte dal DNS e non dal browser.",
          "Perché le URL relative non generano richieste HTTP."],
         spiegazione="Una URL relativa viene completata dal browser a partire dalla pagina "
                     "corrente: se cambia il nome dell'host, i collegamenti interni continuano "
                     "a funzionare senza modifiche. Per le risorse esterne servono invece URL "
                     "assolute.",
         rif=R % "Meglio relative o assolute?"))

d(chiusa("c02-directory", CAP, "URL che puntano a una directory",
         "Un browser richiede `http://localhost:8080/docs/`, che corrisponde a una "
         "directory. Che cosa restituisce di solito un server web statico?",
         "Il file indice della directory (tipicamente `index.html`), se esiste.",
         ["Sempre l'elenco dei file contenuti nella directory.",
          "Il codice di stato `400 Bad Request`, perché le URL non possono finire con `/`.",
          "Un archivio compresso con tutti i file della directory.",
          "Il primo file della directory in ordine alfabetico.",
          "Il file `index.html` della radice del sito."],
         spiegazione="Per convenzione il server cerca un file indice (`index.html`). Se non c'è, "
                     "alcuni server possono generare l'elenco dei file (*autoindex*): comodo, "
                     "ma pericoloso, perché espone file che non si volevano pubblicare.",
         rif=R % "URL che puntano a una directory"))

d(chiusa("c02-tabelle", CAP, "tabelle",
         "In una tabella HTML, come si ottiene una cella che occupa **due colonne**?",
         '``<td colspan="2">``',
         ['``<td rowspan="2">``', '``<td width="2">``', '``<td span="2">``',
          '``<tr colspan="2">``', '``<th cols="2">``'],
         spiegazione="`colspan` estende la cella su più colonne, `rowspan` su più righe. Le "
                     "righe sono `<tr>`, le celle di dati `<td>` e quelle di intestazione "
                     "`<th>`.",
         rif=R % "Tabelle"))

d(chiusa("c02-tabelle-layout", CAP, "tabelle",
         "Perché non si devono usare le tabelle HTML per impaginare una pagina (colonne, "
         "barre laterali, ...)?",
         "Perché la tabella dichiara dati tabellari: usarla per l'aspetto ne falsa il "
         "significato.",
         ["Perché i browser moderni non visualizzano più le tabelle annidate.",
          "Perché una pagina può contenere al massimo una tabella.",
          "Perché le tabelle non possono contenere immagini o collegamenti.",
          "Perché il contenuto delle tabelle non viene indicizzato in alcun caso.",
          "Perché le tabelle si possono usare solo all'interno di un form."],
         spiegazione="HTML descrive la struttura: una tabella dice «questi sono dati in righe "
                     "e colonne». Usata per l'impaginazione confonde lettori di schermo e "
                     "motori di ricerca, e rende il layout rigido; l'impaginazione si fa con "
                     "il CSS (Flexbox, Grid).",
         rif=R % "Tabelle"))

d(chiusa("c02-liste", CAP, "liste",
         "Quali coppie di elementi sono corrette per una **lista di descrizione** (glossario)?",
         "`<dl>` per la lista, `<dt>` per il termine e `<dd>` per la descrizione.",
         ["`<ul>` per la lista, `<li>` per il termine e `<p>` per la descrizione.",
          "`<dl>` per la lista, `<li>` per il termine e `<dd>` per la descrizione.",
          "`<ol>` per la lista, `<dt>` per il termine e `<dd>` per la descrizione.",
          "`<list>` per la lista, `<term>` per il termine e `<desc>` per la descrizione.",
          "`<dd>` per la lista, `<dl>` per il termine e `<dt>` per la descrizione."],
         spiegazione="Le liste di descrizione associano termini e definizioni: `dl` (description "
                     "list) contiene coppie `dt` (termine) e `dd` (descrizione). Le liste "
                     "puntate sono `ul`, quelle numerate `ol`, entrambe con elementi `li`.",
         rif=R % "Liste di descrizione"))

d(chiusa("c02-entita", CAP, "riferimenti a caratteri",
         "Che testo visualizza il browser per il seguente paragrafo?",
         "`Il tag <b> e \"x\" & co.`",
         ["`Il tag &lt;b&gt; e &quot;x&quot; &amp; co.`",
          "`Il tag e \"x\" & co.` (con il resto del testo in grassetto)",
          "`Il tag <b> e &quot;x&quot; & co.`",
          "`Il tag lt;b gt; e quot;x quot; amp; co.`",
          "`Il tag e \"x\" &amp; co.`"],
         codice=L("html", "<p>Il tag &lt;b&gt; e &quot;x&quot; &amp; co.</p>"),
         spiegazione="I riferimenti a caratteri (entità) permettono di scrivere nel testo "
                     "caratteri che altrimenti avrebbero un significato speciale: `&lt;` per "
                     "`<`, `&gt;` per `>`, `&amp;` per `&`, `&quot;` per le virgolette. Il "
                     "browser li sostituisce con il carattere corrispondente.",
         rif=R % "Riferimenti a caratteri (entità)",
         verifica=dict(tipo="dom",
                       html="<!DOCTYPE html><html><body><p>Il tag &lt;b&gt; e &quot;x&quot; "
                            "&amp; co.</p></body></html>",
                       espressione="document.querySelector('p').textContent",
                       atteso='Il tag <b> e "x" & co.')))

d(chiusa("c02-nbsp", CAP, "riferimenti a caratteri",
         "A che cosa serve il riferimento `&nbsp;`?",
         "Inserisce uno spazio che non viene compresso e su cui non si va a capo.",
         ["Inserisce un a capo, come l'elemento `<br>`.",
          "Inserisce un carattere invisibile che separa due parole lunghe.",
          "Indica la fine del contenuto di un paragrafo.",
          "Inserisce una tabulazione larga quattro spazi.",
          "Impedisce al browser di interpretare i tag che seguono."],
         spiegazione="HTML comprime spazi e a capo consecutivi in un solo spazio. Lo spazio non "
                     "divisibile (*non-breaking space*) non viene compresso e impedisce di "
                     "andare a capo in quel punto (es. `10&nbsp;km`).",
         rif=R % "Riferimenti a caratteri (entità)"))

d(chiusa("c02-alt", CAP, "immagini",
         "Quali delle seguenti affermazioni sull'attributo `alt` di `<img>` sono **vere**?",
         ["Fornisce un testo alternativo letto dai lettori di schermo.",
          "Viene mostrato al posto dell'immagine se questa non si carica.",
          "Va sempre indicato (vuoto, `alt=\"\"`, se l'immagine è solo decorativa)."],
         ["Indica il percorso alternativo da cui scaricare l'immagine.",
          "Specifica il testo del suggerimento mostrato al passaggio del mouse.",
          "Imposta la larghezza alternativa dell'immagine sui dispositivi mobili.",
          "È facoltativo e non ha alcun effetto sull'accessibilità.",
          "Contiene la didascalia che il browser scrive sotto l'immagine."],
         multi=True,
         spiegazione="`alt` descrive l'immagine a chi non può vederla (lettori di schermo, "
                     "immagine non caricata, motori di ricerca). Non è facoltativo: per le "
                     "immagini decorative si usa la stringa vuota.",
         rif=R % "Immagini"))

d(chiusa("c02-richieste-immagini", CAP, "immagini",
         "Il browser riceve un documento HTML che include un foglio di stile, uno script e "
         "tre immagini, tutti con URL diverse e nessuno in cache. Quante richieste HTTP "
         "servono, in tutto, per caricare la pagina?",
         "Sei: una per il documento e una per ciascuna risorsa inclusa.",
         ["Una sola: il server invia il documento con tutte le risorse incluse.",
          "Due: una per il documento e una per tutte le risorse insieme.",
          "Tre: una per il documento, una per lo stile e una per lo script.",
          "Quattro: le immagini viaggiano in un'unica richiesta.",
          "Cinque: il documento HTML non richiede una richiesta separata."],
         spiegazione="Ogni risorsa ha la propria URL e viene richiesta separatamente: il "
                     "browser legge l'HTML e, man mano che incontra `link`, `script` e `img`, "
                     "invia nuove richieste. Si vede bene nella scheda Rete dei DevTools.",
         rif=R % "Dietro le quinte"))

d(chiusa("c02-ancore", CAP, "attributi globali",
         "Una pagina contiene ``<h2 id=\"esami\">Esami</h2>``. Come si scrive un collegamento "
         "che porti direttamente a quell'intestazione, nella stessa pagina?",
         '``<a href="#esami">``',
         ['``<a href="esami">``', '``<a name="#esami">``', '``<a href="?id=esami">``',
          '``<a target="esami">``', '``<a href="/esami">``'],
         spiegazione="L'ancora (il frammento dopo `#`) fa scorrere la pagina fino all'elemento "
                     "con quell'`id`. Il frammento non viene inviato al server.",
         rif=R % "Ancore nelle URL"))

d(chiusa("c02-id-class", CAP, "attributi globali",
         "Quali delle seguenti affermazioni sugli attributi `id` e `class` sono **vere**?",
         ["Un `id` deve essere unico nel documento.",
          "Più elementi possono avere la stessa classe.",
          "Un elemento può avere più classi, separate da spazi."],
         ["Un elemento può avere più `id`, separati da spazi.",
          "`class` si può usare solo sugli elementi di blocco.",
          "Due elementi con lo stesso `id` vengono uniti dal browser.",
          "`id` e `class` sono attributi riservati agli elementi del form.",
          "Il valore di `class` deve iniziare con un punto."],
         multi=True,
         spiegazione="`id` identifica un singolo elemento (unico nel documento, usato da "
                     "ancore, CSS `#id` e `getElementById`); `class` raggruppa elementi "
                     "(anche più classi per elemento, CSS `.classe`). Sono attributi globali, "
                     "validi su qualunque elemento.",
         rif=R % "Attributi globali"))

d(chiusa("c02-name-id", CAP, "form: invio e codifica",
         "In un form, quale attributo di un `<input>` determina la chiave con cui il valore "
         "viene inviato al server?",
         "`name`", ["`id`", "`value`", "`for`", "`label`", "`key`"],
         spiegazione="I dati di un form viaggiano come coppie `name=valore`: un campo senza "
                     "`name` non viene inviato. L'`id` serve a collegare l'etichetta "
                     "(`<label for=\"...\">`) e a trovare l'elemento con CSS o JavaScript.",
         rif=R % "Invio del form"))

d(chiusa("c02-label", CAP, "form: invio e codifica",
         "Come si collega correttamente un'etichetta a un campo di testo?",
         '``<label for="email">Email</label> <input id="email" name="email">``',
         ['``<label name="email">Email</label> <input name="email">``',
          '``<label id="email">Email</label> <input for="email">``',
          '``<label for="email">Email</label> <input name="mail" class="email">``',
          '``<label>Email</label> <input label="Email">``',
          '``<label href="#email">Email</label> <input id="email">``'],
         spiegazione="L'attributo `for` dell'etichetta contiene l'`id` del campo: così un clic "
                     "sull'etichetta attiva il campo e i lettori di schermo leggono "
                     "l'etichetta insieme al campo. In alternativa il campo si può mettere "
                     "dentro la `label`.",
         rif=R % "Etichette"))

d(chiusa("c02-get-post", CAP, "form: invio e codifica",
         "Quali delle seguenti affermazioni sull'invio di un form sono **vere**?",
         ["Con `GET` i dati compaiono nella URL, come stringa di query.",
          "Con `POST` i dati viaggiano nel corpo della richiesta.",
          "Una ricerca, che non modifica nulla, si presta all'invio con `GET`."],
         ["Con `POST` i dati sono cifrati anche senza HTTPS.",
          "Con `GET` i dati viaggiano nelle intestazioni della richiesta.",
          "Con `POST` non è possibile inviare caratteri accentati.",
          "Il metodo predefinito di un form, se non indicato, è `POST`.",
          "Una richiesta `GET` non può contenere più di un parametro."],
         multi=True,
         spiegazione="`GET` mette i dati nella query: comodo per ricerche (la URL si può "
                     "salvare e condividere) ma i dati restano nella cronologia. `POST` li "
                     "mette nel corpo, ed è adatto alle operazioni che modificano lo stato. "
                     "Nessuno dei due cifra nulla: lo fa HTTPS. Il metodo predefinito è `GET`.",
         rif=R % "Invio con GET"))

d(chiusa("c02-percent", CAP, "form: invio e codifica",
         "Un campo `q` contiene `pane & vino`. Come compare nella query string della "
         "richiesta `GET`?",
         "`q=pane+%26+vino`",
         ["`q=pane & vino`", "`q=pane+&+vino`", "`q=pane%20&%20vino`", "`q=\"pane & vino\"`",
          "`q=pane&vino`"],
         spiegazione="Nella query alcuni caratteri hanno un significato (`&` separa i "
                     "parametri, `=` separa chiave e valore), quindi i valori vengono codificati: "
                     "lo spazio diventa `+` e `&` diventa `%26` (*percent encoding*).",
         rif=R % "Codifica delle URL",
         verifica=dict(tipo="node", strict=True,
                       codice='console.log(new URLSearchParams({ q: "pane & vino" }).toString());',
                       righe=["q=pane+%26+vino"], errore=None)))

d(chiusa("c02-checkbox-vuote", CAP, "form: invio e codifica",
         "Un form ha tre checkbox con ``name=\"esami\"`` e l'utente non ne spunta nessuna. "
         "Che cosa riceve il server per il parametro `esami`?",
         "Nulla: il parametro non compare affatto nei dati inviati.",
         ["Il parametro con valore vuoto, `esami=`.",
          "Il parametro con valore `off` per ciascuna casella.",
          "Il parametro con valore `false`.",
          "Il parametro con valore `null`.",
          "Il form non viene inviato finché non si spunta almeno una casella."],
         spiegazione="Le checkbox non spuntate non vengono inviate: il server non deve "
                     "aspettarsi di trovare il parametro. Le caselle spuntate con lo stesso "
                     "`name` ripetono invece la chiave (`esami=web&esami=pl2`).",
         rif=R % "Caselle di spunta"))

d(chiusa("c02-radio", CAP, "form: invio e codifica",
         "Che cosa rende mutuamente esclusivi tre pulsanti radio di un form?",
         "Il fatto di avere lo stesso valore dell'attributo `name`.",
         ["Il fatto di avere lo stesso valore dell'attributo `id`.",
          "Il fatto di essere dentro lo stesso elemento `<label>`.",
          "L'attributo `exclusive` sul primo pulsante del gruppo.",
          "Il fatto di avere valori diversi dell'attributo `value`.",
          "L'attributo `type=\"group\"` sul `<form>`."],
         spiegazione="I radio con lo stesso `name` formano un gruppo in cui si può scegliere "
                     "una sola opzione; all'invio si trasmette `name=value` dell'opzione "
                     "scelta. Gli `id` devono anzi essere diversi.",
         rif=R % "Pulsanti radio"))

d(chiusa("c02-div-span", CAP, "organizzare il contenuto",
         "Qual è la differenza fra `<div>` e `<span>`?",
         "`<div>` è un contenitore generico di blocco, `<span>` un contenitore generico in "
         "linea.",
         ["`<div>` è un contenitore in linea, `<span>` un contenitore di blocco.",
          "`<span>` si può usare solo all'interno di una tabella.",
          "`<div>` ha un significato semantico preciso, `<span>` no.",
          "`<span>` ridimensiona il testo, `<div>` lo allinea.",
          "Sono sinonimi: cambia solo il numero di caratteri da scrivere."],
         spiegazione="Entrambi sono privi di significato e servono a raggruppare contenuto da "
                     "stilizzare o manipolare: `div` raggruppa blocchi (va a capo), `span` "
                     "porzioni di testo all'interno di una riga. Se esiste un tag semantico "
                     "adatto, va preferito.",
         rif=R % "Organizzare il contenuto"))

d(chiusa("c02-semantici", CAP, "tag semantici",
         "Quali dei seguenti sono **tag semantici** di HTML5 per strutturare una pagina?",
         ["`<header>`", "`<nav>`", "`<main>`", "`<article>`", "`<footer>`", "`<aside>`"],
         ["`<div>`", "`<span>`", "`<b>`", "`<center>`", "`<container>`"],
         multi=True, quante_giuste=(2, 3),
         spiegazione="`header`, `nav`, `main`, `article`, `section`, `aside` e `footer` dicono "
                     "che cosa contengono: aiutano lettori di schermo e motori di ricerca e "
                     "rendono il codice più leggibile. `div` e `span` sono contenitori "
                     "generici; `<container>` non esiste.",
         rif=R % "Tag semantici"))

d(chiusa("c02-annidamento", CAP, "il documento come albero",
         "Quale dei seguenti frammenti HTML è annidato **correttamente**?",
         "`<p>Un <em>testo <strong>molto</strong> importante</em>.</p>`",
         ["`<p>Un <em>testo <strong>molto</em> importante</strong>.</p>`",
          "`<p>Un <em>testo</p> molto importante</em>.`",
          "`<em><p>Un testo</em> molto importante.</p>`",
          "`<p>Un <strong>testo <em>molto</strong></em> importante.</p>`"],
         n=4,
         spiegazione="Il documento è un albero: un elemento aperto dentro un altro deve "
                     "chiudersi prima del suo contenitore. Tag «incrociati» non sono validi e "
                     "il browser li corregge a modo suo.",
         rif=R % "Il documento come albero"))

d(chiusa("c02-cache", CAP, "strumenti per sviluppatori",
         "Perché durante lo sviluppo conviene spuntare «Disattiva cache» nella scheda Rete "
         "dei DevTools?",
         "Per essere sicuri che il browser scarichi la versione aggiornata di CSS e script.",
         ["Perché la cache impedisce di vedere le richieste nella scheda Rete.",
          "Perché altrimenti il server rifiuta le richieste con codice `403`.",
          "Perché la cache rende la pagina vulnerabile ad attacchi XSS.",
          "Perché la cache funziona solo con HTTPS e in sviluppo si usa HTTP.",
          "Per poter modificare il codice HTML direttamente nel browser."],
         spiegazione="La cache HTTP conserva copie delle risorse già scaricate per non "
                     "richiederle di nuovo: ottima in produzione, ma in sviluppo può farci "
                     "vedere una versione vecchia di un file appena modificato.",
         rif=R % "Analisi di rete"))

d(chiusa("c02-living", CAP, "che cos'è HTML",
         "Che cosa significa che HTML è un *Living Standard*?",
         "Che è una specifica aggiornata di continuo, senza numeri di versione.",
         ["Che ogni browser ne definisce una versione diversa.",
          "Che la specifica viene riscritta da zero ogni anno.",
          "Che si può usare solo nelle pagine generate dinamicamente.",
          "Che il suo sviluppo si è fermato con HTML5.",
          "Che solo i tag più usati fanno parte dello standard."],
         spiegazione="Lo standard HTML, curato dal WHATWG, evolve in modo continuo: nuove "
                     "funzionalità vengono aggiunte senza versioni numerate («HTML5» è ormai "
                     "solo un nome).",
         rif=R % "Un po' di storia"))

# ----------------------------------------------------------------------
# Domande aperte
d(aperta("c02-a-get-post", CAP, "form: invio e codifica",
         "Si descrivano le differenze fra l'invio di un form con il metodo `GET` e con il "
         "metodo `POST`, indicando in quali casi conviene usare l'uno o l'altro.",
         ["`GET`: i dati diventano la query della URL (`?nome=valore&...`), visibile, "
          "salvabile nei segnalibri, registrata in cronologia e nei log.",
          "`POST`: i dati viaggiano nel corpo della richiesta, codificati allo stesso modo "
          "(`application/x-www-form-urlencoded`).",
          "`GET` per operazioni che leggono (ricerche, filtri): è sicura e ripetibile.",
          "`POST` per operazioni che modificano lo stato (registrazioni, acquisti) o per dati "
          "lunghi; nessuno dei due metodi cifra i dati: per questo serve HTTPS."],
         rif=R % "Invio con GET"))

d(aperta("c02-a-semantici", CAP, "tag semantici",
         "Si spieghi perché in HTML conviene usare i **tag semantici** (`header`, `nav`, "
         "`main`, `article`, `footer`, ...) invece di semplici `div`, con un esempio.",
         ["I tag semantici dichiarano il ruolo del contenuto, non il suo aspetto.",
          "Accessibilità: i lettori di schermo permettono di saltare alla navigazione o al "
          "contenuto principale.",
          "Motori di ricerca e altri programmi capiscono meglio la struttura della pagina.",
          "Il codice è più leggibile e manutenibile; l'aspetto resta compito del CSS.",
          "Esempio: `<nav>` con i link del menu, `<main>` con il contenuto, `<footer>` con "
          "contatti e note legali."],
         rif=R % "Tag semantici"))

d(aperta("c02-a-relative", CAP, "URL relative e assolute",
         "Si spieghi la differenza fra URL assolute e URL relative (con e senza barra "
         "iniziale e con i segmenti `.` e `..`), indicando quando conviene usare le une o le "
         "altre.",
         ["Assoluta: contiene schema e host (`https://example.org/a.html`).",
          "Relativa con `/` iniziale: si risolve a partire dalla radice del sito corrente.",
          "Relativa senza `/`: si risolve a partire dalla directory della pagina corrente; "
          "`.` è la directory corrente, `..` la directory padre.",
          "Le relative per le risorse interne (sopravvivono al cambio di host); le assolute per "
          "le risorse esterne."],
         rif=R % "URL relative e assolute"))

d(aperta("c02-a-cache", CAP, "strumenti per sviluppatori",
         "Si spieghi che cos'è la **cache HTTP**, quali vantaggi offre e perché durante lo "
         "sviluppo di un sito può creare problemi.",
         ["Il browser conserva copie delle risorse già scaricate e le riusa invece di "
          "richiederle di nuovo.",
          "Vantaggi: meno richieste e meno dati trasferiti, pagine più veloci, meno carico "
          "sul server.",
          "Il server può indicare per quanto tempo una risorsa è valida; per verificarla il "
          "client può chiedere se è cambiata e ricevere `304 Not Modified`.",
          "In sviluppo si rischia di vedere una versione vecchia di CSS o script: si disattiva "
          "la cache dai DevTools (scheda Rete)."],
         rif=R % "Analisi di rete"))
