import asyncio
import binascii
from aiohttp import web
from bleak import BleakScanner, BleakClient

# 玩具的通道 UUID
WRITE_UUID = "0000ffe1-0000-1000-8000-00805f9b34fb"
current_hex = None

async def handle_post(request):
    """接收 AstrBot 发来的 HEX"""
    global current_hex
    try:
        data = await request.json()
        new_hex = data.get("hex")
        if new_hex:
            current_hex = new_hex
            print(f"📩 收到 AstrBot 新指令: {current_hex}")
        return web.Response(text="OK")
    except Exception as e:
        return web.Response(text=f"Error: {e}", status=400)

async def bluetooth_task():
    """蓝牙连接与自动重连任务"""
    global current_hex
    while True:
        try:
            print("\n🔍 正在扫描玩具 SL278H...")
            devs = await BleakScanner.discover(timeout=5.0)
            dev = next((d for d in devs if d.name and "SL278" in d.name), None)
            
            if not dev:
                print("❌ 未找到玩具，5秒后自动重试扫描...")
                await asyncio.sleep(5)
                continue
                
            print(f"✅ 找到玩具 {dev.name}，正在尝试连接...")
            async with BleakClient(dev) as client:
                print("🚀 蓝牙连接成功！可以开始发送指令了。")
                
                # 连接成功后，进入 1.5秒 的续命循环
                while client.is_connected:
                    if current_hex:
                        try:
                            data_bytes = binascii.unhexlify(current_hex)
                            await client.write_gatt_char(WRITE_UUID, data_bytes, response=False)
                            print(f"🔄 续命发送 -> {current_hex}")
                        except Exception as e:
                            print(f"⚠️ 发送数据失败: {e}，准备断开重连...")
                            break # 退出当前循环，触发重连逻辑
                            
                    await asyncio.sleep(1.5)
                    
        except Exception as e:
            print(f"💔 蓝牙发生异常: {e}")
            
        print("⏳ 准备重新连接，等待 3 秒...")
        await asyncio.sleep(3)

async def main():
    # 1. 启动 HTTP 接收服务 (只启动一次，挂在后台)
    app = web.Application()
    app.router.add_post('/command', handle_post)
    runner = web.AppRunner(app)
    await runner.setup()
    
    # 注意这里用的是 0.0.0.0，方便你的 Tailscale 穿透
    site = web.TCPSite(runner, '0.0.0.0', 8080)
    await site.start()
    print("🌐 本地 API 接口已启动 (监听 0.0.0.0:8080)")

    # 2. 启动蓝牙自动重连任务 (阻塞主线程)
    await bluetooth_task()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 程序已手动退出。")
