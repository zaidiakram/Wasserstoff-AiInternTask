import os
import json
import faiss
import numpy as np
from config import PathConfig, ModelConfig, ApiKeys
from services.embedding import embed_text, batch_embed
import google.generativeai as genai
from services.vectorstore import build_vector_store, load_vector_store
from dotenv import load_dotenv

load_dotenv()



def query_rag_pipeline(user_query, top_k=3):
    index, docs = load_vector_store()
    query_vector = np.array([embed_text(user_query)]).astype("float32")

    D, I = index.search(query_vector, top_k)
    retrieved_docs = [docs[i] for i in I[0]]

    context = ""
    for i, doc in enumerate(retrieved_docs, 1):
        context += f"\n---\nSource {i} ({doc['file_name']}):\n{doc['content'][:1000]}\n"

    prompt = f"""
        You are a document research assistant. Answer the question below using the provided sources.
        Be concise, but include key details. Cite the source files in the format (Source X).

        Context:
        {context}

        Question:
        {user_query}

        """

    model = genai.GenerativeModel(ModelConfig.GEMINI_MODEL)
    response = model.generate_content(prompt)

    return response.text.strip()
