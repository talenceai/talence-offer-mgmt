import pdfkit
import os
from uuid import uuid4
from pathlib import Path
from jinja2 import Template

def generate_offer_pdf(template_html, offer_data, candidate_id, job_id):
    # ✅ Step 1: Render Jinja2 template with offer_data
    template = Template(template_html)
    rendered_html = template.render(**offer_data)

    # ✅ Step 2: Save to /static/pdfs/
    output_dir = Path("static/pdfs")
    output_dir.mkdir(parents=True, exist_ok=True)

    file_name = f"{uuid4()}.pdf"
    file_path = output_dir / file_name

    # ✅ Step 3: Convert HTML → PDF using wkhtmltopdf
    config = pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf')  # ✅ your path is correct
    pdfkit.from_string(rendered_html, str(file_path), configuration=config)

    # ✅ Step 4: Return path to store in DB
    return f"/static/pdfs/{file_name}"
