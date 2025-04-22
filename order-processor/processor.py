from kafka import KafkaConsumer, KafkaProducer
import json
import time
import os

KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")
TOPIC_IN = "orders-new"
TOPIC_OUT = "orders-processed"

# Wait until Kafka is ready
def create_kafka_consumer(retries=10, delay=5):
    for attempt in range(1, retries + 1):
        try:
            print(f"🔁 Trying to connect to Kafka (attempt {attempt})...")
            consumer = KafkaConsumer(
                "orders",
                bootstrap_servers=KAFKA_BROKER,
                value_deserializer=lambda v: json.loads(v.decode('utf-8')),
                group_id="order-processor-group"
            )
            print("✅ Connected to Kafka and listening on 'orders' topic")
            return consumer
        except Exception as e:
            print(f"❌ Kafka not ready: {e}")
            time.sleep(delay)
    raise Exception("🛑 Could not connect to Kafka after several attempts")

# # Kafka consumer (subscribes to 'orders-new')
# consumer = KafkaConsumer(
#     TOPIC_IN,
#     bootstrap_servers=KAFKA_BROKER,
#     value_deserializer=lambda m: json.loads(m.decode("utf-8")),
#     auto_offset_reset='earliest',
#     group_id='order-processor-group',
#     enable_auto_commit=True
# )

# Create consumer
consumer = create_kafka_consumer()



# Kafka producer (publishes to 'orders-processed')
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

print("🚀 Order Processor started...")

for msg in consumer:
    order = msg.value
    print(f"➡️  Received order: {order}")
    
    # Simulate processing logic
    order["status"] = "processed"
    time.sleep(1)  # Simulate processing delay
    
    # Publish to the next topic
    producer.send(TOPIC_OUT, order)
    print(f"✅ Processed and forwarded: {order}")
