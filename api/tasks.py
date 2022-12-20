from fastapi.websockets import WebSocket

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

    async for msg in consumer:
        data: dict = msg.value
        websocket: WebSocket = manager.active_connections[data['socket']]
        await websocket.send_text("teas")
        print(f"LC: {data}")