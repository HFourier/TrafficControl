from utils.tools import *
import xmlrpc.client
import os
import psutil
import time



def set_fifo_priority(thread_id):
    # SCHED_FIFO的值为1，表示实时调度策略FIFO
    SCHED_FIFO = 1
    # 设置优先级，取值范围一般为1到99
    priority = 50

    # 构造sched_param结构
    param = os.sched_param(priority)
    
    # 使用sched_setscheduler设置线程的调度策略为FIFO
    os.sched_setscheduler(thread_id, SCHED_FIFO, param)
    print(f"[INFO] Thread {thread_id} set to FIFO with priority {priority}")

if __name__ == '__main__':
    ppid = os.getpid()
    p = psutil.Process(ppid)
    p.cpu_affinity([3])
    # set_fifo_priority(ppid)
    a = 0
    while True:
        start_time = time.time()
        # Busy loop to simulate load
        while time.time() - start_time < 0.98 / 100:
            a+=1
            a-=1
            pass            
        # Sleep to let the CPU rest
        time.sleep(max(0,0.01-0.9/100))

        # time.sleep(0.00001)
        # print(f"[INFO] Thread {ppid} is running")
        
# csv_file = './data/traffic_data.csv'
    # timestamp, traffic_bps_dl, traffic_bps_ul = read_csv(csv_file)
    # interface = "eno1" # 要限制流量的网卡

    # proxy = xmlrpc.client.ServerProxy("http://10.120.66.21:8000/") # 服务端ip
    # proxy.send_control_traffic("10.120.66.23") # 本机ip 
    # print("[INFO] Begin sending")
    