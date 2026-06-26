# AI Toy Controller - Local Bridge (AI 控制玩具 - 本地中继服务)

本仓库是 [AI 控制玩具 AstrBot 插件](https://github.com/nikonotnicotine/astrbot_plugin_toy_controller) 的**配套本地运行服务**。

## 💡 为什么需要这个？
因为 AstrBot 机器人通常部署在云端服务器（VPS）上，而你的实体玩具使用的是**本地电脑的蓝牙**。云端无法直接发送蓝牙信号到你的房间里。
因此，我们需要在本地电脑上运行本仓库中的中继脚本。它的工作原理是：
1. 监听本地端口，接收 AstrBot 插件通过 HTTP 发来的 HEX（十六进制）指令。
2. 将指令转换为蓝牙信号，发送给你的实体玩具。

---

## 📂 文件说明

本仓库提供两个脚本，你可以根据自己的需求选择使用：

### 1. `my_local_bridge.py` (🌟 推荐，开箱即用)
专为 **SVAKOM SL278H（分欣 plus）** 编写的异步完整版中继脚本。
- **特性**：自带蓝牙扫描与连接功能、自带 `1.5` 秒防断连续命循环（防止玩具自动停止）、基于 `aiohttp` 的轻量化接收端。

### 2. `VPS_local_server.py` (🛠️ 供开发者二次开发)
一个极简的基于 `Flask` 的接收端框架。
- **特性**：只包含了接收 AstrBot 发送的 HTTP POST 请求的逻辑。如果你有其他品牌的玩具，或者想使用其他蓝牙库控制设备，可以在这个文件的注释处填入你自己的控制代码。

---

## 🚀 使用教程 (以 `my_local_bridge.py` 为例)

### 第一步：安装依赖环境
请确保你的电脑已经安装了 [Python](https://www.python.org/)，然后打开命令行（终端/CMD/PowerShell），输入以下命令安装所需的第三方库：
```bash
pip install aiohttp bleak flask
```

### 第二步：运行脚本与连接设备
1. 打开你的 SL278H 玩具电源（请确保它**没有**被官方手机 App 连着，蓝牙设备通常只能被一个终端独占）。
2. 在终端中运行脚本：
   ```bash
   python my_local_bridge.py
   ```
3. 观察控制台输出，当你看到 `🚀 蓝牙连接成功！启动本地 API 接口` 时，说明本地服务已经就绪。

### 第三步：连接到 AstrBot 插件

根据你的 AstrBot 部署位置，按以下方式配置 AstrBot 插件中的 `toy_api_url`：

- **情况 A：AstrBot 也运行在这台本地电脑上**
  - 直接在 AstrBot 插件配置中填写：`http://127.0.0.1:8080/command`。

- **情况 B：AstrBot 运行在云端 VPS 上（⚠️ 重点）**
  1. 请在 VPS 和本地电脑上安装 [Tailscale](https://tailscale.com/) 并登录，组建安全的私有局域网。
  2. 获取本地电脑的 Tailscale 内网 IP（例如 `100.11.22.33`）。
  3. 用文本编辑器打开 `my_local_bridge.py`，将代码 `site = web.TCPSite(runner, '127.0.0.1', 8080)` 中的 `'127.0.0.1'` 修改为 `'0.0.0.0'` 或你的 Tailscale IP。重启脚本。
  4. 在 AstrBot 插件配置中填写：`http://100.11.22.33:8080/command`。

---

## 💝 鸣谢
本仓库中蓝牙连接与控制逻辑的实现，离不开以下开源项目与热心网友的教程，特此致谢：
* **GitHub 开源项目参考**：[vickyldr/svakom-ble-ai](https://github.com/vickyldr/svakom-ble-ai)
* **小红书博主**：[@0oo0🥕] 与 [@住在宝宝手机里的el]
