# AI Toy Controller - Local Bridge (AI 控制玩具 - 本地中继服务)

本仓库是 [AI 控制玩具 AstrBot 插件](https://github.com/nikonotnicotine/astrbot_plugin_toy_controller) 的**配套本地运行服务**。

## 💡 为什么需要这个？
因为 AstrBot 机器人通常部署在云端服务器（VPS）上，而你的实体玩具使用的是**本地电脑的蓝牙**。云端无法直接发送蓝牙信号到你的房间里。
因此，我们需要在本地电脑上运行本仓库中的中继脚本。它的工作原理是：
1. 监听本地端口，接收 AstrBot 插件通过 HTTP 发来的 HEX（十六进制）指令。
2. 将指令转换为蓝牙信号，发送给你的实体玩具。

## 💝 鸣谢
本仓库中蓝牙连接与控制逻辑的实现，离不开以下开源项目与热心网友的教程，特此致谢：
* **GitHub 开源项目参考**：[vickyldr/svakom-ble-ai](https://github.com/vickyldr/svakom-ble-ai)
* **小红书博主**：[@0oo0🥕] 与 [@住在宝宝手机里的el]
