import random
from click_def import perform_boost_actions, run_auto_battle, setup_logging


def main():
    setup_logging()
    # 定义点击区域
    ranges = {
        "menu": {'x': [1301, 1674], 'y': [359, 395]},  # 主页面
        "start": {'x': [1717, 1747], 'y': [734, 760]},  # 挑战按钮
        "boost_button": {'x': [1292, 1293], 'y': [320, 326]},  # 加成按钮
        "boost_hun": {'x': [1551, 1556], 'y': [418, 423]}  # 御魂加成
    }

    # 开启御魂加成（如不需要可注释掉）
    # perform_boost_actions(ranges["boost_button"], [ranges["boost_hun"]])

    def get_battle_end_delay() -> float:
        # 默认是魂土战斗结束后的等待时间
        return random.randrange(20, 22)

    extra_menu_click_delays = [1, 1, 1, 1, 0.5, 0.5]

    # 执行主操作
    run_auto_battle(
        circle_time=circleTime,
        ranges=ranges,
        get_battle_end_delay=get_battle_end_delay,
        extra_menu_click_delays=extra_menu_click_delays,
    )

    # 关闭加成
    perform_boost_actions(ranges["boost_button"], [ranges["boost_hun"]])


if __name__ == "__main__":
    circleTime = 600
    main()
