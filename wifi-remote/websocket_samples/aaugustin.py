# sample with pip3 install websockets 
# authentication works


def connect(url):
    from websockets.client import connect, WebSocketClientProtocol
    from ssl import CERT_NONE
    import asyncio
    async def tv_conn():
        async with connect(url, ssl=CERT_NONE, close_timeout=2000, ping_interval=2000) as websocket:
            
            res = await websocket.recv()
            print(res)

    asyncio.get_event_loop().run_until_complete(tv_conn())


if __name__ == "__main__":
    from tv import SSL_URL
    connect(SSL_URL)