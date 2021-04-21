# sample with pip3 install tornado and tornado.httpclient
# authentication works
# send key works
# reauthentication works


from tv import SSL_URL
# SSL_URL += "&token=72995033"


from tornado.websocket import websocket_connect
from tornado.httpclient import HTTPRequest
import asyncio
from requests import get

async def tv_conn():
    ws_req = HTTPRequest(SSL_URL, validate_cert=False)
    ws = await websocket_connect(ws_req)
    
    msg = await ws.read_message()
    if not msg:
        pass
    print(msg)
    from json import loads, dumps
    data = loads(msg)
    if data["event"] == "ms.channel.connect":
        print(data["data"]["token"])
        cmd = dumps({
            "method":"ms.remote.control", 
            "params":{
                "Cmd": "Click", 
                "DataOfCmd":"KEY_MUTE", 
                "Option":"false",
                "TypeOfRemote":"SendRemoteKey"
            }
        })
        ws.write_message(cmd)

asyncio.get_event_loop().run_until_complete(tv_conn())