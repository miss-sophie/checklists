import argparse
from pathlib import Path
import sys

from .converters import foreflight
from .converters import latex
def main():
    parser = argparse.ArgumentParser(
        description="Aviation checklist management suite (YAML, ForeFlight .fmd, LaTeX)"
    )
    subparsers = parser.add_subparsers(dest='command', required=True)

    # import-fmd: FMD -> YAML
    sp_import = subparsers.add_parser('import-fmd', help='Import ForeFlight .fmd to YAML')
    sp_import.add_argument('fmd', type=Path, help='Input .fmd file path')
    sp_import.add_argument('yaml', type=Path, help='Output YAML file path')

    # export-fmd: YAML -> FMD
    sp_export = subparsers.add_parser('export-fmd', help='Export YAML to ForeFlight .fmd')
    sp_export.add_argument('yaml', type=Path, help='Input YAML file path')
    sp_export.add_argument('fmd', type=Path, help='Output .fmd file path')

    # render-latex: YAML -> LaTeX .tex
    sp_render = subparsers.add_parser('render-latex', help='Render LaTeX checklist from YAML')
    sp_render.add_argument('yaml', type=Path, help='Input YAML checklist')
    sp_render.add_argument('output', type=Path, help='Output .tex file')
    sp_render.add_argument('--papersize', type=str, default="a6single", help='Paper size for document')
    sp_render.add_argument('--use-sections', action='store_true', help='Include section headers for subgroups')
    sp_render.add_argument('--legal_disclaimer', action='store_true', help='Include legal disclaimer on title page')

    args = parser.parse_args()

    if args.command == 'import-fmd':
        foreflight.import_fmd_to_yaml(args.fmd, args.yaml)
        print(f"Imported {args.fmd} -> {args.yaml}")
    elif args.command == 'export-fmd':
        foreflight.export_yaml_to_fmd(args.yaml, args.fmd)
        print(f"Exported {args.yaml} -> {args.fmd}")
    elif args.command == 'render-latex':
        latex.render_checklist_tex(
            yaml_path=args.yaml,
            output_path=args.output,
            use_sections=args.use_sections,
            papersize=args.papersize,
            legal_disclaimer=args.legal_disclaimer
        )

if __name__ == '__main__':
    main()