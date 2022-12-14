import json
from functools import lru_cache

from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import NoBrokersAvailable

from utils.config import get_settings

config = get_settings()

# TODO: add bootstrap connected check to getters

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
def get_consumer(topic: str) -> KafkaConsumer | None:
    try: # Trying connecting to kafka
        consumer = KafkaConsumer(
            topic,
            bootstrap_servers=config.broker_address,
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            #consumer_timeout_ms=1000
        )
        return consumer
    except NoBrokersAvailable as e:
        return None

# For Testing ONLY!
# 
# @lru_cache
# def get_consumer_all(topic: str) -> KafkaConsumer | None:
#     try: # Trying connecting to kafka
#         consumer = KafkaConsumer(
#             topic,
#             bootstrap_servers=config.broker_address,
#             value_deserializer=lambda m: json.loads(m.decode('utf-8')),
#             consumer_timeout_ms=1000,
#             auto_offset_reset='earliest',
#             enable_auto_commit=False
#         )
#         return consumer
#     except NoBrokersAvailable as e:
#         return None