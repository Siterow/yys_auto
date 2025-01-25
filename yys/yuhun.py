import logging
import random
from click_def import click_info, perform_boost_actions

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,          # 设置最低日志级别为 DEBUG，记录所有级别的日志
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # 设置日志格式
    datefmt='%Y-%m-%d %H:%M:%S'   # 设置时间格式
)


def main():
    # 定义点击区域
    ranges = {
        "menu": {'x': [1301, 1674], 'y': [359, 395]},  # 主页面
        "start": {'x': [1717, 1747], 'y': [734, 760]},  # 挑战按钮
        "boost_button": {'x': [1292, 1293], 'y': [320, 326]},  # 加成按钮
        "boost_hun": {'x': [1551, 1556], 'y': [418, 423]}  # 御魂加成
    }
    # 先点击一下聚焦到窗口内
    click_info(ranges["menu"])
    # 开启御魂加成
    # perform_boost_actions(ranges["boost_button"], [ranges["boost_hun"]])

    # 执行主操作
    for i in range(circleTime):  # 修改循环次数可控制操作重复次数
        click_info(ranges["start"], delay=1)
        logging.info(f"开始第 {i + 1} 次操作")
        # click_info(ranges["menu"], delay=random.randrange(23, 25))  # 魂土战斗结束后点击界面
        click_info(ranges["menu"], delay=random.randrange(16, 18))  # 魂十战斗结束后点击界面
        # click_info(ranges["menu"], delay=random.randrange(48, 49))  # 魂王战斗结束后点击界面
        click_info(ranges["menu"], delay=0.5)  # 再次点击回到主界面
        click_info(ranges["menu"], delay=3)  # 再次点击回到主界面
        click_info(ranges["menu"], delay=0.5)  # 再次点击回到主界面

        # click_info(ranges["menu"], delay=1)  # 再次点击回到主界面
        # click_info(ranges["menu"], delay=1)  # 再次点击回到主界面
        # click_info(ranges["menu"], delay=0.5)  # 再次点击回到主界面

    # 关闭加成
    perform_boost_actions(ranges["boost_button"], [ranges["boost_hun"]])


if __name__ == "__main__":
    circleTime = 293
    main()
