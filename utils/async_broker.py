import json
from functools import lru_cache

from aiokafka import AIOKafkaConsumer

from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import NoBrokersAvailable, KafkaConnectionError

from utils.config import get_settings

config = get_settings()

# TODO: add bootstrap connected check to getters
# TODO: create a list of consumers and producer to close at shutdown

@lru_cache
def get_producer() -> KafkaProducer | None:
    try: # Trying connecting to kafka
        producer = KafkaProducer(
            bootstrap_servers=config.broker_address,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        return producer
    except NoBrokersAvailable as e:
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
        return consumer
    except KafkaConnectionError as e:
        await consumer.stop()
        return None