from typing import Optional, Dict, Any

from jinja2 import Environment, select_autoescape, FileSystemLoader

env = Environment(
    loader=FileSystemLoader("templates"),
    autoescape=select_autoescape(["html"]),
    trim_blocks=True,
    lstrip_blocks=True,
)


def render_template(name: str, values: Optional[Dict[str, Any]] = None, **kwargs: object):
    """
    Renders template & returns texts
    :param language:
    :param name: Name of template
    :param values: Values for template (optional)
    :param kwargs: Keyword-arguments for template (high-priority)
    """
    template = env.get_template(f'{name}')
    if values:
        rendered_template = template.render(values, **kwargs)
    else:
        rendered_template = template.render(**kwargs)
    return rendered_template


