
import socket
import struct

def hex_enc(mac_address):
    # create the magic packet from MAC address
    split_mac = mac_address.split(':')
    hex_mac = list(int(h, base=16) for h in split_mac)
    hex_mac = struct.pack('BBBBBB', *hex_mac)
    
    return b'\xff' * 6 + hex_mac * 16

def multicast(packet):
    # send packag
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.sendto(packet, ('255.255.255.255', 9))
    sock.close()

def wol(mac_address):
    packet = hex_enc(mac_address)
    multicast(packet)


if __name__ == "__main__":
    mac_address = "D0:D0:03:7E:2E:A1"
    wol(mac_address)
    print("wol sent")
