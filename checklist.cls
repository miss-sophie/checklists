%% checklist.cls
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{checklist}

\makeatletter

% -----------------------------------------------------------------------------
% Options
% -----------------------------------------------------------------------------
\RequirePackage{kvoptions}
\RequirePackage{etoolbox}

\SetupKeyvalOptions{family=checklist,prefix=checklist@}
\DeclareStringOption[4]{papersize}
\DeclareBoolOption[false]{legal_disclaimer}
\ProcessKeyvalOptions*

% Legal disclaimer toggle
\newif\if@legaldisclaimer
\ifboolexpr{ bool {checklist@legal_disclaimer} }{\@legaldisclaimertrue}{\@legaldisclaimerfalse}

% Papersize mapping
\def\checklist@papersizeint{4} % default a4double
\DeclareOption{a4double}{\def\checklist@papersizeint{4}}
\DeclareOption{a5double}{\def\checklist@papersizeint{5}}
\DeclareOption{a6double}{\def\checklist@papersizeint{6}}
\DeclareOption{a6single}{\def\checklist@papersizeint{7}}

% Pass unknown options to article
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{article}}
\ProcessOptions\relax

% -----------------------------------------------------------------------------
% Base class
% -----------------------------------------------------------------------------
\ifnum\checklist@papersizeint=4
  \LoadClass[12pt]{article}
\else
  \LoadClass[10pt]{article}
\fi

% -----------------------------------------------------------------------------
% Packages
% -----------------------------------------------------------------------------
% Core
\RequirePackage{ifthen}
\RequirePackage{geometry}
\RequirePackage{environ}
\RequirePackage{fancyhdr}

% Tables & graphics
\RequirePackage{multirow}
\RequirePackage{booktabs}
\RequirePackage{tikz}
\RequirePackage{xcolor}
\RequirePackage{colortbl}
\RequirePackage{tcolorbox}
\RequirePackage{graphicx}

% Other utilities
\RequirePackage{lastpage}
\RequirePackage[T1]{fontenc}
\RequirePackage{microtype}
\usepackage{textcomp}

% Fonts
\IfFileExists{cuprum.sty}{
  \RequirePackage{cuprum}
}{
  \RequirePackage{lmodern}
}

% -----------------------------------------------------------------------------
% Document layout
% -----------------------------------------------------------------------------
\setlength{\parindent}{0pt}

% Geometry settings per papersize
\ifnum\checklist@papersizeint=4
  \geometry{a4paper,twocolumn,total={192mm,280mm},includehead,headsep=5mm,top=5mm,left=10mm,footskip=5mm,marginparwidth=0mm,marginparsep=0mm}
\else\ifnum\checklist@papersizeint=5
  \geometry{a5paper,twocolumn,total={130mm,190mm},includehead,headsep=5mm,top=5mm,left=10mm,footskip=5mm,marginparwidth=0mm,marginparsep=0mm}
\else\ifnum\checklist@papersizeint=6
  \geometry{a6paper,twocolumn,total={95.5mm,130mm},includehead,headsep=2mm,top=5mm,left=5mm,footskip=5mm,marginparwidth=0mm,marginparsep=0mm}
\else\ifnum\checklist@papersizeint=7
  \geometry{a6paper,total={80.5mm,130mm},includehead,headsep=2mm,top=5mm,left=15mm,footskip=5mm,marginparwidth=0mm,marginparsep=0mm}
\fi\fi\fi\fi

% -----------------------------------------------------------------------------
% Checklist styling & environments
% -----------------------------------------------------------------------------
\tcbsetforeverylayer{colback=white,colframe=black,arc=0mm,outer arc=0mm}

\newcommand{\checkbox}{\makebox[3ex][r]{\Large\(\square\)}}

