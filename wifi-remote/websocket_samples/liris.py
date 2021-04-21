
# sample with pip3 install websocket_client
# does not work

from websocket import create_connection, enableTrace
from ssl import CERT_NONE 

from requests import get
from tv import SSL_URL, HTTPS_URL
get(HTTPS_URL, verify=False)
sock = create_connection(SSL_URL, timeout=None, 
    sslopt={"cert_reqs": CERT_NONE})

print(sock.recv())
