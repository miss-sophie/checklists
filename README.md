# Checklists template in LaTeX

![Example Checklist](example_checklist_1.jpg)
![Example Checklist](example_checklist_2.jpg)


This is a simple set of LaTex files to produce nice PDF formatted checklists.

You need to have a LaTex environment set up with `xelatex` and `ttfutils` available.

## Creating a checklist

First create a file called `checklist.tex` on source directory. You can use any name as long the
file has the extension `.tex`.

Here's an example of a simple checklist:

```Tex
\def\papersize{4}
\input{preamble.inc}

\begin{document}

\title{Example}
\versionchecklist{1}
\datechecklist{25.10.2024}

\begin{checklist}{Checklist Name}
  \item{Checkitem 1}{result}
  \item{Checkitem 2}{another result}
    \hint{I am a hint!}
  \decision{Decision: Cold}
    \step{Step: 1}
    \step{Step: Math is hard...}
  \decision{Decision: Warm}
    \step{Heater: Off}
    \item{Checkitem 3}{result}
\end{checklist}

\end{document}
```

## Supported Variables and Elements
| Type        | Name       | Usage                                                                        | Parameter            |
|-------------|------------|------------------------------------------------------------------------------|----------------------|
| Environment | checklist  | Defines the base environment for all further commands.                       | checklist_name       |
| Command     | item       | Base element for checklist, representing an individual step.                 | item_name, condition |
| Command     | hint       | Indented paragraph, used for notes within a step.                            | hint_text            |
| Command     | decision   | Creates a decision header.                                                   | decision_name        |
| Command     | step       | Subelement for decision, representing an indivudual step withing a decision. | item_name, condition |
| Parameter   | title      | Title of the entire checklist, printed on top of the page.                   | checklist_name       |
| Parameter   | versionchecklist | Version of the checklist                                               | checklist_version    |
| Paramter    | datechecklist    | Date when the version of this checklist was released                   | checklist_date       |

## Build process
After this, running `make all` should output a PDF file on `pdf/` directory, which
will look similar to this:

You will find templates wihtin the `source` directory.
