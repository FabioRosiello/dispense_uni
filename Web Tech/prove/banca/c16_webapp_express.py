"""Capitolo 16: una web app con Express (ORM e Sequelize, configurazione con
.env, organizzazione dell'applicazione, autenticazione con un middleware, la
trappola del middleware di un router)."""

from generatore import L, aperta, chiusa, famiglia, risposte_server

CAP = 16
R = "cap. 16, «%s»"

DOMANDE = []
d = DOMANDE.append


# ----------------------------------------------------------------------
# Famiglia: il middleware di un router
TESTA = """import express from "express";

const app = express();
const todoRouter = express.Router();

function richiediLogin(req, res, next) {
  if (req.headers.cookie === "login=si") next();
  else res.redirect("/auth");
}
"""
CODA = """
app.get("/", (req, res) => res.send("Home"));
%s
app.get("/*splat", (req, res) => res.status(404).send("Non trovato"));

app.listen(3000);"""
VARIANTI_ROUTER = [
    ("trappola", 'todoRouter.use(richiediLogin);\n'
                 'todoRouter.get("/todo", (req, res) => res.send("La lista"));',
     "app.use(todoRouter);"),
    ("percorso", 'todoRouter.use("/todo", richiediLogin);\n'
                 'todoRouter.get("/todo", (req, res) => res.send("La lista"));',
     "app.use(todoRouter);"),
    ("prefisso", 'todoRouter.use(richiediLogin);\n'
                 'todoRouter.get("/", (req, res) => res.send("La lista"));',
     'app.use("/todo", todoRouter);'),
    ("rotta", 'todoRouter.get("/todo", richiediLogin, (req, res) => res.send("La lista"));',
     "app.use(todoRouter);"),
]


@famiglia("c16-router", CAP, "autenticazione", varianti=3)
def _router(rng):
    nome, rotte, montaggio = rng.choice(VARIANTI_ROUTER)
    codice = TESTA + rotte + CODA % montaggio
    richieste = ["GET /", "GET /nonesiste", "GET /todo",
                 {"percorso": "/todo", "intestazioni": {"Cookie": "login=si"}}]
    trappola = nome == "trappola"
    giusta = ["200 Home", "302 -> /auth" if trappola else "404 Non trovato", "302 -> /auth",
              "200 La lista"]
    altra = ["200 Home", "404 Non trovato" if trappola else "302 -> /auth", "302 -> /auth",
             "200 La lista"]
    esiti = [altra,
             ["302 -> /auth", "302 -> /auth", "302 -> /auth", "200 La lista"],
             ["200 Home", giusta[1], "404 Non trovato", "200 La lista"],
             ["200 Home", giusta[1], "200 La lista", "200 La lista"],
             ["200 Home", "404 Non trovato", "302 -> /auth", "302 -> /auth"]]
    esiti = [e for i, e in enumerate(esiti) if e != giusta and e not in esiti[:i]]
    rng.shuffle(esiti)
    return risposte_server(
        "c16-router", CAP, "autenticazione", codice, richieste, giusta, esiti,
        applicazione="Express",
        testo="Si consideri la seguente applicazione Express, in ascolto sulla porta 3000. Che "
              "cosa rispondono, nell'ordine, le richieste `GET /`, `GET /nonesiste`, `GET /todo` "
              "e `GET /todo` con l'header `Cookie: login=si`?",
        spiegazione="Un router montato senza percorso (`app.use(todoRouter)`) riceve **tutte** le "
                    "richieste che le rotte precedenti non hanno gestito, e `todoRouter.use(mw)` "
                    "senza percorso applica il middleware a tutte quelle che entrano nel router: "
                    "anche `/nonesiste` verrebbe intercettata e reindirizzata al login invece di "
                    "arrivare al *catch-all*. Il problema sparisce dando un percorso al "
                    "middleware, montando il router sotto un prefisso o applicando il middleware "
                    "rotta per rotta.",
        rif=R % "Una trappola: il middleware di un router")


d(_router)

