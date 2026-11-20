
import re
import hashlib

from io import BytesIO
from pathlib import Path
from pypdf import PdfReader
from langchain_core.documents import Document

def make_doc_id(filename: str, data: bytes) -> str:
    """Builds a stable id for a document from its name and contents.

    The same file always gets the same id, so re-uploading a PDF overwrites its
    chunks instead of duplicating them.

    Args:
        filename: The uploaded file's name.
        data: The file's bytes.

    Returns:
        The slugified file stem plus the first six hex digits of its SHA-256,
        for example `paddy-cultivation-guide-a29d87`.
    """
    stem = re.sub(r"[^a-z0-9]+", "-", Path(filename).stem.lower()).strip("-")
    digest = hashlib.sha256(data).hexdigest()[:6]
    return f"{stem}-{digest}"


def read_pdf(data: bytes, metadata: dict) -> list[Document]:
    pdf = PdfReader(BytesIO(data))

    return [
        Document(
            page_content=text, metadata={**metadata, "page": number}
        )
        for number, page in enumerate(pdf.pages, start=1)
        if (text := page.extract_text()) and text.strip() #Wulrus Operator ' := '
    ]


