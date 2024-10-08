from utils.tools import *
import time
from threading import Thread, Event
from utils import config
from utils.measure import Measure
from xmlrpc.server import SimpleXMLRPCServer
from utils.tools import update_stop_thread, get_stop_thread

csv_file = './data/traffic_data.csv'
interface = "ens6" # 要限制流量的网卡

def send_control_traffic(ip):
    timestamp, traffic_bps_dl, traffic_bps_ul = read_csv(csv_file)
    try:
        # 持续发送数据
        t1 = Thread(target=send_data_max, args=(ip,))
        t1.daemon = True
        t1.start()
    except:
        print ("Error: unable to start thread to monitor")

    for i in range(10):
        record_t = time.time()
        band = traffic_bps_dl[i]
        if band < 2048:
            band = 2048
        limit_bandwidth(interface, band, direction = 'outgoing')
        print("------------time slot: {}, band {} Kbps -------------".format(timestamp[i], band))
        if i == 9:
            update_stop_thread(True) # 停止发送数据
        time_diff = time.time()-record_t
        time.sleep(1-time_diff)
        print("[Debug] Time: ", time.time()-record_t)
    clear_bandwidth_limit(interface)

if __name__ == '__main__':
    update_stop_thread(False)
    clear_bandwidth_limit(interface)
    server = SimpleXMLRPCServer(("0.0.0.0", 8000))
    print("[INFO]Listening on port 8000...")
    server.register_function(send_control_traffic)
    print("[INFO] Wait for request...")
    server.serve_forever()
