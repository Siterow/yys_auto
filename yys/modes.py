"""各刷本模式的坐标与节奏配置，统一在这里维护。

坐标是屏幕绝对像素，换分辨率或移动窗口后需要重新采集：
    python -m yys.get_coord --mode yuling
然后把打印出来的 Region(...) 行替换到下面。
"""

from __future__ import annotations

from yys.click_def import BattleMode, Region

MODES: dict[str, BattleMode] = {
    "yuling": BattleMode(
        name="yuling",
        display_name="御灵",
        menu=Region(949, 276, 1325, 344),
        start=Region(1627, 860, 1676, 898),
        end_delay_range=(12, 14),
        extra_menu_click_delays=(1.0, 1.0, 1.0, 1.0),
        default_circle_time=190,
    ),
    "qiling": BattleMode(
        name="qiling",
        display_name="契灵/活动",
        menu=Region(1202, 260, 1476, 289),
        start=Region(1677, 890, 1736, 948),
        end_delay_range=(8, 10),
        extra_menu_click_delays=(1.0, 1.0, 1.0),
        default_circle_time=100,
    ),
    "yuhun": BattleMode(
        name="yuhun",
        display_name="御魂·魂土",
        menu=Region(1638, 850, 1706, 906),
        start=Region(1622, 851, 1700, 904),
        end_delay_range=(33, 35),
        extra_menu_click_delays=(1.0, 1.0, 1.0, 0.5, 0.5),
        boost_button=Region(874, 158, 903, 197),
        boost_options=(Region(1262, 361, 1356, 376),),
        # 默认只在刷完后点一次加成（开始前不自动开）。
        # 需要“开始前也开一次”时用 python -m yys.farm yuhun --boost。
        boost_after_run=True,
        default_circle_time=200,
    ),
    "huodong": BattleMode(
        name="huodong",
        display_name="活动",
        menu=Region(1227, 266, 1641, 342),
        start=Region(1660, 903, 1708, 953),
        end_delay_range=(4, 6),
        extra_menu_click_delays=(1.0, 1.0),
        default_circle_time=1,
    ),
}
