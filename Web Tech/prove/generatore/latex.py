"""Composizione del LaTeX: la prova, le soluzioni e la raccolta.

Lo stile riproduce quello delle prove del corso (pdfLaTeX, Linux Libertine
per il testo, Latin Modern Mono per il codice, listings per i riquadri): le
misure sono state prese dai PDF dei facsimile.
"""

import re

from .markup import a_latex
from .modello import disposizione, NESSUNA

LINGUE_LISTINGS = {
    "js": "esJS", "html": "esHTML", "css": "esCSS", "http": "esHTTP", "pug": "esPug",
    "php": "esPHP", "json": "esJSON", "sh": "esSh", "sql": "esSQL", "testo": "esTesto",
}

PREAMBOLO = r"""\documentclass[10pt,a4paper]{article}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage[italian]{babel}
\usepackage{lmodern}
\usepackage[mono=false]{libertine}
\usepackage{textcomp}
\usepackage[a4paper, margin=1cm, includeheadfoot]{geometry}
\usepackage{fancyhdr, enumitem, multicol, xcolor, listings, eso-pic, graphicx, array}

% caratteri usati nei testi che inputenc non conosce
\DeclareUnicodeCharacter{2192}{\ensuremath{\rightarrow}}
\DeclareUnicodeCharacter{2190}{\ensuremath{\leftarrow}}
\DeclareUnicodeCharacter{2194}{\ensuremath{\leftrightarrow}}
\DeclareUnicodeCharacter{21D2}{\ensuremath{\Rightarrow}}
\DeclareUnicodeCharacter{2265}{\ensuremath{\geq}}
\DeclareUnicodeCharacter{2264}{\ensuremath{\leq}}
\DeclareUnicodeCharacter{2260}{\ensuremath{\neq}}
\DeclareUnicodeCharacter{2248}{\ensuremath{\approx}}
\DeclareUnicodeCharacter{2212}{\ensuremath{-}}

% ---- intestazione e piè di pagina ------------------------------------
\pagestyle{fancy}
\fancyhf{}
\lhead{\textbf{@@TITOLO@@}}
\chead{@@CENTRO@@}
\rhead{ID Prova: \textbf{@@ID@@}}
\lfoot{@@PIE_SINISTRA@@}
\cfoot{@@PIE_CENTRO@@}
\rfoot{@@PIE_DESTRA@@}
\renewcommand{\headrulewidth}{0.4pt}
\renewcommand{\footrulewidth}{0.4pt}
\setlength{\parindent}{0pt}

% ---- filigrana --------------------------------------------------------
\AddToShipoutPictureBG{\AtPageCenter{\makebox(0,0){\rotatebox{45}{%
  \fontsize{@@CORPO_FILIGRANA@@}{@@CORPO_FILIGRANA@@}\selectfont
  \textcolor[gray]{0.9}{\textsc{@@FILIGRANA@@}}}}}}

% ---- listati ----------------------------------------------------------
\lstloadaspects{html}
\lstset{keywords={}}
\lstdefinelanguage{esJS}{sensitive=true,
  keywords={break,case,catch,class,const,continue,debugger,default,delete,do,else,export,
    extends,finally,for,function,if,import,in,instanceof,let,new,return,super,switch,this,
    throw,try,typeof,var,void,while,with,yield,async,await,of,static,get,set,true,false,
    null,undefined,then,from,as},
  morestring=[b]", morestring=[b]', morestring=[b]`,
  morecomment=[l]{//}, morecomment=[s]{/*}{*/}}
\lstdefinelanguage{esHTML}{sensitive=false, morestring=[b]", tag=**[s]<>,
  usekeywordsintag=false, markfirstintag=true, morecomment=[s]{<!--}{-->}}
\lstdefinelanguage{esCSS}{sensitive=true, alsoletter={-:@},
  keywords={@@PROPRIETA_CSS@@},
  morestring=[b]", morestring=[b]', morecomment=[s]{/*}{*/}}
\lstdefinelanguage{esHTTP}{sensitive=true}
\lstdefinelanguage{esPug}{sensitive=true, morestring=[b]", morestring=[b]',
  morecomment=[l]{//-}}
\lstdefinelanguage{esPHP}{sensitive=true,
  keywords={echo,if,else,elseif,foreach,for,while,function,return,as,isset,array,print,
    true,false,null,session_start,header},
  morestring=[b]", morestring=[b]', morecomment=[l]{//}, morecomment=[s]{/*}{*/}}
\lstdefinelanguage{esJSON}{sensitive=true, morestring=[b]", keywords={true,false,null}}
\lstdefinelanguage{esSh}{sensitive=true, morestring=[b]", morestring=[b]',
  morecomment=[l]{\#}}
\lstdefinelanguage{esSQL}{sensitive=false,
  keywords={select,from,where,insert,into,values,update,set,delete,create,table,and,or,
    not,null,primary,key,order,by,limit,join,on,as,like},
  morestring=[b]'}
\lstdefinelanguage{esTesto}{}
\lstset{basicstyle=\footnotesize\ttfamily, numbers=left, numberstyle=\footnotesize\ttfamily,
  numbersep=9pt, frame=single, keywordstyle=\color{blue}\bfseries,
  stringstyle=\color{red}\mdseries, commentstyle=\color{black!55}\mdseries,
  tagstyle=\color{blue}\bfseries, showstringspaces=false, upquote=true,
  inputencoding=utf8, extendedchars=true,
  literate={à}{{\`a}}1 {è}{{\`e}}1 {é}{{\'e}}1 {ì}{{\`\i}}1 {ò}{{\`o}}1 {ù}{{\`u}}1
    {À}{{\`A}}1 {È}{{\`E}}1 {É}{{\'E}}1 {Ì}{{\`I}}1 {Ò}{{\`O}}1 {Ù}{{\`U}}1
    {«}{{\guillemotleft}}1 {»}{{\guillemotright}}1 {’}{{\textquoteright}}1
    {…}{{\ldots}}1 {€}{{\texteuro}}1 {→}{{$\rightarrow$}}1 {·}{{\textperiodcentered}}1
    {×}{{\texttimes}}1 {–}{{--}}1 {—}{{---}}1}

% ---- domande e opzioni --------------------------------------------------
\newcommand{\cod}[1]{\texttt{#1}}
% punto in cui il codice in linea può andare a capo, se proprio serve
\newcommand{\codbreak}{\penalty300\relax}
\newcommand{\punti}[1]{\textbf{(#1 punti)}}
\newcommand{\casella}[1]{{\setlength{\fboxsep}{0pt}\setlength{\fboxrule}{0.4pt}%
  \raisebox{1.2pt}{\fbox{\parbox[c][10.9pt][c]{11pt}{\centering\scriptsize #1}}}}}
\newcommand{\casellapiena}[1]{{\setlength{\fboxsep}{0pt}\setlength{\fboxrule}{0.4pt}%
  \raisebox{1.2pt}{\fcolorbox{black}{black}{\parbox[c][10.9pt][c]{11pt}{%
    \centering\scriptsize\bfseries\color{white}#1}}}}}
\setlength{\multicolsep}{5.9pt}
\setlength{\columnsep}{10pt}
\newlist{elencoopzioni}{enumerate}{1}
\setlist[elencoopzioni]{label=\protect\casella{\Alph*}, leftmargin=24.9pt, labelindent=3.1pt,
  labelwidth=11.8pt, labelsep=10pt, align=left, itemsep=1.9pt, parsep=0pt, topsep=0pt,
  partopsep=0pt}
\newenvironment{opzioni}{\begin{multicols}{2}\begin{elencoopzioni}}%
  {\end{elencoopzioni}\end{multicols}}
\newenvironment{opzionilarghe}{\par\vspace{5.9pt}\begin{elencoopzioni}}%
  {\end{elencoopzioni}\par\vspace{5.9pt}}
\newcommand{\giusta}[1]{\stepcounter{elencoopzionii}\item[\casellapiena{#1}]}
\newlist{domande}{enumerate}{1}
\setlist[domande]{label={Es.~\textbf{\arabic*.}}, leftmargin=25pt, labelsep=5pt,
  itemsep=@@DISTANZA_DOMANDE@@, parsep=0pt, topsep=5.8pt}
% ogni domanda sta in una scatola che non si divide fra due pagine
\newenvironment{domanda}{\begin{minipage}[t]{\linewidth}}{\end{minipage}}
% righe per la risposta a una domanda aperta
\newcommand{\righerisposta}[1]{\par\vspace{3.4pt}{\baselineskip=18bp
  \count255=#1 \loop\ifnum\count255>0 \rule{499.9bp}{0.4pt}\par
  \advance\count255 by -1 \repeat}\vspace{-0.3pt}}
% soluzioni
\definecolor{sfondosoluzione}{gray}{0.93}
\newenvironment{soluzione}{\par\vspace{3pt}\small
  \setlength{\fboxsep}{4pt}\begin{lrbox}{\scatolasoluzione}%
  \begin{minipage}{\dimexpr\linewidth-2\fboxsep}\setlength{\parskip}{2pt}}%
  {\end{minipage}\end{lrbox}\colorbox{sfondosoluzione}{\usebox{\scatolasoluzione}}\par
  \vspace{2pt}}
\newsavebox{\scatolasoluzione}
\newcommand{\rif}[1]{\textit{(Dispensa: #1)}}
\newlist{traccia}{itemize}{1}
\setlist[traccia]{label=\textbullet, leftmargin=12pt, itemsep=1pt, parsep=0pt, topsep=2pt}
\newcommand{\capitolo}[1]{\par\vspace{14pt}{\large\bfseries #1}\par\vspace{2pt}\hrule
  \vspace{4pt}}

\begin{document}
% nelle vecchie versioni di babel-italian le virgolette doppie sono un carattere attivo
\makeatletter\@ifundefined{active@char\string"}{}{\shorthandoff{"}}\makeatother
"""

