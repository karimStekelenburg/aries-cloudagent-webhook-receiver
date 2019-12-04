#!/usr/bin/env python3

import argparse
import asyncio
import aiohttp
from aiohttp import web
import json

from webhookprocessor import Message

app = web.Application()
app.msg_queue = asyncio.Queue()
routes = web.RouteTableDef()

class Topic:
    CONNECTIONS = 'connections'
    BASICMESSAGES = 'basicmessages'
    ISSUE_CREDENTIAL = 'issue_credential'
    PRESENT_PROOF = 'present_proof'

class Message:
    def __init__(self, topic: Topic, payload: dict):
        self.topic = topic
        self.payload = payload

    def to_json(self) -> str:
        return json.dumps(self.__dict__)

async def on_ws_connection(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    while not ws.closed:
        msg = await request.app.msg_queue.get()
        await ws.send_str(msg.to_json())
        
    return ws

@routes.post('/topic/connections/')
async def connections_handler(request):
    msg = Message(Topic.CONNECTIONS, await request.json())
    await request.app.msg_queue.put(msg)
    return web.Response(status=200)

@routes.post('/topic/basicmessages/')
async def basicmessages_handler(request):
    msg = Message(Topic.BASICMESSAGES, await request.json())
    await request.app.msg_queue.put(msg)
    return web.Response(status=200)

@routes.post('/topic/issue_credential/')
async def issue_credential_handler(request):
    msg = Message(Topic.ISSUE_CREDENTIAL, await request.json())
    await request.app.msg_queue.put(msg)
    return web.Response(status=200)

@routes.post('/topic/present_proof/')
async def present_proofs_handler(request):
    msg = Message(Topic.PRESENT_PROOF, await request.json())
    await request.app.msg_queue.put(msg)
    return web.Response(status=200)

@routes.get('/new_messages')
async def new_messages_handler(request):
    response = []
    while not request.app.msg_queue.empty():
        msg = await request.app.msg_queue.get()
        response.append(msg.to_json())

    return web.Response(body=json.dumps(response))

app.add_routes(routes)  # add routes
app.add_routes([web.get('/ws', on_ws_connection)])  # add webdocket route


if __name__ == '__main__':

    # CLI Argument Setup
    parser = argparse.ArgumentParser(
        prog='aca-py webhook receiver',
        description="collects and cache's aca-py webhook calls until requested by controller."
        )
    parser.add_argument(
        '-c', '--collect',
        action='store_true',
        help='test'
     )
    parser.add_argument('--host', '-H', action='store', default='0.0.0.0')
    parser.add_argument('--port', '-p', action='store', default=8080)

    args = parser.parse_args()
    web.run_app(app, host=args.host, port=args.port)