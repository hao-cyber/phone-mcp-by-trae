# Phone MCP By Trae - 快速发布指南

## 发布到PyPI的快速步骤

### 1. 安装必要工具

```bash
pip install build twine
```

### 2. 更新版本号

在发布新版本前，请在`setup.py`文件中更新版本号：

```python
version="0.1.0",  # 修改为新版本号，如 "0.1.1"
```

### 3. 使用发布脚本

我们提供了一个便捷的发布脚本，可以一键完成构建和发布：

```bash
# 查看帮助
python publish_to_pypi.py --help

# 清理、构建并上传到PyPI
python publish_to_pypi.py --clean --build --upload

# 或者执行所有步骤（包括上传到测试PyPI）
python publish_to_pypi.py --all
```

### 4. 手动发布步骤

如果您想手动控制发布流程，可以按以下步骤操作：

```bash
# 清理旧的构建文件
rm -rf build/ dist/ *.egg-info/

# 构建分发包
python -m build

# 上传到PyPI
python -m twine upload dist/*
```

### 5. 使用GitHub Actions自动发布

本项目已配置GitHub Actions工作流。创建新的版本标签后，会自动构建并发布到PyPI：

```bash
# 创建新版本标签
git tag v0.1.1
git push origin v0.1.1
```

### 6. 验证发布

发布完成后，可以通过以下命令验证包是否可以正常安装：

```bash
pip install phone-mcp-by-trae
```

更详细的发布指南请参考 [PYPI_PUBLISH.md](PYPI_PUBLISH.md) 文件。