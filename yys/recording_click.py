from pynput.mouse import Listener
import time
import json

# 存储点击记录的列表
clicks = []

# 记录开始时间
start_time = time.time()


def on_click(x, y, button, pressed):
    if pressed:
        # 计算当前时间与开始时间的间隔
        elapsed_time = time.time() - start_time
        # 存储点击位置(x, y)和时间间隔
        clicks.append({
            'x': x,
            'y': y,
            'time': elapsed_time
        })
        print(f"Clicked at ({x}, {y}), Time: {elapsed_time:.2f} seconds")


def on_move(x, y):
    pass  # 这里只是为了响应鼠标移动事件


def on_scroll(x, y, dx, dy):
    pass  # 这里只是为了响应滚轮事件


try:
    # 启动监听器
    with Listener(on_click=on_click, on_move=on_move, on_scroll=on_scroll) as listener:
        print("Recording mouse clicks... Press Ctrl+C to stop.")
        listener.join()

except KeyboardInterrupt:
    print("\nRecording stopped by user.")
    # 将点击记录保存为JSON文件
    with open('mouse_clicks.json', 'w') as f:
        json.dump(clicks, f)
    print(f"Recording finished. {len(clicks)} clicks recorded.")
