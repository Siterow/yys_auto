"""御魂（魂土）自动刷本入口。

直接运行本文件，等价于：
    python -m yys.farm yuhun

加成默认与当前 yuhun.py 行为一致：刷完后再点一次（收尾关闭）。
开始前也想自动开一次（加成当前为关）时：
    python -m yys.farm yuhun --boost
完全不碰加成按钮时：
    python -m yys.farm yuhun --no-boost
"""

from pathlib import Path
import sys

if __package__ in (None, ""):
    # 兼容“在 yys 目录下 python yuhun.py”和“在项目根目录 python yys/yuhun.py”
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from yys.click_def import setup_logging
from yys.farm import run_mode


def main() -> None:
    setup_logging()
    run_mode("yuhun")


if __name__ == "__main__":
    main()
