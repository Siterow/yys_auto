import random
from click_def import run_auto_battle, setup_logging


def main():
    setup_logging()
    # 定义点击区域
    ranges = {
        "menu": {'x': [949, 1325], 'y': [276, 344]},  # 主页面
        "start": {'x': [1627, 1676], 'y': [860, 898]}  # 挑战按钮
    }
    # 御灵战斗结束后等待时间
    def get_battle_end_delay() -> float:
        return random.randrange(12, 13)

    extra_menu_click_delays = [1, 1, 1, 1]

    run_auto_battle(
        circle_time=circleTime,
        ranges=ranges,
        get_battle_end_delay=get_battle_end_delay,
        extra_menu_click_delays=extra_menu_click_delays,
    )


if __name__ == "__main__":
    circleTime = 500
    main()
