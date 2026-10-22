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
  lo stile `bastoncini` le distribuzioni discrete
- i riquadri (`richiamo`, `dimostrazione`, `\info`, `\warning`, `\gbox`) vengono prima misurati: se stanno in una
  pagina passano interi alla pagina successiva invece di spezzarsi. Per questo al loro interno non si mettono `\label`
- disegni ricorrenti: `\venn{riempimenti}{didascalia}` e `\venntre{...}{...}` (diagrammi di Venn con le forme
  `\vennA`, `\vennB`, `\vennOmega`...), `\dado{n}` (faccia di un dado), `\moneta{T}` (una moneta)
- i titoli dei riquadri che contengono una virgola vanno racchiusi in doppie graffe: `\info{{Titolo, con virgola}}{...}`
