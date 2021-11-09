import asyncio
import websockets

clients = {}


async def send_nickname(websocket, sms):
    await websocket.send(sms)


async def get_nickname(websocket):
    c = await websocket.recv()
    return c


async def send_sms(websocket, sms):
    sms, chat = sms[:sms.index(' TO - > '):], sms[sms.index(' TO - > '):]
    print('>'+chat[8::]+'<')
    if chat[8::] == 'GROUP':
        for socket in clients:
            if socket != websocket:
                await socket.send(f'[red]{clients[websocket]}[/red]  ->  {sms}')
    else:
        for socket in clients:
            if clients[socket] == chat[8::]:
                await socket.send(f'[red]{clients[websocket]} privat[/red]  ->  {sms}')


async def get_sms(websocket):
    sms = await websocket.recv()
    print(sms)
    if sms == '':
        pass
    elif sms == 'GET_ALL_CHATS':
        print(1)
        print('CHATS__!@#!#'+',  '.join(list(clients.values()) + ['GROUP']))
        await websocket.send('CHATS__!@#!#'+',  '.join(list(clients.values()) + ['GROUP']))
        print(1)
    else:
        await send_sms(websocket, sms)

    await get_sms(websocket)


async def main_2(websocket, path):
    try:
        await send_nickname(websocket, 'nickname')
        nickname = await get_nickname(websocket)
        # print(nickname)
        print(', '.join(clients.values()))
        await websocket.send(',  '.join(list(clients.values()) + ['GROUP']))
        clients[websocket] = nickname
        # await send_sms(websocket, clients[websocket])
        task1 = asyncio.create_task(get_sms(websocket))
        await task1
    except Exception:
        clients.pop(websocket)


async def main():
    async with websockets.serve(main_2, 'localhost', 15346):
        await asyncio.Future()


asyncio.run(main())
