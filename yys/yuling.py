"""御灵自动刷本入口。

直接运行本文件，等价于：
    python -m yys.farm yuling
"""

from pathlib import Path
import sys

if __package__ in (None, ""):
    # 兼容“在 yys 目录下 python yuling.py”和“在项目根目录 python yys/yuling.py”
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from yys.click_def import setup_logging
from yys.farm import run_mode


def main() -> None:
    setup_logging()
    run_mode("yuling")


if __name__ == "__main__":
    main()
