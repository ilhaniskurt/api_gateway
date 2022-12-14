from fastapi import FastAPI
from fastapi.websockets import WebSocket, WebSocketDisconnect

from api.schemas import EventSchema
from utils.validator import valid_schema_data_or_error
from utils.config import Settings, get_settings
from utils.broker import get_consumer, get_producer

app = FastAPI()

config: Settings
producer: None

@app.on_event('startup')
def startup():
    global config, producer
    config = get_settings()
    # producer = get_producer()

    # print('Startup')

@app.on_event('shutdown')
def startup():
    pass
    # print('Shutdown')



@app.get("/")
async def root():
    return {'msg':'cuzdan0.1'}


async def login(websocket: WebSocket , data: dict):
    print(f"Login data was: {data}")
    
    pass


@app.websocket_route("/ws")
async def websocket(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            raw_data = await websocket.receive_text()

            data, errors = valid_schema_data_or_error(raw_data, EventSchema)

            # Test
            # print(f'ws: {raw_data}')
            # print(f"type: {type(raw_data)}")
            # if errors:
            #     print(f'Errors: {errors}')
            # else:
            #     print(f'Data: {data}')
            #     print(f"type: {type(raw_data)}")

            if errors:
                await websocket.send_text(f"{errors}")
                continue
            
            match data['event']:
                case 'login':
                    await login(websocket, data['data'])

            print("hey")
            await websocket.send_text(f"Message text was: {data}")
    except WebSocketDisconnect:
        pass