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
                rj = {'event':'login', 'result':await response.json()}

        await manager.send(data['socket'], rj)

async def two_fa_consumer():
    consumer = await get_async_consumer(config.kafka_two_fa_topic)
    if not consumer:
        print('Two factor consumer is offline')
        return

    url = config.cuzdan_api_base_url + config.cuzdan_two_factor_api

    async for msg in consumer:
        data: dict = msg.value
        
        print(f"TFC: {data}")

        async with ClientSession() as session:
            async with session.post(url, headers={'Authorization':data['data']['token']}, json={'two_factor_code': data['data']['pin']}) as response:
                rj = {'event':'login', 'result':await response.json()}
        
        await manager.send(data['socket'], rj)

async def customer_list_consumer():
    consumer = await get_async_consumer(config.kafka_customer_list)
    if not consumer:
        print('Customer list consumer is offline')
        return

    url = config.cuzdan_api_base_url + config.cuzdan_customer_list_api

    async for msg in consumer:
        data: dict = msg.value
        
        print(f"CLC: {data}")

        async with ClientSession() as session:
            async with session.get(url, headers={'Authorization':data['data']['token']}) as response:
                rj = {'event':'login', 'result':await response.json()}
        
        await manager.send(data['socket'], rj)

async def customer_connect_consumer():
    consumer = await get_async_consumer(config.kafka_customer_connect)
    if not consumer:
        print('Customer connect consumer is offline')
        return

    url = config.cuzdan_api_base_url + config.cuzdan_customer_connect_api

    async for msg in consumer:
        data: dict = msg.value
        
        print(f"CCC: {data}")

        async with ClientSession() as session:
            async with session.post(url, headers={'Authorization':data['data']['token']}, json={'customer_no': data['data']['customer_no']}) as response:
                rj = {'event':'login', 'result':await response.json()}
        
        await manager.send(data['socket'], rj)

async def transaction_consumer():
    consumer = await get_async_consumer(config.kafka_transaction)
    if not consumer:
        print('Customer list consumer is offline')
        return

    url = config.cuzdan_api_base_url + config.cuzdan_trasnaction_api

    async for msg in consumer:
        data: dict = msg.value
        
        print(f"TC: {data}")

        async with ClientSession() as session:
            async with session.get(url, headers={'Authorization':data['data']['token']}) as response:
                rj = {'event':'login', 'result':await response.json()}
        
        await manager.send(data['socket'], rj)