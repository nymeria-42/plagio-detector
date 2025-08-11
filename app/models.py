import os
import json
from typing import List
import csv
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import TfidfVectorizer

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
DOCS_DIR = os.path.join(DATA_DIR, "docs")

class Corpus:
    def __init__(self):
        self.ids: List[str] = []
        self.titles: List[str] = []
        self.texts: List[str] = []

        self._load_docs()

        # TF-IDF
        self.tfidf_vectorizer = TfidfVectorizer(ngram_range=(1,2), max_features=20000)
        self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(self.texts)

        # Embeddings
        self.embed_model = SentenceTransformer("all-MiniLM-L6-v2")
        self.embeddings = self.embed_model.encode(self.texts, show_progress_bar=False)

    def _load_docs(self):
        mapping_file = os.path.join(DATA_DIR, "metadata.csv")
        id_to_title = {}

        with open(mapping_file, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                id_to_title[row["id"]] = row["title"]

        files = [f for f in os.listdir(DOCS_DIR) if f.endswith('.txt')]

        for fn in files:
            doc_id = fn.replace('.txt', '')
            self.ids.append(doc_id)
            self.titles.append(id_to_title.get(doc_id, "Título desconhecido"))
            with open(os.path.join(DOCS_DIR, fn), "r", encoding="utf-8") as fd:
                self.texts.append(fd.read())

CORPUS = Corpus()