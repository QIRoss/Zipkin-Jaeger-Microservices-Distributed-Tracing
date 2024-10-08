from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2
import random

app = FastAPI()

class Payment(BaseModel):
    user_id: int
    order_id: int
    amount: float

def get_connection():
    return psycopg2.connect("dbname='paymentdb' user='payment_user' password='password' host='payment_db'")

@app.post("/payment/")
def process_payment(payment: Payment):
    payment_status = random.choice(["success", "failure"])

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO payments (user_id, order_id, amount, status) VALUES (%s, %s, %s, %s) RETURNING id", 
                (payment.user_id, payment.order_id, payment.amount, payment_status))
    payment_id = cur.fetchone()[0]
    conn.commit()
    
    return {"payment_id": payment_id, "status": payment_status}

@app.get("/payment/{payment_id}")
def get_payment(payment_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT user_id, order_id, amount, status FROM payments WHERE id = %s", (payment_id,))
    payment = cur.fetchone()
    if payment:
        return {"payment_id": payment_id, "user_id": payment[0], "order_id": payment[1], "amount": payment[2], "status": payment[3]}
    else:
        return {"status": "Payment not found"}
