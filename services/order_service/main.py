from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2
from opentelemetry import trace
from opentelemetry.exporter.zipkin.json import ZipkinExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
import os
from opentelemetry.exporter.zipkin.json import ZipkinExporter

zipkin_url = os.getenv("ZIPKIN_URL", "http://localhost:9411/api/v2/spans")

zipkin_exporter = ZipkinExporter(endpoint=zipkin_url)

app = FastAPI()

trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

span_processor = BatchSpanProcessor(zipkin_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

FastAPIInstrumentor.instrument_app(app)

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
