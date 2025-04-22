#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Phone MCP CLI - 命令行界面，用于直接与Android设备交互
"""

import argparse
import sys
from typing import List, Optional, Dict, Any

# 导入主模块
from phone_mcp import ADBExecutor

adb = ADBExecutor()

def parse_args() -> argparse.Namespace:
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description="Phone MCP命令行工具")
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # 检查连接
    check_parser = subparsers.add_parser("check", help="检查设备连接")
    
    # 设置设备
    device_parser = subparsers.add_parser("device", help="设置要使用的设备")
    device_parser.add_argument("device_id", help="设备ID")
    
    # 电话功能
    call_parser = subparsers.add_parser("call", help="拨打电话")
    call_parser.add_argument("phone_number", help="电话号码")
    
    hangup_parser = subparsers.add_parser("hangup", help="结束当前通话")
    
    # 短信功能
    sms_parser = subparsers.add_parser("send-sms", help="发送短信")
    sms_parser.add_argument("phone_number", help="接收者电话号码")
    sms_parser.add_argument("message", help="短信内容")
    
    # 应用管理
    app_parser = subparsers.add_parser("app", help="打开应用")
    app_parser.add_argument("app_name", help="应用名称或包名")
    
    close_app_parser = subparsers.add_parser("close-app", help="关闭应用")
    close_app_parser.add_argument("package_name", help="应用包名")
    
    # 屏幕交互
    tap_parser = subparsers.add_parser("tap", help="点击屏幕")
    tap_parser.add_argument("x", type=int, help="X坐标")
    tap_parser.add_argument("y", type=int, help="Y坐标")
    
    swipe_parser = subparsers.add_parser("swipe", help="滑动屏幕")
    swipe_parser.add_argument("x1", type=int, help="起始X坐标")
    swipe_parser.add_argument("y1", type=int, help="起始Y坐标")
    swipe_parser.add_argument("x2", type=int, help="结束X坐标")
    swipe_parser.add_argument("y2", type=int, help="结束Y坐标")
    swipe_parser.add_argument("--duration", type=int, default=300, help="滑动持续时间(毫秒)")
    
    text_parser = subparsers.add_parser("text", help="输入文本")
    text_parser.add_argument("text", help="要输入的文本")
    
    key_parser = subparsers.add_parser("key", help="按下按键")
    key_parser.add_argument("keycode", help="按键代码")
    
    # 媒体功能
    screenshot_parser = subparsers.add_parser("screenshot", help="截取屏幕截图")
    screenshot_parser.add_argument("--output", default="screenshot.png", help="本地保存路径")
    
    # 浏览器功能
    url_parser = subparsers.add_parser("open-url", help="打开URL")
    url_parser.add_argument("url", help="要打开的URL")
    
    # 统一交互接口
    interact_parser = subparsers.add_parser("screen-interact", help="统一屏幕交互接口")
    interact_parser.add_argument("action", choices=["tap", "swipe", "text", "key", "find", "wait", "scroll"], 
                                help="交互动作")
    interact_parser.add_argument("params", nargs="*", help="参数，格式为key=value")
    
    return parser.parse_args()

def parse_key_value_params(params: List[str]) -> Dict[str, Any]:
    """解析key=value格式的参数列表"""
    result = {}
    for param in params:
        if "=" in param:
            key, value = param.split("=", 1)
            # 尝试转换数值
            try:
                if value.isdigit():
                    value = int(value)
                elif value.lower() == "true":
                    value = True
                elif value.lower() == "false":
                    value = False
            except ValueError:
                pass
            result[key] = value
    return result

def handle_screen_interact(action: str, params: List[str]) -> str:
    """处理统一屏幕交互命令"""
    parsed_params = parse_key_value_params(params)
    
    if action == "tap":
        if "x" in parsed_params and "y" in parsed_params:
            return adb.run_command(["shell", "input", "tap", str(parsed_params["x"]), str(parsed_params["y"])], 
                                  check_output=False)
        elif "element_text" in parsed_params:
            # 通过UI Automator查找元素并点击
            text = parsed_params["element_text"]
            cmd = ["shell", "uiautomator", "dump", "/sdcard/window_dump.xml"]
            adb.run_command(cmd, check_output=False)
            # 解析XML并查找元素（简化版）
            return f"尝试点击文本为'{text}'的元素"
        elif "element_content_desc" in parsed_params:
            desc = parsed_params["element_content_desc"]
            return f"尝试点击描述为'{desc}'的元素"
    
    elif action == "swipe":
        required = ["x1", "y1", "x2", "y2"]
        if all(k in parsed_params for k in required):
            duration = parsed_params.get("duration", 300)
            cmd = ["shell", "input", "swipe", 
                   str(parsed_params["x1"]), str(parsed_params["y1"]),
                   str(parsed_params["x2"]), str(parsed_params["y2"]),
                   str(duration)]
            return adb.run_command(cmd, check_output=False)
    
    elif action == "text":
        if "content" in parsed_params:
            cmd = ["shell", "input", "text", parsed_params["content"]]
            return adb.run_command(cmd, check_output=False)
    
    elif action == "key":
        if "keycode" in parsed_params:
            cmd = ["shell", "input", "keyevent", parsed_params["keycode"]]
            return adb.run_command(cmd, check_output=False)
    
    elif action == "find":
        if "method" in parsed_params and "value" in parsed_params:
            # 简化版查找实现
            method = parsed_params["method"]
            value = parsed_params["value"]
            partial = parsed_params.get("partial", False)
            return f"查找方法:{method}, 值:{value}, 部分匹配:{partial}"
    
    elif action == "wait":
        if "method" in parsed_params and "value" in parsed_params:
            method = parsed_params["method"]
            value = parsed_params["value"]
            timeout = parsed_params.get("timeout", 10)
            return f"等待方法:{method}, 值:{value}, 超时:{timeout}秒"
    
    elif action == "scroll":
        if "method" in parsed_params and "value" in parsed_params:
            method = parsed_params["method"]
            value = parsed_params["value"]
            direction = parsed_params.get("direction", "down")
            max_swipes = parsed_params.get("max_swipes", 5)
            return f"滚动查找方法:{method}, 值:{value}, 方向:{direction}, 最大滑动次数:{max_swipes}"
    
    return "无效的屏幕交互参数"

def main():
    """命令行主函数"""
    args = parse_args()
    
    if not args.command:
        print("错误: 请指定命令。使用 --help 查看帮助。")
        sys.exit(1)
    
    # 处理各种命令
    if args.command == "check":
        devices = adb.get_devices()
        if devices:
            print("已连接的设备:")
            for device in devices:
                print(f"  ID: {device['id']}")
                print(f"  状态: {device['status']}")
                print(f"  型号: {device['model']}")
                print("")
            print(f"当前使用的设备: {adb.device or '未设置'}")
        else:
            print("未找到已连接的设备")
    
    elif args.command == "device":
        result = adb.set_device(args.device_id)
        print(result)
    
    elif args.command == "call":
        cmd = ["shell", "am", "start", "-a", "android.intent.action.CALL", "-d", f"tel:{args.phone_number}"]
        result = adb.run_command(cmd, check_output=False)
        print(result)
    
    elif args.command == "hangup":
        cmd = ["shell", "input", "keyevent", "KEYCODE_ENDCALL"]
        result = adb.run_command(cmd, check_output=False)
        print(result)
    
    elif args.command == "send-sms":
        cmd = [
            "shell", "am", "start", "-a", "android.intent.action.SENDTO", 
            "-d", f"smsto:{args.phone_number}", "--es", "sms_body", args.message
        ]
        result = adb.run_command(cmd, check_output=False)
        print(result)
    
    elif args.command == "app":
        # 尝试作为包名启动
        if "." in args.app_name:
            cmd = ["shell", "monkey", "-p", args.app_name, "-c", "android.intent.category.LAUNCHER", "1"]
            result = adb.run_command(cmd, check_output=False)
        else:
            # 尝试查找匹配的应用
            cmd = ["shell", "pm", "list", "packages", args.app_name]
            result = adb.run_command(cmd)
            if result.startswith("package:"):
                package = result.split("package:")[1].strip()
                cmd = ["shell", "monkey", "-p", package, "-c", "android.intent.category.LAUNCHER", "1"]
                result = adb.run_command(cmd, check_output=False)
            else:
                result = f"找不到应用: {args.app_name}"
        print(result)
    
    elif args.command == "close-app":
        cmd = ["shell", "am", "force-stop", args.package_name]
        result = adb.run_command(cmd, check_output=False)
        print(result)
    
    elif args.command == "tap":
        cmd = ["shell", "input", "tap", str(args.x), str(args.y)]
        result = adb.run_command(cmd, check_output=False)
        print(result)
    
    elif args.command == "swipe":
        cmd = ["shell", "input", "swipe", str(args.x1), str(args.y1), 
               str(args.x2), str(args.y2), str(args.duration)]
        result = adb.run_command(cmd, check_output=False)
        print(result)
    
    elif args.command == "text":
        cmd = ["shell", "input", "text", args.text]
        result = adb.run_command(cmd, check_output=False)
        print(result)
    
    elif args.command == "key":
        cmd = ["shell", "input", "keyevent", args.keycode]
        result = adb.run_command(cmd, check_output=False)
        print(result)
    
    elif args.command == "screenshot":
        device_path = "/sdcard/screenshot.png"
        cmd = ["shell", "screencap", "-p", device_path]
        result = adb.run_command(cmd, check_output=False)
        
        # 将截图拉到本地
        pull_cmd = ["pull", device_path, args.output]
        pull_result = adb.run_command(pull_cmd, check_output=False)
        print(f"截图已保存到: {args.output}")
    
    elif args.command == "open-url":
        # 确保URL有协议前缀
        url = args.url
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "https://" + url
            
        cmd = ["shell", "am", "start", "-a", "android.intent.action.VIEW", "-d", url]
        result = adb.run_command(cmd, check_output=False)
        print(result)
    
    elif args.command == "screen-interact":
        result = handle_screen_interact(args.action, args.params)
        print(result)

if __name__ == "__main__":
    main()