# Sorgenti della dispensa di Ingegneria del Software

Questa cartella contiene i sorgenti LaTeX di `DispensaIGSW.pdf` e del cheat sheet `CheatSheetIGSW.pdf`.

## Struttura
- `main.tex` — inclusione dei capitoli della dispensa
- `preamble/igsw.tex` — preambolo comune a dispensa e cheat sheet: pacchetti, colori, stili TikZ dei diagrammi UML, riquadri, listati
- `chapters/chapter_0.tex` — Prefazione
- `chapters/chapter_1.tex` — Introduzione all'Ingegneria del Software (L_01)
- `chapters/chapter_2.tex` — I processi software (L_01)
- `chapters/chapter_3.tex` — Il modello a cascata (L_01)
- `chapters/chapter_4.tex` — La qualità del software (L_01 + appunti L_03)
- `chapters/chapter_5.tex` — Requisiti: elicitazione e analisi (L_05)
- `chapters/chapter_6.tex` — Diagrammi dei casi d'uso (L_04-A)
- `chapters/chapter_7.tex` — UML e il diagramma delle classi (L_05, UML Recap)
- `chapters/chapter_8.tex` — Diagrammi dei package e di sequenza (L_05, UML Recap)
- `chapters/chapter_9.tex` — Altri diagrammi UML: componenti, deployment, stati, attività (L_06)
- `chapters/chapter_10.tex` — System Design e buone pratiche di progettazione: obiettivi di progetto, scomposizione, coesione (tipi e livelli, God Class), accoppiamento, Legge di Demetra, schede CRC (L_09, L_11, L_12)
- `chapters/chapter_11.tex` — Architetture software: definizione, livelli e partizioni, architettura chiusa e aperta, client/server, repository, a livelli, three-tier, multi-tier, SOA (L_13)
- `chapters/chapter_12.tex` — Architetture software moderne: scalabilità e load balancing, disponibilità e fail-over, dati (ACID, replica, sharding, NoSQL e consistenza finale), code di messaggi (anche per più dispositivi dello stesso utente), microservizi e DDD, un caso reale con i suoi anti-pattern (scomposizione, interazione, sicurezza, organizzazione), legge di Conway (L_14, L_15)
- `chapters/chapter_13.tex` — Virtualizzazione e cloud computing: CPU multi-core, data center tradizionale, macchine virtuali e hypervisor, alta disponibilità con SAN, live migration, consolidamento, cloud computing, scalabilità ed elasticità, provisioning dinamico, IaaS/PaaS/SaaS, cloud pubblico, privato e ibrido (Lecture 16)
- `chapters/chapter_14.tex` — Il paradigma REST: API, HTTP (verbi, codici di stato), risorse e rappresentazioni (JSON, XML), progettazione degli URI, risorse annidate, filtri e ordinamenti, autenticazione a token, JWT e funzioni di hash, OpenAPI (Lecture 17)
- `chapters/chapter_15.tex` — I design pattern: definizione, storia (Alexander, GoF), le quattro parti di un pattern, come leggere i disegni della memoria (stack, heap, campi statici), catalogo GoF; pattern creazionali (Singleton, Builder con e senza Director, builder delle librerie Java), strutturali (Adapter di classe e di oggetto, Composite, Decorator e flussi di I/O), comportamentali (Observer, State, Strategy); Dependency Injection e test con oggetti fittizi. Ogni esempio è compilato ed eseguito con Java 21: gli output riportati sono quelli reali (lezione *Software Design: Design Patterns* ed esempi `EsempioSingleton`, `EsempioBuilder`, `EsempioComposite`, `EsempioDecorator`)
- `chapters/chapter_16.tex` — Build automation: che cos'è e perché il codice di build fa parte del programma, script di shell (comandi del prompt di Windows, espansione ritardata, uno script Bash con collaudo e codice di uscita), Python, Make (regole, target come nomi di file, variabili `$@` `$^` `$<`, il grafo delle dipendenze, tabulazioni), Apache Ant (target, `depends`, proprietà, task, `if`/`unless`, il `javac` per Java 1.5 che il JDK 21 rifiuta), Apache Maven (archetipi, struttura del POM, ciclo di vita e fasi, dipendenze e repository locale, pubblicazione con `settings.xml`), Gradle (Groovy e Kotlin DSL, catalogo delle versioni, wrapper, grafo dei task, build incrementale, dipendenze transitive), installabilità e portabilità, GitHub Actions e YAML (un workflow convertito in JSON, la chiave `on` letta come `true`, versioni delle action), DevOps. Tutti gli esempi sono eseguiti davvero (GNU Make 4.3, Ant 1.10.18, Maven 3.9.11, Gradle 8.14.3, Java 21) e gli output sono quelli reali; segnalate cinque sviste delle slide (`$<`, `unless`, `{$variabile}`, fasi e scope di Maven, `application.properties` attribuito a Maven) (lezione *Build Automation*)
- `chapters/chapter_17.tex` — Container: il software che cambia, la «matrice infernale» di stack e ambienti, l'analogia dei container del trasporto merci, vantaggi per sviluppatori e operazioni, macchine virtuali e container (il kernel condiviso, verificato con `uname -r`), Docker (architettura, `hello-world`, immagini a strati, `pull`, `save` e `load`), un servizio Spring Boot dalle slide (POM, Dockerfile, `docker build` e `docker run`, Docker Compose, log con PID 1, `restart: always` messo alla prova), due servizi che si trovano per nome sulla rete di Compose e un servizio interno senza porte pubblicate, l'esempio più complesso delle slide (reti, volumi, gateway) con il suo diagramma di deployment. Tutto eseguito davvero con Docker 29.9 e Compose 5.6, output reali; segnalata una svista delle slide (`mvn build`) (lezione *An Introduction to Containerization for Software Engineers*)
- `chapters/chapter_18.tex` — Controllo delle versioni: perché gestire le versioni e che cosa deve offrire un sistema di controllo delle versioni, CVS e le modifiche perse, i modelli lock/modify/unlock e copy/modify/merge, la risoluzione dei conflitti; Git (architettura distribuita, working copy, index e repository, operazioni locali e remote), un progetto di esempio con due sviluppatori (configurazione, commit, `diff` e `log`, tag, rami e fusioni, un conflitto risolto a mano, un repository remoto *bare*, il push rifiutato e il `pull` con la scelta fra merge e rebase, una pull request), Git e CVS a confronto, GitHub, GitLab e Bitbucket, il lavoro su GitHub (fork, watch, star, issue). Gli esempi sono eseguiti davvero con Git 2.43, con le date dei commit fissate perché gli hash restino riproducibili: gli output sono quelli reali; segnalate alcune imprecisioni delle slide (il nome di Linus Torvalds, chi può fare push e che cosa fa il server, login e password al posto del token) (lezione *Version Control: Git & GitHub*)
- `chapters/chapter_19.tex` — Linee guida e principi dell'interazione uomo-macchina: le otto regole d'oro di Shneiderman e le dieci euristiche di Nielsen e Molich (con la tabella della loro unione e la versione del 1994), dialogo semplice e naturale (legge di Hick), lingua dell'utente, carico sulla memoria, coerenza, feedback (persistenza, tempi di risposta, bias della percezione del lavoro), uscite e azioni reversibili, scorciatoie, messaggi di errore (le quattro regole di Shneiderman, messaggi a più livelli), prevenzione degli errori (slip e mistake), aiuto e documentazione, usabilità universale, dialoghi che arrivano a una conclusione, letture. Le finestre di esempio delle slide sono ridisegnate e tradotte in italiano (lezione *Guidelines and Principles in Human-Computer Interaction*)
- `preamble/listati-vscode.tex` — aspetto dei listati: finestre di VS Code con il tema Dark+, come nella dispensa di Tecnologie Web
- `preamble/nomi_listati.py` — genera `preamble/listati-nomi.tex` e `cheatsheet/listati-nomi.tex`, gli elenchi dei metodi e dei tipi usati nei listati Java della dispensa e del cheat sheet (per colorarli come in VS Code); va rilanciato dopo aver aggiunto esempi
- `unina_doc_class.cls`, `fonts/`, `sources/` — template Unina Docs (da `Materiale/Dispense.rar`)
- `Images/` — immagini tratte dalle slide del corso

