import asyncio

from fastapi import FastAPI
from fastapi.websockets import WebSocket, WebSocketDisconnect

from api.managers import get_manager
from api.schemas import EventSchema
from api.tasks import (
    login_consumer,
    two_fa_consumer,
    customer_list_consumer,
    customer_connect_consumer,
    transaction_consumer
)
from utils.async_broker import clients
from utils.broker import get_producer
from utils.config import get_settings
from utils.validator import valid_schema_data_or_error

app = FastAPI()

config = get_settings()
producer = get_producer()
manager = get_manager()

@app.on_event('startup')
def startup():
    global producer

    if producer is None:
        print('Producer is offline')

    # Might throw an exception if no loops exists
    loop = asyncio.get_running_loop() 
    # Listening on login events
    loop.create_task(login_consumer())
    # Listening on two_factor events
    loop.create_task(two_fa_consumer())
    # Listening on customer_list events
    loop.create_task(customer_list_consumer())
    # Listening on customer_connect events
    loop.create_task(customer_connect_consumer())
    # Listening on transaction events
    loop.create_task(transaction_consumer())



@app.on_event('shutdown')
async def shutdown():
    # Close all Kafka Clients
    for client in clients:
        await client.stop()
    # Waiting for background tasks to finish
    # all_tasks = asyncio.all_tasks()
    # current_task = asyncio.current_task()
    # all_tasks.remove(current_task)
    # await asyncio.wait(all_tasks)
    pass

# Event Functions 

def login(ws_id: str, data: dict) -> str | None:
    producer = get_producer()

    if not producer:
        err = '[{"loc":"non_field_error", "msg": "Service unavailable"}]'
        return err

    data.update({'socket':ws_id})
    producer.send(config.kafka_login_topic, data)
    return None

def two_factor(ws_id: str, data: dict) -> str | None:
    producer = get_producer()

    if not producer:
        err = '[{"loc":"non_field_error", "msg": "Service unavailable"}]'
        return err

    data.update({'socket':ws_id})
    producer.send(config.kafka_two_fa_topic, data)
    return None

def customer_list(ws_id: str, data: dict) -> str | None:
    producer = get_producer()

    if not producer:
        err = '[{"loc":"non_field_error", "msg": "Service unavailable"}]'
        return err

    data.update({'socket':ws_id})
    producer.send(config.kafka_customer_list, data)
    return None

def customer_connect(ws_id: str, data: dict) -> str | None:
    producer = get_producer()

    if not producer:
        err = '[{"loc":"non_field_error", "msg": "Service unavailable"}]'
        return err

    data.update({'socket':ws_id})
    producer.send(config.kafka_customer_connect, data)
    return None

def transaction(ws_id: str, data: dict) -> str | None:
    producer = get_producer()

    if not producer:
        err = '[{"loc":"non_field_error", "msg": "Service unavailable"}]'
        return err

    data.update({'socket':ws_id})
    producer.send(config.kafka_transaction, data)
    return None


# Websocket Routing

@app.websocket_route("/ws")
async def websocket(websocket: WebSocket):
    socket_id = await manager.connect(websocket)
    try:
        while True:

            raw_data = await websocket.receive_text()

            # Validate event schema
            data, errors = valid_schema_data_or_error(raw_data, EventSchema)

            # On invalid event schema
            if errors:
                await manager.send(socket_id, f"{errors}")
                continue
            
            err: str | None
            # Event matching
            match data['event']:
                case 'login':
                    err = login(socket_id, data)
                case 'two_factor':
                    err = two_factor(socket_id, data)
                case 'customer_list':
                    err = customer_list(socket_id, data)
                case 'customer_connect':
                    err = customer_connect(socket_id, data)
                case 'transaction':
                    err = transaction(socket_id, data)

            # Any errors while processing event
            if err:
                await manager.send(socket_id, err)

            # await websocket.send_text(f"Message text was: {data}")
    except WebSocketDisconnect:
        manager.disconnect(socket_id)