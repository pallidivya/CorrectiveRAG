from langchain_community.vectorstores import FAISS
from app.embeddings import get_embeddings


def create_vector_store(chunks):

    embeddings = get_embeddings()

    vector_store = FAISS.from_documents(
        documents=chunks,
        embedding=embeddings
    )

    vector_store.save_local("data/vectorstore")

    print("FAISS vector store created successfully.")

    return vector_store