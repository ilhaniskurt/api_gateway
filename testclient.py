import asyncio
import websockets
import json

data = {"event":"login", "data":{"username":"asdsfgd"}}

async def test():
    async with websockets.connect('ws://localhost:8000/ws') as websocket:
        await websocket.send(json.dumps(data))
        response = await websocket.recv()
        print(response)
 
asyncio.new_event_loop().run_until_complete(test())