INTESTAZIONE = r"""\textbf{Nome e Cognome:}\hspace{0.8em}\rule{9.5cm}{0.4pt}\hspace{0.75em}\textbf{Matricola:}\hspace{0.8em}\rule{4cm}{0.4pt}

\vspace{6.9pt}
{\setlength{\fboxsep}{5pt}\setlength{\fboxrule}{0.75pt}%
\fcolorbox{black}{white}{\parbox{\dimexpr\linewidth-2\fboxsep-2\fboxrule}{\textbf{Istruzioni:} Il tempo a disposizione per completare la prova è di \textbf{@@MINUTI@@ minuti}. Durante la prova, non è consentito consultare materiale didattico, né interagire con dispositivi elettronici o colleghi. Nel caso di domande a risposta multipla con più risposte corrette, ciascuna risposta corretta indicata vale una corrispondente frazione del punteggio complessivo, mentre le risposte errate comportano una pari penalizzazione. In nessun caso, il punteggio complessivo relativo a una domanda sarà negativo.}}}
"""

_PROPRIETA = re.compile(r"(--[A-Za-z0-9-]+|[A-Za-z-]+):(?=[^{}]*?[;}])")


def proprieta_css(istanze):
    """Le proprietà CSS che compaiono nei listati, da colorare come parole chiave."""
    trovate = set()
    for istanza in istanze:
        for listato in istanza.codice:
            if listato.lingua == "css":
                # il segnaposto finale fa riconoscere anche l'ultima dichiarazione
                trovate.update(m.group(1) + ":"
                               for m in _PROPRIETA.finditer(listato.sorgente + "\n}"))
    return ",".join(sorted(trovate)) or "color:"


