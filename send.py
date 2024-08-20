from utils.tools import send_data, send_control_data, get_global_rate, update_rate


data_size = 1024*1024 # 发送1M的数据量
target_rate = 350 # 控制速率
adjust = 1 # 调整器
packet_size = 1 # 初始化为发送1个包

pac = packet_size
while True:
    # 持续发送数据
    # target_rate = get_global_rate()
    
    get_rate = send_control_data(data_size=data_size,packet_size=pac,ip = '10.120.66.21')
    adjust = target_rate / get_rate
    pac = int(pac * adjust) + 1
    if pac < 1:
        pac =1
    elif pac > 1024*60:
        pac = 1024*60

    # print('[Debug] pac: ', pac )
# time.sleep(0.001)
