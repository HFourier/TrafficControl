'''
本代码用于模拟基站负载情况,基本原理是通过While Ture内的sleep来控制CPU的负载占空比
- 通过多线程的方式模拟多个CPU处在负载状态
- 将这些线程的策略设置为FIFO，保证优先级

- 任务数：表示需要占用的CPU核心数，默认绑定 任务id+2 的CPU上

'''
from multiprocessing import Process
import multiprocessing
import time
import psutil
import os
import threading
import numpy as np


TASKS = 5 # 任务数
CHANGE_INTERVAL = 5 # int: 多久更改一次CPU负载
ROUNDS = 10 # 执行多少轮次测试
Press_Level = []

def set_fifo_priority(thread_id):
    # SCHED_FIFO的值为1，表示实时调度策略FIFO
    SCHED_FIFO = 1
    # 设置优先级，取值范围一般为1到99
    priority = 50

    # 构造sched_param结构
    param = os.sched_param(priority)
    
    # 使用sched_setscheduler设置线程的调度策略为FIFO
    os.sched_setscheduler(thread_id, SCHED_FIFO, param)
    print(f"[INFO] Thread {thread_id} set to FIFO with priority {priority}")

class Payload:
    def __init__(self,taskid,precent,cpu_id) -> None:
        self.taskid = taskid
        self.precent = precent
        self.cpu_id = cpu_id
        self.a = 0
        pass
    def cpu_press(self,shared_precent):   
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
            set_fifo_priority(pid) # 设置为FIFO策略
            p = psutil.Process(pid)
            p.cpu_affinity(self.cpu_id)
            print(f"[INFO] Process {pid} is now bound to CPU cores: {self.cpu_id}, press: {self.precent}")
        while True:
            self.precent = shared_precent[self.taskid]
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
    choseable_level = [0.34,0.66,0.98]
    CPU_Percent = [0.99]*TASKS
    for j in range(TASKS):
        CPU_Percent[j] = np.random.choice(choseable_level)
    print('[INFO] Parent PID: ', ppid)

    shared_precent = multiprocessing.Array("f",CPU_Percent)
    processes = []
    for t in range(TASKS):
        Press_Level.append(np.random.choice(choseable_level))
        payload = Payload(t,Press_Level[t], [t+2]) # CPU 压力百分比:0-1 , 绑定核心 [0-cores]
        process = Process(target=payload.cpu_press,args=(shared_precent,))
        processes.append(process)

    for p in processes:
        p.start()

    for i in range(ROUNDS):
        for j in range(TASKS):
            shared_precent[j] = np.random.choice(choseable_level)
        time.sleep(CHANGE_INTERVAL)
        print(f"[INFO] Global CPU Press: {CPU_Percent}")

    for p in processes:
        # 主函数等待子进程结束
        p.join()

    