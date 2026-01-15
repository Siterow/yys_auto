import random
from click_def import run_auto_battle, setup_logging


def main():
    setup_logging()
    # 定义点击区域
    ranges = {
        "menu": {'x': [944, 1306], 'y': [234, 311]},  # 主页面
        "start": {'x': [1654, 1715], 'y': [903, 952]},  # 挑战按钮
    }
    # 活动战斗结束后等待时间
    def get_battle_end_delay() -> float:
        return random.randrange(10, 12)

    extra_menu_click_delays: list[float] = []

    run_auto_battle(
        circle_time=circleTime,
        ranges=ranges,
        get_battle_end_delay=get_battle_end_delay,
        extra_menu_click_delays=extra_menu_click_delays,
    )


if __name__ == "__main__":
    circleTime = 900
    main()
