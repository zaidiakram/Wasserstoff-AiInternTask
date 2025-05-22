import os
import json
import faiss
import numpy as np
from config import PathConfig, ModelConfig, ApiKeys
from services.embedding import embed_text, batch_embed



def build_vector_store():
    with open(PathConfig.DOCS_PATH, "r", encoding="utf-8") as f:
        docs = json.load(f)

    texts = [doc["content"] for doc in docs]
    embeddings = batch_embed(texts)

    dim = len(embeddings[0])
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings).astype("float32"))

    # Save index
    faiss.write_index(index, PathConfig.INDEX_PATH)

    print(f"FAISS index created with {len(texts)} documents.")

    return index, docs


def load_vector_store():
    index = faiss.read_index(PathConfig.INDEX_PATH)
    with open(PathConfig.DOCS_PATH, "r", encoding="utf-8") as f:
        docs = json.load(f)
    return index, docs