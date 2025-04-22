from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from kafka import KafkaProducer
import time
import json
import os

KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")
TOPIC = "orders-new"

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def create_kafka_producer(retries=10, delay=5):
    for attempt in range(1, retries + 1):
        try:
            print(f"🔁 Connecting to Kafka (attempt {attempt})...")
            producer = KafkaProducer(
                bootstrap_servers=KAFKA_BROKER,
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
            print("✅ Connected to Kafka!")
            return producer
        except Exception as e:
            print(f"❌ Kafka not ready: {e}")
            time.sleep(delay)
    raise Exception("🛑 Failed to connect to Kafka after multiple attempts")

# Create the producer with retry
producer = create_kafka_producer()

class OrderRequest(BaseModel):
    customer_name: str
    item: str
    quantity: int

@app.post("/orders")
def create_order(order: OrderRequest):
    try:
        producer.send(TOPIC, order.dict())
        return {"message": "Order received", "order": order}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/debug/routes")
def list_routes():
    return [{"path": route.path, "methods": route.methods} for route in app.routes]
