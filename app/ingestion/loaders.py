import pdfplumber
from docx import Document
from app.utils.logger import get_logger

logger = get_logger(__name__)

def load_pdf(file_path: str) -> str:
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
            
            # Extract underlying hyperlinks (like mailto: emails or URLs)
            if page.hyperlinks:
                for link in page.hyperlinks:
                    uri = link.get("uri")
                    if uri:
                        if uri.startswith("mailto:"):
                            text += f"\nContact Email: {uri.replace('mailto:', '')}\n"
                        else:
                            text += f"\nLink: {uri}\n"
    return text

def load_docx(file_path: str) -> str:
    doc = Document(file_path)
    return "\n".join(p.text for p in doc.paragraphs if p.text.strip())

def load_txt(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()

def load_document(file_path: str, filename: str) -> str:
    try:
        if filename.lower().endswith(".pdf"):
            return load_pdf(file_path)
        elif filename.lower().endswith(".docx"):
            return load_docx(file_path)
        elif filename.lower().endswith(".txt"):
            return load_txt(file_path)
        else:
            raise ValueError(f"Unsupported file type: {filename}")
    except Exception as e:
        logger.error(f"Failed to load {filename}: {e}")
        raise