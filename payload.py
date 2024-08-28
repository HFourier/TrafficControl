from multiprocessing import Process
import time
import psutil
import os
import threading


TASKS = 5


class Payload:
    def __init__(self,precent,cpu_id) -> None:
        self.precent = precent
        self.cpu_id = cpu_id
        self.a = 0
        pass
    def cpu_press(self):   
        '''
        CPU 压力程序
        precent: float, CPU压力百分比
        cpu_id: list, 要绑定的CPU核心编号组
        '''
        
        if self.cpu_id is None:
            pass
        else:
            # pid = os.getppid()
            pid = threading.get_native_id()
            p = psutil.Process(pid)
            p.cpu_affinity(self.cpu_id)
            print(f"[INFO] Process {pid} is now bound to CPU cores: {self.cpu_id}, press: {self.precent}")
        while True:
            start_time = time.time()
            # Busy loop to simulate load
            while time.time() - start_time < self.precent/100:
                self.a+=1
                self.a-=1
                pass
            
            # Sleep to let the CPU rest
            time.sleep(max(0,0.01-self.precent/100))


if __name__ == '__main__':
    ppid = os.getpid()
    print('[INFO] Parent PID: ', ppid)

    processes = []
    for t in range(TASKS):
        payload = Payload(0.8, [t+2]) # CPU 压力百分比:0-1 , 绑定核心 [0-cores]
        process = Process(target=payload.cpu_press)
        processes.append(process)

    for p in processes:
        p.start()

    for p in processes:
        p.join()