### Il cheat sheet (`CheatSheetIGSW.pdf`)
Un riassunto da consultare, come il formulario di MSPI: la notazione UML e i design pattern del corso, presi dalle slide
attraverso i capitoli 6, 7, 8, 9 e 15 della dispensa. Le voci aggiunte per essere pronti ai casi che le slide non
mostrano sono marcate «oltre le slide».
- `cheatsheet.tex` — copertina, indice e inclusione degli argomenti
- `cheatsheet/stile.tex` — stile: argomenti numerati, voci di notazione (`\voce`), casi «dal codice al diagramma» (ambiente
  `caso`: codice Java a sinistra, diagramma e regola a destra), esempi completi dei pattern (ambiente `programma`), carta
  d'identità dei pattern (`\scheda`), riquadri `guida` e `attenzione`, rimandi cliccabili (`\vv`)
- `cheatsheet/introduzione.tex` — come è fatto il cheat sheet
- Parte I, i diagrammi UML: `classi_elementi.tex` (classi, attributi, operazioni, visibilità, molteplicità, ordered e
  nonunique, statici, astratti, interfacce, enumerazioni), `classi_relazioni.tex` (le frecce in un colpo d'occhio,
  associazioni, ruoli, navigazione, aggregazione, composizione, generalizzazione, realizzazione, pallina e presa,
  dipendenze, classi associative, riflessive, qualificate, n-arie, annidate, template), i casi dal codice al diagramma
  `codice_attributi.tex`, `codice_riferimenti.tex`, `codice_collezioni.tex` (array, liste, insiemi, code, mappe,
  `Optional`, matrici, vincoli di quantità), `codice_gerarchie.tex` (extends, implements, enum con campi, generici, classi
  annidate, record, metodi default, eccezioni), `codice_dipendenze.tex` («call», «use», «create», composizione e
  aggregazione nel codice, classe associativa, iniezione delle dipendenze, liste di ascoltatori); poi `casi_uso.tex`,
  `sequenza.tex` (con la tabella dal codice al diagramma di sequenza), `architettura.tex` (package, componenti,
  deployment), `stato.tex`, `attivita.tex` e `scelta_diagramma.tex` (quale diagramma usare)
