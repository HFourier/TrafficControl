from utils.tools import *
import time
from threading import Thread, Event
from utils import config
from utils.measure import Measure



def measure():
    nm = Measure(config.nic_name)
    try:
        while 1:
            time.sleep(0.1)
            nm.renew_nic_state()
            nm.record()
            ans = nm.get_state()
            
            # print(f'{ans[0]}:  net_in:{ans[1]}   net_out:{ans[2]}   mem: {ans[3]}({ans[4]})   cpu: {ans[5]}--{ans[6][0]}Hz')
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
        # t1 = Thread(target=send_data_max)
        t1 = Thread(target=send_data_ac_rate)
        t1.daemon = True
        t1.start()

    except:
        print ("Error: unable to start thread to monitor")

    try:
        # 持续监控数据
        t2 = Thread(target=measure)
        t2.daemon = True
        t2.start()

    except:
        print ("Error: unable to start thread to monitor")


    
    # while True:
        # 控制带宽 间隔1s
    # for i in range(len(timestamp)):
    # limit_bandwidth(interface, 4080)
    print('Interface: ', interface)
    # clear_bandwidth_limit(interface)
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

    # for i in range(100):
    #     time.sleep(1)
    #     band = traffic_bps_dl[i]
    #     update_rate(band)   
        # send_control_data(data_size=1024*1024,packet_size=10,ip = '10.120.66.21')

