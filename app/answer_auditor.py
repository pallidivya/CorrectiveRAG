from langchain_core.prompts import ChatPromptTemplate
from app.llm import get_llm


def audit_answer(question, answer, documents):

    context = "\n\n".join(
        document.page_content
        for document in documents
    )

    prompt = ChatPromptTemplate.from_template(
        """
You are a strict but fair quality auditor for a Retrieval-Augmented
Generation (RAG) system.

Your job is to verify whether the generated answer correctly answers
the user's question using only the provided context.

Question:
{question}

Context:
{context}

Answer:
{answer}

Evaluate the answer using these rules:

1. Faithfulness:
   - Every factual claim in the answer must be supported by the context.
   - If the answer contains factual information that is not supported
     by the context, mark faithful: no.
   - Do not mark an answer unfaithful merely because it is shorter
     than the context.

2. Relevance:
   - The answer must directly address the user's question.
   - Minor additional information is acceptable if it is related to
     the question.
   - If the answer contains substantial unrelated information,
     mark relevant: no.

3. Completeness:
   - Judge completeness based primarily on the QUESTION, not on
     whether every detail from the context was included.
   - A concise answer can be complete if it sufficiently answers
     the question.
   - Do NOT require the answer to include all information contained
     in the context.
   - For questions asking for a specific number, list, categories,
     steps, comparison, or multiple parts, make sure the required
     items are included.
   - If the question asks for N items and the answer claims there
     are N items but provides fewer than N, mark complete: no.
   - If the question can be answered with a definition or short
     explanation, do not mark complete: no simply because additional
     examples or details exist in the context.
   - If the answer clearly fails to address an important part of
     the question, mark complete: no.

Important:
- Evaluate the answer against the user's question.
- Do not expect the answer to reproduce the context.
- Do not add information that is not present in the answer.
- Do not give the answer yourself.
- Be strict about unsupported claims, but fair about concise answers.

Respond ONLY in exactly this format:

faithful: yes/no
relevant: yes/no
complete: yes/no
"""
    )

    llm = get_llm()

    chain = prompt | llm

    response = chain.invoke({
        "question": question,
        "context": context,
        "answer": answer
    })

    return response.content.strip()