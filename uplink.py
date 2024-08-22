from utils.tools import *
import time
from threading import Thread, Event
from utils import config
from utils.measure import Measure



def measure():
    nm = Measure(config.nic_name)
    try:
        while 1:
            time.sleep(0.02)
            nm.renew_nic_state()
            nm.record()
            ans = nm.get_state()
            print(ans)
    except KeyboardInterrupt:
        nm.write_data()
        print('end!')

if __name__ == '__main__':

    csv_file = './data/traffic_data.csv'
    timestamp, traffic_bps_dl, traffic_bps_ul = read_csv(csv_file)
    interface = "eno1" # 要限制流量的网卡
    
    try:
        # 持续发送数据
        t1 = Thread(target=send_data_max)
        t1.daemon = True
        t1.start()

    except:
        print ("Error: unable to start thread to monitor")

    try:
        t2 = Thread(target=measure)
        t2.daemon = True
        t2.start()

    except:
        print ("Error: unable to start thread to monitor")


    print('Interface: ', interface)
    # ======================= 2024年08月20日 =======================
    for i in range(10):
        time.sleep(1)
        band = traffic_bps_dl[i]
        if band < 2048:
            band = 2048
        limit_bandwidth(interface, band, direction = 'outgoing')
        print("------------time slot: {}, band {} Kbps -------------".format(timestamp[i], band))
    clear_bandwidth_limit(interface)
    # ======================= 2024年08月20日 =======================


