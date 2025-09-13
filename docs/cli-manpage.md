% CHECKLIST(1) | User Commands
% miss-sophie
% September 2025

# NAME

**checklist** — Aviation checklist management toolkit (YAML, ForeFlight .fmd, LaTeX)

# SYNOPSIS

**checklist** [*COMMAND*] [*OPTIONS*] [*ARGS*...]

A modular, extensible Python package and CLI for managing aircraft checklists. Supports conversion between YAML, ForeFlight `.fmd`, and LaTeX formats.

# DESCRIPTION

The **checklist** tool provides a workflow for maintaining aircraft checklists in a single editable YAML format, exporting them to ForeFlight’s encrypted `.fmd` format for mobile use, and rendering high-quality printable PDF documents using LaTeX.

Checklist data is authorable and version-controlled as YAML, then converted or rendered as needed:

- **YAML**: Human-editable source format ([see YAML spec](docs/yaml-checklist-file-format-spec.md))
- **ForeFlight .fmd**: Encrypted binary format for ForeFlight mobile import ([see FMD spec](docs/fmd-file-format-spec.md))
- **LaTeX**: Structured, styled printable checklists ([see class documentation](docs/checklist_cls.md))

# COMMANDS

The CLI supports the following subcommands:

## import-fmd

> Import a ForeFlight `.fmd` file and convert to YAML.

**Usage:**
```
checklist import-fmd input.fmd output.yaml
```

- `input.fmd` — Path to ForeFlight `.fmd` file
- `output.yaml` — Destination for converted YAML

## export-fmd

> Export a YAML checklist file to ForeFlight `.fmd` format.

**Usage:**
```
checklist export-fmd input.yaml output.fmd
```

- `input.yaml` — Source YAML checklist
- `output.fmd` — Destination ForeFlight file

## render-latex

> Render a LaTeX `.tex` document from a YAML checklist for printing.

**Usage:**
```
checklist render-latex input.yaml output.tex [--papersize SIZE] [--use-sections] [--legal_disclaimer]
```

- `input.yaml` — Source YAML checklist
- `output.tex` — Destination LaTeX file
- `--papersize SIZE` — Paper size (`a4double`, `a5double`, `a6single`, etc.; default: `a6single`)
- `--use-sections` — Add section headers for subgroups
- `--legal_disclaimer` — Include legal disclaimer on title page

# FILE FORMATS

## YAML Checklist Format

- See [docs/yaml-checklist-file-format-spec.md](docs/yaml-checklist-file-format-spec.md)
- Top-level fields: `checklist_name`, `tailNumber`, `detail`, `schemaVersion`, `categories`
- Hierarchy: categories → groups → checklists → items

## ForeFlight `.fmd` Format

- See [docs/fmd-file-format-spec.md](docs/fmd-file-format-spec.md)
- Encrypted JSON, AES-128 CBC, PKCS#7 padding
- Hierarchy matches YAML, with metadata and UUIDs for sync

## LaTeX Checklist Format

- See [docs/checklist_cls.md](docs/checklist_cls.md)
- Uses `checklist.cls` class for chapters, environments, metadata, and styling

# EXAMPLES

## Example YAML to PDF workflow

```bash
checklist render-latex my_checklist.yaml my_checklist.tex --papersize a4double --use-sections
xelatex -output-directory=build my_checklist.tex
```

## Example YAML to ForeFlight

```bash
checklist export-fmd my_checklist.yaml my_checklist.fmd
```

## Example ForeFlight to YAML

```bash
checklist import-fmd my_checklist.fmd my_checklist.yaml
```

# OPTIONS

For all commands:

- `--help` — Show usage information

For `render-latex`:

- `--papersize SIZE` — Choose document size/layout (see [class docs](docs/checklist_cls.md))
- `--use-sections` — Enable section headers per subgroup
- `--legal_disclaimer` — Add POH disclaimer box to title page

# ENVIRONMENT

- Requires Python 3.8+
- Dependencies: PyYAML, pycryptodome, jinja2
- For LaTeX rendering: A working TeX/LaTeX environment (`xelatex` recommended)

# SEE ALSO

- [docs/yaml-checklist-file-format-spec.md](docs/yaml-checklist-file-format-spec.md) — YAML schema
- [docs/fmd-file-format-spec.md](docs/fmd-file-format-spec.md) — ForeFlight file format details
- [docs/checklist_cls.md](docs/checklist_cls.md) — LaTeX class documentation
- [README.md](README.md) — Project overview and example

# AUTHOR

Written and maintained by **miss-sophie**

# BUGS

Report issues or feature requests via the [GitHub repository](https://github.com/miss-sophie/checklists).

# COPYRIGHT

MIT License. See repository for details.