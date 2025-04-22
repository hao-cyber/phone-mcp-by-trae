# 📱 Phone MCP Plugin

🌟 一个强大的MCP插件，让你通过ADB命令轻松控制Android手机。

## ⚡ 快速开始

### 📥 安装

```bash
pip install phone-mcp
# 或使用uvx
uvx phone-mcp
```

### 🔧 配置

#### Cursor设置

在 `~/.cursor/mcp.json` 中配置：

```json
{
    "mcpServers": {
        "phone-mcp": {
            "command": "uvx",
            "args": [
                "phone-mcp"
            ]
        }
    }
}
```

#### Claude设置

在Claude配置中添加：

```json
{
    "mcpServers": {
        "phone-mcp": {
            "command": "uvx",
            "args": [
                "phone-mcp"
            ]
        }
    }
}
```

### 使用方法：

在Claude对话中直接使用命令，例如：
```
请给联系人小明打电话
```

⚠️ 使用前请确保：

- ADB已正确安装和配置
- Android设备已启用USB调试
- 设备通过USB连接到电脑

## 🎯 主要功能

- 📞 **电话功能**：拨打电话、结束通话、接听来电
- 💬 **短信**：发送和接收短信，获取原始消息
- 👥 **联系人**：访问手机联系人，通过自动化UI交互创建新联系人
- 📸 **媒体**：截图、屏幕录制、媒体控制
- 📱 **应用**：启动应用程序，使用intent启动特定活动，列出已安装的应用，终止应用
- 🔧 **系统**：窗口信息，应用快捷方式
- 🗺️ **地图**：搜索带有电话号码的兴趣点
- 🖱️ **UI交互**：点击、滑动、输入文本、按键
- 🔍 **UI检查**：通过文本、ID、类或描述查找元素
- 🤖 **UI自动化**：等待元素，滚动查找元素
- 🧠 **屏幕分析**：结构化屏幕信息和统一交互
- 🌐 **网页浏览器**：在设备的默认浏览器中打开URL
- 🔄 **UI监控**：监控UI变化并等待特定元素出现或消失

## 🛠️ 要求

- Python 3.7+
- 启用USB调试的Android设备
- ADB工具

## 📋 基本命令

### 设备和连接

```bash
# 检查设备连接
phone-cli check

# 获取屏幕尺寸
phone-cli screen-interact find method=clickable
```

### 通信

```bash
# 拨打电话
phone-cli call 1234567890

# 结束当前通话
phone-cli hangup

# 发送短信
phone-cli send-sms 1234567890 "你好"

# 获取接收的消息（带分页）
phone-cli messages --limit 10

# 获取发送的消息（带分页）
phone-cli sent-messages --limit 10

# 获取联系人（带分页）
phone-cli contacts --limit 20

# 通过UI自动化创建新联系人
phone-cli create-contact "张三" "1234567890"
```

### 媒体和应用

```bash
# 截图
phone-cli screenshot

# 录制屏幕
phone-cli record --duration 30

# 启动应用（可能不适用于所有设备）
phone-cli app camera

# 关闭应用
phone-cli close-app com.android.camera

# 列出已安装的应用（基本信息，更快）
phone-cli list-apps

# 分页列出应用
phone-cli list-apps --page 1 --page-size 10

# 列出应用的详细信息（较慢）
phone-cli list-apps --detailed

# 启动特定活动（适用于所有设备的可靠方法）
phone-cli launch com.android.settings/.Settings

# 在默认浏览器中打开URL
phone-cli open-url baidu.com
```

### 屏幕分析和交互

```bash
# 使用结构化信息分析当前屏幕
phone-cli analyze-screen

# 统一交互接口
phone-cli screen-interact <action> [parameters]

# 在坐标处点击
phone-cli screen-interact tap x=500 y=800

# 通过文本点击元素
phone-cli screen-interact tap element_text="登录"

# 通过内容描述点击元素
phone-cli screen-interact tap element_content_desc="日历"

# 滑动手势（向下滚动）
phone-cli screen-interact swipe x1=500 y1=1000 x2=500 y2=200 duration=300

# 按键
phone-cli screen-interact key keycode=back

# 输入文本
phone-cli screen-interact text content="你好世界"

# 查找元素
phone-cli screen-interact find method=text value="登录" partial=true

# 等待元素
phone-cli screen-interact wait method=text value="成功" timeout=10

# 滚动查找元素
phone-cli screen-interact scroll method=text value="设置" direction=down max_swipes=5

# 监控UI变化
phone-cli monitor-ui --interval 0.5 --duration 30
```