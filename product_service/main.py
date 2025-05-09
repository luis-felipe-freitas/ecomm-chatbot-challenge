import pandas as pd
from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import List
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Load data
df = pd.read_csv("../shared/Product_Information_Dataset.csv")
df["text"] = df["title"].fillna("") + " " + df["description"].fillna("")

# Create embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')
corpus_embeddings = model.encode(df["text"].tolist(), convert_to_numpy=True)

# Create FAISS index
dimension = corpus_embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(corpus_embeddings)

# FastAPI setup
app = FastAPI(title="Product Search with RAG")

class ProductResponse(BaseModel):
    title: str
    description: str
    rating: float
    price: float

@app.get("/search/", response_model=List[ProductResponse])
def search_products(query: str = Query(..., description="Search query")):
    query_embedding = model.encode([query], convert_to_numpy=True)
    top_k = 5
    distances, indices = index.search(query_embedding, top_k)
    
    results = []
    for idx in indices[0]:
        product = df.iloc[idx]
        results.append(ProductResponse(
            title=product["title"],
            description=product["description"],
            rating=product.get("average_rating", 0),
            price=product.get("price", 0)
        ))
    return results
