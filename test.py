import os
import psutil
import time
from PIL import Image
import numpy as np
import random



if __name__ == '__main__':
    image_path = './data/random_image.png'
    ppid = os.getpid()
    p = psutil.Process(ppid)
    p.cpu_affinity([3])
    width, height = 200, 200
    image = Image.new('RGB', (width, height))
    precent = 0.10 # (0.01 - 0.99)

    while True:
        start_time = time.time()
        # Busy loop to simulate load
        while time.time() - start_time < precent / 100: # 0.9 为控制的percent
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            image.putpixel((10,15),(r,g,b))
            image.save(image_path) # 启用这一行的时候，precent最小控制在0.2，小于该值CPU占用率都会保持在18%左右，也因CPU而异
        # Sleep to let the CPU rest
        time.sleep(max(0,0.01-precent/100))

