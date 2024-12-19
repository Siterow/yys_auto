import pyautogui
from pynput import mouse
import time

coords = []  # 用于存储点击的坐标

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

# def capture_and_save_region(region):
#     """
#     根据指定区域范围截取屏幕图像并保存
#     :param region: 区域范围字典，格式 {"x": [x_min, x_max], "y": [y_min, y_max]}
#     """
#     x_min, x_max = region["x"]
#     y_min, y_max = region["y"]
#     width = x_max - x_min
#     height = y_max - y_min
#
#     print(f"截取区域：(x={x_min}, y={y_min}, width={width}, height={height})")
#     screenshot = pyautogui.screenshot(region=(x_min, y_min, width, height))
#     screenshot.save("captured_region.png")
#     print("区域截图已保存为 captured_region.png")


if __name__ == "__main__":
    # 第一步：获取用户选定区域的坐标
    region_coords = get_region_coords()
    #
    # # 第二步：根据坐标范围截取屏幕
    # if region_coords:
    #     capture_and_save_region(region_coords)