\NewDocumentEnvironment{checklist}{m O{} +b}{%
  \def\checklist@nametmp{#1}%
  % Redefine item macros
  \let\checkitem\relax\newcommand{\checkitem}[2]{##1\dotfill\makebox{\uppercase{##2}}\par}%
  \let\notes\relax\newcommand{\notes}[1]{{\small\hspace*{0.8em}##1}\par}%
  \let\decision\relax\newcommand{\decision}[1]{\textbf{##1}\\}%
  \let\vertbar\relax\newcommand\vertbar{\kern1pt\rule[-\dp\strutbox]{.8pt}{\baselineskip}\kern1pt}%
  \let\step\relax\newcommand{\step}[1]{\hspace*{0.5em}\vertbar\hspace*{\labelsep}##1\\}%
  \let\lowersection\relax\newcommand{\lowersection}[1]{\tcblower\textbf{##1}\vspace*{0.5em}\\}%
  \let\detailitem\relax\newcommand{\detailitem}[2]{\par\smallskip\noindent\hrule
     \vspace{0.25\baselineskip}\centerline{\textbf{##1}}\vspace{0.25\baselineskip}\par
     \noindent ##2 \par\vspace{0.25\baselineskip}\hrule\par\vspace{0.25\baselineskip}\medskip}%
  \begin{tcolorbox}[title=\textbf{\uppercase{\checklist@nametmp}},colback=white,colframe=black,#2]%
    #3
  \end{tcolorbox}%
}{}

% -----------------------------------------------------------------------------
% Metadata
% -----------------------------------------------------------------------------
\newcommand\checklist@name{}
\newcommand\checklist@description{}
\newcommand\checklist@logo{}
\newcommand\checklist@revision{}
\newcommand\checklist@issuedate{}

\newcommand{\checklistName}[1]{\gdef\checklist@name{#1}}
\newcommand{\checklistDescription}[1]{\gdef\checklist@description{#1}}
\newcommand{\checklistLogo}[1]{\gdef\checklist@logo{#1}}
\newcommand{\checklistRevision}[1]{\gdef\checklist@revision{#1}}
\newcommand{\checklistDateIssue}[1]{\gdef\checklist@issuedate{#1}}

% -----------------------------------------------------------------------------
% Titlepage
% -----------------------------------------------------------------------------
\renewcommand{\maketitle}{%
  \begin{titlepage}
    \centering
    {\Huge\bfseries \checklist@name \par}
    \vspace{0.5cm}

    \if\relax\detokenize\expandafter{\checklist@description}\relax
    % No description specified, do nothing
    \else
      {\Large\bfseries \checklist@description \par}
      \vspace{0.5cm}
    \fi

    \if\relax\detokenize\expandafter{\checklist@revision}\relax
    % No revision specified, do nothing
    \else
      {\Large Revision: \checklist@revision \par}
      \vspace{0.5cm}
    \fi

    \if\relax\detokenize\expandafter{\checklist@issuedate}\relax
    % No issue date specified, do nothing
    \else
      {\Large Date Issued: \checklist@issuedate \par}
      \vspace{0.5cm}
    \fi

    \if@legaldisclaimer
      \vspace{1cm}
      \begin{tcolorbox}[colback=yellow,colframe=black,arc=1mm]
        {\small This document is for reference only and does not replace the official Pilot Operating Handbook.\par Dieses Dokument dient nur zur Referenz und ersetzt nicht das offizielle Flughandbuch.}
      \end{tcolorbox}\vspace{1cm}
    \fi

    \if\relax\detokenize\expandafter{\checklist@logo}\relax
    % No logo specified, do nothing
    \else
      {\includegraphics[height=4cm]{\checklist@logo}\par}
    \fi

    \vfill

  \end{titlepage}
}

% -----------------------------------------------------------------------------
% Header & footer
% -----------------------------------------------------------------------------
\pagestyle{fancy}
\fancyhf{}
\renewcommand\headrulewidth{0.4pt}
\fancyhead[L]{\protect\checklist@name/\protect\currentchaptype}
\fancyhead[R]{\ifnum\value{section}>0 \thesection\quad\protect\currentsection\fi}
\fancyfoot[L]{\textcolor{lightgray}{\footnotesize Revision \checklist@revision}}
\fancyfoot[C]{\textcolor{lightgray}{\footnotesize\thepage\ of \pageref{LastPage}}}
\fancyfoot[R]{\textcolor{lightgray}{\footnotesize \checklist@issuedate}}

% -----------------------------------------------------------------------------
% Counters & chapter management
% -----------------------------------------------------------------------------
\newcounter{chapter}
\@addtoreset{section}{chapter}
\renewcommand\thechapter{\arabic{chapter}}
\renewcommand\thesection{\thechapter.\arabic{section}}

\newcommand\currentchaptype{}
\newcommand\currentsection{}

\newcommand\setchaptype[1]{%
  \clearpage
  \refstepcounter{chapter}%
  \setcounter{section}{0}%
  \renewcommand\currentchaptype{#1}%
  \renewcommand\currentsection{}%
  {\thispagestyle{empty}%
    \vspace*{\fill}%
    \begin{center}\Huge\bfseries #1\end{center}%
    \vspace*{\fill}%
    \clearpage
  }%
}

\newcommand\normalchapter{\setchaptype{Normal}}
\newcommand\abnormalchapter{\setchaptype{Abnormal}}
\newcommand\emergencychapter{\setchaptype{Emergency}}

\providecommand\chapter[1]{%
  \PackageError{checklist}{Invalid chapter}{%
    Use \string\normalchapter, \string\abnormalchapter\space or
    \string\emergencychapter\space instead}%
}

% -----------------------------------------------------------------------------
% Section handling
% -----------------------------------------------------------------------------
\renewcommand\section[1]{%
  \clearpage
  \refstepcounter{section}%
  \renewcommand\currentsection{#1}%
  {\noindent\bfseries\thesection\quad #1\par\medskip}%
}

\makeatother
