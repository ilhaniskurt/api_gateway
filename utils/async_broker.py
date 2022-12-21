import json
from functools import lru_cache

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from kafka.errors import KafkaConnectionError

from utils.config import get_settings

config = get_settings()

# TODO: add bootstrap connected check to getters
# TODO: create a list of consumers and producer to close at shutdown

clients = []

@lru_cache
async def get_async_producer() -> AIOKafkaProducer | None:
    producer = AIOKafkaProducer(
            bootstrap_servers=config.broker_address,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    try: 
        # Trying connecting to kafka
        await producer.start()
        return producer
    except KafkaConnectionError as e:
        await producer.stop()
        return None

@lru_cache
async def get_async_consumer(topic: str) -> AIOKafkaConsumer | None:
    consumer = AIOKafkaConsumer(
            topic,
            bootstrap_servers=config.broker_address,
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            #consumer_timeout_ms=1000
    )
    try: 
        # Trying connecting to kafka
        await consumer.start()
        clients.append(consumer)
        return consumer
    except KafkaConnectionError as e:
        await consumer.stop()
        return None