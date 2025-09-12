# Checklists template in LaTeX
Welcome to checklists — your toolkit for creating structured, print-ready checklists. Whether you’re documenting preflight procedures, emergency protocols, or the occasional intergalactic unicorn adventure, this class makes it easy to organize, style, and color your checklists professionally.

### Key Features:

| Feature        | Description                                                                                                                                          |
| -------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| **YAML**       | Define checklists in YAML and render them to LaTeX or FMD. Maintain editable, shareable checklist data.                                              |
| **LaTeX**      | Create structured, print-ready checklists with `checklist.cls`. Supports multiple paper sizes, chapters, metadata, and customizable checklist boxes. |
| **ForeFlight** | Import checklists from ForeFlight and convert them into YAML, or export YAML checklists to ForeFlight format.                                        |



You need to have a LaTex environment set up with `xelatex` and `ttfutils` available.



## 📖 TeX
Please refer to the [docs](docs/checklist_cls.md) for all available options.

### Example Document
```latex
\documentclass[a4double,legal_disclaimer]{checklist}

\checklistName{Diamond DA20-A1 Checklist}
\checklistDescription{Normal, Abnormal, Emergency}
\checklistRevision{1.0}
\checklistDateIssue{2025-09-12}
\checklistLogo{logo.pdf}

\begin{document}
\maketitle

\normalchapter
\section{Preflight}
\begin{checklist}{Exterior Inspection}[colback=blue!5,colframe=black]
  \checkitem{Aircraft Papers}{CHECKED}
  \checkitem{Fuel}{CHECK}
  \notes{Drain fuel samples from both tanks}
\end{checklist}

\end{document}
```

![Example Checklist](./sample/sample.jpg)