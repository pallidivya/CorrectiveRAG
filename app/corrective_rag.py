from app.retriever import get_retriever
from app.retrieval_grader import grade_document
from app.query_rewriter import rewrite_query
from app.answer_generator import generate_answer
from app.answer_auditor import audit_answer


def corrective_rag(question, max_retries=2):

    retriever = get_retriever()

    current_question = question

    stats = {
        "attempts": 0,
        "retrieved_documents": 0,
        "relevant_documents": 0,
        "correction_used": False,
        "audit_passed": False,
        "attempt_history":[]
    }

    for attempt in range(max_retries + 1):

        stats["attempts"] = attempt + 1

        print(f"\n========== ATTEMPT {attempt + 1} ==========")
        print(f"Query: {current_question}")

        # --------------------------------
        # 1. Retrieve documents
        # --------------------------------

        print("\nRetrieving documents...")

        documents = retriever.invoke(current_question)

        stats["retrieved_documents"] = len(documents)

        print(f"Retrieved {len(documents)} documents.")

        # --------------------------------
        # 2. Grade retrieved documents
        # --------------------------------

        print("\nGrading retrieved documents...")

        relevant_documents = []

        for document in documents:

            is_relevant = grade_document(
                current_question,
                document
            )

            if is_relevant:
                relevant_documents.append(document)

        stats["relevant_documents"] = len(relevant_documents)
        stats["attempt_history"].append({
            "attempt": attempt + 1,
            "query": current_question,
            "retrieved": len(documents),
            "relevant": len(relevant_documents)
        })

        print(
            f"Relevant documents: "
            f"{len(relevant_documents)}/{len(documents)}"
        )

        # --------------------------------
        # 3. Rewrite query if retrieval fails
        # --------------------------------

        if not relevant_documents:

            if attempt < max_retries:

                print("\nNo relevant documents found.")
                print("Rewriting query...")

                stats["correction_used"] = True

                current_question = rewrite_query(
                    current_question
                )

                print(
                    f"Rewritten query: "
                    f"{current_question}"
                )

                continue

            else:

                print("\nMaximum retries reached.")

                return (
                    "I don't have enough information "
                    "in the provided documents.",
                    [],
                    stats
                )

        # --------------------------------
        # 4. Generate answer
        # --------------------------------

        print("\nGenerating answer...")

        answer = generate_answer(
            current_question,
            relevant_documents
        )

        print("\nAnswer generated.")
        print("\nGENERATED ANSWER:")
        print(answer)

        # --------------------------------
        # 5. Audit answer
        # --------------------------------

        print("\nAuditing answer...")

        audit_result = audit_answer(
            question,
            answer,
            relevant_documents
        )

        print("\n==============================")
        print("ANSWER AUDIT")
        print("==============================")

        print(audit_result)

        # --------------------------------
        # 6. Check audit result
        # --------------------------------

        audit_lower = audit_result.lower()

        faithful = "faithful: yes" in audit_lower
        relevant = "relevant: yes" in audit_lower
        complete = "complete: yes" in audit_lower

        if faithful and relevant and complete:

            print("\nAnswer passed audit.")

            stats["audit_passed"] = True

            return (
                answer,
                relevant_documents,
                stats
            )

        # --------------------------------
        # 7. Answer failed audit
        # --------------------------------

        print("\nAnswer failed audit.")

        if attempt < max_retries:

            print("Correcting query and retrying...")

            stats["correction_used"] = True

            current_question = rewrite_query(
                current_question
            )

            print(
                f"New query: "
                f"{current_question}"
            )

        else:

            print("\nMaximum retries reached.")

    # --------------------------------
    # 8. Final safety fallback
    # --------------------------------

    return (
        "I don't have enough information "
        "in the provided documents.",
        [],
        stats
    )