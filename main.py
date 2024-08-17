from tools import read_csv, send_data, send_data_max, clear_bandwidth_limit, limit_bandwidth
import time
from threading import Thread, Event
from measure import *



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

    csv_file = 'traffic_data.csv'
    timestamp, traffic_bps_dl, traffic_bps_ul = read_csv(csv_file)
    interface = 'eno1'
    
    try:
        # 持续发送数据
        t1 = Thread(target=send_data_max)
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


    
    while True:
        # 控制带宽 间隔1s
        for i in range(len(timestamp)):
            time.sleep(1)
            clear_bandwidth_limit(interface)
            band = traffic_bps_dl[i]
            if band < 1024:
                band = 1024
            limit_bandwidth(interface, band, direction = 'incoming')
            print("------------time slot: {}, band {} Kbps -------------".format(timestamp[i], band))

    
    # for i in range(len(timestamp)):
    #     # time.sleep(1)
    #     traffic_bytes_per_second = int(traffic_bps_dl[i] // 8)
    #     # for ... 
    #     send_data(traffic_bytes_per_second)
    #     if traffic_bytes_per_second == 0:
    #         print("No data sent")
    #     print("------------time slot: {} -------------".format(timestamp[i]))


