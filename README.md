# Wasserstoff AI Software Intern Task  
## Document Research & Theme Identification Chatbot

---

## Overview

This project is a **web-based interactive chatbot** designed to assist research by enabling users to upload large sets of documents (75+), perform advanced queries, and extract detailed, cited answers. It also identifies common themes across the documents and synthesizes responses for comprehensive research insights.

---

## Features

- **Document Upload & OCR Processing**  
  Upload PDF, DOCX, TXT, and scanned image documents. Scanned documents are processed using OCR (PaddleOCR) to extract high-fidelity text content for research.

- **Document Management**  
  View all uploaded documents, filter, and select documents for targeted querying.

- **Natural Language Query Interface**  
  Ask questions in natural language and receive precise answers based on the document corpus.

- **Detailed Citations**  
  Answers include exact citations indicating document ID, page, paragraph, or sentence where relevant information was found.

- **Theme Identification & Synthesis**  
  The system analyzes query responses across documents to identify and present common themes, enhancing cross-document insights.

- **User-Friendly UI**  
  Built using Streamlit for an intuitive, interactive experience.

---

## Tech Stack

- **Backend:** FastAPI  
- **Frontend:** Streamlit  
- **OCR:** PaddleOCR  
- **LLM:** OpenAI GPT (or alternatives Gemini, Groq)  
- **Vector Database:** Qdrant (for semantic search)  
- **Language Orchestration:** LangChain  
- **Database:** Document metadata and text storage (e.g., local JSON or DB)  


---



