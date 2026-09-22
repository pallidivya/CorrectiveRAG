from langchain_core.prompts import ChatPromptTemplate
from app.llm import get_llm


def rewrite_query(question):

    prompt = ChatPromptTemplate.from_template(
        """
You are a query rewriting assistant.

Rewrite the user's question so that it is clearer and
more useful for retrieving relevant information from documents.

Keep the original meaning.

Return ONLY the rewritten question.
Do not provide an answer.

Original question:
{question}

Rewritten question:
"""
    )

    llm = get_llm()

    chain = prompt | llm

    response = chain.invoke({
        "question": question
    })

    return response.content.strip()