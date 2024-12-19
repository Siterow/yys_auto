from pynput.mouse import Controller
import time
import json

# 读取点击记录
with open('mouse_clicks.json', 'r') as f:
    clicks = json.load(f)

# 创建一个鼠标控制器对象
mouse = Controller()

# 自动点击
print("Replaying recorded mouse clicks...")
start_time = time.time()

for click in clicks:
    # 计算当前点击的时间点
    elapsed_time = click['time']
    # 等待直到该时间点
    time.sleep(elapsed_time - (time.time() - start_time))
    # 移动鼠标到指定位置
    mouse.position = (click['x'], click['y'])
    # 执行点击
    mouse.click(mouse.Button.left)
    print(f"Clicked at ({click['x']}, {click['y']})")