import asyncio
import os

import aiohttp.web
import aiohttp

HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', 8080))


async def testhandle(request):
    return aiohttp.web.Response(text='Test handle')

async def prompt_and_send(ws):
    new_msg_to_send = input('Type a message to send to the server: ')
    if new_msg_to_send == 'exit':
        print('Exiting!')
        raise SystemExit(0)
    await ws.send_str(new_msg_to_send)


async def websocket_handler(request):
    print('Websocket connection starting')
    ws = aiohttp.web.WebSocketResponse()
    await ws.prepare(request)
    print('Websocket connection ready')

    while True:
        await prompt_and_send(ws)


    print('Websocket connection closed')
    return ws


def main():
    loop = asyncio.get_event_loop()
    app = aiohttp.web.Application(loop=loop)
    app.router.add_route('GET', '/', testhandle)
    app.router.add_route('GET', '/ws', websocket_handler)
    aiohttp.web.run_app(app, host=HOST, port=PORT)


if __name__ == '__main__':
    main()