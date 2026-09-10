# yys_auto
# yys_auto

基于屏幕坐标的鼠标自动化脚本（Mac / 阴阳师）。

## 安装

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

首次运行前，请在 macOS「系统设置 → 隐私与安全性 → 辅助功能」中，
允许运行脚本的终端或 IDE 控制鼠标；录制/回放还需要允许“输入监控”。

## 自动刷本

统一入口：

```bash
# 在项目根目录
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

御魂模式默认与 `yuhun.py` 现状一致：刷完后再点一次加成（用于收尾关闭）。
`--boost` 会额外在开始前开一次，`--no-boost` 则完全不碰加成按钮。

也可以照旧直接运行 `yys/yuling.py` 等文件，行为与不带参数的模式入口等价。

## 坐标配置

所有模式的坐标统一放在 `yys/modes.py`，需要重新采集时运行：

```bash
.venv/bin/python -m yys.get_coord --mode yuling
```

按提示在每个区域的左上角和右下角各点一次左键，程序会打印可直接粘贴的
`Region(...)` 配置。`--mode` 会自动列出该模式需要的全部区域；也可以手动
指定区域名，如 `python -m yys.get_coord menu start`。

## 录制 / 回放

```bash
# 录制：左键记录，Esc 或 Ctrl+C 结束
.venv/bin/python -m yys.auto_UI.recording_click

# 回放：3 秒后开始，可指定次数、倍速和坐标抖动
.venv/bin/python -m yys.auto_UI.replaying_click
.venv/bin/python -m yys.auto_UI.replaying_click --repeat 10 --scale 1.2
```

录制文件为 `yys/mouse_clicks.json`，新版格式为
`[{"x": .., "y": .., "t": 相对第一次点击的秒数}]`；回放兼容旧版
`time_interval` 格式。

## 停止脚本

鼠标快速甩到屏幕左上角可触发 pyautogui 的 FailSafe 停止循环；
录制/回放可直接 Ctrl+C。
