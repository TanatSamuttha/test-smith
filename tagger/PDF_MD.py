from fastapi import UploadFile
from tempfile import SpooledTemporaryFile
import fitz

# Receive pdf and return string
async def convert_pdf_to_markdown_string(file: UploadFile) -> str:
    print("Called")
    pdf_bytes = await file.read()
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")

    text = ""
    for i, page in enumerate(doc):
        text += f"\n" + page.get_text()

    markdown_string = plain_text_to_markdown(text)

    return markdown_string

# Receive pdf and return md
async def convert_pdf_to_markdown_file(file: UploadFile) -> SpooledTemporaryFile:
    pdf_bytes = await file.read()
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")

    text = ""
    for i, page in enumerate(doc):
        text += f"\n" + page.get_text()

    markdown_text = plain_text_to_markdown(text)

    temp_md = SpooledTemporaryFile()
    temp_md.write(markdown_text.encode("utf-8"))
    temp_md.seek(0)

    return temp_md

# Convert formatless string to md form string
def plain_text_to_markdown(text: str) -> str:
    md_lines = [
        ("## " + line.strip()) if line.strip().endswith(":")
        else ("- " + line.strip()[1:].strip()) if line.strip().startswith("•")
        else line
        for line in text.splitlines()
    ]
    return "\n".join(md_lines)

