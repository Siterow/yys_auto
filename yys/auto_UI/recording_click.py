from pynput.mouse import Listener
import time
import json

# 存储点击记录的列表
clicks = []

# 初始化上一次点击时间
last_click_time = None


def on_click(x, y, button, pressed):
    global last_click_time

    if pressed:
        # 获取当前时间
        current_time = time.time()

        # 计算时间间隔
        if last_click_time is None:
            elapsed_time = 0  # 第一次点击时间间隔为 0
        else:
            elapsed_time = current_time - last_click_time

        # 更新上一次点击时间
        last_click_time = current_time

        # 存储点击位置(x, y)和时间间隔
        x_coord = int(x)
        y_coord = int(y)
        clicks.append({
            'x_coord': x_coord,
            'y_coord': y_coord,
            'time_interval': elapsed_time
        })
        print(f"Clicked at ({x_coord}, {y_coord}), Time since last click: {elapsed_time:.2f} seconds")


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
    with open('../mouse_clicks.json', 'w') as f:
        json.dump(clicks, f, indent=4)
    print(f"Recording finished. {len(clicks)} clicks recorded.")