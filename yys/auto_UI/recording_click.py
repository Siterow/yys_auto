"""录制鼠标左键点击序列。

用法（在项目根目录执行）：
    python -m yys.auto_UI.recording_click

左键点击会被记录；按 Esc 或 Ctrl+C 结束录制。
结果保存为 yys/mouse_clicks.json，格式为
[{"x": .., "y": .., "t": 距第一次点击的秒数}, ...]
"""

from __future__ import annotations

import json
import threading
import time
from pathlib import Path

from pynput import keyboard, mouse

OUTPUT_FILE = Path(__file__).resolve().parent.parent / "mouse_clicks.json"


def main() -> None:
    events: list[dict[str, float | int]] = []
    first_ts: float | None = None
    prev_ts: float | None = None
    stop_requested = threading.Event()

    def on_click(x: int, y: int, button: mouse.Button, pressed: bool) -> None:
        nonlocal first_ts, prev_ts
        if not pressed or button != mouse.Button.left:
            return
        ts = time.monotonic()
        if first_ts is None:
            first_ts = ts
        interval = 0.0 if prev_ts is None else ts - prev_ts
        prev_ts = ts
        events.append({"x": int(x), "y": int(y), "t": round(ts - first_ts, 3)})
        print(f"记录 ({int(x)}, {int(y)})，距上次 {interval:.2f}s，共 {len(events)} 次")

    def on_press(key: keyboard.Key) -> bool:
        if key == keyboard.Key.esc:
            stop_requested.set()
            return False  # 停止键盘监听
        return True

    print("开始录制：左键记录点击，按 Esc 或 Ctrl+C 结束...")
    try:
        with mouse.Listener(on_click=on_click) as mouse_listener, keyboard.Listener(
            on_press=on_press
        ) as keyboard_listener:
            while mouse_listener.running and not stop_requested.is_set():
                time.sleep(0.05)
            keyboard_listener.stop()
    except KeyboardInterrupt:
        print("Ctrl+C，结束录制。")

    with OUTPUT_FILE.open("w", encoding="utf-8") as f:
        json.dump(events, f, ensure_ascii=False, indent=4)
    print(f"录制完成，共 {len(events)} 次点击，已保存到 {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
