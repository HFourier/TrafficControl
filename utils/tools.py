import csv
import time
import socket
import os
import threading
import subprocess


rate = 0
def read_csv(csv_file):
    # 打开CSV文件
    traffic_bps_dl = []
    traffic_bps_ul = []
    timestamp = []
    with open(csv_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        # 读取CSV文件中的每一行
        for row in reader:
            start_time = time.perf_counter()
            timestamp.append(row['datetime']) # 获取时间戳
            traffic_bps_dl.append(float(row['DL(kbps)']))
            traffic_bps_ul.append(float(row['UL(kbps)']))
        
    return timestamp, traffic_bps_dl, traffic_bps_ul   


def send_data(amount, packet_size=4096, ip = '10.120.66.21', port = 9999):
    # 创建一个UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (ip, port)
    
    # 生成随机字节数据
    num_packets = (amount + packet_size - 1) // packet_size  # 计算需要发送的包数
    
    try:
        for _ in range(int(num_packets)):
            message = os.urandom(min(packet_size, amount))
            amount -= packet_size
            sock.sendto(message, server_address) # 计算sent to执行的时间
            # 负反馈机制，比设定值高一点点 
            # print(f'Sent {len(message)} bytes of data')
    finally:
        # 关闭socket
        sock.close()


def send_control_data(data_size=1024*1024,packet_size=4096, ip = '10.120.66.21', port = 9999):
    # 创建一个UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (ip, port)

    amount = data_size
    
    # 生成随机字节数据
    num_packets = (amount + packet_size - 1) // packet_size  # 计算需要发送的包数
    record_size = amount/1024

    try:
        record_t1 = time.time()
        # print('[Debug packet_size]: ', packet_size)
        # print('[Debug num_packets]: ', num_packets)
        for _ in range(int(num_packets)):
            message = os.urandom(min(packet_size, amount))
            amount -= packet_size
            sock.sendto(message, server_address) # 计算sent to执行的时间
            # 负反馈机制，比设定值高一点点 
            # print(f'Sent {len(message)} bytes of data')
        record_t2 = time.time()
        get_rate = record_size/(record_t2-record_t1)
        print('[Debug get rate]: ', get_rate," kbps")
    finally:
        # 关闭socket
        sock.close()
    
    return get_rate




def start_server(host='0.0.0.0', port=9999, output_file='received_traffic.csv'):
    # 创建一个UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (host, port)
    sock.bind(server_address)
    
    print(f'Server started on {host}:{port}')
    
    received_data = []
    stop_event = threading.Event()

    def log_traffic():
        while not stop_event.is_set():
            start_time = time.perf_counter()
            received_bytes = 0
            t1=time.time()
            while time.perf_counter() - start_time < 1:
                try:
                    data, address = sock.recvfrom(4096)
                    if data:
                        received_bytes += len(data)
                except socket.timeout:
                    pass
                except OSError:
                    break
            tr=time.time()-t1
            if not stop_event.is_set():
                timestamp = int(start_time)
                received_bits = received_bytes * 8  # 转换为比特
                received_data.append((timestamp, received_bits))
                print(f"Time: {timestamp}, Received: {received_bits} bits, using time:{tr}")
        # 确保记录最后一秒的数据
        if received_bytes > 0:
            timestamp = int(start_time)
            received_bits = received_bytes * 8  # 转换为比特
            received_data.append((timestamp, received_bits))
            print(f"Time: {timestamp}, Received: {received_bits} bits")

    log_thread = threading.Thread(target=log_traffic)
    log_thread.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    finally:
        # 通知线程停止
        stop_event.set()
        # 发送一个小的数据包来触发 recvfrom 退出阻塞状态
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as trigger_sock:
            trigger_sock.sendto(b'', server_address)
        log_thread.join()
        # 关闭socket
        sock.close()
        # 将记录的数据写入CSV文件
        with open(output_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['timestamp', 'traffic'])
            writer.writerows(received_data)
        print(f"Data saved to {output_file}")


def limit_bandwidth(interface,bandwidth, direction = 'both'):
    if direction == 'both':
        subprocess.run(['tcset', interface, '--rate', f'{bandwidth}Kbps', '--change'])
    else:
        subprocess.run(['tcset', interface,'--direction', direction, '--rate', f'{bandwidth}Kbps', '--overwrite'])


def clear_bandwidth_limit(interface):
    # subprocess.run(['tcdel', interface])
    subprocess.run(['tc', 'qdisc', 'del', 'dev', interface, 'root'])


def send_data_max():
    while (1):
        send_data(1024)

def update_rate(rate_):
    global rate
    rate = rate_

def get_global_rate():
    global rate
    return rate

def send_data_ac_rate():
    data_size = 1024*1024 # 发送1M的数据量
    target_rate = 350 # 控制速率
    adjust = 1 # 调整器
    packet_size = 1 # 初始化为发送1个包
    pac = packet_size

    
    while True:
        # 持续发送数据
        target_rate = get_global_rate()
        get_rate = send_control_data(data_size=data_size,packet_size=pac,ip = '10.120.66.21')
        adjust = target_rate / get_rate
        pac = int(pac * adjust) + 1
        if pac < 1:
            pac =1
        elif pac > 1024*60:
            pac = 1024*60
