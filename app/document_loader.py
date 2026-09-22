from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader


def load_documents():
    documents_path = Path("data/documents")

    documents = []

    for pdf_file in documents_path.glob("*.pdf"):
        print(f"Loading: {pdf_file.name}")

        loader = PyPDFLoader(str(pdf_file))
        pdf_documents = loader.load()

        documents.extend(pdf_documents)

    print(f"Total pages loaded: {len(documents)}")

    return documents