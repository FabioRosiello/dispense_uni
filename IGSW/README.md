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
- `chapters/chapter_7.tex` — UML e il diagramma delle classi (L_05, UML Recap)
- `chapters/chapter_8.tex` — Diagrammi dei package e di sequenza (L_05, UML Recap)
- `chapters/chapter_9.tex` — Altri diagrammi UML: componenti, deployment, stati, attività (L_06)
- `chapters/chapter_10.tex` — Esercizi sui diagrammi di stato, con soluzioni ridisegnate e correzioni (L_06-E)
- `chapters/chapter_11.tex` — System Design e buone pratiche di progettazione: obiettivi di progetto, scomposizione, coesione, accoppiamento, Legge di Demetra, schede CRC (L_09, L_11, L_12)
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
- `esempio` ed `esercizio` sono composti in una scatola: se stanno in una pagina non si
  spezzano mai (passano interi alla pagina successiva)
- nei listati le legature di FiraCode sono disattivate (`\FiraCodeNL`): `!=` e `>=` restano come nel sorgente
- i titoli dei riquadri che contengono una virgola vanno racchiusi in doppie graffe:
  `\info{{Titolo, con virgola}}{...}`
