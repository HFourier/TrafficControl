from scapy.all import *
import random

for _ in range(100):
    src_port = random.randint(1024, 65535)
    payload = "Data: " + str(random.randint(1, 1000))
    packet = IP(dst="127.0.0.0")/UDP(sport=src_port, dport=9999)/Raw(load=payload)
    send(packet)