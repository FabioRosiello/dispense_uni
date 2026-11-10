"""Capitolo 10: il lato server del Web (limiti delle pagine statiche, CGI,
scripting lato server con PHP, NGINX e PHP-FPM)."""

from generatore import L, aperta, chiusa, famiglia

CAP = 10
R = "cap. 10, «%s»"

DOMANDE = []
d = DOMANDE.append


# ----------------------------------------------------------------------
# Famiglia: come passano i dati fra server e programma CGI
CANALI = [
    ("gli header della richiesta HTTP", "Come **variabili d'ambiente**."),
    ("la *query string* della richiesta", "Come **variabili d'ambiente**."),
    ("il corpo di una richiesta `POST`", "Sullo **standard input** del programma."),
    ("il corpo della risposta HTTP", "È ciò che il programma scrive sullo **standard output**."),
]
SBAGLIATI = ["Come **variabili d'ambiente**.", "Sullo **standard input** del programma.",
             "È ciò che il programma scrive sullo **standard output**.",
             "Come argomenti sulla riga di comando del programma.",
             "In un file temporaneo il cui nome è passato al programma.",
             "Tramite un cookie impostato dal server."]


@famiglia("c10-cgi-canali", CAP, "CGI", varianti=3)
def _canali(rng):
    elemento, giusta = rng.choice(CANALI)
    entrata = "risposta" not in elemento
    domanda = ("Secondo la specifica CGI, come arriva al programma esterno %s?" % elemento
               if entrata else
               "Secondo la specifica CGI, come produce il programma esterno %s?" % elemento)
    return chiusa(
        "c10-cgi-canali", CAP, "CGI", domanda,
        giusta, [s for s in SBAGLIATI if s != giusta],
        spiegazione="La specifica CGI stabilisce come server e programma comunicano: header e "
                    "query string arrivano come variabili d'ambiente, il corpo della richiesta "
                    "sullo standard input; ciò che il programma scrive sullo standard output "
                    "(header, riga vuota, corpo) diventa la risposta.",
        rif=R % "CGI: Common Gateway Interface")


d(_canali)

# ----------------------------------------------------------------------
d(chiusa("c10-statico", CAP, "pagine statiche e dinamiche",
         "Un server serve soltanto i file della sua *document root*. Quali delle seguenti "
         "esigenze **non** si possono soddisfare in questo modo?",
         ["Personalizzare una pagina per l'utente che la richiede.",
          "Registrare un ordine in seguito all'invio di un form.",
          "Gestire milioni di pagine con la stessa struttura senza duplicarla in ogni file."],
         ["Servire un foglio di stile CSS condiviso da tutte le pagine.",
          "Servire immagini e script JavaScript.",
          "Aggiornare il contenuto della pagina nel browser con JavaScript.",
          "Servire la stessa pagina a tutti gli utenti, in HTTPS."],
         multi=True,
         spiegazione="Un server statico restituisce sempre lo stesso documento: niente "
                     "personalizzazione, nessuna azione in seguito a una richiesta, e una "
                     "struttura comune da ripetere in ogni file (per Wikipedia, terabyte di dati "
                     "duplicati e milioni di file da rigenerare per cambiare la barra di "
                     "navigazione). Il dinamismo di JavaScript avviene dentro il browser.",
         rif=R % "I limiti delle web app statiche"))

d(chiusa("c10-cgi", CAP, "CGI",
         "Che cos'è CGI (*Common Gateway Interface*)?",
         "Una specifica che permette a un server web di eseguire programmi esterni per elaborare "
         "le richieste HTTP.",
         ["Un linguaggio di programmazione per scrivere pagine dinamiche.",
          "Un motore di template per generare HTML.",
          "Il protocollo con cui il browser invia i dati dei form.",
          "Un'estensione di JavaScript eseguita sul server.",
          "Un formato binario per le risposte HTTP."],
         spiegazione="CGI (primi anni Novanta) è una specifica di interfaccia: definisce come il "
                     "server passa gli input a un programma esterno, scritto in qualunque "
                     "linguaggio (anche Bash), e come ne raccoglie l'output per costruire la "
                     "risposta.",
         rif=R % "CGI: Common Gateway Interface"))

