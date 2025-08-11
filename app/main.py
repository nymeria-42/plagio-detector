from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import os

from .compare import lexical_topk, semantic_topk
from .setup_data import initialize_data 

app = FastAPI(title="Plagio Detector")

class CompareRequest(BaseModel):
    text: str
    top_k: Optional[int] = 5

CORPUS_DIR = "app/data/docs"
@app.on_event("startup")
async def startup_event():
    if not os.path.exists(CORPUS_DIR) or not os.listdir(CORPUS_DIR):
        print(f"Corpus directory '{CORPUS_DIR}' is empty or missing. Initializing data...")
        initialize_data(search_query="inteligência artificial")
    else:
        print(f"Corpus directory '{CORPUS_DIR}' already has data. Skipping initialization.")

@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/compare")
async def compare(req: CompareRequest):
    text = req.text
    k = req.top_k or 5
    lexical = lexical_topk(text, k)
    semantic = semantic_topk(text, k)
    return {"lexical": lexical, "semantic": semantic}