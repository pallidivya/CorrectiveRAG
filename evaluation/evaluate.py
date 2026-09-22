from app.corrective_rag import corrective_rag


test_questions = [
    {
        "question": "What is Machine Learning?",
        "expected": "answer"
    },
    {
        "question": "What are the types of Machine Learning?",
        "expected": "answer"
    },
    {
        "question": "What is supervised learning?",
        "expected": "answer"
    },
    {
        "question": "What is unsupervised learning?",
        "expected": "answer"
    },
    {
        "question": "What is the difference between supervised and unsupervised learning?",
        "expected": "answer"
    },
    {
        "question": "What is a machine learning algorithm?",
        "expected": "answer"
    },
    {
        "question": "What are the health benefits of eating apples?",
        "expected": "reject"
    },
    {
        "question": "What is quantum computing?",
        "expected": "reject"
    },
    {
        "question": "How does photosynthesis work?",
        "expected": "reject"
    },
    {
        "question": "What is the capital of France?",
        "expected": "reject"
    }
]


# Basic evaluation counters
correct = 0

# Retrieval metrics
total_retrieved = 0
total_relevant = 0
answerable_questions = 0

# Correction metric
corrections_used = 0
correction_successes = 0
audit_passes = 0
auditable_questions = 0

for item in test_questions:

    question = item["question"]
    expected = item["expected"]
    if expected == "answer":
        answerable_questions += 1
        auditable_questions += 1

    print("\n==============================")
    print("QUESTION:", question)
    print("EXPECTED:", expected)
    print("==============================")

    answer, documents, stats = corrective_rag(question)

    print("\nSYSTEM ANSWER:")
    print(answer)

    print("\nEVALUATION STATS:")

    print("Attempts:", stats["attempts"])

    print(
        "Retrieved documents:",
        stats["retrieved_documents"]
    )

    print(
        "Relevant documents:",
        stats["relevant_documents"]
    )

    print(
        "Correction used:",
        stats["correction_used"]
    )

    print(
        "Audit passed:",
        stats["audit_passed"]
    )

    if stats["audit_passed"]:
        audit_passes +=1

    # Count whether correction was used
    if stats["correction_used"]:
        corrections_used += 1
        if expected == "answer" and stats["audit_passed"]:
            correction_successes += 1
        elif expected == "reject" and not documents:
            correction_successes += 1
    if expected == "answer":
        total_retrieved += sum(
            attempt["retrieved"]
            for attempt in stats["attempt_history"]
        )
        total_relevant += sum(
            attempt["relevant"]
            for attempt in stats["attempt_history"]
        )

    # Display attempt history
    print("\nATTEMPT HISTORY:")

    for attempt_data in stats["attempt_history"]:

        print(
            f"Attempt {attempt_data['attempt']}: "
            f"Retrieved={attempt_data['retrieved']}, "
            f"Relevant={attempt_data['relevant']}"
        )

    # Determine actual result
    if documents:
        actual = "answer"
    else:
        actual = "reject"

    print("\nACTUAL:", actual)

    # Compare expected and actual result
    if actual == expected:

        correct += 1

        print("RESULT: CORRECT")

    else:

        print("RESULT: WRONG")


# ---------------------------------
# FINAL EVALUATION
# ---------------------------------

accuracy = (
    correct / len(test_questions)
) * 100


if total_retrieved > 0:
    retrieval_relevance = (
        total_relevant / total_retrieved
    ) * 100
else:
    retrieval_relevance = 0

correction_rate = (
    corrections_used / len(test_questions)
) * 100


print("\n==============================")
print("EVALUATION RESULT")
print("==============================")


print(
    f"Correct: "
    f"{correct}/{len(test_questions)}"
)


print(
    f"Accuracy: "
    f"{accuracy:.2f}%"
)


print(
    f"Retrieval Relevance: "
    f"{retrieval_relevance:.2f}%"
)


correction_rate = (
    corrections_used / len(test_questions)
) * 100

print(
    f"Correction Rate: "
    f"{correction_rate:.2f}%"
)
if auditable_questions > 0:
    audit_pass_rate = (
        audit_passes / auditable_questions
    ) * 100
else:
    audit_pass_rate = 0

print(
    f"Audit Pass Rate: "
    f"{audit_pass_rate:.2f}%"
)

correction_success_rate = (
    correction_successes / corrections_used
) * 100

print(
    f"Correction Success Rate: "
    f"{correction_success_rate:.2f}%"
)