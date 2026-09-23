import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.corrective_rag import corrective_rag
import streamlit as st

from app.corrective_rag import corrective_rag


st.set_page_config(
    page_title="CorrectiveRAG",
    page_icon="🤖",
    layout="wide"
)


st.title("🤖 CorrectiveRAG")
st.subheader("Self-Correcting RAG — Self-Auditing Retrieval Pipeline")

st.write(
    "Ask a question based on the available documents. "
    "CorrectiveRAG retrieves relevant information, evaluates the retrieved "
    "documents, corrects the query when necessary, generates an answer, "
    "and audits the final answer."
)


question = st.text_input(
    "Enter your question:",
    placeholder="Example: What is Machine Learning?"
)


if st.button("Ask", type="primary"):

    if not question.strip():

        st.warning("Please enter a question.")

    else:

        with st.spinner("Running CorrectiveRAG..."):

            answer, documents, stats = corrective_rag(question)

        st.markdown("## Final Answer")

        st.write(answer)

        st.markdown("## Pipeline Statistics")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Attempts",
            stats["attempts"]
        )

        col2.metric(
            "Retrieved",
            stats["retrieved_documents"]
        )

        col3.metric(
            "Relevant",
            stats["relevant_documents"]
        )

        col4.metric(
            "Correction Used",
            "Yes" if stats["correction_used"] else "No"
        )

        st.markdown("## Audit Status")

        if stats["audit_passed"]:

            st.success("✅ Answer passed the quality audit.")

        else:

            st.warning("⚠️ Answer did not pass the quality audit.")

        st.markdown("## Retrieved Sources")

        if documents:

            for i, document in enumerate(documents):

                with st.expander(f"Source {i + 1}"):

                    st.write(document.page_content)

        else:

            st.info(
                "No relevant documents were found."
            )