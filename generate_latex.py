#!/usr/bin/env python3
"""
Render LaTeX QRH from YAML using Jinja2 templates.
Usage:
  python render_checklist.py input.yaml checklist.tex.j2 output.tex [--use-sections]
"""
import argparse
import re
import yaml
from pathlib import Path
from jinja2 import Environment, FileSystemLoader


def latex_escape(text):
    if not isinstance(text, str):
        return text
    escape_map = {
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '°': r'\textdegree ',
        '~': r'\textasciitilde{}',
        '^': r'\textasciicircum{}',
        '\\': r'\textbackslash{}',
    }
    return re.sub(r'([&%$#_{}~^\\°])', lambda m: escape_map[m.group()], text)


def render_checklist_tex(yaml_path: Path, template_path: Path, output_path: Path, use_sections: bool, papersize: int, legal_disclaimer: bool) -> None:
    data = yaml.safe_load(yaml_path.read_text(encoding="utf-8"))
    data["use_sections"] = use_sections
    data["papersize"] = papersize
    data["legal_disclaimer"] = legal_disclaimer

    env = Environment(
        loader=FileSystemLoader(template_path.parent),
        autoescape=False,
        trim_blocks=True,
        lstrip_blocks=True
    )
    env.filters["e"] = latex_escape

    template = env.get_template(template_path.name)
    tex_content = template.render(**data)
    output_path.write_text(tex_content, encoding="utf-8")
    print(f"Rendered: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Render LaTeX QRH from YAML using Jinja2.")
    parser.add_argument("yaml", type=Path, help="Input YAML checklist")
    parser.add_argument("template", type=Path, help="Jinja2 LaTeX template")
    parser.add_argument("output", type=Path, help="Output .tex file")
    parser.add_argument("--papersize", type=str, default="a6single", help="Papersize to use. Supported range: 4-7")
    parser.add_argument("--use-sections", action="store_true", help="Include section headers for checklist subgroups")
    parser.add_argument("--legal_disclaimer", action="store_true", help="Include legal disclaimer on tile page")


    args = parser.parse_args()

    render_checklist_tex(args.yaml, args.template, args.output, args.use_sections, args.papersize, args.legal_disclaimer)


if __name__ == "__main__":
    main()
