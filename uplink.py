from utils.tools import *
import time
from threading import Thread, Event
from utils import config
from utils.measure import Measure
import xmlrpc.client

def measure():
    # 测量带宽
    nm = Measure(config.nic_name) # 网卡名称
    try:
        while 1:
            time.sleep(0.02) # 每隔0.02 秒记录一次
            nm.renew_nic_state()
            nm.record()
            ans = nm.get_state()
            print(ans)
    except KeyboardInterrupt:
        nm.write_data()
        print('end!')
    
def get_downlink_traffic():
    # 发送RPC到 ip地址为10.120.66.21 的服务器，让对面也开始发送流量
    proxy = xmlrpc.client.ServerProxy("http://10.120.66.21:8000/") # 服务端ip
    proxy.send_control_traffic("10.120.66.23") # 本机ip 
    print("[INFO] Begin sending")

if __name__ == '__main__':

    csv_file = './data/traffic_data.csv' # 流量大小预设文件
    timestamp, traffic_bps_dl, traffic_bps_ul = read_csv(csv_file)
    interface = "eno1" # 要限制流量的网卡
    # 初始化限制带宽为10240 kbps 
    limit_bandwidth(interface, 10240, direction = 'outgoing')

    try:
        # 启动测量进程
        t2 = Thread(target=measure)
        t2.daemon = True
        t2.start()

    except:
        print ("Error: unable to start thread to monitor")
    
    try:
        # PRC调用对端持续发送流量
        t3 = Thread(target=get_downlink_traffic)
        t3.daemon = True
        t3.start()

    except:
        print ("Error: unable to start thread to downlink")
    
    try:
        # 本端持续发送数据
        t1 = Thread(target=send_data_max)
        t1.daemon = True
        t1.start()

    except:
        print ("Error: unable to start thread to monitor")


    print('Interface: ', interface)
    # ======================= 2024年08月20日 =======================
    time.sleep(0.43) # 手动调整参数，为了两段控制带宽的时间点对齐
    for i in range(10):
        record_t = time.time()
        band = traffic_bps_dl[i]
        if band < 2048: # 防止带宽限制过小
            band = 2048
        limit_bandwidth(interface, band, direction = 'outgoing')
        print("------------time slot: {}, band {} Kbps -------------".format(timestamp[i], band))
        time_diff = time.time()-record_t
        time.sleep(1-time_diff) # 保证一次循环是1s
        print("[Debug] Time: ", time.time()-record_t)
        
    clear_bandwidth_limit(interface)
    # ======================= 2024年08月20日 =======================