d(chiusa("c10-cgi-riga-vuota", CAP, "CGI",
         "Lo script CGI seguente stampa una riga vuota dopo l'header `Content-type`. Perché?",
         "Perché la riga vuota separa gli header dal corpo, come in ogni risposta HTTP.",
         ["Per far andare a capo il testo nel browser.",
          "Perché la specifica CGI richiede una riga vuota alla fine dell'output.",
          "Per segnalare al server che lo script è terminato.",
          "Per svuotare il buffer dello standard output.",
          "Non serve: è solo una scelta di stile."],
         codice=L("sh", """
#!/bin/bash
echo "Content-type: text/html; charset=utf-8"
echo ""
echo "<!DOCTYPE html>"
echo "<html><head><title>Hello CGI!</title></head><body>"
echo "<h1>Hello CGI!</h1>"
date +"<p>%d/%m/%Y alle %H:%M:%S</p></body></html>\""""),
         spiegazione="Il programma CGI scrive a mano la risposta: prima gli header, poi una riga "
                     "vuota, poi il corpo. È esattamente la struttura di una risposta HTTP.",
         rif=R % "CGI: Common Gateway Interface"))

d(chiusa("c10-cgi-limiti", CAP, "CGI",
         "Qual è il motivo principale per cui CGI è inefficiente su un sito con molto traffico?",
         "Per ogni richiesta viene creato un nuovo processo, e il costo di avvio supera quello "
         "dell'elaborazione.",
         ["Perché i programmi CGI possono essere scritti solo in Bash.",
          "Perché CGI non può leggere il corpo delle richieste `POST`.",
          "Perché ogni programma CGI deve aprire una nuova connessione TCP con il browser.",
          "Perché CGI trasmette le risposte in formato binario.",
          "Perché le pagine generate con CGI non possono essere messe in cache."],
         spiegazione="Oltre a essere scomodo (HTML prodotto con delle `echo`, query string e "
                     "corpo da analizzare a mano), CGI crea e distrugge un processo per ogni "
                     "richiesta. Le architetture successive tengono invece un pool di processi "
                     "già pronti.",
         rif=R % "CGI: Common Gateway Interface"))

d(chiusa("c10-php", CAP, "scripting lato server",
         "Si consideri la seguente pagina PHP. Che cosa riceve il browser che la richiede?",
         "Solo l'HTML generato: una lista con due `<li>`, senza alcuna traccia del codice PHP.",
         ["Il file così com'è: il codice PHP viene eseguito dal browser.",
          "L'HTML della pagina, con il ciclo `foreach` da eseguire con JavaScript.",
          "Una lista vuota: il ciclo viene eseguito solo dopo il caricamento.",
          "Solo il codice fra `<?php` e `?>`, senza l'HTML.",
          "Un errore, perché il browser non conosce PHP."],
         codice=L("php", """
<ul>
  <?php $array = ["Hello", "PHP"] ?>
  <?php foreach($array as $item): ?>
    <li><?= $item ?></li>
  <?php endforeach; ?>
</ul>"""),
         spiegazione="Il codice fra i delimitatori `<?php ... ?>` viene eseguito **sul server**, e "
                     "il suo output inserito nell'HTML; il testo fuori dai delimitatori resta "
                     "invariato (`<?=` abbrevia `<?php echo`). Al browser arriva HTML puro.",
         rif=R % "PHP"))

d(chiusa("c10-php-parametri", CAP, "scripting lato server",
         "In PHP, come si legge il valore del campo `todo` di un form inviato con il metodo "
         "`POST`?",
         "`$_POST['todo']`",
         ["`$_GET['todo']`", "`$_COOKIE['todo']`", "`$request.body.todo`",
          "`getenv('todo')`", "`$_POST.todo()`"],
         spiegazione="Uno dei vantaggi dello scripting lato server è la pre-elaborazione della "
                     "richiesta: in PHP i parametri sono già negli array associativi `$_GET` e "
                     "`$_POST`, e i cookie in `$_COOKIE`.",
         rif=R % "PHP"))

