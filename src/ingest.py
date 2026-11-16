from pathlib import Path
import io

def extract_pdf(uploaded_file) -> str:
    try:
        from pypdf import PdfReader
        reader = PdfReader(io.BytesIO(uploaded_file.getvalue()))
        return "\n\n".join(page.extract_text() or "" for page in reader.pages).strip()
    except Exception as exc:
        raise RuntimeError(f"Could not read this PDF: {exc}") from exc

def extract_docx(uploaded_file) -> str:
    from docx import Document
    doc = Document(io.BytesIO(uploaded_file.getvalue()))
    return "\n".join(p.text for p in doc.paragraphs)

def extract_pptx(uploaded_file) -> str:
    from pptx import Presentation
    prs = Presentation(io.BytesIO(uploaded_file.getvalue()))
    chunks = []
    for i, slide in enumerate(prs.slides, 1):
        lines = [shape.text for shape in slide.shapes if hasattr(shape, "text_frame") and shape.text.strip()]
        chunks.append(f"SLIDE {i}\n" + "\n".join(lines))
    return "\n\n".join(chunks)

def extract_text(uploaded_file) -> str:
    name = uploaded_file.name.lower()
    if name.endswith(".pdf"):
        return extract_pdf(uploaded_file)
    if name.endswith(".docx"):
        return extract_docx(uploaded_file)
    if name.endswith((".pptx", ".ppt")):
        if name.endswith(".ppt"):
            raise ValueError("Legacy .ppt is not supported yet. Save it as .pptx and upload again.")
        return extract_pptx(uploaded_file)
    if name.endswith((".txt", ".md", ".csv")):
        return uploaded_file.getvalue().decode("utf-8", errors="replace")
    raise ValueError("Supported files: PDF, DOCX, PPTX, TXT, MD and CSV.")
