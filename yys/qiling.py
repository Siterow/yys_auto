import random
from click_def import run_auto_battle, setup_logging


def main():
    setup_logging()
    # 定义点击区域
    ranges = {
        "menu": {'x': [1202, 1476], 'y': [260, 289]},  # 主页面
        "start": {'x': [1677, 1736], 'y': [890, 948]}  # 挑战按钮
    }
    # 契灵/活动：战斗结束后等待时间
    def get_battle_end_delay() -> float:
        # click_info(ranges["menu"], delay=random.randrange(23, 25))  # 契灵战斗结束后点击界面
        return random.randrange(8, 10)  # 活动战斗结束后点击界面

    extra_menu_click_delays = [1, 1, 1]

    run_auto_battle(
        circle_time=circleTime,
        ranges=ranges,
        get_battle_end_delay=get_battle_end_delay,
        extra_menu_click_delays=extra_menu_click_delays,
    )


if __name__ == "__main__":
    circleTime = 100
    main()
