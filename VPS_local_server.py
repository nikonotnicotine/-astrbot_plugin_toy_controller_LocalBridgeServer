# 需要安装: pip install flask
from flask import Flask, request

app = Flask(__name__)

@app.route('/command', methods=['POST'])
def receive_command():
    data = request.json
    hex_cmd = data.get("hex")
    if hex_cmd:
        print(f"收到来自 VPS 的控制指令: {hex_cmd}")
        # 【在这里加上你控制本地蓝牙设备的代码】
        # 例如将 hex_cmd 转换为 bytearray 发送给蓝牙特征值
        # bytes.fromhex(hex_cmd) 
        return {"status": "success", "msg": "指令已发送"}, 200
    return {"status": "error", "msg": "缺少指令"}, 400

if __name__ == '__main__':
    # 监听本地 8080 端口
    app.run(host='0.0.0.0', port=8080)