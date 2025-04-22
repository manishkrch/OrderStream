from kafka import KafkaConsumer
import psycopg2
import json
import os
import time

# Configs
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")
TOPIC = "orders-processed"
PG_HOST = os.getenv("POSTGRES_HOST", "postgres")
PG_USER = os.getenv("POSTGRES_USER", "postgres")
PG_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
PG_DB = os.getenv("POSTGRES_DB", "orderstream")

# Wait for DB to be ready
time.sleep(5)

# PostgreSQL connection
conn = psycopg2.connect(
    host=PG_HOST,
    dbname=PG_DB,
    user=PG_USER,
    password=PG_PASSWORD
)
cursor = conn.cursor()

# Kafka consumer
consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    auto_offset_reset='earliest',
    group_id='order-logger-group',
    enable_auto_commit=True
)

print("🗃️ Order Logger started...")

for msg in consumer:
    order = msg.value
    print(f"📝 Logging order: {order}")

    cursor.execute("""
        INSERT INTO orders (customer_name, item, quantity, status)
        VALUES (%s, %s, %s, %s)
    """, (
        order["customer_name"],
        order["item"],
        order["quantity"],
        order.get("status", "unknown")
    ))

    conn.commit()
