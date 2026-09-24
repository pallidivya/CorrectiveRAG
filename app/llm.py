import os

from langchain_ollama import ChatOllama
from langchain_groq import ChatGroq


_llm = None


def get_llm():

    global _llm

    if _llm is None:

        provider = os.getenv(
            "LLM_PROVIDER",
            "ollama"
        ).lower()

        if provider == "groq":

            _llm = ChatGroq(
                model=os.getenv(
                    "GROQ_MODEL",
                    "llama-3.1-8b-instant"
                ),
                temperature=0,
                api_key=os.getenv("GROQ_API_KEY")
            )

        else:

            _llm = ChatOllama(
                model="llama3.2:3b",
                temperature=0
            )

    return _llm