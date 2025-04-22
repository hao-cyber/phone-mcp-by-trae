#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Phone MCP 基本使用示例

这个示例展示了如何使用Phone MCP插件与Android手机交互。
"""

import time
from phone_mcp import ADBExecutor

def main():
    # 创建ADB执行器
    adb = ADBExecutor()
    
    # 检查设备连接
    print("检查设备连接...")
    devices = adb.get_devices()
    if not devices:
        print("未找到已连接的设备，请确保您的Android设备已通过USB连接并启用了USB调试。")
        return
    
    # 显示已连接的设备
    print(f"找到 {len(devices)} 个设备:")
    for i, device in enumerate(devices):
        print(f"  {i+1}. ID: {device['id']}")
        print(f"     状态: {device['status']}")
        print(f"     型号: {device['model']}")
    
    # 如果有多个设备，让用户选择一个
    if len(devices) > 1:
        choice = input("\n请选择要使用的设备 (输入编号): ")
        try:
            device_index = int(choice) - 1
            if 0 <= device_index < len(devices):
                adb.set_device(devices[device_index]['id'])
            else:
                print("无效的选择，使用第一个设备。")
                adb.set_device(devices[0]['id'])
        except ValueError:
            print("无效的输入，使用第一个设备。")
            adb.set_device(devices[0]['id'])
    else:
        # 只有一个设备，直接使用
        adb.set_device(devices[0]['id'])
    
    print(f"\n使用设备: {adb.device}\n")
    
    # 基本功能演示菜单
    while True:
        print("\n请选择要演示的功能:")
        print("1. 获取设备信息")
        print("2. 打开应用")
        print("3. 发送文本")
        print("4. 截取屏幕截图")
        print("5. 打开网页")
        print("6. 退出")
        
        choice = input("\n请输入选项编号: ")
        
        if choice == "1":
            # 获取设备信息
            print("\n获取设备信息...")
            cmd = ["shell", "getprop", "ro.product.model"]
            model = adb.run_command(cmd)
            print(f"设备型号: {model}")
            
            cmd = ["shell", "getprop", "ro.build.version.release"]
            android_version = adb.run_command(cmd)
            print(f"Android版本: {android_version}")
            
            cmd = ["shell", "wm", "size"]
            screen_size = adb.run_command(cmd)
            print(f"屏幕尺寸: {screen_size}")
            
        elif choice == "2":
            # 打开应用
            app_name = input("\n请输入要打开的应用名称或包名: ")
            print(f"\n尝试打开应用: {app_name}")
            
            # 尝试作为包名启动
            if "." in app_name:
                cmd = ["shell", "monkey", "-p", app_name, "-c", "android.intent.category.LAUNCHER", "1"]
                result = adb.run_command(cmd, check_output=False)
            else:
                # 尝试查找匹配的应用
                cmd = ["shell", "pm", "list", "packages", app_name]
                result = adb.run_command(cmd)
                if result.startswith("package:"):
                    package = result.split("package:")[1].strip()
                    cmd = ["shell", "monkey", "-p", package, "-c", "android.intent.category.LAUNCHER", "1"]
                    result = adb.run_command(cmd, check_output=False)
                else:
                    result = f"找不到应用: {app_name}"
            
            print(result)
            
        elif choice == "3":
            # 发送文本
            text = input("\n请输入要发送的文本: ")
            print(f"\n发送文本: {text}")
            cmd = ["shell", "input", "text", text]
            result = adb.run_command(cmd, check_output=False)
            print(result)
            
        elif choice == "4":
            # 截取屏幕截图
            print("\n截取屏幕截图...")
            device_path = "/sdcard/screenshot.png"
            cmd = ["shell", "screencap", "-p", device_path]
            adb.run_command(cmd, check_output=False)
            
            # 将截图拉到本地
            local_path = "screenshot.png"
            pull_cmd = ["pull", device_path, local_path]
            adb.run_command(pull_cmd, check_output=False)
            print(f"截图已保存到: {local_path}")
            
        elif choice == "5":
            # 打开网页
            url = input("\n请输入要打开的URL: ")
            if not url.startswith("http://") and not url.startswith("https://"):
                url = "https://" + url
                
            print(f"\n在设备浏览器中打开: {url}")
            cmd = ["shell", "am", "start", "-a", "android.intent.action.VIEW", "-d", url]
            result = adb.run_command(cmd, check_output=False)
            print(result)
            
        elif choice == "6":
            # 退出
            print("\n退出演示。")
            break
            
        else:
            print("\n无效的选择，请重试。")
        
        # 暂停一下，让用户看到结果
        time.sleep(1)

if __name__ == "__main__":
    main()