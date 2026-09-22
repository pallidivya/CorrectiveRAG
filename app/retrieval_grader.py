from langchain_core.prompts import ChatPromptTemplate
from app.llm import get_llm


def grade_document(question, document):

    prompt = ChatPromptTemplate.from_template(
        """
You are a document relevance grader.

Your task is to determine whether the given document
contains information that is relevant to answering the question.

Question:
{question}

Document:
{document}

Respond with ONLY one word:

yes

or

no
"""
    )

    llm = get_llm()

    chain = prompt | llm

    response = chain.invoke({
        "question": question,
        "document": document.page_content
    })

    result = response.content.strip().lower()

    if "yes" in result:
        return True

    return False