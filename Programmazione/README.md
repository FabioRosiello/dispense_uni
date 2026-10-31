# Dispensa di Programmazione

Dispensa in italiano del corso di **Programmazione** (prof. Francesco Isgrò),
Università degli Studi di Napoli Federico II, corso di laurea in Informatica.
Il linguaggio del corso è il **C**.

È pensata per chi **parte da zero**: il primo capitolo guida passo passo
nell'installazione di tutto ciò che serve (Visual Studio Code, il compilatore
gcc, le estensioni) su Windows (con WSL e Ubuntu), macOS e Linux, con le
schermate disegnate; i capitoli successivi seguono l'ordine delle lezioni.

L'obiettivo è **capire, non memorizzare**: ogni regola è accompagnata dal suo
perché, ogni programma è stato compilato ed eseguito e ne è mostrato l'output
reale, e ciò che accade dentro il computer (variabili in memoria, puntatori,
chiamate di funzione, nodi di una lista) è disegnato in uno schema. Dove le
slide contengono una svista, il testo la corregge e lo segnala.

Ogni listato è disegnato come una piccola **finestra di Visual Studio Code** con
il tema scuro: sfondo quasi nero, numeri di riga, colori della sintassi del
tema e, in alto, la scheda del file aperto. Accanto al codice compare il
**terminale** con l'output: i comandi digitati sono in bianco, ciò che si
scrive mentre il programma è in esecuzione è in giallo.

La dispensa contiene **solo i contenuti tecnici** visti a lezione. Le
informazioni organizzative (orari, modalità d'esame, appelli) sono escluse:
restano sulle slide e sui canali del docente.

> **Lavori in corso**: la dispensa viene scritta un capitolo alla volta. I
> capitoli già presenti sono elencati qui sotto.

## Contenuto

| Percorso | Descrizione |
|---|---|
| `main.tex` | Documento principale: copertina, estratto, indice, inclusione dei capitoli |
| `preamble/prog-preamble.tex` | Font, linguaggi per i listati (C, Makefile, shell), finestra di VS Code, terminale, diagrammi di flusso, schemi della memoria, liste collegate, interfaccia di VS Code disegnata |
| `chapters/1. Ambiente di lavoro.tex` | Che cosa serve (editor, compilatore, terminale), Linux/Windows/macOS e WSL, installazione di VS Code, del compilatore (WSL e Ubuntu, strumenti da riga di comando di macOS, `build-essential`), estensioni (C/C++, WSL), la cartella del corso e la finestra di VS Code, il terminale (prompt, percorsi, comandi essenziali), il primo programma (salvare, compilare, eseguire, `./`, messaggi di errore), problemi comuni |
| `chapters/2. Il calcolatore.tex` | Che cos'è la programmazione, schema di von Neumann, CPU e linguaggio macchina (ciclo preleva-decodifica-esegui), l'esempio in assembly dei bit a 1 seguito passo passo, livelli di astrazione (traduzione reale di `c = a + b`), algoritmo e programma, memoria e indirizzi, notazione binaria, numeri negativi (modulo e segno, complemento a due), tipi di dato, gerarchia di memoria, software, avvio e sistema operativo |
| `chapters/3. Dal problema al programma.tex` | Linguaggi di alto livello, interprete e compilatore, bytecode, librerie, compilazione e linking mostrati con `gcc -c`, `nm`, `gcc -E`, `ldd` e `-static`, librerie statiche e dinamiche, proprietà degli algoritmi e risorse (la forza bruta), pseudo-codice e diagrammi di flusso, i tre esempi del corso in C |
| `chapters/4. Programmazione strutturata.tex` | Storia e standard del C, spaghetti code e GOTO, teorema di Böhm-Jacopini, sequenza, selezione a una, due e n vie, iterazione su contatore e su condizione (in testa e in coda) con gli esempi delle lezioni ridisegnati e simulati a mano, combinazione delle strutture, sviluppo top-down, sottoprogrammi, parametri formali e attuali, tipi di istruzione |
| `chapters/5. Primi programmi in C.tex` | Il primo programma riga per riga (preprocessore, `main`, `printf`, `return` e `echo $?`), output e cursore, variabili, dichiarazioni, assegnazione e albero di un'espressione, divisione intera, `#define` e `#include`, header contro libreria (`pow` e `-lm`), Pacific Sea (`const`, `%e`), conversioni di `printf` e `scanf`, operatore `&`, l'esempio echo con i caratteri consumati da ogni conversione, `if`, `if`-`else`, `while`, `+=` e `++`, `for`, `running_sum` (valore di `scanf`, `exit`, input da tastiera con Ctrl+D e redirezione `<` `>`), errori a cascata, funzioni e prototipi (maxmin, dichiarazioni implicite, il `;` di troppo), passaggio per valore |
| `chapters/6. Elementi lessicali.tex` | Token (colorati per categoria), spazi necessari e superflui con i messaggi di gcc, commenti, le 32 parole chiave, identificatori con il diagramma sintattico, precedenza e associatività (alberi delle espressioni, tabella, `%`), incremento e decremento prefissi e postfissi simulati a mano, comportamento indefinito di `a * a++` (risultati diversi con gcc e clang), ridefinizione di `scanf` |
| `unina_doc_class.cls` | Classe di documento (ripresa dalle *Dispense APA*, non modificata) |
| `fonts/` | Font usati dalla classe (Lato, Gobold, FiraCode, IcoMoon, …) |
| `sources/` | Logo dell'ateneo per la copertina |
| `build.ps1` | Script di compilazione |
| `DispensaProgrammazione.pdf` | PDF già compilato |

## Come compilare

Serve **LuaLaTeX** (la classe usa `fontspec` e `luacode`, quindi `pdflatex` non
funziona). Da PowerShell, nella cartella del progetto:

```bash
powershell -ExecutionPolicy Bypass -File build.ps1
```

Su Linux e macOS basta lanciare più volte `lualatex main.tex` nella cartella
del progetto. Servono diverse passate: oltre all'indice e ai riferimenti
incrociati, la dispensa registra nel file `.aux` la posizione di ogni blocco
(da un titolo al successivo) per non spezzare un concetto fra due pagine, e le
posizioni si stabilizzano dopo qualche compilazione.
