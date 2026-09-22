# CorrectiveRAG — Self-Correcting RAG System

## Overview

**CorrectiveRAG** is a Retrieval-Augmented Generation (RAG) system designed to improve the reliability of AI-generated answers.

Unlike a traditional RAG pipeline that retrieves documents and directly generates an answer, CorrectiveRAG evaluates the retrieved documents and audits the generated answer before returning the final response.

### Core Workflow

**Retrieve → Grade → Correct → Generate → Audit → Answer**

The project uses **Ollama with Llama 3.2 3B** for local answer generation, **FAISS** for vector search, and **Hugging Face embeddings** for document representation.

---

## Problem Statement

Traditional RAG systems may produce incorrect or unsupported answers when:

* Retrieved documents are not relevant to the user's question.
* The user's query is unclear.
* The knowledge base does not contain enough information.
* The generated answer contains unsupported information.

CorrectiveRAG addresses these problems by adding:

1. Document relevance grading
2. Automatic query rewriting
3. Corrective retrieval
4. Answer generation
5. Answer auditing
6. Out-of-domain question rejection

---

## Architecture

```text
                    User Question
                          |
                          v
                  +---------------+
                  | Query         |
                  | Processing    |
                  +---------------+
                          |
                          v
                  +---------------+
                  | FAISS         |
                  | Retriever     |
                  +---------------+
                          |
                          v
                  +---------------+
                  | Retrieval     |
                  | Grader        |
                  +---------------+
                          |
              Relevant Documents?
                    /           \
                  No             Yes
                  |               |
                  v               v
          +---------------+  +---------------+
          | Query         |  | Answer        |
          | Rewriter      |  | Generator     |
          +---------------+  +---------------+
                  |               |
                  |               v
                  |       +---------------+
                  |       | Answer        |
                  |       | Auditor       |
                  |       +---------------+
                  |               |
                  |        Audit Passed?
                  |          /       \
                  |        No         Yes
                  |        |           |
                  +--------+           v
                  |                Final Answer
                  v
                Retry
```

---

## How CorrectiveRAG Works

### 1. Document Loading

The system loads the knowledge source from:

```text
data/machine_learning.pdf
```

The current knowledge base focuses on Machine Learning concepts.

### 2. Text Splitting

The document is divided into smaller chunks so that relevant sections can be retrieved efficiently.

### 3. Embeddings

Each document chunk is converted into a numerical vector using:

```text
sentence-transformers/all-MiniLM-L6-v2
```

### 4. Vector Store

The embeddings are stored in a **FAISS** vector database.

The generated vector store is stored under:

```text
data/vectorstore/
```

### 5. Retrieval

For each user question, the system retrieves the top 4 potentially relevant documents.

### 6. Retrieval Grading

Each retrieved document is evaluated to determine whether it is relevant to the user's question.

### 7. Query Correction

If relevant documents are not found, CorrectiveRAG rewrites the query and performs retrieval again.

This creates a corrective loop instead of immediately generating an answer from poor context.

### 8. Answer Generation

Relevant documents are passed to the local LLM.

The project uses:

```text
Llama 3.2 3B
```

through **Ollama**.

### 9. Answer Auditing

The generated answer is checked using three criteria:

* **Faithfulness** — Are the claims supported by the retrieved context?
* **Relevance** — Does the answer directly address the question?
* **Completeness** — Does the answer sufficiently answer the question?

Only answers that pass the configured audit are returned as successful responses.

### 10. Out-of-Domain Rejection

If the system cannot find relevant information after the allowed correction attempts, it does not invent an answer.

Instead, it returns:

```text
I don't have enough information in the provided documents.
```

---

## Technologies Used

| Technology       | Purpose                            |
| ---------------- | ---------------------------------- |
| Python           | Core programming language          |
| LangChain        | RAG pipeline and LLM orchestration |
| Ollama           | Local LLM execution                |
| Llama 3.2 3B     | Answer generation                  |
| Hugging Face     | Embeddings                         |
| all-MiniLM-L6-v2 | Document embeddings                |
| FAISS            | Vector similarity search           |
| PyPDF            | PDF document processing            |
| FastAPI          | Backend API                        |
| Streamlit        | Frontend/UI                        |
| python-dotenv    | Environment configuration          |

---

## Project Structure

```text
CorrectiveRAG/
│
├── app/
│   ├── answer_auditor.py
│   ├── answer_generator.py
│   ├── config.py
│   ├── corrective_rag.py
│   ├── document_loader.py
│   ├── embeddings.py
│   ├── llm.py
│   ├── query_rewriter.py
│   ├── retrieval_grader.py
│   ├── retriever.py
│   ├── text_splitter.py
│   └── vector_store.py
│
├── backend/
│
├── frontend/
│
├── data/
│   ├── machine_learning.pdf
│   └── vectorstore/
│       ├── index.faiss
│       └── index.pkl
│
├── evaluation/
│   └── evaluate.py
│
├── tests/
│
├── .gitignore
├── README.md
├── requirements.txt
├── run.py
├── test_auditor.py
└── test_ollama.py
```

---

## Installation

### 1. Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd CorrectiveRAG
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

### 3. Activate the Virtual Environment

For Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Install Dependencies

```powershell
pip install -r requirements.txt
```

---

## Ollama Setup

CorrectiveRAG uses Ollama to run the LLM locally.

Install the required model:

```powershell
ollama pull llama3.2:3b
```

Verify that the model is available:

```powershell
ollama list
```

The project uses:

```text
llama3.2:3b
```

The LLM runs locally, so answer generation does not require a paid OpenAI API.

---

## Run the Project

Activate the virtual environment:

```powershell
.venv\Scripts\Activate.ps1
```

Then run:

```powershell
python run.py
```

Example question:

```text
What is Machine Learning?
```

The system will:

1. Retrieve relevant documents.
2. Grade the retrieved documents.
3. Generate an answer.
4. Audit the answer.
5. Return the final answer and sources.

---

## Example: In-Domain Question

### Question

```text
What is Machine Learning?
```

The system retrieves relevant Machine Learning documents and generates a knowledge-grounded answer.

The generated answer is then checked by the answer auditor.

---

## Example: Out-of-Domain Question

### Question

```text
What are th
```