def preambolo(istanze, titolo, centro, id_prova, filigrana, pie=None, distanza="14.4pt"):
    pie = pie or ("Università degli Studi di Napoli Federico II",
                  "Corso di Studi in Informatica", "Simulazione non ufficiale")
    # la filigrana occupa la diagonale: più lettere, corpo più piccolo
    corpo = "%dpt" % min(119, int(1070 / max(len(filigrana), 1)))
    sostituzioni = {
        "@@TITOLO@@": titolo, "@@CENTRO@@": centro, "@@ID@@": id_prova,
        "@@PIE_SINISTRA@@": pie[0], "@@PIE_CENTRO@@": pie[1], "@@PIE_DESTRA@@": pie[2],
        "@@FILIGRANA@@": filigrana, "@@CORPO_FILIGRANA@@": corpo,
        "@@PROPRIETA_CSS@@": proprieta_css(istanze), "@@DISTANZA_DOMANDE@@": distanza,
    }
    testo = PREAMBOLO
    for chiave, valore in sostituzioni.items():
        testo = testo.replace(chiave, valore)
    return testo


# ----------------------------------------------------------------------
def _listato(listato, primo=None):
    opzioni = "language=%s" % LINGUE_LISTINGS[listato.lingua]
    primo = listato.primo if primo is None else primo
    if primo != 1:
        opzioni += ", firstnumber=%d" % primo
    return "\\begin{lstlisting}[%s]\n%s\n\\end{lstlisting}" % (opzioni, listato.sorgente)


def _codice(listati):
    if not listati:
        return ""
    frazioni = disposizione(listati)
    if frazioni:
        return ("\\par\\vspace{-8.6pt}\n\\begin{minipage}[t]{%.3f\\linewidth}\n%s\n\\end{minipage}"
                "\\hfill\n\\begin{minipage}[t]{%.3f\\linewidth}\n%s\n\\end{minipage}"
                "\\par\\vspace{-2.3pt}\n" % (frazioni[0], _listato(listati[0]),
                                               frazioni[1], _listato(listati[1])))
    return "\n".join(_listato(l) for l in listati) + "\n"


def _opzioni(istanza, soluzioni):
    ambiente = "opzioni" if istanza.due_colonne() else "opzionilarghe"
    righe = ["\\begin{%s}" % ambiente]
    for i, (testo, corretta) in enumerate(istanza.opzioni):
        if soluzioni and corretta:
            righe.append("\\giusta{%s} %s" % (chr(65 + i), a_latex(testo)))
        else:
            righe.append("\\item %s" % a_latex(testo))
    righe.append("\\end{%s}" % ambiente)
    return "\n".join(righe) + "\n"


