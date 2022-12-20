import requests

from api.managers import get_manager
from utils.config import get_settings
from utils.async_broker import get_async_consumer

config = get_settings()
manager = get_manager()

async def login_consumer():
    consumer = await get_async_consumer(config.kafka_login_topic)
    if not consumer:
        print('Login consumer is offline')
        return

    url = config.cuzdan_api_base_url + config.cuzdan_login_api

    # Use AIOHTTP \

    async for msg in consumer:
        data: dict = msg.value
        
        response = requests.post(url, json=data['data'])
        r = {'event':'login', 'result':response.json()}
        await manager.send(data['socket'], f"{r}")
        print(f"LC: {data}")

async def two_fa_consumer():
    consumer = await get_async_consumer(config.kafka_two_fa_topic)
    if not consumer:
        print('Two factor consumer is offline')
        return

    url = config.cuzdan_api_base_url + config.cuzdan_two_factor_api

    # Use AIOHTTP \

    async for msg in consumer:
        data: dict = msg.value
        
        print(f"LC: {data}")