"""统一刷本入口。

用法：
    python yys/farm.py                    # 用下面 DEFAULT_MODE 指定的模式直接跑
    python -m yys.farm yuling --times 190  # 也可以命令行指定模式
    python -m yys.farm yuhun --no-boost   # 完全不碰御魂加成按钮
    python -m yys.farm yuhun --boost      # 开始前也开一次加成（加成当前为关时使用）

换模式只要改下面的 DEFAULT_MODE，或者用命令行参数指定。
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

import pyautogui

if __package__ in (None, ""):
    # 支持从任意目录直接执行 python yys/farm.py
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from yys.click_def import perform_boost_actions, run_auto_battle, setup_logging
from yys.modes import MODES

# 直接运行 python yys/farm.py 时使用的模式，改这里即可（yuling / qiling / yuhun / huodong）
DEFAULT_MODE = "huodong"

logger = logging.getLogger("yys.farm")


def run_mode(
    mode_name: str,
    circle_time: int | None = None,
    boost_before: bool | None = None,
    boost_after: bool | None = None,
) -> None:
    """运行某个模式。参数不传时使用模式配置的默认值。"""
    try:
        mode = MODES[mode_name]
    except KeyError:
        names = "、".join(sorted(MODES))
        raise SystemExit(f"未知模式 {mode_name!r}，可用模式：{names}") from None

    if circle_time is None:
        circle_time = mode.default_circle_time
    if boost_before is None:
        boost_before = mode.boost_before_run
    if boost_after is None:
        boost_after = mode.boost_after_run

    has_boost = mode.boost_button is not None
    finished_ok = False
    try:
        if has_boost and boost_before:
            perform_boost_actions(mode.boost_button, mode.boost_options, label="御魂加成")
        run_auto_battle(mode, circle_time)
        finished_ok = True
    except pyautogui.FailSafeException:
        logger.warning("检测到 FailSafe：鼠标被移到屏幕角落，循环已停止。")
    finally:
        # 只在正常跑完时才在结束后点一次加成
        if finished_ok and has_boost and boost_after:
            perform_boost_actions(mode.boost_button, mode.boost_options, label="御魂加成")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="阴阳师自动刷本")
    parser.add_argument(
        "mode",
        nargs="?",
        choices=sorted(MODES),
        default=DEFAULT_MODE,
        help=f"刷本模式，默认 {DEFAULT_MODE}",
    )
    parser.add_argument("-n", "--times", type=int, help="刷本次数（默认使用模式配置值）")
    boost_group = parser.add_mutually_exclusive_group()
    boost_group.add_argument("--boost", action="store_true", help="刷本开始前也开一次御魂加成")
    boost_group.add_argument("--no-boost", action="store_true", help="完全不碰御魂加成按钮")
    args = parser.parse_args(argv)

    setup_logging()
    run_mode(
        args.mode,
        circle_time=args.times,
        boost_before=True if args.boost else None,
        boost_after=False if args.no_boost else None,
    )
    logger.info("完成")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
