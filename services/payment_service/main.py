from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2
import random
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor

app = FastAPI()

class Payment(BaseModel):
    user_id: int
    order_id: int
    amount: float

def configure_tracer():
    trace.set_tracer_provider(
        TracerProvider(
            resource=Resource.create({"service.name": "payment_service"})
        )
    )
    jaeger_exporter = JaegerExporter(
        agent_host_name="jaeger",
        agent_port=6831,
    )
    span_processor = BatchSpanProcessor(jaeger_exporter)
    trace.get_tracer_provider().add_span_processor(span_processor)

configure_tracer()
tracer = trace.get_tracer(__name__)

FastAPIInstrumentor.instrument_app(app)
RequestsInstrumentor().instrument()

def get_connection():
    return psycopg2.connect("dbname='paymentdb' user='payment_user' password='password' host='payment_db'")

@app.post("/payment/")
def process_payment(payment: Payment):
    with tracer.start_as_current_span("process_payment") as span:
        payment_status = random.choice(["success", "failure"])

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO payments (user_id, order_id, amount, status) VALUES (%s, %s, %s, %s) RETURNING id", 
                    (payment.user_id, payment.order_id, payment.amount, payment_status))
        payment_id = cur.fetchone()[0]
        conn.commit()

        span.set_attribute("payment.id", payment_id)
        span.set_attribute("payment.status", payment_status)

        return {"payment_id": payment_id, "status": payment_status}

@app.get("/payment/{payment_id}")
def get_payment(payment_id: int):
    with tracer.start_as_current_span("get_payment") as span:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT user_id, order_id, amount, status FROM payments WHERE id = %s", (payment_id,))
        payment = cur.fetchone()
        if payment:
            span.set_attribute("payment.id", payment_id)
            return {"payment_id": payment_id, "user_id": payment[0], "order_id": payment[1], "amount": payment[2], "status": payment[3]}
        else:
            return {"status": "Payment not found"}

@app.on_event("shutdown")
def shutdown_event():
    pass
