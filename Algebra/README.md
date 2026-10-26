# Sorgenti della dispensa di Algebra per Informatica

Questa cartella contiene i sorgenti LaTeX di `DispensaAlgebra.pdf`, la dispensa del corso di Algebra per Informatica
da **6 CFU** (canale 3, prof. Mattia Brescia). Segue le prime sei parti del programma ufficiale: **polinomi e grafi
non fanno parte del corso** e non sono trattati.

## Struttura
- `main.tex` — documento principale: carica la classe e il preambolo e include i capitoli
- `preamble/algebra.tex` — aggiunte alla classe: riquadri «Spiegazione», passi numerati, targhette, stili TikZ
  (diagrammi di Hasse, di Venn, a frecce, circuiti) e disegni ricorrenti
- `chapters/chapter_0.tex` — Prefazione: il programma, come leggere la dispensa, il significato dei riquadri
- **Parte I — Logica**
  - `chapters/1. Logica/chapter_1.tex` — Logica proposizionale: alfabeto, sintassi, semantica, tavole di verità,
    tautologie notevoli, XOR, NAND e NOR, completezza di NAND e NOR (generato da `strumenti/chapter_1.tpl.tex`)
  - `chapters/1. Logica/chapter_2.tex` — Logica dei predicati: termini, formule, quantificatori, variabili libere,
    negazione dei quantificatori, quantificatori ristretti
- **Parte II — Teoria degli insiemi**
  - `chapters/2. Insiemi/chapter_3.tex` — Insiemi: assiomi, Russell, operazioni, traduzione delle tautologie,
    diagrammi di Venn (generato da `strumenti/chapter_3.tpl.tex`)
  - `chapters/2. Insiemi/chapter_4.tex` — Coppie ordinate, prodotto cartesiano, corrispondenze
  - `chapters/2. Insiemi/chapter_5.tex` — Funzioni: composizione, iniettive, suriettive, biettive, immagine e
    antiimmagine, sezioni, retrazioni e inversa
- **Parte III — Strutture algebriche**
  - `chapters/3. Strutture algebriche/chapter_6.tex` — Semigruppi, monoidi e gruppi: neutri, inversi, sottostrutture
    (proprietà conservate e non), simmetrie del triangolo, cancellabili, tavole di Cayley, omomorfismi e automorfismi
  - `chapters/3. Strutture algebriche/chapter_7.tex` — Anelli e campi: regole di calcolo, automorfismi, divisori dello
    zero, domini di integrità, corpi e campi, anelli booleani
- **Parte IV — Relazioni binarie**
  - `chapters/4. Relazioni/chapter_8.tex` — Relazioni binarie e di equivalenza: proprietà, duale, congruenza modulo m,
    nucleo, classi, quoziente, teorema di omomorfismo per insiemi, partizioni
  - `chapters/4. Relazioni/chapter_9.tex` — Relazioni d'ordine: ordini larghi e stretti, minimi e minimali, buon
    ordine, applicazioni crescenti, diagrammi di Hasse, minoranti e maggioranti
- **Parte V — Numeri naturali e calcolo combinatorio**
  - `chapters/5. Combinatoria/chapter_10.tex` — Numeri naturali e induzione: equipotenza, infinito, induzione di prima
    e seconda forma, potenze e multipli
  - `chapters/5. Combinatoria/chapter_11.tex` — Insiemi finiti e calcolo combinatorio: ordine, inclusione-esclusione,
    numero di funzioni, iniettive, suriettive e biettive, funzioni caratteristiche, monoidi e anelli finiti
  - `chapters/5. Combinatoria/chapter_12.tex` — Coefficienti binomiali: somma, simmetria, formula ricorsiva,
    triangolo di Tartaglia, formula chiusa, teorema binomiale
- **Parte VI — Aritmetica**
  - `chapters/6. Aritmetica/chapter_13.tex` — Divisibilità in Z: MCD e mcm, divisione euclidea, algoritmo di Euclide,
    Bézout, primi, teorema fondamentale dell'aritmetica, sottogruppi di Z
  - `chapters/6. Aritmetica/chapter_14.tex` — Congruenze e anelli Z_m: classi di resto, congruenze nelle strutture,
    strutture quoziente, quando Z_m è un campo
  - `chapters/6. Aritmetica/chapter_15.tex` — Equazioni diofantee e congruenziali, invertibili di Z_m, periodo
