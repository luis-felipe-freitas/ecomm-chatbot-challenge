
import requests
from fastapi import FastAPI, Query
from pydantic import BaseModel

app = FastAPI(title="Chat Router Service")

PRODUCT_SERVICE_URL = "http://localhost:8001/search"
ORDER_SERVICE_URL = "http://localhost:8002/orders"

class ChatQuery(BaseModel):
    message: str
    customer_id: int = None  # optional, required only for order-related queries

@app.post("/chat/")
def handle_chat(query: ChatQuery):
    msg = query.message.lower()

    try:
        if "order" in msg or "status" in msg or "shipping" in msg:
            if not query.customer_id:
                return {"response": "Please provide your customer ID to retrieve your order details."}
            res = requests.post(ORDER_SERVICE_URL, json={"customer_id": query.customer_id})
            if res.status_code == 200:
                return {"response": res.json()}
            return {"response": "No orders found or failed to retrieve order data."}
        else:
            res = requests.get(PRODUCT_SERVICE_URL, params={"query": query.message})
            if res.status_code == 200:
                return {"response": res.json()}
            return {"response": "Could not find relevant products."}
    except Exception as e:
        return {"response": f"An error occurred: {str(e)}"}
