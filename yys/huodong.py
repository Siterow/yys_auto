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
        "menu": {'x': [944, 1306], 'y': [234, 311]},  # 主页面
        "start": {'x': [1654, 1715], 'y': [903, 952]},  # 挑战按钮
    }
    # 先点击一下聚焦到窗口内
    click_info(ranges["menu"])

    # 执行主操作
    for i in range(circleTime):  # 修改循环次数可控制操作重复次数
        click_info(ranges["start"], delay=1)
        logging.info(f"开始第 {i + 1} 次操作")
        click_info(ranges["menu"], delay=random.randrange(10, 12))  # 魂土战斗结束后点击界面
        click_info(ranges["menu"], delay=0.5)  # 再次点击回到主界面
        click_info(ranges["menu"], delay=0.5)  # 再次点击回到主界面


if __name__ == "__main__":
    circleTime = 993
    main()
