from utils.tools import *
import xmlrpc.client


if __name__ == '__main__':

    csv_file = './data/traffic_data.csv'
    timestamp, traffic_bps_dl, traffic_bps_ul = read_csv(csv_file)
    interface = "eno1" # 要限制流量的网卡

    proxy = xmlrpc.client.ServerProxy("http://10.120.66.21:8000/") # 服务端ip
    proxy.send_control_traffic("10.120.66.23") # 本机ip 
    print("[INFO] Begin sending")
    