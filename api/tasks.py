from aiohttp import ClientSession

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

    async for msg in consumer:
        data: dict = msg.value
        rj = ''

        print(f"LC: {data}")

        # Async Http request to api
        async with ClientSession() as session:
            async with session.post(url, json=data['data']) as response:
                rj = await response.json()

        rd = {'event':'login', 'result':rj}

        await manager.send(data['socket'], f"{rd}")

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