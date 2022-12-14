from threading import Thread

from fastapi import FastAPI
from fastapi.websockets import WebSocket, WebSocketDisconnect

from api.schemas import EventSchema
from api.managers import ConnectionManager
from utils.validator import valid_schema_data_or_error
from utils.config import Settings, get_settings
from utils.broker import get_consumer, get_producer

app = FastAPI()

config: Settings
manager: ConnectionManager

# TODO: replace threading with asyncio 

@app.on_event('startup')
def startup():
    global config, producer, manager

    config = get_settings()
    producer = get_producer()
    manager = ConnectionManager()

    if producer is None:
        print('Producer is offline')

    Thread(target=login_consumer, args={}, 
			   name="login_consumer", daemon=True).start()

@app.on_event('shutdown')
def shutdown():
    pass

# Thread Functions

def login_consumer():
    consumer = get_consumer(config.kafka_login_topic)
    if not consumer:
        print('Login consumer is offline')
        return

    for msg in consumer:
        data: dict = msg.value
        websocket: WebSocket = manager.active_connections[data['socket']]
        print(f"LC: {data}")


# Functions 

async def login(websocket: WebSocket, ws_id: str, data: dict):
    producer = get_producer()

    if not producer:
        # TODO: send this error message from outside this function (/ws)
        await websocket.send_text('[{"loc":"non_field_error", "msg": "Service unavailable"}]')
        return

    data.update({'socket':ws_id})

    producer.send(config.kafka_login_topic, data)

# Websocket Routing

@app.websocket_route("/ws")
async def websocket(websocket: WebSocket):
    ws_id = await manager.connect(websocket)
    try:
        while True:
            raw_data = await websocket.receive_text()

            data, errors = valid_schema_data_or_error(raw_data, EventSchema)

            if errors:
                await websocket.send_text(f"{errors}")
                continue
            
            match data['event']:
                case 'login':
                    await login(websocket, ws_id, data['data'])

            await websocket.send_text(f"Message text was: {data}")
    except WebSocketDisconnect:
        manager.disconnect(ws_id)