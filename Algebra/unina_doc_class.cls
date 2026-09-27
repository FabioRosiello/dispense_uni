\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{unina_doc_class}[2023/09/14 Unina Doc Class]
\LoadClass[10pt,twoside]{extreport}

% Requirements

% Requirements
\RequirePackage[svgnames]{xcolor}
\RequirePackage{mdframed}                             % usato nei capitoli
\RequirePackage{graphicx}
\RequirePackage{geometry}
\RequirePackage{tikz}
\RequirePackage{afterpage}
\RequirePackage{fancyhdr}
\RequirePackage{mathtools}
\RequirePackage[no-math]{fontspec}
\RequirePackage[explicit]{titlesec}
\RequirePackage{titletoc}
\RequirePackage{etoolbox}
\RequirePackage[italian]{babel}
\RequirePackage{hyphenat}
\RequirePackage{parskip}
\RequirePackage{listings, lstautogobble, lstfiracode} % usato nel .cls
\RequirePackage[hidelinks]{hyperref}
\RequirePackage{amsmath, amssymb, fdsymbol}
\RequirePackage{enumitem}
\RequirePackage{calc}
\RequirePackage[most, many, breakable]{tcolorbox}     % usato nel .cls
\RequirePackage{luacode}
\RequirePackage{xparse}
\RequirePackage[object=vectorian]{pgfornament}        % usato nel .cls
\RequirePackage{float}                                % usato nei capitoli
\RequirePackage{tabularx}                             % usato nei capitoli
\RequirePackage{xurl}                                 % usato nei capitoli
\RequirePackage{ifthen}                               % usato nei capitoli
\RequirePackage{pdfpages}

\usetikzlibrary{arrows.meta, matrix, positioning, decorations.pathreplacing, fit, backgrounds, trees, positioning, shapes.geometric, calc}

\makeatletter
\titlecontents{part}
    [0pt]                               % Rientro sinistro
    {\addvspace{1cm}\centering}          % Spazio verticale e allineamento
    {\color{primary!60!black}\fontsize{16}{0}\selectfont\Gobold Parte \thecontentslabel\quad} % Etichetta (es. Parte I)
    {\color{primary!60!black}\fontsize{16}{0}\selectfont\Gobold} % Formattazione per parti senza numero
    {\hfill\color{primary!80!black}\bfseries\Scientifica\fontsize{14}{0}\selectfont\contentspage} % Numero pagina
    [\addvspace{0.3cm}\hrule height 1.5pt\addvspace{0.5cm}] % Linea decorativa sotto
\makeatother

% Macros
\newcommand\blankpage{\null\thispagestyle{empty}\addtocounter{page}{-1}\newpage}

% Define colors
\definecolor{orange}{HTML}{FF9507}
\definecolor{blue}{HTML}{179AFF}
\definecolor{sapphire}{HTML}{2B50AA}
\definecolor{cherryred}{HTML}{FF004D}
\definecolor{turquoise}{HTML}{00F5CC}
\definecolor{seagreen}{HTML}{22AAA1}
\definecolor{green}{HTML}{17FF7C}
\definecolor{red}{HTML}{FF3E4B}
\definecolor{yellow}{HTML}{DBED00}
\definecolor{naplesyellow}{HTML}{FFDF64}
\definecolor{violet}{HTML}{47007D}
\definecolor{pink}{HTML}{FF69B4}
\definecolor{neutral}{HTML}{888888}

% Azure
\definecolor{azure-gradient-1}{HTML}{B1E7E1}
\definecolor{azure-gradient-2}{HTML}{A1E2DB}
\definecolor{azure-gradient-3}{HTML}{92DDD6}
\definecolor{azure-gradient-4}{HTML}{83D8CF}
\definecolor{azure-gradient-5}{HTML}{73D3C9}
\definecolor{azure-gradient-6}{HTML}{64CEC3}

% Pink
\definecolor{pink-gradient-1}{HTML}{ECD7D5}
\definecolor{pink-gradient-2}{HTML}{E6C9C7}
\definecolor{pink-gradient-3}{HTML}{DFBBB9}
\definecolor{pink-gradient-4}{HTML}{D8ADAB}
\definecolor{pink-gradient-5}{HTML}{D2A09D}
\definecolor{pink-gradient-6}{HTML}{CC928F}

% Purple
\definecolor{purple-gradient-1}{HTML}{C5C2EB}
\definecolor{purple-gradient-2}{HTML}{B5B2E6}
\definecolor{purple-gradient-3}{HTML}{A6A3E1}
\definecolor{purple-gradient-4}{HTML}{9793DC}
\definecolor{purple-gradient-5}{HTML}{8884D7}
\definecolor{purple-gradient-6}{HTML}{7974D2}

% Yellow
\definecolor{yellow-gradient-1}{HTML}{EDE8AB}
\definecolor{yellow-gradient-2}{HTML}{EAE39A}
\definecolor{yellow-gradient-3}{HTML}{EAE39A}
\definecolor{yellow-gradient-4}{HTML}{E3DA78}
\definecolor{yellow-gradient-5}{HTML}{E0D667}
\definecolor{yellow-gradient-6}{HTML}{DCD156}

% Red
\definecolor{red-gradient-1}{HTML}{FF7073}
\definecolor{red-gradient-2}{HTML}{FF5C5F}
\definecolor{red-gradient-3}{HTML}{FF474A}
\definecolor{red-gradient-4}{HTML}{FF3336}
\definecolor{red-gradient-5}{HTML}{FF1F22}
\definecolor{red-gradient-6}{HTML}{FF0A0E}

% Orange
\definecolor{orange-gradient-1}{HTML}{FABE75}
\definecolor{orange-gradient-2}{HTML}{F9B562}
\definecolor{orange-gradient-3}{HTML}{F9AC4E}
\definecolor{orange-gradient-4}{HTML}{F8A23A}
\definecolor{orange-gradient-5}{HTML}{F79926}
\definecolor{orange-gradient-6}{HTML}{F69013}

% Brown
\definecolor{brown-gradient-1}{HTML}{BCA576}
\definecolor{brown-gradient-2}{HTML}{B59C69}
\definecolor{brown-gradient-3}{HTML}{AE925B}
\definecolor{brown-gradient-4}{HTML}{A48851}
\definecolor{brown-gradient-5}{HTML}{967D4A}
\definecolor{brown-gradient-6}{HTML}{897243}

% Green
\definecolor{green-gradient-1}{HTML}{D4E5B3}
\definecolor{green-gradient-2}{HTML}{CCE0A4}
\definecolor{green-gradient-3}{HTML}{C3DB95}
\definecolor{green-gradient-4}{HTML}{B9D585}
\definecolor{green-gradient-5}{HTML}{B1D076}
\definecolor{green-gradient-6}{HTML}{A8CB67}

% Color palette
\colorlet{primary}{sapphire}
\colorlet{accent}{violet}


% Icon definitions

