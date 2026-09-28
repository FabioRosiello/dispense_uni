# Sorgenti della dispensa di Ingegneria del Software

Questa cartella contiene i sorgenti LaTeX di `../Dispensa.pdf`.

## Struttura
- `main.tex` — preambolo (colori, stili TikZ, macro) e inclusione dei capitoli
- `chapters/chapter_0.tex` — Prefazione
- `chapters/chapter_1.tex` — Introduzione all'Ingegneria del Software (L_01)
- `chapters/chapter_2.tex` — I processi software (L_01)
- `chapters/chapter_3.tex` — Il modello a cascata (L_01)
- `chapters/chapter_4.tex` — La qualità del software (L_01 + appunti L_03)
- `chapters/chapter_5.tex` — Requisiti: elicitazione e analisi (L_05)
- `chapters/chapter_6.tex` — Diagrammi dei casi d'uso (L_04-A)
- `unina_doc_class.cls`, `fonts/`, `sources/` — template Unina Docs (da `Materiale/Dispense.rar`)
- `Images/` — immagini tratte dalle slide del corso

## Come ricompilare
Serve una distribuzione LaTeX con **LuaLaTeX** (il template usa `fontspec` e `luacode`)
e i pacchetti: `extsizes mdframed zref needspace fancyhdr mathtools fontspec titlesec
etoolbox babel-italian hyphenat parskip listings lstaddons lstfiracode hyperref amsfonts
fdsymbol enumitem tcolorbox tikzfill pdfcol luacode luatexbase pgf pgfopts pgfornament
float tools xurl pdfpages eso-pic l3packages xcolor graphics geometry trimspaces environ
pgfplots booktabs multirow colortbl`.

```bash
lualatex -interaction=nonstopmode main.tex   # due volte, per l'indice
cp main.pdf ../Dispensa.pdf
```

## Convenzioni usate
- `\dfn{Titolo}{...}` definizione · `\info` approfondimento · `\warning` attenzione ·
  `\error` avvertimento forte · `\gbox{In sintesi}{colore}{...}` riepilogo di capitolo
- ambienti `esempio` ed `esercizio` (numerati per capitolo)
- `\Needspace{...}` prima di riquadri, esempi, esercizi e listati per evitare che un
  concetto si spezzi tra due pagine
- i titoli dei riquadri che contengono una virgola vanno racchiusi in doppie graffe:
  `\info{{Titolo, con virgola}}{...}`
