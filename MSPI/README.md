# Sorgenti della dispensa di Metodi Statistici per l'Informazione

Questa cartella contiene i sorgenti LaTeX di `DispensaMSPI.pdf`.

## Struttura
- `main.tex` — documento principale: carica il preambolo e include i capitoli
- `preamble/mspi.tex` — pacchetti, colori, riquadri per la matematica, stili dei grafici
- `chapters/chapter_0.tex` — Prefazione: organizzazione del corso, come è fatta la dispensa, i simboli usati e che
  cosa significano i riquadri
- **Parte I — Probabilità e variabili aleatorie discrete** (primo pacchetto di slide, `Slides_Metodi_statistici_parte_I.pdf`)
  - `chapters/chapter_1.tex` — Esperimenti, eventi e insiemi: spazio campione, eventi, operazioni fra eventi, leggi di
    De Morgan, proprietà associativa e distributive, nomenclatura (slide 4-13)
  - `chapters/chapter_2.tex` — Contare: il calcolo combinatorio: eventi equivalenti, principio fondamentale,
    disposizioni, permutazioni, combinazioni, binomio di Newton, stringhe binarie (slide 14-24)
  - `chapters/chapter_3.tex` — Dalla frequenza alla probabilità: limite della frequenza, spazi equiprobabili, poker,
    dado truccato, proprietà, probabilità condizionata e composta, probabilità totale, indipendenza (slide 25-39)
  - `chapters/chapter_4.tex` — L'approccio assiomatico: algebre e sigma-algebre, assiomi di Kolmogorov, serie
    (richiamo), proprietà dimostrate dagli assiomi, teorema di Bayes, monotonia (slide 40-48)
  - `chapters/chapter_5.tex` — Variabili aleatorie discrete: pmf, notazioni, media campionaria e statistica, binomiale,
    uniforme, Poisson (con il numero e e la Poisson come limite della binomiale) (slide 49-61)
  - `chapters/chapter_6.tex` — Pmf condizionate e funzioni di variabili aleatorie: pmf e medie condizionate,
    probabilità totale per le pmf, funzioni di v.a., teorema fondamentale per il calcolo della media (slide 62-73)
  - `chapters/chapter_7.tex` — Varianza e disuguaglianze: valore quadratico medio, varianza, derivate (richiamo),
    varianza di binomiale, uniforme e Poisson, proprietà, disuguaglianze di Markov e Chebyshev (slide 74-94)
  - `chapters/chapter_8.tex` — Variabili aleatorie multiple: pmf congiunta, marginali, indipendenza, pmf condizionate,
    Bayes, regola della catena, tre bit con bit di parità (slide 95-112)
  - `chapters/chapter_9.tex` — Funzioni di più variabili, covarianza e correlazione: linearità della media, teorema
    della media condizionata, covarianza, coefficiente di correlazione, varianza di una somma (slide 113-133)
