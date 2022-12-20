import asyncio
from threading import Thread

from fastapi import FastAPI
from fastapi.websockets import WebSocket, WebSocketDisconnect

from api.schemas import EventSchema
from api.managers import get_manager
from api.tasks import login_consumer
from utils.validator import valid_schema_data_or_error
from utils.config import get_settings
from utils.broker import get_producer

app = FastAPI()

config: get_settings()
producer = get_producer()
manager = get_manager()

# TODO: replace threading with asyncio 

@app.on_event('startup')
def startup():
    global producer

    if producer is None:
        print('Producer is offline')

    # Might throw an exception if no loops exists
    loop = asyncio.get_running_loop() 
    loop.create_task(login_consumer())


@app.on_event('shutdown')
async def shutdown():
    # Waiting for background tasks to finish
    # all_tasks = asyncio.all_tasks()
    # current_task = asyncio.current_task()
    # all_tasks.remove(current_task)
    # await asyncio.wait(all_tasks)
    pass

# Event Functions 

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
                    await login(websocket, ws_id, data)

            await websocket.send_text(f"Message text was: {data}")
    except WebSocketDisconnect:
        manager.disconnect(ws_id)