# ----------------------------------------------------------------------
d(chiusa("c16-orm", CAP, "ORM e Sequelize",
         "Quali delle seguenti affermazioni sulle librerie ORM (*Object-Relational Mapping*) "
         "sono **vere**?",
         ["Mantengono allineate la rappresentazione a oggetti dei dati e quella relazionale del "
          "database.",
          "Permettono di definire in modo dichiarativo come le tabelle sono mappate sugli "
          "oggetti.",
          "Rendono più facile passare da un database supportato a un altro.",
          "Possono introdurre un sovraccarico nelle prestazioni, soprattutto se usate male."],
         ["Eliminano del tutto la necessità di un database.",
          "Funzionano solo con i database che non usano SQL.",
          "Rendono più semplice qualunque operazione rispetto all'SQL scritto a mano.",
          "Impediscono di eseguire interrogazioni con condizioni.",
          "Rendono impossibile cambiare la libreria ORM usata."],
         multi=True,
         spiegazione="Un ORM evita il codice ripetitivo che tiene allineati oggetti e tabelle: "
                     "modelli dichiarativi, schema generato, operazioni CRUD e interrogazioni "
                     "come chiamate di metodo, portabilità fra database. In cambio ci sono una "
                     "curva di apprendimento, operazioni a volte più contorte che in SQL, un "
                     "possibile sovraccarico e il *vendor lock-in* verso l'ORM.",
         rif=R % "Object-Relational Mapping"))

d(chiusa("c16-sync", CAP, "ORM e Sequelize",
         "In Sequelize, che cosa fa `User.sync({ force: true })`?",
         "Elimina la tabella, se esiste, e la ricrea vuota secondo il modello.",
         ["Crea la tabella solo se non esiste, altrimenti non fa nulla.",
          "Controlla colonne e tipi della tabella e la modifica se serve, senza perdere dati.",
          "Forza la scrittura su disco delle modifiche in sospeso.",
          "Sincronizza i dati della tabella con quelli di un altro database.",
          "Ricrea il modello JavaScript a partire dalla tabella esistente."],
         spiegazione="`sync()` crea la tabella se non esiste; `sync({ alter: true })` la adatta "
                     "al modello; `sync({ force: true })` la elimina e la ricrea, cancellando "
                     "tutti i dati: comodo in sviluppo, distruttivo in produzione.",
         rif=R % "Sincronizzazione dei modelli"))

d(chiusa("c16-chiave-esterna", CAP, "ORM e Sequelize",
         "Si considerino i modelli `User` (con chiave primaria `id`) e `Todo`, e le associazioni "
         "`User.hasMany(Todo)` e `Todo.belongsTo(User)`. Che cosa aggiunge Sequelize allo schema?",
         "La colonna `UserId` nella tabella `Todos`, chiave esterna verso `Users`.",
         ["La colonna `TodoId` nella tabella `Users`.",
          "Una tabella di collegamento `UserTodos` con le due chiavi.",
          "Le colonne `UserId` in `Todos` e `TodoId` in `Users`.",
          "Nulla: le associazioni esistono solo negli oggetti JavaScript.",
          "La colonna `userId` nella tabella `Users`."],
         spiegazione="In un'associazione uno-a-molti la chiave esterna sta nella tabella dei "
                     "«molti», e prende il nome del modello riferito seguito da quello della sua "
                     "chiave primaria (`User` + `Id`). Una tabella di collegamento serve solo per "
                     "il molti-a-molti (`belongsToMany` con `through`).",
         rif=R % "Modelli come classi e associazioni"))

d(chiusa("c16-include", CAP, "ORM e Sequelize",
         "Con Sequelize, `Todo.findAll()` restituisce le cose da fare ma non i loro utenti. Come "
         "si ottengono le une con gli altri in un'unica interrogazione?",
         "Con `Todo.findAll({ include: [User] })`, che produce una *join*.",
         ["Con `Todo.findAll({ where: User })`.",
          "Non si può: bisogna chiamare `User.findByPk` per ogni cosa da fare.",
          "Con `Todo.findAll().join(User)`.",
          "Con `Todo.findAll({ force: true })`.",
          "Le associazioni vengono sempre caricate, basta leggere `todo.User`."],
         spiegazione="Per impostazione predefinita le associazioni non vengono caricate: si "
                     "chiedono con `include`, e Sequelize risponde con una `LEFT OUTER JOIN` "
                     "(per questo una cosa da fare senza utente ha `User` nullo).",
         rif=R % "Caricare le associazioni, cercare per chiave"))

d(chiusa("c16-parametri", CAP, "ORM e Sequelize",
         "Nei log di Sequelize gli `INSERT` contengono segnaposto come `VALUES ($1,$2,NULL,$3,$4)` "
         "invece dei valori. Perché?",
         "Sono query parametriche: i dati viaggiano separati dall'SQL, e questo protegge dalla "
         "*SQL injection*.",
         ["Perché Sequelize nasconde i dati sensibili nei log.",
          "Perché i valori non sono ancora stati inseriti nel database.",
          "Perché SQLite non accetta valori scritti dentro l'SQL.",
          "Perché i valori sono cifrati prima di essere salvati.",
          "Perché l'`INSERT` viene eseguito più tardi, in un'unica transazione."],
         spiegazione="Con le query parametriche il database riceve separatamente l'istruzione e i "
                     "dati: un valore inserito dall'utente non può mai diventare parte del "
                     "comando SQL. `NULL` è l'`id`, scelto dal database grazie ad "
                     "`AUTOINCREMENT`.",
         rif=R % "Creare entità"))