def _risposta(istanza):
    """Il riquadro grigio con la risposta e la spiegazione."""
    lettere = istanza.lettere_giuste
    righe = ["\\begin{soluzione}"]
    if istanza.aperta:
        righe.append("\\textbf{Traccia della risposta.}")
        righe.append("\\begin{traccia}")
        righe.extend("\\item %s" % a_latex(punto) for punto in istanza.traccia)
        righe.append("\\end{traccia}")
    else:
        etichetta = "Risposta" if len(lettere) == 1 else "Risposte"
        righe.append("\\textbf{%s: %s.} %s" % (etichetta, ", ".join(lettere),
                                               a_latex(istanza.spiegazione)))
    if istanza.rif:
        righe.append("\\rif{%s}" % a_latex(istanza.rif))
    righe.append("\\end{soluzione}")
    return "\n".join(righe) + "\n"


def domanda_tex(istanza, soluzioni=False):
    righe = ["\\item \\begin{domanda}\\punti{%d} %s" % (istanza.punti, a_latex(istanza.testo))]
    righe.append(_codice(istanza.codice))
    if istanza.dopo:
        righe.append(a_latex(istanza.dopo))
    if istanza.aperta:
        righe.append(_risposta(istanza) if soluzioni else "\\righerisposta{%d}" % istanza.righe)
    else:
        righe.append(_opzioni(istanza, soluzioni))
        if soluzioni:
            righe.append(_risposta(istanza))
    righe.append("\\end{domanda}")
    return "\n".join(r for r in righe if r) + "\n"


def prova_tex(prova, soluzioni=False):
    """Il sorgente LaTeX completo di una prova (o delle sue soluzioni)."""
    istanze = prova.istanze
    centro = "simulazione — soluzioni" if soluzioni else "simulazione"
    parti = [preambolo(istanze, prova.titolo, centro, prova.id_testo,
                       "Soluzioni" if soluzioni else "Simulazione")]
    parti.append(INTESTAZIONE.replace("@@MINUTI@@", str(prova.minuti)))
    parti.append("\\begin{domande}")
    parti.extend(domanda_tex(i, soluzioni) for i in istanze)
    parti.append("\\end{domande}")
    if soluzioni:
        parti.append(_griglia(prova))
    parti.append("\\end{document}\n")
    return "\n".join(parti)


def _griglia(prova):
    chiuse = [i for i in prova.istanze if not i.aperta]
    aperte = [i for i in prova.istanze if i.aperta]
    righe = ["\\vspace{10pt}", "\\begin{minipage}{\\linewidth}",
             "\\textbf{Griglia delle risposte}\\par\\vspace{4pt}",
             "{\\small\\renewcommand{\\arraystretch}{1.15}",
             "\\begin{tabular}{@{}rlll@{}}",
             "\\textbf{Es.} & \\textbf{Risposta} & \\textbf{Capitolo} & \\textbf{Argomento} \\\\ \\hline"]
    for n, istanza in enumerate(prova.istanze, 1):
        risposta = ", ".join(istanza.lettere_giuste) if not istanza.aperta else "aperta"
        righe.append("%d & %s & %d & %s \\\\" % (n, risposta, istanza.cap,
                                                 a_latex(istanza.tema)))
    righe.append("\\end{tabular}}")
    punti_chiuse = sum(i.punti for i in chiuse)
    punti_aperte = sum(i.punti for i in aperte)
    righe.append("\\par\\vspace{6pt}{\\small Punteggio massimo: %d (chiuse) + %d (aperte) = "
                 "\\textbf{%d punti}. Nelle domande con più risposte corrette ogni risposta "
                 "giusta indicata vale una frazione dei punti e ogni risposta sbagliata "
                 "indicata ne toglie altrettanti; il punteggio di una domanda non scende mai "
                 "sotto zero.}" % (punti_chiuse, punti_aperte, punti_chiuse + punti_aperte))
    righe.append("\\end{minipage}")
    return "\n".join(righe) + "\n"


def raccolta_tex(sezioni, sottotitolo):
    """Tutte le domande della banca, per capitolo, con le soluzioni.

    sezioni: lista di (titolo del capitolo, [istanze]).
    """
    istanze = [i for _, gruppo in sezioni for i in gruppo]
    parti = [preambolo(istanze, "Raccolta delle domande di Tecnologie Web", sottotitolo,
                       "banca", "Raccolta", distanza="16pt")]
    prima = True
    for titolo, gruppo in sezioni:
        parti.append("\\capitolo{%s}" % a_latex(titolo))
        parti.append("\\begin{domande}%s" % ("" if prima else "[resume]"))
        parti.extend(domanda_tex(i, soluzioni=True) for i in gruppo)
        parti.append("\\end{domande}")
        prima = False
    parti.append("\\end{document}\n")
    return "\n".join(parti)
