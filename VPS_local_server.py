# my_local_bridge.py
import asyncio
import binascii
from aiohttp import web
from bleak import BleakScanner, BleakClient

# 根据 GitHub 文档的提示，通道 UUID 是这个
WRITE_UUID = "0000ffe1-0000-1000-8000-00805f9b34fb"
current_hex = None

async def keepalive_loop(client):
    """文档里提到的核心：每 1.5 秒循环续命，否则玩具会自己停"""
    global current_hex
    while True:
        if client.is_connected and current_hex:
            try:
                # 转换十六进制并发送给玩具
                data_bytes = binascii.unhexlify(current_hex)
                await client.write_gatt_char(WRITE_UUID, data_bytes, response=False)
                print(f"🔄 续命发送 -> {current_hex}")
            except Exception as e:
                print(f"蓝牙发送失败: {e}")
        await asyncio.sleep(1.5)

async def handle_post(request):
    """接收 AstrBot 发来的 HEX"""
    global current_hex
    data = await request.json()
    new_hex = data.get("hex")
    if new_hex:
        current_hex = new_hex
        print(f"📩 收到 AstrBot 新指令: {current_hex}")
    return web.Response(text="OK")

async def main():
    print("🔍 扫描玩具 SL278H...")
    devs = await BleakScanner.discover(timeout=6.0)
    dev = next((d for d in devs if d.name and "SL278" in d.name), None)
    if not dev:
        print("❌ 未找到玩具，请确认设备已开机并且没有连着官方App")
        return
        
    print(f"✅ 找到玩具 {dev.name}，正在连接...")
    async with BleakClient(dev) as client:
        print("🚀 蓝牙连接成功！启动本地 API 接口 (监听 0.0.0.0:8080)")
        
        # 启动 HTTP 接收服务
        app = web.Application()
        app.router.add_post('/command', handle_post)
        runner = web.AppRunner(app)
        await runner.setup()
        
        # 【关键修复】改成 0.0.0.0 才能接收 Tailscale 的外部请求
        site = web.TCPSite(runner, '0.0.0.0', 8080)
        await site.start()

        # 启动 1.5秒 的蓝牙续命循环
        await keepalive_loop(client)

if __name__ == "__main__":
    asyncio.run(main())
