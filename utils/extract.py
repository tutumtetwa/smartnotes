from PyPDF2 import PdfReader
from docx import Document

def extract_text_from_file(file):
    if file.filename.endswith('.pdf'):
        reader = PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text() or ''
        return text

    elif file.filename.endswith('.docx'):
        doc = Document(file)
        return '\n'.join(p.text for p in doc.paragraphs)

    elif file.filename.endswith(('.txt', '.md')):
        return file.read().decode('utf-8')

    return ''
