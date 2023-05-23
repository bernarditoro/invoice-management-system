from django.template.loader import get_template

from weasyprint import HTML


def generate_pdf(template: str, context: dict, stylesheets: list = [], **kwargs):
    html_template = get_template(template)

    rendered_html = html_template.render(context)

    return HTML(string=rendered_html).write_pdf(stylesheets=stylesheets)
