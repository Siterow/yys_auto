import random
import pyautogui
from typing import Dict, List


def click_info(range_dict: Dict[str, List[int]], delay: float = 1.0):
    """
    在指定范围内生成随机坐标并模拟鼠标点击。

    :param range_dict: 包含横坐标和纵坐标范围的字典，格式为 {"x": [min_x, max_x], "y": [min_y, max_y]}
    :param delay: 点击前的延迟时间（秒）
    """
    x_coord = random.randint(range_dict['x'][0], range_dict['x'][1])
    y_coord = random.randint(range_dict['y'][0], range_dict['y'][1])
    pyautogui.sleep(delay)  # 暂停指定时间
    print(f"点击位置：({x_coord}, {y_coord})")
    pyautogui.click(x_coord, y_coord, button='left')


def perform_boost_actions(range_boost_button: Dict[str, List[int]], boost_options: List[Dict[str, List[int]]]):
    """
    执行开启或关闭加成操作。

    :param range_boost_button: 加成按钮的点击范围
    :param boost_options: 加成选项的范围列表
    """
    # 点击加成按钮
    click_info(range_boost_button)
    for option in boost_options:
        click_info(option, delay=1)  # 每个选项之间延迟 1 秒
    # 再次点击加成按钮关闭菜单
    click_info(range_boost_button)


def main():
    # 定义点击区域
    ranges = {
        "group": {"x": [1599, 1628], "y": [735, 767]},  # 组队
        "start": {"x": [1689, 1760], "y": [764, 802]},  # 挑战按钮
        "boost_button": {"x": [1176, 1192], "y": [290, 310]},  # 加成按钮
        "boost_hun": {"x": [1498, 1505], "y": [416, 427]},  # 御魂加成
    }
    # 先点击一下聚焦到窗口内
    click_info(ranges["menu"])
    # 开启御魂加成
    perform_boost_actions(ranges["boost_button"], [ranges["boost_hun"]])

    # 执行主操作
    for i in range(circleTime):  # 修改循环次数可控制操作重复次数
        print(f"开始第 {i + 1} 次操作")
        click_info(ranges["start"])
        pyautogui.sleep(random.randrange(28, 31))  # 每轮操作之间暂停
        click_info(ranges["menu"])  # 战斗结束后点击界面
        pyautogui.sleep(random.randrange(1, 3))
        click_info(ranges["menu"])  # 再次点击回到主界面

    # 关闭加成
    perform_boost_actions(ranges["boost_button"], [ranges["boost_hun"]])


if __name__ == "__main__":
    circleTime = 50
    main()
