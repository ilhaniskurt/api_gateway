import asyncio
import websockets
import json

login_data = {"event":"login", "data":{"username":"+905374391258", "password":"123456789aA?"}}

token = ''

async def login_test():
    async with websockets.connect('ws://localhost:8000/ws') as websocket:
        await websocket.send(json.dumps(login_data))
        response = json.loads(await websocket.recv())
        print('Login Request Result:')
        print(response)

        try:
            token = response['result']['attr']['token']['access_token']
        except TypeError:
            return

        


asyncio.run(login_test())
