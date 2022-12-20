import asyncio
import websockets
import json

data = {"event":"login", "data":{"username":"+905374391258", "password":"123456789aA?"}}

async def login_test():
    async with websockets.connect('ws://localhost:8000/ws') as websocket:
        await websocket.send(json.dumps(data))
        response = await websocket.recv()
        print(response)
        response = await websocket.recv()
        print(response)

asyncio.new_event_loop().run_until_complete(login_test())
