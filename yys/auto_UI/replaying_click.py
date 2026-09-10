"""回放录制的鼠标点击序列。

用法（在项目根目录执行）：
    python -m yys.auto_UI.replaying_click                  # 播放一遍
    python -m yys.auto_UI.replaying_click --repeat 5        # 循环 5 遍
    python -m yys.auto_UI.replaying_click --scale 1.5       # 1.5 倍速

兼容新版（t 字段）和旧版（time_interval 字段）录制文件。
播放会在 3 秒后开始，方便你切到游戏窗口；Ctrl+C 随时中断。
"""

from __future__ import annotations

import argparse
import json
import random
import time
from pathlib import Path

from pynput import mouse

DEFAULT_FILE = Path(__file__).resolve().parent.parent / "mouse_clicks.json"


def load_clicks(path: Path) -> list[dict[str, float]]:
    """读取录制文件并统一成 [{"x", "y", "t"}]，t 为距第一次点击的秒数。"""
    raw = json.loads(path.read_text(encoding="utf-8"))
    events: list[dict[str, float]] = []
    prev_t = 0.0
    for index, item in enumerate(raw, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"第 {index} 条记录不是对象: {item!r}")
        x = item.get("x", item.get("x_coord"))
        y = item.get("y", item.get("y_coord"))
        if x is None or y is None:
            raise ValueError(f"第 {index} 条记录缺少坐标字段 x/y: {item!r}")
        if "t" in item:
            t = float(item["t"])
        elif "time_interval" in item:
            # 旧版录的是“距上一次点击的间隔”，累加为时间点
            t = prev_t + float(item["time_interval"])
        else:
            raise ValueError(f"第 {index} 条记录缺少时间字段 t/time_interval: {item!r}")
        prev_t = t
        events.append({"x": float(x), "y": float(y), "t": t})
    return events


def replay(
    events: list[dict[str, float]],
    *,
    repeat: int = 1,
    scale: float = 1.0,
    jitter: int = 0,
) -> None:
    """按录制节奏回放。t 是相对第一次点击的时间，直接按间隔播放。"""
    controller = mouse.Controller()
    print(
        f"回放 {len(events)} 次点击 × {repeat} 轮，速度 ×{scale}"
        + (f"，坐标随机抖动 ±{jitter}px" if jitter else "")
    )
    print("3 秒后开始，请切换到游戏窗口...")
    time.sleep(3)

    for round_no in range(1, repeat + 1):
        round_start = time.monotonic()
        for index, event in enumerate(events, start=1):
            target = round_start + event["t"] / scale
            wait = target - time.monotonic()
            if wait > 0:
                time.sleep(wait)
            x = int(event["x"]) + random.randint(-jitter, jitter)
            y = int(event["y"]) + random.randint(-jitter, jitter)
            controller.position = (x, y)
            controller.click(mouse.Button.left)
            print(f"第 {round_no}/{repeat} 轮，第 {index}/{len(events)} 次：({x}, {y})")
    print("回放完成。")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="回放录制的鼠标点击序列")
    parser.add_argument("--file", type=Path, default=DEFAULT_FILE, help="录制的 JSON 文件")
    parser.add_argument("-r", "--repeat", type=int, default=1, help="循环播放次数")
    parser.add_argument("-s", "--scale", type=float, default=1.0, help="播放速度倍率，>1 更快")
    parser.add_argument("-j", "--jitter", type=int, default=0, help="每次点击坐标的随机抖动(px)")
    args = parser.parse_args(argv)

    if args.repeat < 1:
        parser.error("--repeat 必须 >= 1")
    if args.scale <= 0:
        parser.error("--scale 必须 > 0")
    if args.jitter < 0:
        parser.error("--jitter 必须 >= 0")

    events = load_clicks(args.file)
    replay(events, repeat=args.repeat, scale=args.scale, jitter=args.jitter)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
