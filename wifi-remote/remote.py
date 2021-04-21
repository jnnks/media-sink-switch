# general data
from base64 import b64encode
HOST_NAME = b64encode("solctl".encode()).decode("utf-8")

TV_WIFIMAC = "D0:D0:03:7E:2E:A1"
TV_IP = "192.168.0.66"
SSL_PORT = 8002

SSL_URL = f"wss://{TV_IP}:{SSL_PORT}/api/v2/channels/samsung.remote.control?name={HOST_NAME}"
# ------------

import os 
import json

pwd = os.path.dirname(os.path.realpath(__file__))

settings = None
if os.path.exists(f"{pwd}/settings.json"):
    with open(f"{pwd}/settings.json") as file:
        settings = json.load(file)

#with open(f"{pwd}/settings.json", "w+") as file:
#    json.dump(response, file)






def is_tv_online():
    import subprocess
    result = subprocess.call(["ping", "-c1", "-W1", TV_IP], stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    return result == 0

# create the magic packet from TV MAC address
import struct
split_mac = TV_WIFIMAC.split(':')
hex_mac = list(int(h, base=16) for h in split_mac)
hex_mac = struct.pack('BBBBBB', *hex_mac)
packet = b'\xff' * 6 + hex_mac * 16


# send wake on LAN signal
from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_BROADCAST
from time import sleep
tries = 0

while not is_tv_online() and tries < 10:
        
    with socket(AF_INET, SOCK_DGRAM) as sock:
        sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        sock.sendto(packet, ('255.255.255.255', 9))

    # time buffer to wake up
    sleep(1)

    tries += 1

if not is_tv_online():
    print("TV is offline")





# SSL_URL += "&token=72995033"


from tornado.websocket import websocket_connect
from tornado.httpclient import HTTPRequest
import asyncio
from requests import get

from json import loads, dumps

class TvClient():
    def __init__(self, url, handlers):
        self.url = url
        self.handlers = handlers


    def handle_response(self, msg: str):
        payload = json.loads(msg)
        if "event" in payload:
            event = payload["event"]
            if event in self.handlers:
                self.handlers[event](payload)

    async def connect(self):
        ws_req = HTTPRequest(self.url, validate_cert=False)
        self.connection = await websocket_connect(ws_req, on_message_callback=self.handle_response)
        response = await self.connection.read_message()
        self.handle_response(response)


    async def send(self, key: str):
        cmd = dumps({
            "method":"ms.remote.control", 
            "params":{
                "Cmd": "Click", 
                "DataOfCmd":"KEY_MUTE", 
                "Option":"false",
                "TypeOfRemote":"SendRemoteKey"
            }
        })
        self.connection.write_message(cmd)
        self.connection.read_message(callback=self.handle_response)


def channel_connect(payload: {}):
    print("channel connect")


async def main(token):
    client = TvClient(SSL_URL + f"&{token}", handlers={
        "ms.channel.connect": channel_connect
    })
    await client.connect()

    while True:
        await client.send("KEY_MUTE")
        sleep(2)


asyncio.get_event_loop().run_until_complete(main(settings["token"]))
#async def tv_conn():
#    
#    
#    data = loads(msg)
#    if data["event"] == "ms.channel.connect":
#        print(data["data"]["token"])
#        cmd = dumps({
#            "method":"ms.remote.control", 
#            "params":{
#                "Cmd": "Click", 
#                "DataOfCmd":"KEY_MUTE", 
#                "Option":"false",
#                "TypeOfRemote":"SendRemoteKey"
#            }
#        })
#    connection.write_message(cmd)

input("Press Enter to continue...")
print("done")