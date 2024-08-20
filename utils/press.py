import csv
import time
import socket
import os
import threading
import subprocess


def send_data(amount, packet_size=4096, ip = 'localhost', port = 9999):
    # 创建一个UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (ip, port)
    
    # 生成随机字节数据
    num_packets = (amount + packet_size - 1) // packet_size  # 计算需要发送的包数
    
    try:
        for _ in range(int(num_packets)):
            message = os.urandom(min(packet_size, amount))
            amount -= packet_size
            sock.sendto(message, server_address)
            # print(f'Sent {len(message)} bytes of data')
    finally:
        # 关闭socket
        sock.close()



while True:
    send_data(100000000)
