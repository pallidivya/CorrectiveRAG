from langchain_core.prompts import ChatPromptTemplate
from app.llm import get_llm


def generate_answer(question, documents):

    context = "\n\n".join(
        document.page_content
        for document in documents
    )

    prompt = ChatPromptTemplate.from_template(
        """
You are a precise question-answering assistant for a RAG system.

Answer the user's question using ONLY the provided context.

Important rules:

1. Use only information supported by the context.
2. Answer every part of the question.
3. If the question asks for types, categories, steps, differences,
   or multiple items, include ALL relevant items supported by the context.
4. Do not claim a number of items unless you actually list that number.
5. Do not invent information.
6. Keep the answer clear and concise.
7. If the answer cannot be found in the context, say:
   "I don't have enough information in the provided documents."

Context:
{context}

Question:
{question}

Answer:
"""
    )

    llm = get_llm()

    chain = prompt | llm

    response = chain.invoke({
        "context": context,
        "question": question
    })

    return response.content