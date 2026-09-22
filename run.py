from app.corrective_rag import corrective_rag


question = "What is Machine learning?"


answer, documents, stats = corrective_rag(question)


print("\n==============================")
print("FINAL ANSWER")
print("==============================")

print(answer)


print("\n==============================")
print("SOURCES")
print("==============================")

for i, document in enumerate(documents):

    print(f"\n--- Source {i + 1} ---")
    print(document.page_content[:300])