import asyncio
import websockets
from aioconsole import ainput, aprint
from rich import print as pr
import time


chats = None
chat = None

async def get_chats(websocket):
    all_clients = await websocket.recv()
    while True:
        client = all_clients.split(',  ')
        print(all_clients)
        name = input('which chat  ')
        if name in client:
            print('ok')
            break
    return name


async def get_sms(websocket):
    global chat, chats
    sms = await websocket.recv()
    if 'CHATS__!@#!#' not in sms:
        pr(sms)
        await get_sms(websocket)
    else:
        chats = sms[12::]



async def send_sms(websocket):
    global chat, chats
    sms = await ainput('')
    if sms != 'CHANGE GROUP':
        await websocket.send(sms + ' TO - > ' + chat)
        await send_sms(websocket)
    else:
        await websocket.send('GET_ALL_CHATS')
        while True:
            if chats is not None:
                print(chats)
                break
            await asyncio.sleep(0)
        while True:
            k = await ainput(' wich chat      ')
            if k in chats:
                chat = k
                break
        await send_sms(websocket)



async def listener():
    global chat, chats
    async with websockets.connect('ws://localhost:15346') as websocket:
        message = await websocket.recv()
        nickname = input(message + '  ')
        await websocket.send(nickname)
        chat = await get_chats(websocket)

        task1 = asyncio.create_task(get_sms(websocket))
        task2 = asyncio.create_task(send_sms(websocket))
        await task1
        await task2


# asyncio.run(listener())

loop = asyncio.get_event_loop()
loop.create_task(listener())
loop.run_forever()
