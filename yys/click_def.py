import random
from typing import Dict, List

import pyautogui


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