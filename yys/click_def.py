import logging
import random
from typing import Callable, Dict, List

import pyautogui


def setup_logging() -> None:
    """
    统一的日志配置函数，供各个脚本复用。
    多次调用也不会有副作用（logging.basicConfig 只在第一次生效）。
    """
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def click_info(range_dict: Dict[str, List[int]], delay: float = 1.0) -> None:
    """
    在指定范围内生成随机坐标并模拟鼠标点击。

    :param range_dict: 包含横坐标和纵坐标范围的字典，格式为 {"x": [min_x, max_x], "y": [min_y, max_y]}
    :param delay: 点击前的延迟时间（秒）
    """
    x_coord = random.randint(range_dict["x"][0], range_dict["x"][1])
    y_coord = random.randint(range_dict["y"][0], range_dict["y"][1])
    pyautogui.sleep(delay)  # 暂停指定时间
    print(f"点击位置：({x_coord}, {y_coord})")
    pyautogui.click(x_coord, y_coord, button="left")


def perform_boost_actions(
    range_boost_button: Dict[str, List[int]],
    boost_options: List[Dict[str, List[int]]],
) -> None:
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


def run_auto_battle(
    circle_time: int,
    ranges: Dict[str, Dict[str, List[int]]],
    get_battle_end_delay: Callable[[], float],
    extra_menu_click_delays: List[float],
) -> None:
    """
    通用的自动战斗循环逻辑，不同脚本只需传入坐标和时间配置即可。

    :param circle_time: 循环次数（刷本次数）
    :param ranges: 坐标范围配置，至少需要包含 "menu" 和 "start" 两个键
    :param get_battle_end_delay: 返回每局战斗结束后首次点击的延迟（秒）的函数
    :param extra_menu_click_delays: 首次点击后，为了回到主界面额外点击的延迟列表
    """
    # 先点击一下聚焦到窗口内
    click_info(ranges["menu"])

    for i in range(circle_time):
        logging.info(f"开始第 {i + 1} 次操作")
        # 进入战斗
        click_info(ranges["start"], delay=1)
        # 战斗结束后第一次点击
        click_info(ranges["menu"], delay=get_battle_end_delay())
        # 为了防止卡界面，额外多点几次
        for delay in extra_menu_click_delays:
            click_info(ranges["menu"], delay=delay)