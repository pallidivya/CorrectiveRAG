from app.retriever import get_retriever
from app.answer_generator import generate_answer
from app.answer_auditor import audit_answer


question = "What is Machine Learning?"

retriever = get_retriever()

documents = retriever.invoke(question)

answer = generate_answer(
    question,
    documents
)

audit_result = audit_answer(
    question,
    answer,
    documents
)

print("\n==============================")
print("GENERATED ANSWER")
print("==============================")

print(answer)

print("\n==============================")
print("ANSWER AUDIT")
print("==============================")

print(audit_result)