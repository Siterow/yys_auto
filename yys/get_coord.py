import pyautogui
from pynput import mouse
import time

coords = []  # 用于存储点击的坐标。此文件用于直接输入坐标范围

def on_click(x, y, button, pressed):
    """
    鼠标点击事件处理函数
    :param x: 鼠标点击的横坐标
    :param y: 鼠标点击的纵坐标
    :param button: 鼠标按键
    :param pressed: 是否是按下事件
    """
    if pressed:
        print(f"记录坐标: ({x}, {y})")
        coords.append((int(x), int(y)))
        if len(coords) == 2:  # 记录两个点后停止监听
            return False


def get_region_coords():
    """
    获取用户选定的区域坐标
    """
    print("请手动点击区域的两个角点（左上角和右下角）...")
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()
    if len(coords) == 2:
        # 计算区域范围
        x_min, y_min = coords[0]
        x_max, y_max = coords[1]
        x_range = [min(x_min, x_max), max(x_min, x_max)]
        y_range = [min(y_min, y_max), max(y_min, y_max)]
        range_info = {"x": x_range, "y": y_range}
        print(f'区域范围：{range_info}')
        coords.clear()
        return range_info
    else:
        print("未正确选定区域")
        return None


if __name__ == "__main__":
    region_coords = get_region_coords()
