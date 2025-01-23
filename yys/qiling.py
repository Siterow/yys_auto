import logging
import random
import pyautogui
from typing import Dict, List

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,          # 设置最低日志级别为 DEBUG，记录所有级别的日志
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # 设置日志格式
    datefmt='%Y-%m-%d %H:%M:%S'   # 设置时间格式
)


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


def main():
    # 定义点击区域
    ranges = {
        "menu": {'x': [1318, 1619], 'y': [366, 384]},  # 主页面
        "start": {'x': [1720, 1749], 'y': [802, 829]}  # 挑战按钮
    }
    # 先点击一下聚焦到窗口内
    click_info(ranges["menu"])

    # 执行主操作
    for i in range(circleTime):  # 修改循环次数可控制操作重复次数
        logging.info(f"开始第 {i + 1} 次操作")
        click_info(ranges["start"], delay=1)
        # click_info(ranges["menu"], delay=random.randrange(23, 25))  # 契灵战斗结束后点击界面
        click_info(ranges["menu"], delay=random.randrange(20, 22))  # 活动战斗结束后点击界面
        click_info(ranges["menu"], delay=1)  # 再次点击回到主界面
        click_info(ranges["menu"], delay=2)  # 再次点击回到主界面
        click_info(ranges["menu"], delay=1)  # 再次点击回到主界面
        click_info(ranges["menu"], delay=random.randrange(1, 2))  # 再次点击回到主界面


if __name__ == "__main__":
    circleTime = 200
    main()