d(chiusa("c16-env", CAP, "configurazione",
         "Quali delle seguenti pratiche sulla configurazione di un'applicazione sono corrette?",
         ["Tenere credenziali e impostazioni dell'ambiente in un file `.env`, letto all'avvio "
          "(per esempio con `dotenv`, che le copia in `process.env`).",
          "Aggiungere il file `.env` al `.gitignore`, e versionare al suo posto una versione "
          "fittizia da copiare e modificare.",
          "Usare file diversi per ambienti diversi, per esempio sviluppo e produzione."],
         ["Scrivere le credenziali nel codice e rimuoverle prima di pubblicare il repository.",
          "Versionare il file `.env` con le password, così il gruppo le condivide.",
          "Lasciare che `dotenv` sovrascriva le variabili d'ambiente già definite dal sistema.",
          "Duplicare l'applicazione in una versione di sviluppo e una di produzione."],
         multi=True,
         spiegazione="Le impostazioni sensibili o specifiche dell'ambiente vanno in un unico file "
                     "di configurazione non versionato (una chiave finita in un commit resta "
                     "nella cronologia anche se poi viene rimossa). `dotenv` non sovrascrive le "
                     "variabili già definite: così in produzione il sistema può imporre le "
                     "proprie.",
         rif=R % "Configurazione"))

d(chiusa("c16-organizzazione", CAP, "organizzazione dell'app",
         "Nell'organizzazione dell'applicazione Express adottata nel corso, che cosa contiene la "
         "cartella `controllers`?",
         "Il codice che implementa la logica di business per gestire le richieste.",
         ["I template Pug delle pagine.",
          "La definizione dei router, che indirizzano le richieste.",
          "I file statici: CSS, immagini, script.",
          "I middleware personalizzati, come quello di autenticazione.",
          "I modelli dei dati e la connessione al database."],
         spiegazione="La struttura è: `views` (template), `routes` (router che indirizzano le "
                     "richieste verso il controller giusto), `controllers` (logica di business), "
                     "`models` (modelli e database), `middleware` (middleware personalizzati), "
                     "`public` (file statici), e `index.js` come punto d'ingresso. Express è "
                     "unopinionated: è una scelta, non una regola.",
         rif=R % "Organizzare un'applicazione Express"))

d(chiusa("c16-ordine-middleware", CAP, "organizzazione dell'app",
         "Un'applicazione usa `express-session` e `connect-flash`, che salva i messaggi nella "
         "sessione. In che ordine vanno registrati i middleware?",
         "Prima `app.use(session(...))`, poi `app.use(flash())`.",
         ["Prima `app.use(flash())`, poi `app.use(session(...))`.",
          "L'ordine non conta: Express li ordina da sé.",
          "`flash()` va registrato dopo tutte le rotte.",
          "`session(...)` va registrato dopo il gestore degli errori.",
          "Vanno registrati nello stesso `app.use`, in qualunque ordine."],
         spiegazione="I middleware vengono eseguiti nell'ordine di dichiarazione: la sessione "
                     "deve essere già stabilita quando i middleware che la usano (i messaggi "
                     "flash, quelli che ne copiano lo stato in `res.locals`) vengono eseguiti.",
         rif=R % "Configurazione dei middleware"))

d(chiusa("c16-password", CAP, "autenticazione",
         "Come vanno memorizzate le password degli utenti nel database di un'applicazione reale?",
         "Come hash calcolato con una funzione lenta e con *salt* (bcrypt, scrypt, Argon2); al "
         "login si confronta l'hash.",
         ["In chiaro, così si possono confrontare direttamente al login.",
          "Cifrate con una chiave scritta nel codice dell'applicazione.",
          "Codificate in Base64.",
          "Nella sessione dell'utente, invece che nel database.",
          "In un cookie firmato, sul client."],
         spiegazione="Confrontare direttamente la password (come nell'esempio del corso) vuol "
                     "dire memorizzarla in chiaro: chi ottiene il database ottiene tutte le "
                     "password. Una funzione di hash lenta e con salt rende costoso risalire alle "
                     "password originali.",
         rif=R % "Autenticazione"))

