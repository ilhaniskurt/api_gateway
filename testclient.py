import asyncio
import websockets
import json

login_data = {"event":"login", "data":{"username":"+905374391258", "password":"123456789aA?"}}
two_fa_data = {"event":"two_factor", "data":{"token":"Bearer", "pin":123456}}
customer_list_data = {"event":"customer_list", "data":{"token":"Bearer"}}
customer_connect_data = {"event":"customer_connect", "data":{"token":"Bearer","customer_no":67248026}}
transaction_data = {"event":"transaction", "data":{"token":"Bearer"}}

token = ''

async def test():
    async with websockets.connect('ws://localhost:8000/ws') as websocket:

        # Login Request
        await websocket.send(json.dumps(login_data))
        response = json.loads(await websocket.recv())
        print('\nLogin Request Result:')
        print(response)

        try:
            token = response['result']['attr']['token']['access_token']
        except TypeError:
            return

        # Two Factor Authentication Request
        two_fa_data['data']['token'] += token
        await websocket.send(json.dumps(two_fa_data))
        response = json.loads(await websocket.recv())

        print('\nTwo Factor Authentication Result:')
        print(response)

        # Get Customer List
        customer_list_data['data']['token'] += token
        await websocket.send(json.dumps(customer_list_data))
        response = json.loads(await websocket.recv())

        print('\nCustomer List Result:')
        print(response)

        # Customer Connect Request
        customer_connect_data['data']['token'] += token
        await websocket.send(json.dumps(customer_connect_data))
        response = json.loads(await websocket.recv())

        print('\nCustomer Connect Result:')
        print(response)

        try:
            token = response['result']['attr']['token']['access_token']
        except TypeError:
            return

        # Transaction Request
        transaction_data['data']['token'] += token
        await websocket.send(json.dumps(transaction_data))
        response = json.loads(await websocket.recv())
        
        print('\nTransaction Result:')
        print(response)


        

        


asyncio.run(test())
