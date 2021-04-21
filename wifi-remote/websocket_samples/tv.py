
TV_IP = "192.168.0.66"
SSL_PORT = 8002

from base64 import b64encode
HOST_NAME = b64encode("solctl".encode()).decode("utf-8")

SSL_URL = f"wss://{TV_IP}:{SSL_PORT}/api/v2/channels/samsung.remote.control?name={HOST_NAME}"
HTTPS_URL = f"https://{TV_IP}:{SSL_PORT}/api/v2/channels/samsung.remote.control?name={HOST_NAME}"