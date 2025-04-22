#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Phone MCP - 一个通过ADB命令控制Android手机的MCP插件
"""

import json
import subprocess
import sys
from typing import Dict, List, Optional, Any, Union

# 尝试导入MCP库，如果不存在则提供基本实现
try:
    from mcp.server import FastMCP
    HAS_MCP = True
except ImportError:
    HAS_MCP = False
    print("警告: MCP库未安装，使用基本实现")
    
    # 基本MCP服务器实现
    class FastMCP:
        def __init__(self, name):
            self.name = name
            self.tools = {}
            
        def tool(self):
            def decorator(func):
                self.tools[func.__name__] = func
                return func
            return decorator
            
        def run(self, transport='stdio'):
            if transport != 'stdio':
                print(f"警告: 仅支持stdio传输，忽略{transport}")
                
            # 简单的JSON-RPC处理循环
            while True:
                try:
                    line = sys.stdin.readline().strip()
                    if not line:
                        break
                        
                    request = json.loads(line)
                    method = request.get('method')
                    params = request.get('params', {})
                    request_id = request.get('id')
                    
                    if method == 'initialize':
                        response = {
                            "jsonrpc": "2.0",
                            "result": {"version": "1.0", "capabilities": ["tools"]},
                            "id": request_id
                        }
                    elif method == 'list_tools':
                        tools_info = []
                        for name, func in self.tools.items():
                            tools_info.append({
                                "name": name,
                                "description": func.__doc__ or "",
                                "parameters": {}
                            })
                        response = {
                            "jsonrpc": "2.0",
                            "result": {"tools": tools_info},
                            "id": request_id
                        }
                    elif method == 'call_tool':
                        tool_name = params.get('name')
                        tool_params = params.get('parameters', {})
                        
                        if tool_name in self.tools:
                            try:
                                result = self.tools[tool_name](**tool_params)
                                response = {
                                    "jsonrpc": "2.0",
                                    "result": result,
                                    "id": request_id
                                }
                            except Exception as e:
                                response = {
                                    "jsonrpc": "2.0",
                                    "error": {"code": -32603, "message": str(e)},
                                    "id": request_id
                                }
                        else:
                            response = {
                                "jsonrpc": "2.0",
                                "error": {"code": -32601, "message": f"工具 {tool_name} 未找到"},
                                "id": request_id
                            }
                    else:
                        response = {
                            "jsonrpc": "2.0",
                            "error": {"code": -32601, "message": f"方法 {method} 未找到"},
                            "id": request_id
                        }
                        
                    sys.stdout.write(json.dumps(response) + "\n")
                    sys.stdout.flush()
                    
                except Exception as e:
                    error_response = {
                        "jsonrpc": "2.0",
                        "error": {"code": -32700, "message": f"解析错误: {str(e)}"},
                        "id": None
                    }
                    sys.stdout.write(json.dumps(error_response) + "\n")
                    sys.stdout.flush()

# ADB命令执行器
class ADBExecutor:
    def __init__(self):
        self.device = None
        
    def run_command(self, cmd: List[str], check_output: bool = True) -> str:
        """执行ADB命令并返回输出"""
        try:
            if check_output:
                full_cmd = ['adb']
                if self.device:
                    full_cmd.extend(['-s', self.device])
                full_cmd.extend(cmd)
                result = subprocess.check_output(full_cmd, stderr=subprocess.STDOUT, text=True)
                return result.strip()
            else:
                full_cmd = ['adb']
                if self.device:
                    full_cmd.extend(['-s', self.device])
                full_cmd.extend(cmd)
                subprocess.run(full_cmd, check=True)
                return "命令执行成功"
        except subprocess.CalledProcessError as e:
            return f"错误: {e.output if hasattr(e, 'output') else str(e)}"
            
    def set_device(self, device_id: str) -> str:
        """设置要使用的设备ID"""
        self.device = device_id
        return f"已设置设备: {device_id}"
        
    def get_devices(self) -> List[Dict[str, str]]:
        """获取已连接的设备列表"""
        output = self.run_command(['devices', '-l'])
        devices = []
        
        for line in output.splitlines()[1:]:  # 跳过标题行
            if not line.strip() or 'daemon' in line:
                continue
                
            parts = line.split()
            if len(parts) >= 2:
                device_id = parts[0]
                status = parts[1]
                model = next((p.split(':')[1] for p in parts if p.startswith('model:')), "未知")
                devices.append({
                    "id": device_id,
                    "status": status,
                    "model": model
                })
                
        return devices

# 创建MCP服务器
app = FastMCP('phone-mcp')
adb = ADBExecutor()

# 设备管理工具
@app.tool()
def check_connection() -> Dict[str, Any]:
    """检查ADB连接状态并返回已连接的设备"""
    devices = adb.get_devices()
    if devices:
        # 如果没有设置设备但有可用设备，自动设置第一个设备
        if not adb.device and devices[0]['status'] == 'device':
            adb.set_device(devices[0]['id'])
            
        return {
            "connected": True,
            "devices": devices,
            "current_device": adb.device
        }
    else:
        return {
            "connected": False,
            "devices": [],
            "current_device": None
        }

@app.tool()
def set_device(device_id: str) -> str:
    """设置要使用的Android设备
    
    Args:
        device_id: 要使用的设备ID
        
    Returns:
        设置结果消息
    """
    return adb.set_device(device_id)

# 电话功能
@app.tool()
def call(phone_number: str) -> str:
    """拨打电话
    
    Args:
        phone_number: 要拨打的电话号码
        
    Returns:
        操作结果消息
    """
    cmd = ['shell', 'am', 'start', '-a', 'android.intent.action.CALL', '-d', f'tel:{phone_number}']
    return adb.run_command(cmd, check_output=False)

@app.tool()
def hangup() -> str:
    """结束当前通话
    
    Returns:
        操作结果消息
    """
    # 使用按键模拟挂断电话
    cmd = ['shell', 'input', 'keyevent', 'KEYCODE_ENDCALL']
    return adb.run_command(cmd, check_output=False)

# 短信功能
@app.tool()
def send_sms(phone_number: str, message: str) -> str:
    """发送短信
    
    Args:
        phone_number: 接收者的电话号码
        message: 短信内容
        
    Returns:
        操作结果消息
    """
    # 使用intent发送短信
    cmd = [
        'shell', 'am', 'start', '-a', 'android.intent.action.SENDTO', 
        '-d', f'smsto:{phone_number}', '--es', 'sms_body', message
    ]
    return adb.run_command(cmd, check_output=False)

# 应用管理
@app.tool()
def open_app(app_name: str) -> str:
    """打开应用
    
    Args:
        app_name: 应用名称或包名
        
    Returns:
        操作结果消息
    """
    # 尝试作为包名启动
    if '.' in app_name:
        cmd = ['shell', 'monkey', '-p', app_name, '-c', 'android.intent.category.LAUNCHER', '1']
        return adb.run_command(cmd, check_output=False)
    else:
        # 尝试查找匹配的应用
        cmd = ['shell', 'pm', 'list', 'packages', app_name]
        result = adb.run_command(cmd)
        if result.startswith('package:'):
            package = result.split('package:')[1].strip()
            cmd = ['shell', 'monkey', '-p', package, '-c', 'android.intent.category.LAUNCHER', '1']
            return adb.run_command(cmd, check_output=False)
        else:
            return f"找不到应用: {app_name}"

@app.tool()
def close_app(package_name: str) -> str:
    """关闭应用
    
    Args:
        package_name: 应用的包名
        
    Returns:
        操作结果消息
    """
    cmd = ['shell', 'am', 'force-stop', package_name]
    return adb.run_command(cmd, check_output=False)

# 屏幕交互
@app.tool()
def tap(x: int, y: int) -> str:
    """在屏幕上点击指定坐标
    
    Args:
        x: X坐标
        y: Y坐标
        
    Returns:
        操作结果消息
    """
    cmd = ['shell', 'input', 'tap', str(x), str(y)]
    return adb.run_command(cmd, check_output=False)

@app.tool()
def swipe(x1: int, y1: int, x2: int, y2: int, duration: int = 300) -> str:
    """在屏幕上从一个点滑动到另一个点
    
    Args:
        x1: 起始X坐标
        y1: 起始Y坐标
        x2: 结束X坐标
        y2: 结束Y坐标
        duration: 滑动持续时间(毫秒)
        
    Returns:
        操作结果消息
    """
    cmd = ['shell', 'input', 'swipe', str(x1), str(y1), str(x2), str(y2), str(duration)]
    return adb.run_command(cmd, check_output=False)

@app.tool()
def input_text(text: str) -> str:
    """输入文本
    
    Args:
        text: 要输入的文本
        
    Returns:
        操作结果消息
    """
    cmd = ['shell', 'input', 'text', text]
    return adb.run_command(cmd, check_output=False)

@app.tool()
def press_key(keycode: str) -> str:
    """按下按键
    
    Args:
        keycode: 按键代码，如KEYCODE_HOME, KEYCODE_BACK等
        
    Returns:
        操作结果消息
    """
    cmd = ['shell', 'input', 'keyevent', keycode]
    return adb.run_command(cmd, check_output=False)

# 媒体功能
@app.tool()
def take_screenshot(output_path: str = "/sdcard/screenshot.png") -> str:
    """截取屏幕截图
    
    Args:
        output_path: 截图保存路径
        
    Returns:
        操作结果消息
    """
    cmd = ['shell', 'screencap', '-p', output_path]
    result = adb.run_command(cmd, check_output=False)
    
    # 将截图拉到本地
    local_path = "screenshot.png"
    pull_cmd = ['pull', output_path, local_path]
    pull_result = adb.run_command(pull_cmd, check_output=False)
    
    return f"截图已保存到: {local_path}"

# 浏览器功能
@app.tool()
def open_url(url: str) -> str:
    """在设备的默认浏览器中打开URL
    
    Args:
        url: 要打开的URL
        
    Returns:
        操作结果消息
    """
    # 确保URL有协议前缀
    if not url.startswith('http://') and not url.startswith('https://'):
        url = 'https://' + url
        
    cmd = ['shell', 'am', 'start', '-a', 'android.intent.action.VIEW', '-d', url]
    return adb.run_command(cmd, check_output=False)

# 主入口
if __name__ == "__main__":
    app.run(transport='stdio')