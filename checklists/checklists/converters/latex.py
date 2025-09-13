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

def render_checklist_tex(yaml_path: Path, output_path: Path, use_sections: bool, papersize: str, legal_disclaimer: bool) -> None:
    # Locate the template relative to the repo structure
    template_path = Path(__file__).parent.parent / "templates" / "checklist.tex.j2"
    if not template_path.exists():
        raise FileNotFoundError(f"Template not found: {template_path}")

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