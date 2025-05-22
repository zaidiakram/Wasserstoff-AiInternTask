from sentence_transformers import SentenceTransformer
from config import ModelConfig

model = SentenceTransformer(ModelConfig.Embedding_model)


def embed_text(text: str):
    return model.encode(text, convert_to_tensor=False)


def batch_embed(texts: list[str]):
    return model.encode(texts, convert_to_tensor=False)