- Parte II, riconoscere i design pattern: un file per pattern (`pattern_singleton.tex`, `pattern_builder.tex`, ...), con la
  carta d'identità (intento, indizi nel testo, nel codice e nel diagramma, varianti, con che cosa non confonderlo), la
  struttura e un esempio completo con il suo diagramma delle classi
- `cheatsheet/verifica_listati.py` — compila tutti i casi con Java 21, compila ed esegue gli esempi dei pattern e
  confronta l'output con quello stampato; controlla anche che le righe di codice non superino i 52 caratteri (la
  larghezza della colonna del codice)

## Come ricompilare
Serve una distribuzione LaTeX con **LuaLaTeX** (il template usa `fontspec` e `luacode`)
e i pacchetti: `extsizes mdframed zref needspace fancyhdr mathtools fontspec titlesec
etoolbox babel-italian hyphenat parskip listings lstaddons lstfiracode hyperref amsfonts
fdsymbol enumitem tcolorbox tikzfill pdfcol luacode luatexbase pgf pgfopts pgfornament
float tools xurl pdfpages eso-pic l3packages xcolor graphics geometry trimspaces environ
pgfplots booktabs multirow colortbl`.

```bash
python3 preamble/nomi_listati.py              # solo se sono cambiati i listati Java
lualatex -interaction=nonstopmode main.tex    # tre volte, per l'indice e i riferimenti
cp main.pdf DispensaIGSW.pdf

python3 cheatsheet/verifica_listati.py        # il codice del cheat sheet: compilazione ed esecuzione (JDK 21)
lualatex -interaction=nonstopmode cheatsheet.tex   # tre volte
cp cheatsheet.pdf CheatSheetIGSW.pdf
```

## Convenzioni usate
- `\dfn{Titolo}{...}` definizione · `\info` approfondimento · `\warning` attenzione ·
  `\error` avvertimento forte · `\gbox{In sintesi}{colore}{...}` riepilogo di capitolo
- ambiente `esempio` (numerato per capitolo); la dispensa non contiene esercizi
  (l'ambiente `esercizio` resta definito in `main.tex`, ma non è usato)
- `\Needspace{...}` prima di riquadri, esempi e listati per evitare che un
  concetto si spezzi tra due pagine
- gli `esempio` sono composti in una scatola: se stanno in una pagina non si
  spezzano mai (passano interi alla pagina successiva)
- i listati si scrivono come `\begin{lstlisting}[style=java, name=Ordine.java]`: lo stile sceglie colori e icona
  (`java`, `json`, `http`, `shell`, `yaml`, `docker`, `conf`, `xml`, `js`, `c`, `make`, `gradle`, `plain`), il nome compare nella
  scheda in alto; senza `name` la scheda non c'è
- nei listati le legature di FiraCode sono disattivate (`\FiraCodeNL`): `!=` e `>=` restano come nel sorgente
- un listato dentro un riquadro richiede la forma ad ambiente (`\begin{infobox}{{Titolo}} ... \end{infobox}`),
  perché i comandi `\info{...}{...}` non accettano testo verbatim
- i titoli dei riquadri che contengono una virgola vanno racchiusi in doppie graffe:
  `\info{{Titolo, con virgola}}{...}`
- disegni della memoria (Capitolo 15), definiti in `main.tex`:
  `\memblocco[opzioni del bordo]{colore}{nodo}{(x,y)}{larghezza}{intestazione}{campo/valore, ...}` disegna un frame
  dello stack (`swblue`), un oggetto (`swteal`, tratteggiato se irraggiungibile) o i campi statici di una classe
  (`ph3`); `\memrif{nodo-i}` mette il pallino del riferimento nella riga `i` e la coordinata `(nodo-i-p)` da cui parte la
  freccia (stile `memfreccia`); `\memzona[colore]{(nodo)(nodo-fondo)}{Titolo}` racchiude i blocchi in una zona
- negli output dei terminali un apostrofo apre una stringa (colorata): se serve, il listato prende l'opzione
  `deletestring={[b]'}`
- negli output di Git conviene anche `deletekeywords={java}` (altrimenti `java` si colora dentro i nomi dei file, come
  `Contatto.java`) e, se compare un `#`, `deletecomment={[l]\#}`
- finestre di esempio (Capitolo 19), definite all'inizio del capitolo: l'ambiente `finestra[larghezza]{titolo}` disegna
  una finestra di dialogo; dentro si usano `\bottone[colore]{testo}`, `\bottonechiaro{testo}`, `\campo[larghezza]{testo}`,
  `\casella` e `\pulsanti{...}` (i pulsanti allineati a destra); sotto la finestra `\male`, `\bene` e `\benissimo`
  danno il giudizio