\makeatletter
        \newfontfamily\IcoMoon{IcoMoon}[
                Path = fonts/,
                Extension = .ttf,
                UprightFont = *,
        ]

        \def\inumber{{\IcoMoon\char"E918}}
        \def\inumbernegative{{\IcoMoon\char"E919}}
        \def\itick{{\IcoMoon\char"E915}}
        \def\icross{{\IcoMoon\char"E916}}
        \def\ihome{{\IcoMoon\char"E914}}
        \def\ifolder{{\IcoMoon\char"E92F}}
        \def\iquotel{{\IcoMoon\char"E977}}
        \def\iquoter{{\IcoMoon\char"E978}}
        \def\iwrench{{\IcoMoon\char"E991}}
        \def\ieqh{{\IcoMoon\char"E992}}
        \def\ieqv{{\IcoMoon\char"E993}}
        \def\icog{{\IcoMoon\char"E994}}
        \def\icogs{{\IcoMoon\char"E995}}
        \def\istats{{\IcoMoon\char"E99B}}
        \def\iwinnerflag{{\IcoMoon\char"E9CC}}
        \def\iwarning{{\IcoMoon\char"EA07}}
        \def\inotification{{\IcoMoon\char"EA08}}
        \def\iquestion{{\IcoMoon\char"EA09}}
        \def\iinfo{{\IcoMoon\char"EA0C}}
        \def\icancel{{\IcoMoon\char"EA0D}}
        \def\ialphaaasc{{\IcoMoon\char"EA48}}
        \def\ialphaddesc{{\IcoMoon\char"EA49}}
        \def\inumberasc{{\IcoMoon\char"EA4A}}
        \def\inumberdesc{{\IcoMoon\char"EA4B}}
        \def\iorderasc{{\IcoMoon\char"EA4C}}
        \def\iorderdesc{{\IcoMoon\char"EA4D}}
        \def\iboxdone{{\IcoMoon\char"EA52}}
        \def\iboxundone{{\IcoMoon\char"EA53}}
        \def\iradiodone{{\IcoMoon\char"EA54}}
        \def\iradiodonenegative{{\IcoMoon\char"EA55}}
        \def\iradioundone{{\IcoMoon\char"EA56}}
        \def\isuperscript{{\IcoMoon\char"EA69}}
        \def\icodeopentag{{\IcoMoon\char"EA7F}}
        \def\icodeclosetag{{\IcoMoon\char"EA80}}
        \def\iterminal{{\IcoMoon\char"EA81}}
        \def\imail{{\IcoMoon\char"E900}}
        \def\iwindow{{\IcoMoon\char"E906}}
        \def\icpu{{\IcoMoon\char"E907}}
        \def\ieye{{\IcoMoon\char"E908}}
        \def\icomplexcox{{\IcoMoon\char"E901}}
        \def\ibug{{\IcoMoon\char"E902}}
        \def\iattachment{{\IcoMoon\char"E909}}
        \def\ilabel{{\IcoMoon\char"E90A}}
        \def\ibookmark{{\IcoMoon\char"E90B}}
        \def\ibadge{{\IcoMoon\char"E90C}}
        \def\iuser{{\IcoMoon\char"E903}}
        \def\ibusinessman{{\IcoMoon\char"E904}}
        \def\ibusinesswoman{{\IcoMoon\char"E905}}
        \def\iidea{{\IcoMoon\char"E90D}}
        \def\isettings{{\IcoMoon\char"E90E}}
        \def\ifatinfo{{\IcoMoon\char"E90F}}
        \def\iclock{{\IcoMoon\char"E910}}
        \def\itimer{{\IcoMoon\char"E911}}
        \def\iflag{{\IcoMoon\char"E912}}
        \def\iwinnercup{{\IcoMoon\char"E913}}
        \def\igraduate{{\IcoMoon\char"E917}}
        \def\igithub{{\IcoMoon\char"EAB0}}


        \newfontfamily\IcoFont{IcoFont}[
                Path = fonts/,
                Extension = .ttf,
                UprightFont = *,
        ]

        \def\imail{{\IcoFont\char"EF12}}
        \def\igraduate{{\IcoFont\char"EADB}}
        \def\iid{{\IcoFont\char"EF4A}}
        \def\isettings{{\IcoFont\char"EFE1}}
        \def\isettingsalt{{\IcoFont\char"EC83}}
        \def\iterminalalt{{\IcoFont\char"F00A}}
        \def\iauto{{\IcoFont\char"EEA9}}
        \def\ifile{{\IcoFont\char"EB08}}
        \def\ifilecode{{\IcoFont\char"EB0C}}
        \def\ibook{{\IcoFont\char"EAD1}}
        \def\ibookmark{{\IcoFont\char"EEC0}}
        \makeatother
        % Define fonts
        \makeatletter
        \newfontfamily\Lato{Lato}[
                Path = fonts/,
                Extension = .ttf,
                UprightFont = *-Regular,
                BoldFont = *-Bold,
                ItalicFont = *-Italic,
                BoldItalicFont = *-BoldItalic
        ]

        \newfontfamily\Scientifica{scientifica}[
                Path = fonts/,
                Extension = .ttf,
                UprightFont = *,
                BoldFont = *Bold,
                ItalicFont = *Italic,
        ]

        \newfontfamily\FiraCode{FiraCode}[
                Path = fonts/,
                Extension = .ttf,
                UprightFont = *-Regular,
                BoldFont = *-Bold,
                Contextuals=Alternate
        ]

        \newfontfamily\LatoThin{Lato-Thin}[
                Path = fonts/,
                Extension = .ttf,
                UprightFont = *,
                ItalicFont = *Italic,
        ]

        \newfontfamily\LatoLight{Lato-Light}[
                Path = fonts/,
                Extension = .ttf,
                UprightFont = *,
                ItalicFont = *Italic,
        ]

        \newfontfamily\LatoBlack{Lato-Black}[
                Path = fonts/,
                Extension = .ttf,
                UprightFont = *,
                ItalicFont = *Italic,
        ]

        \newfontfamily\Karla{Karla}[
                Path = fonts/,
                Extension = .ttf,
                UprightFont = *-Regular,
                BoldFont = *-Bold,
                ItalicFont = *-Italic,
                BoldItalicFont = *-BoldItalic
        ]

        \newfontfamily\Agency{Agency}[
                Path = fonts/,
                Extension = .ttf,
                UprightFont = *,
        ]

        \newfontfamily\Alte{Alte DIN 1451 Mittelschrift}[
                Path = fonts/,
                Extension = .ttf,
                UprightFont = *,
                BoldFont=*,
                ItalicFont=*,
                BoldItalicFont=*,
                BoldFeatures={FakeBold=2},
                ItalicFeatures={FakeSlant=0.25},
                BoldItalicFeatures={FakeBold=2, FakeSlant=0.25},
        ]

        \newfontfamily\AlteG{Alte DIN 1451 Mittelschrift G}[
                Path = fonts/,
                Extension = .ttf,
                UprightFont = *,
                BoldFont=*,
                ItalicFont=*,
                BoldItalicFont=*,
                BoldFeatures={FakeBold=2},
                ItalicFeatures={FakeSlant=0.25},
                BoldItalicFeatures={FakeBold=2, FakeSlant=0.25},
        ]

        \newfontfamily\Gobold{Gobold}[
                Path = fonts/,
                Extension = .otf,
                UprightFont = *-Regular,
                BoldFont=*-Bold,
                ItalicFont=*-Italic,
                BoldItalicFont=*-BoldItalic,
        ]

        \newfontfamily\GoboldHollow{GoboldHollow}[
                Path = fonts/,
                Extension = .otf,
                UprightFont = *-Regular,
                BoldFont=*-Bold,
                ItalicFont=*-Italic,
                BoldItalicFont=*-BoldItalic,
        ]
\makeatother

%% Document Style
\makeatletter
        %% Global
        \setlength\parindent{0pt}
        \setlength\parskip{0.75em}
        \setlength{\headsep}{2cm}

        %% Define no Par Skip
        \let\svpar\par
        \edef\svparskip{\the\parskip}
        \def\revertpar{\svpar\setlength\parskip{\svparskip}\let\par\svpar}
        \def\noparskip{\leavevmode\setlength\parskip{0pt}\def\par{\svpar\let\par\revertpar}}

        %% Chapter
        \setcounter{chapter}{-1}
        \def\currentchapter{}
        \titlespacing*{\chapter}{0pt}{-10pt}{30pt}

        \titleformat{\chapter}[frame]
                {\setlength{\fboxrule}{5pt}\color{primary!85!black}}
                {\hspace{0.25cm}\fontsize{160}{0}\selectfont\AlteG \textcolor{primary!20!white}{\ibookmark}\hspace{0.25cm}}
                {1cm}
                {\color{primary}\fontsize{30}{42}\selectfont\Gobold\centering #1\global\def\currentchapter{#1}}
                %{\color{primary}\fontsize{30}{42}\selectfont\Gobold\centering\chaptertitlename: #1\global\def\currentchapter{#1}}

        \titleformat{name=\chapter,numberless}[frame]
                {\setlength{\fboxrule}{5pt}\color{primary!85!black}}
                {}
                {1cm}
                {\color{primary}\fontsize{30}{42}\selectfont\Gobold\centering #1\global\def\currentchapter{#1}}

        %% Table of Contents
        \titlecontents*{chapter}
                [0pt]
                {\addvspace{0.5cm}}
                {\color{primary!60!black}\fontsize{12}{0}\selectfont\Gobold\thecontentslabel\hspace{0.125cm}\color{primary}}
                {}
                {\color{primary!80!black}\hfill\bfseries\Scientifica\fontsize{12}{0}\selectfont\contentspage\hrule height 1pt width \textwidth\relax}

        \titlecontents{section}
                [0.5cm]
                {}
                {\color{primary!60!black}\fontsize{10}{0}\selectfont\AlteG\thecontentslabel\hspace{0.125cm}\color{primary}}
                {}
                {\color{primary!80!black}\hfill\bfseries\Scientifica\fontsize{10}{0}\selectfont\contentspage}

        \titlecontents{subsection}
                [1cm]
                {}
                {\color{primary!60!black}\fontsize{8}{0}\selectfont\Lato\thecontentslabel\hspace{0.125cm}\color{primary}}
                {}
                {\color{primary!80!black}\hfill\bfseries\Scientifica\fontsize{8}{0}\selectfont\contentspage}

        %% Section
        \titlespacing*{\section}{0pt}{6mm}{6mm}
        \titleformat{\section}[hang]
        {}
        {\rlap{\color{primary!85!black}\rule[-6pt]{\textwidth}{1.2pt}}\colorbox{primary!85!black}{%
                \raisebox{0pt}[13pt][3pt]{ \makebox[60pt]{% height, width
                                        \fontsize{15}{12}\AlteG\color{white}{\thesection}}
                        }}}%
        {15pt}%
        {\color{primary}\fontsize{20}{12}\selectfont\Gobold#1\hspace{\fill}\ibook}

        %% Subsection
        % \titlespacing*{\subsection}{0pt}{3mm}{0pt}
        \titlespacing*{\subsection}{0pt}{6mm}{6mm}
        \titleformat{\subsection}[hang]
                {\color{primary!20!black}\fontsize{12}{12}\selectfont\Lato}
                {\thesubsection\fontsize{8}{6}\selectfont\ibookmark\hspace{10pt}}
                {0pt}
                {\color{accent!65!black}#1}

        %% Abstract
        \renewenvironment{abstract}
                {\thispagestyle{empty}\vfill{\par\raggedleft\fontsize{16}{18}\selectfont\Gobold\color{primary!75!black} Estratto\par\vspace{0.25cm}\hrule height 2pt \relax\par\noparskip}%
                \setlength{\parskip}{0.5em}\color{primary!35!black}\fontsize{12}{10}\selectfont\Lato}
                {\newpage}


        %% Highlight
        \def\hi#1{{\color{accent!80!black}\LatoBlack\mbox{#1}}}
        \def\dir#1{{\color{primary!80!black}\Mononoki\mbox{\penalty 100\ifolder\hspace{1pt}#1}}}
        \def\file#1{{\color{accent!80!white}\Mononoki\mbox{\penalty 100\ifile\hspace{1pt}#1}}}

        %% Scale text size using current font size
        \def\t@scale#1{\fontsize{#1\dimexpr\f@size pt\relax}{\dimexpr\f@size pt\relax}\selectfont}
        \def\t@apex@measure#1#2{\raisebox{#2\dimexpr\f@size pt\relax}{\t@scale{#2}#1}}
        \def\t@apex#1{\t@apex@measure{#1}{0.65}}
        \def\sp@text#1#2{{#1\t@scale{0.7}\t@apex{#2}}}
        \def\sp@rtext#1#2{{\t@scale{0.7}\t@apex{#2}}{#1}}

        \def\dir#1{{\color{primary!75!black}\sp@rtext{#1}{\ifolder}}}
        \def\qmake{\sp@text{gnu make}{\iauto}}
        \def\qmakefile{\sp@text{makefile}{\ifile\iauto}}
        \def\qterm{{\color{primary}\sp@rtext{terminal emulator}{\iterminal}}\ }
        \def\qstruct#1{{\color{primary}\t@apex@measure{struct}{0.5}\sp@text{#1}{\iwrench}}}
        \def\qfunction#1{{\color{cherryred}\sp@text{#1}{\ifile\icodeopentag}}}

        \newcommand{\mycbox}[1]{\tikz{\path[draw=#1,fill=#1] (0,0) rectangle (1cm,1cm);}}

        \newcommand{\separator}{%
          \noindent
          \begin{center}
            {\color{DarkViolet}
              \resizebox{0.5\linewidth}{1ex}
                        {{%
                            {\begin{tikzpicture}
                                \node  (C) at (0,0) {};
                                \node (D) at (9,0) {};
                                \path (C) to [ornament=85] (D);
            \end{tikzpicture}}}}}%
          \end{center}
        }

        %% \shapeableseparator{<color>}{<ornament>}
        \newcommand{\shapeableseparator}[2]{%
          \nointerlineskip\vspace{.5\baselineskip}\hspace{\fill}
                           {\color{#1}
                             \resizebox{0.5\linewidth}{2ex}
                                       {{%
                                           {\begin{tikzpicture}
                                               \node  (C) at (0,0) {};
                                               \node (D) at (9,0) {};
                                               \path (C) to [ornament=#2] (D);
                           \end{tikzpicture}}}}}%
                           \hspace{\fill}
                           \par\nointerlineskip\vspace{.5\baselineskip}
        }


        %% Xparse commands
        \NewDocumentCommand{\optional}{o}{
          \IfValueTF{#1}{%
            #1
          }{%
            % \phantom{TEXT}
          }%
        }

        \fancypagestyle{plain}{
          \fancyhf{}
          \fancyhead[L]{}
          \fancyhead[C]{}
          \fancyhead[R]{}
          \renewcommand{\headrule}{}

          \fancyfoot[L]{{\fontsize{10}{0}\color{primary}\documentname}}
          \fancyfoot[C]{{\fontsize{14}{0}{\color{primary}\thepage}}}
          \fancyfoot[R]{{\fontsize{10}{0}\color{primary}\currentchapter\hspace{2pt}\ibook}}
          \renewcommand{\footrule}{{\color{primary}\hrule height 1pt width \textwidth \relax}}
        }

\makeatother

% Define page layout(s)
\geometry{ a4paper,
  margin = 7.5mm,
  bottom = 12mm,
  footskip = 10mm,
  heightrounded,
  nohead,
  nomarginpar }

\overfullrule=5pt

% Tikz
\usetikzlibrary{calc, arrows, shapes.geometric, positioning, automata}

\tikzset{
        mpath/.style={
                fill=#1,
                draw=#1,
                line width=0.1pt
        },
        square/.style={regular polygon,regular polygon sides=4, inner sep=0pt, outer sep=0pt},
}

% \coverpage{<SIZE-OF-DOCUMENT-YEAR>}{<DOCUMENT-YEAR>}{<SIZE-OF-DOCUMENT-NAME>}{<DOCUMENT-NAME>}
\newcommand\coverpage[4]{%
        \newgeometry{noheadfoot=true, margin=0pt}\newpage\thispagestyle{empty}%
        \noindent\begin{tikzpicture}[remember picture, overlay, shift=(current page.south west)]%
                \begin{scope}[x={(current page.south east)},y={(current page.north west)}, overlay]
                        % Background
                        \fill [primary!75!white] (0,0) rectangle (1,1);

                        %% Layout
                        % Text box
                        \path [mpath=primary!25!white]  (0,0.25) -- (0.2,0.4) -- (0.8, 0.4) -- (1, 0.55) -- (1, 0.1) -- (0.93, 0.05) -- (0.07, 0.05) -- (0,0) -- cycle;
                        % Left Wing
                        \path [mpath=primary!85!white]	(0,0.27) -- (0.17,0.40) -- (0.2, 0.40) -- (0,0.25) -- cycle;
                        % Right Wing
                        \path [mpath=primary!85!white]	(0.77,0.4) -- (0.8, 0.40) -- (1, 0.55) -- (1, 0.57) -- cycle;
                        % Under Wing
                        \path [mpath=primary!65!black]  (0,0) -- (0.025,0) -- (0.075, 0.035) -- (0.94, 0.035) -- (1, 0.08) -- (1, 0.1) -- (0.93, 0.05) -- (0.07, 0.05) -- (0, 0) -- cycle;
                        % Central Wing
                        \path [mpath=primary!35!black]	(0,0.27) -- (0.17,0.40) -- (0.77, 0.40) -- (1, 0.57) -- (1, 0.8) -- (0.85, 0.8) -- (0.6, 0.6) -- (0.13, 0.6) -- (0,0.5) -- cycle;

                        %% Text nodes
                        % Icon & University
                        \node (fiisymbol) at ([yshift=-0.5cm, xshift=0.5cm]0,1)[align=center, anchor=north west, inner sep=0pt, outer sep=0pt]
                                { \color{primary!65!black}\includegraphics[%
                                                width=3cm,%
                                                height=3cm,%
                                                keepaspectratio%
                                        ] {sources/uni_logo.pdf}};
                        \node (fiitext) at ([xshift=0.25cm] fiisymbol.north east) [align=left, anchor=north west]
                                {{\color{primary!65!black}\Lato\fontsize{10}{0}\selectfont Università degli Studi di Napoli}};
                        \node (fiiname) at ([xshift=0.01cm, yshift=0.2cm]fiitext.south west) [align=left, anchor=north west]
                                {{\color{primary!65!black}\Agency\fontsize{24}{0}\selectfont Federico II}};

                        % Date and academic year
                        \node (academicyear) at ([xshift=-0.5cm] fiitext.north -| 1,1) [align=right, anchor=north east]
                                {{\color{primary!65!black}\Gobold\fontsize{#1}{0}\selectfont #2}};

                        % Title of the documentation
                        \node at ([xshift=0.1cm, yshift=0.1cm] $(0,0)!0.5!(1,1)$) [align=center, anchor=center, inner sep=0pt, outer sep=0pt]
                                {{\color{primary!70!white}\Gobold\fontsize{#3}{0}\selectfont #4}};
                \end{scope}%
        \end{tikzpicture}\restoregeometry\newpage}

% \introduction{Professor Name}{Additional Text}
\newcommand\introduction[2]{
  \begin{abstract}
      Il seguente documento rappresenta una raccolta di appunti,
      riorganizzata e migliorata nelle vesti grafiche,
      del corso di \documentname\  del professor #1,
      per il corso di laurea in Informatica \documentyear,
      della Federico II di Napoli.

      \begin{center}
      #2
      \end{center}

      Si tiene a specificare che questo documento non ha lo scopo di \textbf{sostituire
      libri di testo}, note del professore o lezioni frontali,
      nonostante siano tutte fonti utilizzate per la stesura,
      ma quello di integrare al materiale più complesso una
      rilettura degli argomenti da un punto di vista meno tecnico
      e quindi più lento nel soffermarsi nei passaggi critici.

      %% La materia prima principale per la stesura di questo documento sono gli appunti presi da studenti, per studenti.
      Si ringraziano \href{https://github.com/luftmensch-luftmensch}{\hi{\iuser Valentino Bocchetti}} e \href{https://github.com/43616F73}{\hi{\iuser Pasquale Miranda}}  ideatori e gestori del progetto \textit{Unina Docs},

      Si ringraziano inoltre tutti i revisori che hanno contribuito al documento
      con consigli e proposte di modifica, invitando a dare feedback in caso di errori.

      Si ringraziano in fine i lettori nella speranza che questo lavoro sia stato utile.

      \ifx \xauthors \undefined
      \else
        \begin{flushright}
          \textit{Redazione a cura di} \xauthors
        \end{flushright}
      \fi

      \ifx \yauthors \undefined
      \else
        \begin{flushright}
          \textit{Revisione testo a cura di} \yauthors
        \end{flushright}
      \fi

      \ifx \zauthors \undefined
      \else
      \begin{flushright}
        \textit{Si ringraziano} \zauthors\space per il materiale fornito
      \end{flushright}
      \fi
  \end{abstract}
}


% Tcolorbox theorems
\tcbuselibrary{skins}

\makeatletter
\newtcbtheorem[number within=section]{Definition}{}{
  enhanced,breakable,
  before skip=5mm,after skip=5mm, colback=red!5,colframe=red!80!black,boxrule=0.5mm,
  attach boxed title to top left={xshift=1cm,yshift*=1mm-\tcboxedtitleheight},
  drop fuzzy shadow,
  boxed title style={
    frame code={
      \path[fill=tcbcolback]
      ([yshift=-1mm,xshift=-1mm]frame.north west)
      arc[start angle=0,end angle=180,radius=1mm]
      ([yshift=-1mm,xshift=1mm]frame.north east)
      arc[start angle=180,end angle=0,radius=1mm];
      \path[left color=tcbcolback!60!black,right color=tcbcolback!60!black,
        middle color=tcbcolback!80!black]
      ([xshift=-2mm]frame.north west) -- ([xshift=2mm]frame.north east)
           [rounded corners=1mm]-- ([xshift=1mm,yshift=-1mm]frame.north east)
           -- (frame.south east) -- (frame.south west)
           -- ([xshift=-1mm,yshift=-1mm]frame.north west)
           [sharp corners]-- cycle;
    },
    interior engine=empty,
  },
  fonttitle=\bfseries,
  label={#2},#1}{def}
\makeatother

\makeatletter
\newtcolorbox[number within=section]{infobox}[1]{%
	title=#1, fonttitle=\bfseries,
        drop fuzzy shadow,
	colback=green-gradient-1,enhanced,
	attach boxed title to top left={xshift=-5mm},
	boxrule=0pt,
	before skip=1cm, after skip=1cm, right skip=0cm,
	toprule=0pt, bottomrule=0pt, rightrule=0pt, leftrule=4pt,
	skin=enhancedlast jigsaw,colframe=green-gradient-6,colbacktitle=green-gradient-5,
	boxed title style = {
		frame code={
			\fill[green-gradient-5](frame.south west)--(frame.north west)--(frame.north east)--([xshift=3mm]frame.east)--(frame.south east)--cycle;
			\draw[line width=1mm,green-gradient-5]([xshift=2mm]frame.north east)--([xshift=5mm]frame.east)--([xshift=2mm]frame.south east);
			\draw[line width=1mm,green-gradient-5]([xshift=5mm]frame.north east)--([xshift=8mm]frame.east)--([xshift=5mm]frame.south east);
			\fill[green!40](frame.south west)--+(4mm,-2mm)--+(4mm,2mm)--cycle;
		}
	}
}
\makeatother


\makeatletter
\newtcolorbox[number within=section]{warningbox}[1]{%
	title=#1, fonttitle=\bfseries,
	colback=yellow-gradient-1,enhanced,
        drop fuzzy shadow,
	attach boxed title to top left={xshift=-5mm},
	boxrule=0pt,
	before skip=1cm, after skip=1cm, right skip=0cm,
	toprule=0pt, bottomrule=0pt, rightrule=0pt, leftrule=4pt,
	skin=enhancedlast jigsaw,colframe=yellow-gradient-6,colbacktitle=yellow-gradient-5,
	boxed title style = {
		frame code={
			\fill[yellow-gradient-5](frame.south west)--(frame.north west)--(frame.north east)--([xshift=3mm]frame.east)--(frame.south east)--cycle;
			\draw[line width=1mm,yellow-gradient-5]([xshift=2mm]frame.north east)--([xshift=5mm]frame.east)--([xshift=2mm]frame.south east);
			\draw[line width=1mm,yellow-gradient-5]([xshift=5mm]frame.north east)--([xshift=8mm]frame.east)--([xshift=5mm]frame.south east);
			\fill[yellow!40](frame.south west)--+(4mm,-2mm)--+(4mm,2mm)--cycle;
		}
	}
}
\makeatother

\makeatletter
\newtcolorbox[number within=section]{errorbox}[1]{%
	title=#1, fonttitle=\bfseries,
	colback=red-gradient-1,enhanced,
        drop fuzzy shadow,
	attach boxed title to top left={xshift=-5mm},
	boxrule=0pt,
	before skip=1cm, after skip=1cm, right skip=0cm,
	toprule=0pt, bottomrule=0pt, rightrule=0pt, leftrule=4pt,
	skin=enhancedlast jigsaw,colframe=red-gradient-6,colbacktitle=red-gradient-5,
	boxed title style = {
		frame code={
			\fill[red-gradient-5](frame.south west)--(frame.north west)--(frame.north east)--([xshift=3mm]frame.east)--(frame.south east)--cycle;
			\draw[line width=1mm,red-gradient-5]([xshift=2mm]frame.north east)--([xshift=5mm]frame.east)--([xshift=2mm]frame.south east);
			\draw[line width=1mm,red-gradient-5]([xshift=5mm]frame.north east)--([xshift=8mm]frame.east)--([xshift=5mm]frame.south east);
			\fill[red!40](frame.south west)--+(4mm,-2mm)--+(4mm,2mm)--cycle;
		}
	}
}
\makeatother

\makeatletter
\newtcolorbox{infoboxtag}[1]{
  enhanced,
  drop fuzzy shadow,
  before skip=7pt,
  after skip =7pt,
  left skip=0pt,
  right skip=0pt,
  boxrule=0.4pt,
  top=0pt,
  bottom=0pt,
  left=4mm,
  right=4mm,
  arc=1pt,
  boxsep=4pt,
  before upper={\vphantom{dlg}},
  colframe=green!50!black,
  coltext=green!25!black,
  colback=green!10!white,
  overlay={
    \begin{tcbclipinterior}
      \fill[green!75!blue!50!white]
      (frame.south west)
      rectangle      node[text=white,
        font=\sffamily\bfseries\tiny,
        %rectangle,
        %rotate=90
      ]
      {#1}
      ([xshift=4mm]frame.north west);
      \fill[green!75!blue!50!white]
      ([xshift=-4mm]frame.south east)
      rectangle      node[text=white,
        font=\sffamily\bfseries\tiny,
        %rectangle,
        %rotate=90
      ]
      {#1}
      (frame.north east);
    \end{tcbclipinterior};
  }
}
\makeatother

\makeatletter
\newtcolorbox{halfframedbox}[2]{
  empty,
  coltitle = #1,
  title = #2,
  overlay = {
    \draw[gray!60,line width=1pt](frame.north west)--(frame.north east)--(frame.south east)--(frame.south west)--(frame.north west);
    \draw[#1,line width=1pt]
    ($(frame.north west)!0.33!(frame.south west)$)
    --(frame.north west)
    --($(frame.north west)!0.33!(frame.north east)$);
    \draw[#1,line width=1pt]
    ($(frame.south east)!0.33!(frame.south west)$)
    --(frame.south east)
    --($(frame.south east)!0.33!(frame.north east)$);
  },
}
\makeatother

\makeatletter
\newtcolorbox{boxwithfold}[2]{
  enhanced,
  before skip balanced=2mm,after skip balanced=3mm,
  boxrule=0.4pt,left=5mm,right=2mm,top=1mm,bottom=1mm,
  colback= #1,
  colframe = #2,
  sharp corners,rounded corners=southeast,arc is angular,arc=3mm,
  underlay = {%
    % Folded paper effect
    \path[fill=tcbcolback!80!black] ([yshift=3mm]interior.south east)--++(-0.4,-0.1)--++(0.1,-0.2);
    \path[draw=tcbcolframe,shorten <=-0.05mm,shorten >=-0.05mm] ([yshift=3mm]interior.south east)--++(-0.4,-0.1)--++(0.1,-0.2);
    % Symbol
    \path[fill=tcbcolback!50!black,draw=none] (interior.south west) rectangle node[white]{\Huge\bfseries !} ([xshift=4mm]interior.north west);
  },
  drop fuzzy shadow,
}
\makeatother

\makeatletter
\newtcolorbox{simpletbox}[2]{
  enhanced,
  sharp corners,
  colback = white,
  before skip = 0.2cm,
  after skip = 0.5cm,
  drop fuzzy shadow,
  colback = #1,
  colframe = #2,
  boxrule = 0pt,
  leftrule = 6pt,
}
\makeatother

\makeatletter
\newtcolorbox{generalbox}[2][]{
  enhanced,
  breakable,
  colback=white,
  colframe=azure-gradient-2!80!black,
  drop fuzzy shadow,
  attach boxed title to top left={yshift*=-\tcboxedtitleheight},
  fonttitle=\bfseries,
  title={\optional{#2}},
  boxed title size=title,
  boxed title style={
    sharp corners,
    rounded corners=northwest,
    colback=tcbcolframe,
    boxrule=0pt,
  },
  underlay boxed title={%
    \path[fill=tcbcolframe] (title.south west)--(title.south east)
    to[out=0, in=180] ([xshift=5mm]title.east)--
    (title.center-|frame.east)
    [rounded corners=\kvtcb@arc] |-
    (frame.north) -| cycle;
  },
  #1
}
\makeatother



% Abbreviation for tcolorbox envs
% \dfn è ridefinito in fondo al file (sezione AMBIENTI MATEMATICI) per essere numerato ed etichettabile

\newcommand{\info}[2]{\begin{concetto}\begin{infobox}{#1}#2\end{infobox}\end{concetto}} % Invoke with \info{title}{Content}
\newcommand{\warning}[2]{\begin{concetto}\begin{warningbox}{#1}#2\end{warningbox}\end{concetto}} % Invoke with \warning{title}{Content}
\newcommand{\error}[2]{\begin{concetto}\begin{errorbox}{#1}#2\end{errorbox}\end{concetto}} % Invoke with \error{title}{Content}

\newcommand{\infoalt}[2]{\begin{infoboxtag}{#1}#2\end{infoboxtag}} % Invoke with \infoalt{icon_name}{Content}
\newcommand{\framedbox}[3]{\begin{halfframedbox}{#1}{#2}#3\end{halfframedbox}} % Invoke with \framedbox{color}{Title}{content}
\newcommand{\marker}[3]{\begin{boxwithfold}{#1}{#2}#3\end{boxwithfold}} % Invoke with \marker{color}{border-color}{content}
\newcommand{\simplebox}[3]{\begin{simpletbox}{#1}{#2}#3\end{simpletbox}} % Invoke with \simplebox{color}{border-color}{content}
\newcommand{\gbox}[3]{\begin{generalbox}[colframe=#2]{#1}#3\end{generalbox}} % Invoke with \gbox{[NEEDED] TITLE}{[NEEDED] FRAME COLOR}{[NEEDED] CONTENT}

% Code highlighting  w/ LstListing
\makeatletter
        \lst@Key{firstlineandnumber}\relax{\def\lst@firstline{#1\relax}\def\lst@firstnumber{#1\relax}}
\makeatother

\lstset{%
  autogobble=true,
  mathescape=true,
  style=FiraCodeStyle,
  backgroundcolor=\color{naplesyellow!10!white},
  commentstyle=\itshape\color{seagreen},
  keywordstyle=\color{cherryred},
  stringstyle=\color{naplesyellow!80!black},
  basicstyle=\linespread{1.15}\footnotesize\FiraCode,
  breaklines=true,
  tabsize=2,
  escapeinside={(*@}{@*)},
  xleftmargin=0.5cm,
  xrightmargin=0.5cm,
  framesep=0mm,
  extendedchars=true,
  showstringspaces=false,
  showtabs=false,
  showstringspaces=false,
  captionpos=b,
  title=\color{primary}\fontsize{10}{12}\selectfont\sp@rtext{\lstname}{\ifilecode},
  columns=fixed
}

\lstdefinestyle{wnumbers}{
  % Style of numbers
  xleftmargin=1cm,
  numbers=left,
  numberstyle=\Lato\scriptsize\color{orange!80!black},
  frame=l,
  framesep=0.5cm,
  framexleftmargin=0.3cm,
  rulecolor=\color{white},
  fillcolor=\color{naplesyellow!40!white}
}

\lstdefinelanguage{makefile}{%
  morecomment=[l][commentstyle]{\#},%
}

\lstdefinelanguage{ini}{
  xleftmargin=1cm,
  numbers=left,
  numberstyle=\Lato\scriptsize\color{orange!80!black},
  frame=l,
  framesep=0.5cm,
  framexleftmargin=0.3cm,
  morecomment=[s][\color{violet!60!white}\bfseries]{[}{]},
  morecomment=[l]{\#},
  morecomment=[l]{;},
  commentstyle=\color{gray}\ttfamily,
  morekeywords={},
  otherkeywords={=,:},
  keywordstyle={\color{turquoise!70!black}\bfseries},
  % Automatically skip leading spaces
  autogobble=false,
  escapeinside={(*}{*)}
}

\lstdefinelanguage{asd}[]{}{
  alsoletter={\#},
  sensitive=true,
  xleftmargin=1cm,
  numbers=left,
  numberstyle=\Lato\scriptsize\color{orange!80!black},
  frame=l,
  framesep=0.5cm,
  framexleftmargin=0.3cm,
  %% Handle directives
  %% moredelim=*[s][{\color{violet!60!white}}]{\#include\ <}{.h>},
  %% moredelim=*[l][{\color{blue!65!white}}]\#if,
  %% moredelim=*[l][{\color{blue!65!white}}]\#endif,
  %% moredelim=*[s][{\color{violet!60!white!70!black}}]{\#include\ "}{.h"},
  %% moredelim=*[l][{\color{blue!90!white!70!black}}]\#define,
  moredelim=*[s][{\color{turquoise!70!black}}]{[}{]},
  %% Comments
  comment=[l]//,
  morecomment=[s]{/*}{*/},
  % Strings
  string=[b]{"},
  morestring=[b]{'},
  % Modifiers
  keywords=[0]{i, j, k, n},
  % Primitives
  keywords=[1]{if, else, then, for, while, do},
  % Logical constructs
  keywords=[2]{return},
  keywords=[3]{SUM, MAX, RIS, A, Search},
  keywords=[4]{free, pos},
  % Operators
  otherkeywords={*, &},
  keywords=[3]{*, &},
  escapechar={@},
  % API structs
  % Colors
  directivestyle=\color{blue!85!white},
  keywordstyle=[0]\color{cherryred},
  keywordstyle=[1]\color{green!75!black},
  keywordstyle=[2]\color{cherryred!75},
  keywordstyle=[3]\color{naplesyellow!75!black},
  keywordstyle=[4]\color{violet!75!black},
}[keywords,comments,strings,directives]

\lstdefinelanguage[POSIX]{JAVA}
                  []{}
                  { alsoletter={\#},
                    sensitive=true,
                    %% Handle directives
                    moredelim=*[s][{\color{violet!60!white}}]package,
                    moredelim=*[l][{\color{blue!65!white}}]import,
                    %% Comments
                    comment=[l]//,
                    morecomment=[s]{/*}{*/},
                    % Strings
                    string=[b]{"},
                    morestring=[b]{'},
                    % Modifiers
                    keywords=[0]{class, public, private, static, volatile, Enum},
                    % Primitives
                    keywords=[1]{int, Integer, String, double, long, short, char, void, bool},
                    % Logical constructs
                    keywords=[2]{if, else, return, for, while, do},
                    % Operators
                    otherkeywords={*, &},
                    keywords=[3]{*, &},
                    % Colors
                    directivestyle=\color{blue!85!white},
                    keywordstyle=[0]\color{cherryred},
                    keywordstyle=[1]\color{green!75!black},
                    keywordstyle=[2]\color{cherryred},
                    keywordstyle=[3]\color{naplesyellow!75!black},
                  }[keywords,comments,strings,directives]

\lstdefinelanguage[POSIX]{C}
                  []{}
                  { alsoletter={\#},
                    sensitive=true,
                    %% Handle directives
                    moredelim=*[s][{\color{violet!60!white}}]{\#include\ <}{.h>},
                    moredelim=*[l][{\color{blue!65!white}}]\#if,
                    moredelim=*[l][{\color{blue!65!white}}]\#endif,
                    moredelim=*[s][{\color{violet!60!white!70!black}}]{\#include\ "}{.h"},
                    moredelim=*[l][{\color{blue!90!white!70!black}}]\#define,
                    moredelim=*[s][{\color{turquoise!70!black}}]{[}{]},
                    %% Comments
                    comment=[l]//,
                    morecomment=[s]{/*}{*/},
                    % Strings
                    string=[b]{"},
                    morestring=[b]{'},
                    % Modifiers
                    keywords=[0]{const, unsigned, signed, static, volatile, typedef, struct, union, enum, atomic_t},
                    % Primitives
                    keywords=[1]{int, float, double, long, short, char, void, bool},
                    % Logical constructs
                    keywords=[2]{if, else, return, for, while, do},
                    % Operators
                    otherkeywords={*, &},
                    keywords=[3]{*, &},
                    % API structs
                    % Colors
                    directivestyle=\color{blue!85!white},
                    keywordstyle=[0]\color{cherryred},
                    keywordstyle=[1]\color{green!75!black},
                    keywordstyle=[2]\color{cherryred},
                    keywordstyle=[3]\color{naplesyellow!75!black},
                  }[keywords,comments,strings,directives]

%% \directlua{
%%   function be_quiet ()
%%   end
%%   luatexbase.add_to_callback('start_run', be_quiet, 'stop start run')
%%   luatexbase.add_to_callback('stop_run', be_quiet, 'stop stop run')
%%   luatexbase.add_to_callback('start_page_number', be_quiet, 'stop start page')
%%   luatexbase.add_to_callback('stop_page_number', be_quiet, 'stop stop page')
%%   luatexbase.add_to_callback('start_file', be_quiet, 'stop start file')
%%   luatexbase.add_to_callback('stop_file', be_quiet, 'stop stop file')
%%   luatexbase.add_to_callback('show_warning_message', be_quiet, 'stop show warning message')
%% }

% Lstlisting code vertical guideline support
\begin{luacode}
  local gatherBuffer
  function read(line)
    texio.write_nl(line)
    table.insert(gatherBuffer, line)

    if line:match('.*stop_rec().*') then
      return line
    else return '' end
  end

  function start_rec()
    gatherBuffer  = { }
    luatexbase.add_to_callback('process_input_buffer', read, 'recording')
  end

  function stop_rec()
    luatexbase.remove_from_callback('process_input_buffer', 'recording')
  end

  function retrieve_recording()
  for ix, line in ipairs(gatherBuffer) do
      if ix ~= #gatherBuffer then
        texio.write_nl(line)
        tex.print(line)
      end
    end
  end

  function prepare()
    for ix=2, #gatherBuffer-2 do
      local match    = gatherBuffer[ix]:match('^%s+')
      local spaces  = (match and #match - 1) or 0
      texio.write_nl(tostring(spaces))

      gatherBuffer[ix] = gatherBuffer[ix]:gsub('^%s+',
      string.rep('$\\indentrule$  ', spaces))
    end
  end
\end{luacode}

% Vertical guideline
\newcommand{\indentrule}{\color{gray}\rlap{\smash{\hspace{6pt}\rule[-.35em]{1pt}{1.45em}}}}

% Lstlisting TOC & label customization
\renewcommand\lstlistlistingname{\documentlsttitle}
\renewcommand\lstlistingname{\documentlstlabel}
\makeatletter
\def\l@lstlisting#1#2{
  \@dottedtocline{1}{0em}{2.3em}{\textcolor{primary}{\ilabel \selectfont\AlteG \documentlstlabel\space #1}}{#2}
}
\makeatother

% Used to output definition of a LaTeX macro in console
\def\debugdef#1{%
  \typeout{[DEBUG] Definition of \@backslashchar #1: \expandafter\meaning\csname#1\endcsname ^^J ^^J}}

% Math related
\DeclarePairedDelimiter\abs{\lvert}{\rvert}%
\DeclarePairedDelimiter\norm{\lVert}{\rVert}%

% ============================================================
% AMBIENTI STILE
% ============================================================
%
% UTILIZZO:
%   \begin{esempio}{Titolo opzionale}
%     testo, verbatim, ecc.
%   \end{esempio}
%
%   \begin{esercizio}{Titolo opzionale}
%     testo, verbatim, ecc.
%   \end{esercizio}
%
% Il titolo è OBBLIGATORIO nella sintassi ma può essere lasciato vuoto:
%   \begin{esempio}{}  ...  \end{esempio}
% ============================================================

% Contatori resettati ad ogni capitolo (le sezioni non sono numerate)
\newcounter{esempio}[chapter]
\newcounter{esercizio}[chapter]
\renewcommand{\theesempio}{\thechapter.\arabic{esempio}}
\renewcommand{\theesercizio}{\thechapter.\arabic{esercizio}}

% ── Ambiente ESEMPIO ─────────────────────────────────────────
\newenvironment{esempio}[1]{%
  \begin{concetto}%
  \refstepcounter{esempio}%
  \vspace{0.8em}%
  \noindent\rule{\linewidth}{0.5pt}\par%
  \vspace{0.15em}%
  \noindent\textbf{Esempio \theesempio}%
  \ifx\relax#1\relax\else%
    \textbf{ --- #1}%
  \fi\par%
  \vspace{0.3em}%
}{%
  \par\nopagebreak\vspace{0.3em}\nopagebreak%
  \noindent\rule{\linewidth}{0.5pt}%
  \vspace{0.8em}%
  \end{concetto}%
}

% ── Ambiente ESERCIZIO ───────────────────────────────────────
\newenvironment{esercizio}[1]{%
  \refstepcounter{esercizio}%
  \vspace{0.8em}%
  \noindent\rule{\linewidth}{1.2pt}\vspace{1pt}\par%
  \noindent\rule{\linewidth}{0.4pt}\par%
  \vspace{0.15em}%
  \noindent\textbf{Esercizio \theesercizio}%
  \ifx\relax#1\relax\else%
    \textbf{ --- #1}%
  \fi\par%
  \vspace{0.3em}%
}{%
  \par\nopagebreak\vspace{0.3em}\nopagebreak%
  \noindent\rule{\linewidth}{0.4pt}\vspace{1pt}\par\nopagebreak%
  \noindent\rule{\linewidth}{1.2pt}%
  \vspace{0.8em}%
}

% Swap the definition of \abs* and \norm*, so that \abs
% and \norm resizes the size of the brackets, and the
% starred version does not.
\makeatletter
	\let\oldabs\abs
	\def\abs{\@ifstar{\oldabs}{\oldabs*}}
	%
	\let\oldnorm\norm
	\def\norm{\@ifstar{\oldnorm}{\oldnorm*}}

	%% Angle brackets shortcut -> <CONTENT>
	\def\abrakets#1{\displaystyle{\left\langle{#1}\right\rangle}}

	%% Curly brackets shortcut -> {CONTENT}
	\def\cbrakets#1{\displaystyle{\left\{{#1}\right\}}}
	%% Round brackets shortcut -> (CONTENT)
	\def\rbrakets#1{\displaystyle{\left({#1}\right)}}

	%% Math symbols shortcut (Calligraphic fonts with \mathcal)
	\newcommand{\mcA}{\mathcal{A}}
	\newcommand{\mcB}{\mathcal{B}}
	\newcommand{\mcC}{\mathcal{C}}
	\newcommand{\mcD}{\mathcal{D}}
	\newcommand{\mcE}{\mathcal{E}}
	\newcommand{\mcF}{\mathcal{F}}
	\newcommand{\mcG}{\mathcal{G}}
	\newcommand{\mcH}{\mathcal{H}}
	\newcommand{\mcI}{\mathcal{I}}
	\newcommand{\mcL}{\mathcal{L}}
	\newcommand{\mcM}{\mathcal{M}}
	\newcommand{\mcN}{\mathcal{N}}
	\newcommand{\mcO}{\mathcal{O}}
	\newcommand{\mcP}{\mathcal{P}}
	\newcommand{\mcQ}{\mathcal{Q}}
	\newcommand{\mcR}{\mathcal{R}}
	\newcommand{\mcS}{\mathcal{S}}
	\newcommand{\mcT}{\mathcal{T}}
	\newcommand{\mcU}{\mathcal{U}}
	\newcommand{\mcV}{\mathcal{V}}
	\newcommand{\mcW}{\mathcal{W}}
	\newcommand{\mcX}{\mathcal{X}}
	\newcommand{\mcY}{\mathcal{Y}}
	\newcommand{\mcZ}{\mathcal{Z}}

	%% Math symbols shortcut (blackboard bold fonts with \mathbb)
  \newcommand{\mbA}{\mathbb{A}}
  \newcommand{\mbB}{\mathbb{B}}
  \newcommand{\mbC}{\mathbb{C}}
  \newcommand{\mbD}{\mathbb{D}}
  \newcommand{\mbE}{\mathbb{E}}
  \newcommand{\mbF}{\mathbb{F}}
  \newcommand{\mbG}{\mathbb{G}}
  \newcommand{\mbH}{\mathbb{H}}
  \newcommand{\mbI}{\mathbb{I}}
  \newcommand{\mbJ}{\mathbb{J}}
  \newcommand{\mbK}{\mathbb{K}}
  \newcommand{\mbL}{\mathbb{L}}
  \newcommand{\mbM}{\mathbb{M}}
  \newcommand{\mbN}{\mathbb{N}}
  \newcommand{\mbO}{\mathbb{O}}
  \newcommand{\mbP}{\mathbb{P}}
  \newcommand{\mbQ}{\mathbb{Q}}
  \newcommand{\mbR}{\mathbb{R}}
  \newcommand{\mbS}{\mathbb{S}}
  \newcommand{\mbT}{\mathbb{T}}
  \newcommand{\mbU}{\mathbb{U}}
  \newcommand{\mbV}{\mathbb{V}}
  \newcommand{\mbW}{\mathbb{W}}
  \newcommand{\mbX}{\mathbb{X}}
  \newcommand{\mbY}{\mathbb{Y}}
  \newcommand{\mbZ}{\mathbb{Z}}
  \newcommand\xor{{\displaystyle{\dot{\vee}}}}

\makeatother

% ============================================================
% AMBIENTI MATEMATICI
% ============================================================
%
% UTILIZZO:
%   \dfn[etichetta]{Titolo}{Contenuto}          -> Definizione n.m (etichetta: def:etichetta)
%
%   \begin{Teorema}{Titolo}{etichetta}          -> Teorema n.m     (etichetta: teo:etichetta)
%     \begin{prerequisiti}
%       \dip{Definizione}{def:xxx}               -> link a un enunciato numerato
%       \dipsez{sec:xxx}                         -> link a una sezione
%       \dipvoce{testo libero}                   -> voce senza link
%     \end{prerequisiti}
%     Enunciato...
%   \end{Teorema}
%   \begin{dimostrazione} ... \end{dimostrazione}
%
%   Allo stesso modo: Proposizione (prop:), Lemma (lem:), Corollario (cor:).
%   Definizioni, teoremi, proposizioni, lemmi e corollari condividono
%   un'unica numerazione per capitolo, così sono facili da ritrovare.
% ============================================================

\RequirePackage{colortbl}
\RequirePackage{array}

% ── Ambiente CONCETTO: tutto ciò che contiene resta nella stessa pagina ──
% (enunciato + prerequisiti + dimostrazione, definizioni, note, esempi)
\newenvironment{concetto}{%
  \par\addvspace{2mm}\noindent\begin{minipage}{\linewidth}%
  \setlength{\parskip}{0.75em}\setlength{\parindent}{0pt}%
}{%
  \end{minipage}\par\addvspace{2mm}%
}

\makeatletter

% Stile comune dei box "enunciato" (stessa forma del box Definition originale)
% #1 = colore del bordo, #2 = colore dello sfondo, #3 = colore della targhetta del titolo
\tcbset{
  unina enunciato/.style n args={3}{
    enhanced,
    before skip=5mm,after skip=5mm,
    colback=#2,colframe=#1,boxrule=0.5mm,
    colbacktitle=#3,
    attach boxed title to top left={xshift=1cm,yshift*=1mm-\tcboxedtitleheight},
    drop fuzzy shadow,
    boxed title style={
      frame code={
        \path[fill=tcbcolback]
        ([yshift=-1mm,xshift=-1mm]frame.north west)
        arc[start angle=0,end angle=180,radius=1mm]
        ([yshift=-1mm,xshift=1mm]frame.north east)
        arc[start angle=180,end angle=0,radius=1mm];
        \path[left color=tcbcolback!60!black,right color=tcbcolback!60!black,
          middle color=tcbcolback!80!black]
        ([xshift=-2mm]frame.north west) -- ([xshift=2mm]frame.north east)
             [rounded corners=1mm]-- ([xshift=1mm,yshift=-1mm]frame.north east)
             -- (frame.south east) -- (frame.south west)
             -- ([xshift=-1mm,yshift=-1mm]frame.north west)
             [sharp corners]-- cycle;
      },
      interior engine=empty,
    },
    fonttitle=\bfseries,
    separator sign={\ ---},
    top=3mm,
  }
}

% Definizioni: box rosso come l'originale, ma numerate
\newtcbtheorem[number within=chapter]{Definizione}{Definizione}{
  unina enunciato={red!80!black}{red!5}{red!75!black}}{def}

% Teoremi, proposizioni, lemmi, corollari: box blu (colore primario)
\newtcbtheorem[use counter from=Definizione]{Teorema}{Teorema}{
  unina enunciato={primary!80!black}{primary!5}{primary!75!black}}{teo}
\newtcbtheorem[use counter from=Definizione]{Proposizione}{Proposizione}{
  unina enunciato={primary!80!black}{primary!5}{primary!75!black}}{prop}
\newtcbtheorem[use counter from=Definizione]{Lemma}{Lemma}{
  unina enunciato={primary!80!black}{primary!5}{primary!75!black}}{lem}
\newtcbtheorem[use counter from=Definizione]{Corollario}{Corollario}{
  unina enunciato={seagreen!70!black}{seagreen!5}{seagreen!65!black}}{cor}

% \dfn[etichetta]{Titolo}{Contenuto}
\NewDocumentCommand{\dfn}{O{} m +m}{%
  \begin{concetto}\begin{Definizione}{#2}{#1}#3\end{Definizione}\end{concetto}}

% ── Box PREREQUISITI (da mettere all'inizio di ogni teorema) ──
\newtcolorbox{prerequisitibox}{
  enhanced, breakable=false,
  colback=primary!4!white, colframe=primary!45!white,
  boxrule=0pt, leftrule=3pt, arc=0pt, outer arc=0pt,
  left=2mm, right=2mm, top=1mm, bottom=1.2mm,
  before skip=0mm, after skip=3mm,
  fontupper=\small,
}
\NewDocumentEnvironment{prerequisiti}{}{%
  \begin{prerequisitibox}%
  {\color{primary!80!black}{\mdseries\ilabel}\ \bfseries Prerequisiti: cosa serve sapere}\par\nopagebreak
  \begin{itemize}[nosep, leftmargin=1.3em, label={\color{primary}\scriptsize$\blacktriangleright$}]%
}{%
  \end{itemize}\end{prerequisitibox}%
}
% \dip{Tipo}{etichetta} -> "Tipo n.m — Titolo ........ pag. x" (tutto cliccabile)
\newcommand{\dip}[2]{%
  \item \hyperref[#2]{{\color{primary!85!black}\textbf{#1~\ref*{#2}}}~---~\nameref*{#2}}%
  \hfill{\color{neutral}\scriptsize pag.~\pageref*{#2}}}
% \dipsez{etichetta} -> link a una sezione (le sezioni non sono numerate)
\newcommand{\dipsez}[1]{%
  \item \hyperref[#1]{{\color{primary!85!black}\textbf{Sezione}}~«\nameref*{#1}»}%
  \hfill{\color{neutral}\scriptsize pag.~\pageref*{#1}}}
% \dipvoce{testo} -> voce libera, senza link
\newcommand{\dipvoce}[1]{\item #1}
% \dipgruppo{testo} -> sottotitolo dentro l'elenco (senza pallino)
\newcommand{\dipgruppo}[1]{\item[] {\itshape #1}}
\newcommand{\defsse}{\mathrel{\vcentcolon\mkern1mu\leftrightarrow}}   % ":<->" (definizione)

% ── Ambiente DIMOSTRAZIONE ─────────────────────────────────────
\newtcolorbox{dimostrazionebox}{
  enhanced,
  colback=white, colframe=primary!35!white,
  boxrule=0pt, leftrule=2pt, arc=0pt, outer arc=0pt,
  left=3mm, right=1mm, top=0.5mm, bottom=0.5mm,
  before skip=0mm, after skip=6mm,
}
\NewDocumentEnvironment{dimostrazione}{O{Dimostrazione}}{%
  \begin{dimostrazionebox}{\color{primary!80!black}\bfseries\itshape #1.}\ \ignorespaces
}{%
  % il quadratino va a destra dell'ultima riga, oppure a destra della riga successiva se non c'è spazio
  \ifhmode\unskip\else\leavevmode\fi\nobreak\hfil\penalty50\hskip1em\null\nobreak\hfill
  {\color{primary!80!black}$\blacksquare$}\parfillskip=0pt\finalhyphendemerits=0\par
  \end{dimostrazionebox}%
}

% ── Tavole di verità ──────────────────────────────────────────
\newcommand{\vero}{{\color{seagreen!65!black}\mathrm{V}}}
\newcommand{\falso}{{\color{cherryred!80!black}\mathrm{F}}}
\newcolumntype{T}{>{\columncolor{primary!10}}c}        % colonne evidenziate da confrontare (1° gruppo)
\newcolumntype{U}{>{\columncolor{naplesyellow!35}}c}   % colonne evidenziate da confrontare (2° gruppo)
\newcolumntype{K}{>{\columncolor{seagreen!18}}c}       % colonne evidenziate da confrontare (3° gruppo)
\newenvironment{tavola}[1]{%
  \begin{center}\renewcommand{\arraystretch}{1.25}\setlength{\tabcolsep}{7pt}%
  \begin{tabular}{#1}}{\end{tabular}\end{center}}
\newcommand{\intestazione}{\rowcolor{primary!18}}

% ── Simboli logici ────────────────────────────────────────────
\newcommand{\XOR}{\mathbin{\mathrm{XOR}}}
\newcommand{\NAND}{\mathbin{\mathrm{NAND}}}
\newcommand{\NOR}{\mathbin{\mathrm{NOR}}}
\newcommand{\sse}{\ \Longleftrightarrow\ }   % "se e solo se" (metalinguaggio)
\newcommand{\implica}{\ \Longrightarrow\ }   % "implica" (metalinguaggio)

\makeatother
