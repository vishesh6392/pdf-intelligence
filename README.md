# 🧑‍🏫 TeacherAgent
> **An extensible AI system for intelligent document understanding and precision-oriented RAG.**

TeacherAgent is a modular, Retrieval-Augmented Generation (RAG) system designed to transform static PDFs into interactive knowledge bases. By combining semantic search with neural reranking, it provides high-precision answers grounded in your specific data.

---

## ✨ Core Capabilities

* **📄 Smart Ingestion:** Robust PDF processing with metadata registration.
* **🔍 Precision Retrieval:** Two-stage retrieval using **FAISS** (Dense Vector Search) and **Cross-Encoder Reranking**.
* **🧠 Context-Aware QA:** LLM-powered answers with strict grounding to prevent hallucinations.
* **☁️ Cloud Native:** S3-compatible object storage integration for scalable document management.
* **🛠️ Modular Design:** Independent layers for ingestion, retrieval, and inference.

---

## 🏗️ System Architecture

TeacherAgent is built with a decoupled architecture, allowing you to swap models or storage providers without a full rewrite.

### 🧩 Logic Flow
1. **API Layer:** Handles requests and acts as the gateway.
2. **Storage Layer:** Manages raw PDFs (S3) and document metadata.
3. **Ingestion Pipeline:** (Async) Extracts text, chunks content, and builds FAISS indices.
4. **Retrieval Pipeline:** Performs semantic search, reranks results, and generates the final response.

---

## 🔄 Workflow

The system follows a two-stage process to ensure that the AI has the most relevant information before answering.

### 1. Document Ingestion (Offline)
When a document is uploaded, it enters an asynchronous pipeline:
* **Extraction:** Pure text is pulled from the PDF structure.
* **Chunking:** Text is split into overlapping segments to preserve context across boundaries.
* **Indexing:** Each chunk is converted into a vector embedding and stored in a **FAISS** index unique to that document.

### 2. Retrieval & Reranking (Online)
TeacherAgent uses a "Retrieve-then-Rank" strategy to ensure maximum accuracy:
1.  **Semantic Search:** The user query is vectorized, and FAISS retrieves the top $K$ most similar chunks.
2.  **Neural Reranking:** A Cross-Encoder model evaluates the query and chunks together, re-ordering them based on true relevance rather than just keyword/vector proximity.
3.  **Grounded Generation:** The LLM receives the top-ranked chunks and generates an answer strictly based on that provided context.



---

## 🚀 API Reference

### Upload a Document
`POST /api/upload`

**Request:** `multipart/form-data`
* `file`: The PDF document to process.
* `document_id`: "8cf1-42b9-a472"

### Query a Document
`POST /api/query`
* `query`: "What are the core principles of this system?"
* `document_id`: "8cf1-42b9-a472"

---

## 🔮 Roadmap & Future Vision

TeacherAgent is built to be a foundation for progressively richer document intelligence. The following enhancements are planned to expand its capabilities:

### 🧾 OCR Engine
* **Technology:** Integration of **Tesseract** or **PaddleOCR**.
* **Goal:** Support for scanned documents, handwritten notes, and image-based PDFs.
* **Benefit:** Ensures that "dark data" in non-searchable files becomes accessible to the RAG pipeline.

### 🖼️ Multimodal Understanding
* **Technology:** Vision-Language Models (VLMs).
* **Goal:** Deep analysis of diagrams, tables, and charts within documents.
* **Benefit:** Enables querying visual data (e.g., "Explain the trend in the chart on page 5").



### 🧑‍🏫 Agentic Personas
* **Technology:** Adaptive System Prompting & Session Memory.
* **Goal:** Interactive "Professor" modes utilizing Socratic questioning.
* **Benefit:** Moves beyond direct answers to provide guided learning and difficulty levels adapted to the user's expertise.

### 🤖 Workflow Expansion
* **Technology:** Multi-agent Orchestration.
* **Goal:** Dedicated agents for self-verification, summarization, and question decomposition.
* **Benefit:** Increases reliability by having a "critic" agent verify that the "generator" agent stayed true to the source text.

---

### 📂 Project Structure
```text
TeacherAgent/
├── app/
│   ├── api/          # HTTP API layer (upload, query)
│   ├── core/         # Orchestration logic (RAG pipeline)
│   ├── ingestion/    # Offline document processing pipeline
│   ├── retrieval/    # FAISS-based semantic search
│   ├── reranking/    # Neural rerankers (Cross-Encoder)
│   ├── llm/          # LLM abstraction layer
│   ├── storage/      # Object storage (S3) & metadata registry
│   └── main.py       # FastAPI application entrypoint
├── requirements.txt
└── README.md

