from langchain_community.vectorstores import FAISS
from app.embeddings import get_embeddings


_retriever = None


def get_retriever():

    global _retriever

    if _retriever is None:

        embeddings = get_embeddings()

        vector_store = FAISS.load_local(
            "data/vectorstore",
            embeddings,
            allow_dangerous_deserialization=True
        )

        _retriever = vector_store.as_retriever(
            search_kwargs={"k": 4}
        )

    return _retriever