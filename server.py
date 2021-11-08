import asyncio
import websockets

clients = {}


async def send_nickname(websocket, sms):
    await websocket.send(sms)


async def get_nickname(websocket):
    c = await websocket.recv()
    return c


async def send_sms(websocket, sms):
    for socket in clients:
        if socket != websocket:
            await socket.send(f'[red]{clients[websocket]}[/red]  ->  {sms}')


async def get_sms(websocket):
    sms = await websocket.recv()
    if sms != '':
        await send_sms(websocket, sms)

    await get_sms(websocket)


async def main_2(websocket, path):
    try:
        await send_nickname(websocket, 'nickname')
        nickname = await get_nickname(websocket)
        print(nickname)
        clients[websocket] = nickname
        # await send_sms(websocket, clients[websocket])
        task1 = asyncio.create_task(get_sms(websocket))
        await task1
    except Exception:
        clients.pop(websocket)


async def main():
    async with websockets.serve(main_2, 'localhost', 8796):
        await asyncio.Future()


asyncio.run(main())