d(chiusa("c16-post", CAP, "autenticazione",
         "Nella lista di cose da fare con Express, segnare un elemento come fatto, modificarlo o "
         "eliminarlo avviene con un form `POST`, seguito da un reindirizzamento. Perché?",
         "Perché una `GET` non deve avere effetti (browser, proxy e motori di ricerca la "
         "ripetono o la anticipano), e il reindirizzamento evita di reinviare il form "
         "ricaricando la pagina (*Post/Redirect/Get*).",
         ["Perché i link non possono contenere l'identificativo dell'elemento.",
          "Perché Express non supporta le rotte con il metodo `GET`.",
          "Perché una `POST` è più veloce di una `GET`.",
          "Perché i messaggi flash funzionano solo con le `POST`.",
          "Perché il reindirizzamento cifra i dati del form."],
         spiegazione="Le azioni che modificano i dati usano metodi non sicuri. Dopo la `POST` il "
                     "server risponde `302` verso la lista: il browser la chiede con una `GET` "
                     "innocua, che si può ricaricare quante volte si vuole.",
         rif=R % "Configurazione dei middleware"))

# ----------------------------------------------------------------------
# Domande aperte
d(aperta("c16-a-orm", CAP, "ORM e Sequelize",
         "Che cos'è un ORM e quali problemi risolve? Si descriva, con Sequelize, come si "
         "definiscono i modelli e le associazioni, e si discutano pro e contro di questo "
         "approccio.",
         ["Gli stessi dati hanno due rappresentazioni (oggetti nello heap, righe nelle "
          "tabelle) da tenere allineate: un ORM lo fa con modelli dichiarativi, schema "
          "generato, CRUD e interrogazioni come metodi.",
          "Sequelize: `database.define(...)` o classi che estendono `Model` con `init`; tipi e "
          "vincoli (`allowNull`, `primaryKey`, `autoIncrement`); `sync()` allinea lo schema.",
          "Associazioni: `hasOne`, `belongsTo`, `hasMany`, `belongsToMany` (con `through`); "
          "nell'uno-a-molti la chiave esterna (es. `UserId`) sta nella tabella dei «molti».",
          "Pro: astrazione, produttività, portabilità, leggibilità. Contro: curva di "
          "apprendimento, operazioni complesse più contorte, *vendor lock-in*, prestazioni."],
         rif=R % "Object-Relational Mapping"))

d(aperta("c16-a-auth", CAP, "autenticazione",
         "Si descriva come realizzare l'autenticazione in un'applicazione Express con le "
         "sessioni e un middleware, e si spieghi il problema che nasce applicando il middleware "
         "con `router.use` a un router montato senza percorso.",
         ["Al login (`POST`) il controller verifica le credenziali (password come hash) e "
          "scrive nella sessione `isAuthenticated` e il nome utente; il logout distrugge la "
          "sessione.",
          "Un middleware controlla la sessione e reindirizza al login (con un messaggio flash) "
          "chi non è autenticato, altrimenti chiama `next()`: un solo punto invece di un "
          "controllo in ogni controller.",
          "Si applica a tutte le rotte di un router (`router.use(mw)`) o a una sola rotta "
          "(`router.post(\"/reset\", mw, gestore)`).",
          "Trappola: con `app.use(router)` e `router.use(mw)` senza percorso il middleware "
          "intercetta tutte le richieste non gestite prima (anche quelle per percorsi "
          "inesistenti, che non arrivano mai al 404); rimedio: `router.use(\"/todo\", mw)` o "
          "`app.use(\"/todo\", router)`."],
         rif="cap. 16, «Autenticazione» e «Una trappola: il middleware di un router»"))

d(aperta("c16-a-configurazione", CAP, "configurazione",
         "Dove vanno impostazioni come le credenziali del database o le chiavi API di "
         "un'applicazione Express? Si spieghi perché non vanno scritte nel codice e come si "
         "gestiscono con un file `.env` e il pacchetto `dotenv`.",
         ["Sono dati sensibili (password, chiavi API) o legati all'ambiente (URL del database "
          "di sviluppo o di produzione, livello di log).",
          "Nel codice finirebbero nel repository (una chiave committata resta nella cronologia "
          "anche dopo la rimozione), cambiarle richiederebbe di modificare più file e "
          "servirebbero versioni diverse dell'app per ogni ambiente.",
          "Vanno in un file di configurazione, unico punto in cui si cambiano: il `.env` nella "
          "radice del progetto, **non** versionato (`.gitignore`); si versiona invece una "
          "copia fittizia (es. `.env.dummy`) da copiare e completare.",
          "`import \"dotenv/config\"` legge il file all'avvio e ne copia i valori in "
          "`process.env`; le variabili d'ambiente già definite hanno la precedenza, così in "
          "produzione il sistema può imporre le proprie."],
         rif=R % "Configurazione"))
