"""通用的点击与刷本逻辑：Region 区域抽象、人性化点击、自动战斗循环。"""

from __future__ import annotations

import logging
import random
import time
from dataclasses import dataclass
from typing import Mapping, Optional, Sequence, Union

import pyautogui

logger = logging.getLogger("yys.click_def")

# 兼容旧格式 {"x": [min, max], "y": [min, max]} 的点击目标
ClickTarget = Union["Region", Mapping[str, Sequence[int]]]


def setup_logging() -> None:
    """统一日志配置，可重复调用（basicConfig 只在第一次生效）。"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)-7s %(name)s - %(message)s",
        datefmt="%H:%M:%S",
    )


@dataclass(frozen=True)
class Region:
    """屏幕上的矩形点击区域，点击时在区域内随机取点。"""

    x1: int
    y1: int
    x2: int
    y2: int

    def __post_init__(self) -> None:
        # 自动归一化，采集时两个角点的点击顺序不影响结果
        object.__setattr__(self, "x1", min(self.x1, self.x2))
        object.__setattr__(self, "x2", max(self.x1, self.x2))
        object.__setattr__(self, "y1", min(self.y1, self.y2))
        object.__setattr__(self, "y2", max(self.y1, self.y2))

    @classmethod
    def from_ranges(cls, data: Mapping[str, Sequence[int]]) -> "Region":
        """把旧格式 {"x": [min, max], "y": [min, max]} 转成 Region。"""
        return cls(data["x"][0], data["y"][0], data["x"][1], data["y"][1])

    def random_point(self) -> tuple[int, int]:
        return random.randint(self.x1, self.x2), random.randint(self.y1, self.y2)

    def to_ranges(self) -> dict[str, list[int]]:
        return {"x": [self.x1, self.x2], "y": [self.y1, self.y2]}


@dataclass(frozen=True)
class BattleMode:
    """一个刷本模式的完整配置。"""

    name: str
    display_name: str
    menu: Region  # 战斗结算后点这里回到主界面
    start: Region  # 挑战/开始按钮
    end_delay_range: tuple[int, int]  # 战斗结束后的等待秒数范围，随机取整数
    extra_menu_click_delays: tuple[float, ...] = ()
    boost_button: Optional[Region] = None
    boost_options: tuple[Region, ...] = ()
    boost_before_run: bool = False  # 刷本开始前先点一次加成
    boost_after_run: bool = False  # 刷本结束后再点一次加成
    default_circle_time: int = 100

    def random_end_delay(self) -> int:
        return random.randrange(*self.end_delay_range)


def click_info(
    target: ClickTarget,
    delay: float = 1.0,
    *,
    name: str = "",
    move_duration: tuple[float, float] = (0.15, 0.35),
) -> None:
    """
    在区域内取随机点，等待 delay 秒后平滑移动鼠标并点击。

    :param target: Region 或旧格式 {"x": [min,max], "y": [min,max]}
    :param delay: 点击前等待的秒数
    :param name: 点击目标说明，用于日志
    :param move_duration: 鼠标移动耗时范围，随机取值更像人手
    """
    region = target if isinstance(target, Region) else Region.from_ranges(target)
    x, y = region.random_point()
    if delay > 0:
        pyautogui.sleep(delay)
    pyautogui.moveTo(x, y, duration=random.uniform(*move_duration))
    time.sleep(random.uniform(0.03, 0.08))  # 到位后短暂停顿再点击
    logger.info("点击%s (%d, %d)", f"「{name}」" if name else "", x, y)
    pyautogui.click(x, y)


def perform_boost_actions(
    boost_button: Region,
    boost_options: Sequence[Region],
    *,
    label: str = "加成",
) -> None:
    """打开加成菜单 → 勾选加成项 → 关闭菜单（再调用一次即为切换）。"""
    click_info(boost_button, name=f"{label}按钮")
    for option in boost_options:
        click_info(option, delay=1.0, name=f"{label}选项")
    click_info(boost_button, name=f"关闭{label}菜单")


def run_auto_battle(mode: BattleMode, circle_time: int) -> None:
    """按模式配置循环刷本。"""
    click_info(mode.menu, name="聚焦窗口")

    for i in range(1, circle_time + 1):
        logger.info("=== %s 第 %d/%d 次 ===", mode.display_name, i, circle_time)
        click_info(mode.start, delay=1.0, name="开始挑战")
        # 战斗结束后第一次点击，等待时长由模式配置决定
        click_info(mode.menu, delay=mode.random_end_delay(), name="战斗结算")
        # 额外多点几次主界面，防止卡界面
        for extra_delay in mode.extra_menu_click_delays:
            click_info(mode.menu, delay=extra_delay, name="返回主界面")
