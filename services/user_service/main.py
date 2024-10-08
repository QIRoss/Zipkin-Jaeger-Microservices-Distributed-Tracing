from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2
import os
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter

app = FastAPI()

jaeger_host = os.getenv("JAEGER_HOST", "localhost")
jaeger_exporter = JaegerExporter(
    agent_host_name=jaeger_host,
    agent_port=6831
)

trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

span_processor = BatchSpanProcessor(jaeger_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

FastAPIInstrumentor.instrument_app(app)

class User(BaseModel):
    username: str
    email: str

def get_connection():
    return psycopg2.connect("dbname='userdb' user='user' password='password' host='user_db'")

@app.post("/register/")
def register_user(user: User):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(f"INSERT INTO users (username, email) VALUES (%s, %s)", (user.username, user.email))
    conn.commit()
    return {"status": "User registered"}

@app.get("/profile/{user_id}")
def get_user_profile(user_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT username, email FROM users WHERE id = %s", (user_id,))
    user = cur.fetchone()
    return {"id": user_id, "username": user[0], "email": user[1]}
