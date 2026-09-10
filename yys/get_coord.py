"""采集点击区域坐标的工具。

用法示例（在项目根目录执行）：
    python -m yys.get_coord --mode yuling     # 自动按御灵模式需要的区域逐个采集
    python -m yys.get_coord menu start        # 手动指定区域名
    python -m yys.get_coord                   # 只采集一个区域（兼容旧用法）

每个区域点击两次：左上角、右下角（顺序无所谓）。
按 Esc 放弃当前区域，Ctrl+C 直接退出。
采集结果会打印成可直接粘贴进 modes.py 的代码。
"""

from __future__ import annotations

import argparse
import json
import sys
import threading
import time
from pathlib import Path
from typing import Optional

from pynput import keyboard, mouse

if __package__ in (None, ""):
    # 支持从任意目录直接执行 python yys/get_coord.py
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from yys.click_def import Region
from yys.modes import MODES


def capture_region(label: str, timeout: float = 120.0) -> Optional[Region]:
    """监听鼠标，点击左上角和右下角各一次后返回 Region；Esc 或超时返回 None。"""
    points: list[tuple[int, int]] = []
    done = threading.Event()
    cancelled = threading.Event()

    def on_click(x, y, button, pressed):
        if pressed and button == mouse.Button.left:
            points.append((int(x), int(y)))
            print(f"    第 {len(points)}/2 个点：({int(x)}, {int(y)})")
            if len(points) >= 2:
                done.set()
                return False

    def on_press(key):
        if key == keyboard.Key.esc:
            print("    已按 Esc，放弃该区域")
            cancelled.set()
            return False

    print(f"请点击「{label}」的左上角和右下角（左键取点，Esc 放弃）...")
    with mouse.Listener(on_click=on_click) as mouse_listener, keyboard.Listener(
        on_press=on_press
    ) as keyboard_listener:
        deadline = time.monotonic() + timeout
        while (
            not done.is_set()
            and not cancelled.is_set()
            and time.monotonic() < deadline
        ):
            time.sleep(0.05)

    if cancelled.is_set() or len(points) < 2:
        return None
    (x1, y1), (x2, y2) = points[0], points[1]
    return Region(x1, y1, x2, y2)


def labels_for_mode(mode_name: str) -> list[str]:
    """某个模式需要采集的区域名列表。"""
    mode = MODES[mode_name]
    labels = ["menu", "start"]
    if mode.boost_button is not None:
        labels.append("boost_button")
        labels.extend(f"boost_option_{i + 1}" for i in range(len(mode.boost_options)))
    return labels


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="采集点击区域坐标")
    parser.add_argument("labels", nargs="*", help="区域名，如 menu start boost_button")
    parser.add_argument(
        "--mode",
        choices=sorted(MODES),
        help="按模式自动给出区域名（menu/start/加成等）",
    )
    args = parser.parse_args(argv)

    labels = list(args.labels)
    if args.mode:
        labels = labels_for_mode(args.mode)
    if not labels:
        labels = ["区域"]

    captured: dict[str, Region] = {}
    for label in labels:
        region = capture_region(label)
        if region is None:
            print("已停止采集（Esc 或超时）。")
            break
        captured[label] = region

    if not captured:
        return 1

    print("\n采集完成，以下是可直接粘贴到 modes.py 的配置：")
    for label, region in captured.items():
        print(f"    {label}=Region({region.x1}, {region.y1}, {region.x2}, {region.y2}),")
    print("\nJSON 格式：")
    ranges = {label: region.to_ranges() for label, region in captured.items()}
    print(json.dumps(ranges, ensure_ascii=False, indent=4))
    return 0


def get_region_coords() -> Optional[dict[str, list[int]]]:
    """兼容旧接口：只采集一个区域，返回 {"x": [min,max], "y": [min,max]}。"""
    region = capture_region("目标区域")
    if region is None:
        print("未正确选定区域")
        return None
    return region.to_ranges()


if __name__ == "__main__":
    raise SystemExit(main())
