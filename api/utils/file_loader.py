# api/file_loader.py
import time
import logging
from langchain_community.document_loaders import PyMuPDFLoader, TextLoader

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Load PDF or TXT file (extract relevant sections)
def load_document(path: str, max_pages=3) -> str:
    start_time = time.time()
    if path.endswith(".pdf"):
        loader = PyMuPDFLoader(path)
        text = loader.load()[0].page_content[:max_pages * 1000]  # Limit to first few pages
    elif path.endswith(".txt"):
        text = TextLoader(path).load()[0].page_content
    else:
        raise ValueError("Unsupported file type: only .pdf and .txt are supported.")
    end_time = time.time()
    logger.info(f"Document loaded from {path} in {end_time - start_time:.2f} seconds")
    return text
