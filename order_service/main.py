
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict

df = pd.read_csv("../shared/Order_Data_Dataset.csv")
df['Order_Date'] = pd.to_datetime(df['Order_Date'])

app = FastAPI(title="Order Lookup Microservice")

class OrderRequest(BaseModel):
    customer_id: int

@app.post("/orders/")
def get_orders_by_customer(request: OrderRequest) -> Dict:
    customer_id = request.customer_id
    customer_orders = df[df['Customer_Id'] == customer_id]

    if customer_orders.empty:
        raise HTTPException(status_code=404, detail="No orders found for this customer.")

    sorted_orders = customer_orders.sort_values(by="Order_Date", ascending=False)
    formatted_orders = sorted_orders.to_dict(orient="records")

    return {
        "customer_id": customer_id,
        "total_orders": len(formatted_orders),
        "orders": formatted_orders
    }
