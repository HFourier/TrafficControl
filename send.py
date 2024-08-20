from utils.tools import send_data
import time

while(1):
    send_data(1024,ip = '192.168.122.1')
    time.sleep(0.001)
