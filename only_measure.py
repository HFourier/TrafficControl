
from utils import config
from utils.measure import Measure
import time
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
    measure()