- **Parte II — Variabili aleatorie continue, vettori e processi aleatori** (secondo pacchetto di slide,
  `Slides_Metodi_statistici_parte_II.pdf`)
  - `chapters/chapter_10.tex` — Variabili aleatorie continue: densità e distribuzione: spazi campione continui, PDF e
    istogrammi, CDF, media; integrale come area, integrali impropri, teorema fondamentale del calcolo (richiami)
    (slide 2-12)
  - `chapters/chapter_11.tex` — Le variabili aleatorie continue notevoli: gradino e rettangolo, uniforme, esponenziale
    (assenza di memoria), Laplace, Cauchy; integrazione per parti, cambio di variabile, arcotangente, logaritmo
    (richiami) (slide 13-22)
  - `chapters/chapter_12.tex` — PDF condizionate e funzioni di variabili continue: PDF condizionate, probabilità
    totale, funzioni monotone e non monotone, il faro e la Cauchy, metodo dell'inversione, sinusoide con fase a caso,
    conversione A/D (slide 23-41)
  - `chapters/chapter_13.tex` — Media di funzioni e varianza nel continuo: teorema fondamentale, varianze di uniforme
    (rumore di quantizzazione), esponenziale e Laplace, la Cauchy senza momenti, dizionario discreto-continuo
    (slide 42-51)
  - `chapters/chapter_14.tex` — Variabili aleatorie continue multiple: densità congiunta e integrale doppio, marginali,
    indipendenza, densità condizionate, media condizionata, covarianza, CDF congiunta e derivate parziali (slide 52-66)
  - `chapters/chapter_15.tex` — La variabile gaussiana e la funzione Q: integrale di Gauss in coordinate polari, media
    e varianza, gaussiana generica, funzione Q e sue proprietà, regola delle tre sigma, probabilità di errore di una
    trasmissione binaria (slide 67-71)
  - `chapters/chapter_16.tex` — Vettori aleatori e vettori gaussiani: vettori e matrici (richiami), vettore delle medie,
    matrici di correlazione e covarianza, matrice definita non negativa, vettori gaussiani e gaussiana bivariata,
    incorrelazione e indipendenza, trasformazioni lineari (slide 72-86)
  - `chapters/chapter_17.tex` — Processi aleatori: regola della catena per i vettori, processi a tempo discreto,
    stazionarietà del primo e del secondo ordine e in senso stretto, processi indipendenti, Bernoulli e quaternario,
    processi SSL e autocorrelazione, matrici di Toeplitz, media mobile, passeggiata aleatoria (slide 87-106)
- `Slides_Metodi_statistici_parte_*.pdf` — le slide del corso
- `unina_doc_class.cls`, `fonts/`, `sources/` — template Unina Docs (lo stesso delle altre dispense)
- `Images/` — eventuali immagini

## Come ricompilare
Serve una distribuzione LaTeX con **LuaLaTeX** e gli stessi pacchetti delle altre dispense, più
`pgfplots`, `cancel` e `icomma`.

```bash
lualatex -interaction=nonstopmode main.tex    # tre volte, per l'indice e i riferimenti
cp main.pdf DispensaMSPI.pdf
```

## Convenzioni usate
- `\dfn{Titolo}{...}` definizione (rosso) · `\info` nota (verde) · `\warning` errore tipico (giallo) ·
  `\error` avvertimento forte · `\gbox{In sintesi}{colore}{...}` riepilogo di capitolo
- `\teorema[etichetta]{Titolo}{enunciato}` teorema numerato per capitolo (blu); si cita con `\ref{teo:etichetta}`
- ambiente `dimostrazione`: la dimostrazione passo per passo, con `\passo{Titolo}` per ogni passaggio; finisce con ■
- ambiente `richiamo{Titolo}`: spiegazione da zero di uno strumento di matematica (limiti, derivate, integrali,
  sommatorie...), in viola
- ambiente `formula[Nome]`: formula da ricordare, in evidenza
- ambienti `esempio{Titolo}` ed `esercizio{Titolo}` (con `\svolgimento`), numerati per capitolo; se stanno in una
  pagina non si spezzano mai
- grafici con `pgfplots`: lo stile `quaderno` disegna gli assi con le frecce e la virgola decimale all'italiana,
  lo stile `bastoncini` le distribuzioni discrete, lo stile `realizzazione` le realizzazioni dei processi aleatori
  (bastoncini che partono dalla linea dello zero)
- vettori e matrici come nelle slide: `\vett{X}` sottolinea una volta (vettore), `\matr{A}` due volte (matrice)
- i riquadri (`richiamo`, `dimostrazione`, `\info`, `\warning`, `\gbox`) vengono prima misurati: se stanno in una
  pagina passano interi alla pagina successiva invece di spezzarsi. Per questo al loro interno non si mettono `\label`
- disegni ricorrenti: `\venn{riempimenti}{didascalia}` e `\venntre{...}{...}` (diagrammi di Venn con le forme
  `\vennA`, `\vennB`, `\vennOmega`...), `\dado{n}` (faccia di un dado), `\moneta{T}` (una moneta)
- i titoli dei riquadri che contengono una virgola vanno racchiusi in doppie graffe: `\info{{Titolo, con virgola}}{...}`
