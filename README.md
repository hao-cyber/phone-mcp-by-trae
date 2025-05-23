# Phone MCP By Trae

通过ADB命令控制Android手机的MCP插件, 完全用Trae复刻phone-mcp

#### trae使用方式 （推荐）
```json
{
  "mcpServers": {
    "phone-mcp": {
      "command": "uvx",
      "args": [
        "phone-mcp-by-trae"
      ]
    }
  }
}
```

## 安装

### 从PyPI安装

```bash
# 从PyPI安装最新版本
pip install phone-mcp-by-trae
```

### 从源码安装

```bash
# 从当前目录安装
pip install -e .
```

## 使用方法

### 作为MCP服务器运行

```bash
# 方法1：使用Python模块方式运行
python -m phone_mcp_by_trae

# 方法2：使用安装的命令行工具运行
phone-mcp-by-trae
```

### 使用命令行工具

```bash
# 方法1：使用Python模块方式运行
python -m phone_mcp_by_trae.phone_cli

# 方法2：使用安装的命令行工具运行
phone-cli-by-trae
```

## 命令行工具示例

```bash
# 检查已连接的设备
phone-cli-by-trae check

# 设置要使用的设备
phone-cli-by-trae device <设备ID>

# 拨打电话
phone-cli-by-trae call <电话号码>

# 发送短信
phone-cli-by-trae send-sms <电话号码> <短信内容>

# 打开应用
phone-cli-by-trae app <应用包名>

# 点击屏幕
phone-cli-by-trae tap <X坐标> <Y坐标>
```

## 注意事项

1. 确保已安装ADB工具并添加到系统PATH中
2. 确保Android设备已启用USB调试模式并已授权连接的计算机
3. 如果遇到权限问题，请尝试以管理员/root权限运行命令
