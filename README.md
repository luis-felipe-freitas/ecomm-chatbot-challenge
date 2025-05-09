# E-Commerce Expert Assistant Chatbot

This project implements a modular chatbot system using FastAPI, capable of answering product-related and order-related queries using microservices.

# Sample Questions and Chatbot Responses

## Product Dataset Queries

**User**: What are the top 5 highly-rated guitar products?  
**Chatbot**: Returns 5 guitar-related products ranked by similarity to the query, including Ernie Ball Mondo Slinky, D'Addario Bronze strings, and Amazon Basics stand.

**User**: What's a good product for thin guitar strings?  
**Chatbot**: Suggests D'Addario Guitar Strings - Phosphor Bronze with rating 4.7.

**User**: Is the BOYA BYM1 Microphone good for a cello?  
**Chatbot**: Notes that it's optimized for vocals, not musical instruments.

## Order Dataset Queries

**User**: What are the details of my last order?  
**Customer ID**: 37077  
**Chatbot**: Car Media Player ordered on 2018-01-02 for $140 with $4.60 shipping.

**User**: What is the status of my car body covers?  
**Customer ID**: 41066  
**Chatbot**: Ordered 5 Car Body Covers on 2018-11-08 with Critical priority.

---

All queries are handled via POST /chat/ endpoint with `message` and optional `customer_id`.

---

## 🧪 How to Run in Visual Studio Code

1. **Open Folder**: Launch VSCode and open the `ecomm_chatbot` folder.

2. **Set Up Virtual Environment (optional but recommended):**
```bash
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on Windows
```

3. **Install Requirements**
```bash
pip install -r requirements.txt
```

4. **Run Each Microservice in Separate Terminal Tabs in VSCode**
```bash
# Terminal 1
cd order_service
uvicorn main:app --port 8002

# Terminal 2
cd product_service
uvicorn main:app --port 8001

# Terminal 3
cd chat_service
uvicorn main:app --port 8000
```

5. **Test Chatbot**
Use REST clients like Thunder Client (VSCode extension), Postman, or CURL:
```bash
curl -X POST http://localhost:8000/chat/ \
  -H "Content-Type: application/json" \
  -d '{"message":"What’s the status of my order?", "customer_id":37077}'
```
## 🔍 Product Search Microservice (Upgraded with Real RAG)

This service now uses **true Retrieval-Augmented Generation (RAG)** powered by semantic embeddings.

- **Model**: `all-MiniLM-L6-v2` from `sentence-transformers`
- **Search engine**: `FAISS` for fast vector similarity lookup
- **Data source**: `Product_Information_Dataset.csv`, using the `title` and `description` columns

### Example usage:
```bash
curl "http://localhost:8001/search/?query=guitar strings"