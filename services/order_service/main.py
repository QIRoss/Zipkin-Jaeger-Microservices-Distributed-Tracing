from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2

app = FastAPI()

class Order(BaseModel):
    user_id: int
    item_name: str
    quantity: int

def get_connection():
    return psycopg2.connect("dbname='orderdb' user='order_user' password='password' host='order_db'")

@app.post("/order/")
def place_order(order: Order):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO orders (user_id, item_name, quantity) VALUES (%s, %s, %s) RETURNING id", 
                (order.user_id, order.item_name, order.quantity))
    order_id = cur.fetchone()[0]
    conn.commit()
    return {"order_id": order_id, "status": "Order placed"}

@app.get("/order/{order_id}")
def get_order(order_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT user_id, item_name, quantity FROM orders WHERE id = %s", (order_id,))
    order = cur.fetchone()
    if order:
        return {"order_id": order_id, "user_id": order[0], "item_name": order[1], "quantity": order[2]}
    else:
        return {"status": "Order not found"}
