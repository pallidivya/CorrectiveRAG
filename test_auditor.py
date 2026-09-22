from app.answer_auditor import audit_answer


question = "What is Machine Learning?"

answer = (
    "Machine Learning is a computational approach in which algorithms "
    "learn patterns from data and improve their performance on a task "
    "through experience."
)


documents = [
    type(
        "Document",
        (),
        {
            "page_content": (
                "Machine Learning is a computational approach in which "
                "algorithms learn patterns from data and improve their "
                "performance on a task through experience."
            )
        },
    )()
]


result = audit_answer(
    question,
    answer,
    documents
)


print("\n==============================")
print("AUDITOR RESULT")
print("==============================")
print(result)