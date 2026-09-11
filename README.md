# yys_auto

基于屏幕坐标的鼠标自动化脚本（Mac / 阴阳师）。

## 安装

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

首次运行前，请在 macOS「系统设置 → 隐私与安全性 → 辅助功能」中，
允许运行脚本的终端或 IDE 控制鼠标；用 get_coord.py 采点时按 Esc 取消，还需要“输入监控”权限。

## 自动刷本

统一入口：

```bash
# 方式一：直接运行，模式由 farm.py 顶部的 DEFAULT_MODE 决定
.venv/bin/python yys/farm.py

# 方式二：命令行指定模式
.venv/bin/python -m yys.farm yuling
.venv/bin/python -m yys.farm qiling
.venv/bin/python -m yys.farm yuhun
.venv/bin/python -m yys.farm huodong
```

常用参数：

```bash
.venv/bin/python -m yys.farm yuhun --times 200 --no-boost  # 自定义次数 / 不碰加成按钮
.venv/bin/python -m yys.farm yuhun --boost                 # 开始前也先开一次加成（加成处于关闭状态时用）
```

御魂模式的加成默认行为：刷完后再点一次加成（用于收尾关闭）。
`--boost` 会额外在开始前开一次，`--no-boost` 则完全不碰加成按钮。

直接运行 `yys/farm.py`（模式由文件顶部的 DEFAULT_MODE 决定），或者用命令行参数指定模式。
前面的 yuling.py / qiling.py / yuhun.py / huodong.py 已经删除，逻辑只在 farm.py + modes.py 里。

## 坐标配置

所有模式的坐标统一放在 `yys/modes.py`，需要重新采集时运行：

```bash
.venv/bin/python -m yys.get_coord --mode yuling
```

按提示在每个区域的左上角和右下角各点一次左键，程序会打印可直接粘贴的
`Region(...)` 配置。`--mode` 会自动列出该模式需要的全部区域；也可以手动
指定区域名，如 `python -m yys.get_coord menu start`。

## 停止脚本

鼠标快速甩到屏幕左上角可触发 pyautogui 的 FailSafe 停止循环；
采点脚本按 Esc 放弃当前区域、Ctrl+C 直接退出。
