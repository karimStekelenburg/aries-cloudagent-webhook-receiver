#!/usr/bin/env python3

# This executable can be used to test the websocket connection of a 
# aca-py message processor instance. 

import asyncio
import os

import aiohttp

HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', 8080))

URL = f'http://{HOST}:{PORT}/ws'


async def main():
    session = aiohttp.ClientSession()
    async with session.ws_connect(URL) as ws:

        async for msg in ws:
            print('Message received from server:')
            print(msg)
            print()
        print('done')

async def prompt_and_send(ws):
    new_msg_to_send = input('Type a message to send to the server: ')
    if new_msg_to_send == 'exit':
        print('Exiting!')
        raise SystemExit(0)
    await ws.send_str(new_msg_to_send)


if __name__ == '__main__':
    print('Type "exit" to quit')
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())