from langchain_ollama import ChatOllama


_llm = None


def get_llm():

    global _llm

    if _llm is None:

        _llm = ChatOllama(
            model="llama3.2:3b",
            temperature=0
        )

    return _llm