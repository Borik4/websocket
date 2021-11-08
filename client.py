import asyncio
import websockets
from aioconsole import aprint, ainput
from rich import print as pr


async def get_sms(websocket):
    sms = await websocket.recv()
    pr(sms)
    await get_sms(websocket)


async def send_sms(websocket):
    sms = await ainput('')
    await websocket.send(sms)
    await send_sms(websocket)




async def listener():
    async with websockets.connect('ws://localhost:8796') as websocket:
        message = await websocket.recv()
        nickname = input(message)
        await websocket.send(nickname)
        task1 = asyncio.create_task(get_sms(websocket))
        task2 = asyncio.create_task(send_sms(websocket))
        await task1
        await task2


# asyncio.run(listener())

loop = asyncio.get_event_loop()
loop.create_task(listener())
loop.run_forever()