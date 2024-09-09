'''
本代码用于模拟基站负载情况,基本原理是通过While Ture内的sleep来控制CPU的负载占空比
- 通过多线程的方式模拟多个CPU处在负载状态
- 将这些线程的策略设置为FIFO，保证优先级
- 任务数：表示需要占用的CPU核心数，默认绑定 任务id+2 的CPU上
- 本代码更新了负载放置策略

'''
from multiprocessing import Process
import multiprocessing
import time
import psutil
import os
import threading
import random
import numpy as np
from PIL import Image


TASKS = 11 # 任务数
CHANGE_INTERVAL = 1 # int: 多久更改一次CPU负载
ROUNDS = 300 # 执行多少轮次测试(一次的时间为CHANGE_INTERVAL)
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


# ==================== Version 2 =====================
#                  添加了图像处理作为负载
# ====================================================
class Payload_Image:
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
        _image_path = './data/random_image'+str(self.taskid)+ '.png'
        _width, _height = 200, 200
        _image = Image.new('RGB', (_width, _height))
        
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
                r = random.randint(0, 255)
                g = random.randint(0, 255)
                b = random.randint(0, 255)
                _image.putpixel((10,15),(r,g,b))
                # _image.save(_image_path) # 启用这一行的时候，precent最小控制在0.2，小于该值CPU占用率都会保持在18%左右，也因CPU而异, 如果需要更小的控制，可以减少图像的大小
                pass            
            # Sleep to let the CPU rest
            time.sleep(max(0,0.01-self.precent/100))


def dynamic_press(shared_precent): # 动态负载
    payload_per = 15
    while (payload_per<35):
        payload_per+=3
        shared_precent[0:4] = [payload_per/100]*4
        time.sleep(1)
    while (payload_per>10):
        payload_per-=3
        shared_precent[0:4] = [payload_per/100]*4
        time.sleep(1)
    shared_precent[0:4] = [0.05]*4

def static_press(id,press,wait_time, shared_precent): # 静态负载
    shared_precent[id] = press
    time.sleep(wait_time)
    shared_precent[id] = 0.05


if __name__ == '__main__':
    random.seed(1)
    ppid = os.getpid()
    CPU_Percent = [0.05] * 11

    print('[INFO] Parent PID: ', ppid)

    shared_precent = multiprocessing.Array("f",CPU_Percent)
    processes = []
    for t in range(TASKS):
        payload = Payload_Image(t,CPU_Percent[t], [t+2]) # CPU 压力百分比:0-1 , 绑定核心 [0-cores]
        process = Process(target=payload.cpu_press,args=(shared_precent,))
        processes.append(process)

    for p in processes:
        p.start()

    

    for i in range(ROUNDS):
        for j in range(TASKS):
            if j == 0: # u1 - u4
                r = random.randint(0,100)
                if r < 10: # 10% 的概率
                    # 先增后减的负载
                    print('[INFO]: u1 - u4 increase')
                    process_dynamic_press = Process(target=dynamic_press,args=(shared_precent,))
                    process_dynamic_press.start()
            if j == 4: # u5
                shared_precent[j] = 0.07
                r = random.randint(0,100)
                if r < 1:
                    print('[INFO]: u5 0.3')
                    process_static_press_u5 = Process(target=static_press,args=(j,0.3,3,shared_precent,))
                    process_static_press_u5.start()
                elif r < 10:
                    print('[INFO]: u5 0.2')
                    process_static_press_u5 = Process(target=static_press,args=(j,0.2,10,shared_precent,))
                    process_static_press_u5.start()
            if j == 5: # u6
                r = random.randint(0,100)
                if r < 10:
                    print('[INFO]: u6 0.15')
                    process_static_press_u6 = Process(target=static_press,args=(j,0.15,10,shared_precent,))
                    process_static_press_u6.start()
            if j == 6: # u7, u8
                r = random.randint(0,100)
                if r < 10:
                    print('[INFO]: u7 u8 0.45')
                    process_static_press_u7 = Process(target=static_press,args=(j,0.45,5,shared_precent,))
                    process_static_press_u8 = Process(target=static_press,args=(j+1,0.45,5,shared_precent,))
                    process_static_press_u7.start()
                    process_static_press_u8.start()
            if j == 8: # u9
                shared_precent[j] = 0.2
            if j == 9: # u10
                r = random.randint(0,100)
                if r < 10:
                    print('[INFO]: u10 0.6')
                    process_static_press_u10 = Process(target=static_press,args=(j,0.6,5,shared_precent,))
                    process_static_press_u10.start()
            if j == 10: # u11
                shared_precent[j] = 0.1

        time.sleep(CHANGE_INTERVAL)
        # print(f"[INFO] Global CPU Press: {shared_precent[0:11]}")
        print(f"[INFO] Round: {i}")

    for p in processes:
        # 主函数等待子进程结束
        p.join()




