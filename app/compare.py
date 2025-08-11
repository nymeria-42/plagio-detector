from typing import List, Tuple
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

from .models import CORPUS
from .preprocessing import clean_text


def lexical_topk(query: str, k: int = 5):
    q_clean = clean_text(query)
    q_vec = CORPUS.tfidf_vectorizer.transform([q_clean])
    sims = cosine_similarity(q_vec, CORPUS.tfidf_matrix).flatten()
    idx = np.argsort(sims)[::-1][:k]
    results = [
        {"doc_id": CORPUS.ids[i], "title": CORPUS.titles[i], "similarity": float(sims[i]), "texto": CORPUS.texts[i][:200]}
        for i in idx
    ]
    return results


def semantic_topk(query: str, k: int = 5):
    q_clean = clean_text(query)
    q_emb = CORPUS.embed_model.encode([q_clean], show_progress_bar=False)
    sims = cosine_similarity(q_emb, CORPUS.embeddings).flatten()
    idx = np.argsort(sims)[::-1][:k]
    results = [
        {"doc_id": CORPUS.ids[i], "title": CORPUS.titles[i], "similarity": float(sims[i]), "texto": CORPUS.texts[i][:200]}
        for i in idx
    ]
    return results