- **Parte VII — Insiemi ordinati, reticoli e algebre di Boole**
  - `chapters/7. Reticoli/chapter_16.tex` — Insiemi ordinati: dualità, minimali negli insiemi finiti, Hasse e
    isomorfismi, ordine indotto da una funzione, estremo inferiore e superiore
  - `chapters/7. Reticoli/chapter_17.tex` — Reticoli: limitati e completi, dualità, parti finite, operazioni
    reticolari, equivalenza tra ordine e operazioni, trirettangolo e pentagonale, sottoreticoli, complementi,
    distributività, criterio di Birkhoff
  - `chapters/7. Reticoli/chapter_18.tex` — Algebre di Boole: reticoli booleani, algebre di Boole e anelli booleani,
    teorema di Stone e conseguenze, funzioni caratteristiche, stringhe di bit e operazioni bit a bit
- `strumenti/` — generatore delle tavole di verità: i capitoli 1 e 3 si modificano nei modelli `*.tpl.tex` e poi si
  rigenerano (vedi `strumenti/LEGGIMI.txt`)
- `Appunti/` — appunti scritti a mano (logica, insiemi, strutture algebriche)
- `unina_doc_class.cls`, `fonts/`, `sources/` — template Unina Docs (lo stesso delle altre dispense)

## Come ricompilare
Serve una distribuzione LaTeX con **LuaLaTeX** (con `tikz-cd`, `needspace` e la libreria TikZ `circuits.logic.US`).

```bash
# solo se si è modificato un modello in strumenti/
python3 strumenti/tavole.py strumenti/chapter_1.tpl.tex "chapters/1. Logica/chapter_1.tex"
python3 strumenti/tavole.py strumenti/chapter_3.tpl.tex "chapters/2. Insiemi/chapter_3.tex"

lualatex -interaction=nonstopmode main.tex    # tre volte, per l'indice e i riferimenti
cp main.pdf DispensaAlgebra.pdf
```

## Convenzioni usate
- **Ordine topologico**: ogni risultato compare dopo tutto ciò da cui dipende; nelle dimostrazioni non ci sono
  riferimenti in avanti (solo nelle osservazioni e negli esempi)
- `\dfn[etichetta]{Titolo}{...}` definizione (rosso, etichetta `def:`) · `\ass[...]{...}{...}` assioma (viola)
- ambienti `Teorema`, `Proposizione`, `Lemma`, `Corollario` con `{Titolo}{etichetta}` (etichette `teo:`, `prop:`,
  `lem:`, `cor:`), sempre dentro `concetto` (che non si spezza tra due pagine) e con il riquadro `prerequisiti`,
  dove `\dip{Tipo}{etichetta}` elenca ciò che serve sapere
- ambiente `dimostrazione`, con un riquadro `caso{Titolo}` per ogni direzione, caso o punto
- ambiente `spiegazione` (verde, con la lampadina): **dopo ogni dimostrazione**, la stessa idea con un diagramma o
  un esempio passo per passo; dentro si usa `passi` per l'elenco con i cerchietti numerati
- targhette: `\senzadim` per i risultati che il programma dà «senza dimostrazione», `\facoltativa` per le
  dimostrazioni in più non richieste
- `esempio{Titolo}` numerato per capitolo · `\info{Titolo}{...}` nota · `\warning{Titolo}{...}` attenzione
- `\Needspace{...}` o `\newpage` prima di una sezione quando il titolo resterebbe da solo in fondo alla pagina
- disegni ricorrenti (in `preamble/algebra.tex`):
  - diagrammi di Hasse: stili `hasse`, `hv`, `hv evid` (arancione, i dati), `hv evid2` (verde, i risultati),
    `hv evid3` (rosso), `hv grigio`, `hlato`, `hlato evid`
  - `\cubotre[...]` (le parti di {1, 2, 3}), `\trirettangolo[...]` e `\pentagonale[...]`, con gli stili dei singoli
    nodi modificabili (ad esempio `\cubotre[k1/.style=hv evid]`)
  - grafi di relazioni: `rv`, `rfreccia`, cappi con `to[rcappio]`; classi colorate con `\blocco{classeA}{...}`
  - diagrammi a frecce delle funzioni: `\diagfreccie[opzioni]{dominio}{elementi}{codominio}{elementi}{frecce i/j}`
  - diagrammi di Venn: `\vennUno`, `\vennDue`, `\vennA`, `\vennB`, `\vennC`, con `\vennduecerchi` e `\venntrecerchi`
  - interruttori (`interr`, `filo`) e porte logiche (`circuit logic US`) nel capitolo 1