d(chiusa("c10-fpm", CAP, "scripting lato server",
         "In un'architettura con NGINX e PHP-FPM, quali delle seguenti affermazioni sono "
         "**vere**?",
         ["NGINX inoltra a PHP-FPM, tramite una connessione TCP, le richieste per i file `.php`.",
          "NGINX serve da sé i file statici (immagini, CSS, JavaScript).",
          "I processi di PHP-FPM esistono già e restano vivi fra una richiesta e l'altra.",
          "Se tutti i worker di PHP-FPM sono occupati, le richieste attendono in coda."],
         ["Per ogni richiesta PHP-FPM crea un nuovo processo, come CGI.",
          "PHP-FPM serve anche i file statici, che NGINX non sa gestire.",
          "NGINX esegue direttamente il codice PHP.",
          "Il browser invia le richieste per i file `.php` direttamente a PHP-FPM, sulla porta "
          "9000."],
         multi=True,
         spiegazione="Il salto rispetto a CGI è il **pool** di processi già pronti, riusati fra "
                     "una richiesta e l'altra. NGINX riceve tutte le richieste, serve i file "
                     "statici e inoltra a PHP-FPM (sulla porta TCP 9000) solo quelle per i file "
                     "`.php`; le richieste in eccesso attendono in coda.",
         rif=R % "Un'architettura moderna: NGINX e PHP-FPM"))

# ----------------------------------------------------------------------
# Domande aperte
d(aperta("c10-a-cgi", CAP, "CGI",
         "Che cos'è CGI? Si descriva come un server web e un programma CGI si scambiano i dati "
         "di una richiesta e della risposta, e quali sono i limiti di questo approccio.",
         ["Specifica che permette al server web di eseguire programmi esterni per elaborare le "
          "richieste e generare pagine dinamiche.",
          "Header e query string arrivano al programma come variabili d'ambiente, il corpo "
          "sullo standard input; l'output su standard output (header, riga vuota, corpo) "
          "diventa la risposta.",
          "Limiti: HTML costruito a mano, richiesta da analizzare a mano.",
          "Soprattutto: un nuovo processo per ogni richiesta, il cui costo di avvio domina su "
          "un sito con molto traffico."],
         rif=R % "CGI: Common Gateway Interface"))

d(aperta("c10-a-fpm", CAP, "scripting lato server",
         "Si descriva l'architettura basata su NGINX e PHP-FPM, spiegando in che cosa migliora "
         "l'approccio CGI.",
         ["NGINX riceve tutte le richieste HTTP e serve da sé i file statici.",
          "Le richieste per i file `.php` vengono inoltrate, via TCP (porta 9000), a PHP-FPM.",
          "PHP-FPM mantiene un pool di processi worker già avviati, riusati fra le richieste; "
          "se sono tutti occupati le richieste attendono in coda.",
          "Rispetto a CGI non si crea un processo per richiesta; lo scripting lato server "
          "pre-elabora la richiesta (`$_GET`, `$_POST`, `$_COOKIE`) e mescola codice e HTML."],
         rif=R % "Un'architettura moderna: NGINX e PHP-FPM"))

d(aperta("c10-a-statico", CAP, "pagine statiche e dinamiche",
         "Quali limiti ha un sito composto da sole pagine statiche? Si spieghi, anche con un "
         "esempio, che cosa cambia quando le pagine vengono generate lato server.",
         ["Una pagina statica è un file della *document root*: a ogni richiesta il server "
          "invia sempre lo stesso documento (JavaScript aggiunge dinamismo solo nel browser).",
          "Non si può personalizzare la pagina per l'utente, i contenuti che cambiano spesso "
          "vanno riscritti a mano e non si può *agire* in seguito a una richiesta (per "
          "esempio registrare un ordine).",
          "Con milioni di pagine la struttura comune si ripete in ogni file: per Wikipedia "
          "(circa 60 milioni di pagine) sono circa 9 TB di dati duplicati, e cambiare la barra "
          "di navigazione vorrebbe dire rigenerare tutti i file.",
          "Con la programmazione lato server il server genera la pagina al volo, in base ai "
          "parametri della richiesta e ai dati: la stessa URL può produrre risposte diverse "
          "(CGI, PHP, Node.js)."],
         rif="cap. 10, «I limiti delle web app statiche» e «La programmazione lato server»"))
