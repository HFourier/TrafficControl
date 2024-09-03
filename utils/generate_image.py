from PIL import Image
import random

# 创建一个100x100的新图像
width, height = 200, 200
image = Image.new('RGB', (width, height))

# 遍历每个像素并设置随机颜色
for x in range(width):
    for y in range(height):
        # 生成随机的RGB值
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        image.putpixel((x, y), (r, g, b))

# 显示图像
# image.show()

# 保存图像到文件
image.save('random_image.png')