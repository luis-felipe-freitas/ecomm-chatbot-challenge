
import pandas as pd
from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import List
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

df = pd.read_csv("../shared/Product_Information_Dataset.csv")

# Combine fields for retrieval
df["text"] = df["title"].fillna("") + " " + df["description"].fillna("")

# Vectorize all product entries
vectorizer = TfidfVectorizer(stop_words="english")
product_vectors = vectorizer.fit_transform(df["text"].values)

app = FastAPI(title="Product Search Microservice")

class ProductResponse(BaseModel):
    title: str
    description: str
    rating: float
    price: float

@app.get("/search/", response_model=List[ProductResponse])
def search_products(query: str = Query(..., description="Search query")):
    query_vector = vectorizer.transform([query])
    similarities = cosine_similarity(query_vector, product_vectors).flatten()
    top_indices = similarities.argsort()[-5:][::-1]

    results = []
    for idx in top_indices:
        product = df.iloc[idx]
        results.append(ProductResponse(
            title=product["title"],
            description=product["description"],
            rating=product.get("average_rating", 0),
            price=product.get("price", 0)

        ))
    return results
