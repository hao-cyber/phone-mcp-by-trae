# 发布到PyPI指南

本文档提供了将 Phone MCP By Trae 发布到PyPI的步骤指南。

## 准备工作

1. 确保已安装必要的工具：

```bash
pip install build twine
```

2. 确认项目元数据正确：
   - 检查 `setup.py` 中的版本号、作者信息和描述
   - 确保 `README.md` 内容完整
   - 验证 `MANIFEST.in` 包含所有必要文件

## 构建分发包

在项目根目录下运行以下命令构建分发包：

```bash
python -m build
```

这将在 `dist/` 目录下创建源代码分发包（.tar.gz）和轮子分发包（.whl）。

## 测试分发包

在上传到PyPI之前，建议先测试分发包：

```bash
# 创建一个测试环境
python -m venv test_env
source test_env/bin/activate  # Linux/Mac
# 或 test_env\Scripts\activate  # Windows

# 安装构建的包
pip install dist/phone_mcp_by_trae-*.whl

# 测试包是否正常工作
python -c "import phone_mcp_by_trae; print(phone_mcp_by_trae.__file__)"
```

## 上传到PyPI

### 上传到测试PyPI（可选）

```bash
python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

### 上传到正式PyPI

```bash
python -m twine upload dist/*
```

首次上传时，需要输入PyPI账号和密码。也可以使用API令牌进行身份验证。

## 使用GitHub Actions自动发布

本项目已配置GitHub Actions工作流，当创建新的版本标签（格式为`v*.*.*`）时，会自动构建并发布到PyPI。

使用以下步骤创建新版本：

1. 更新`setup.py`中的版本号
2. 提交并推送更改
3. 创建新的版本标签：

```bash
git tag v0.1.1
git push origin v0.1.1
```

## 安装已发布的包

发布成功后，用户可以通过以下命令安装：

```bash
pip install phone-mcp-by-trae
```

## 常见问题

1. **上传失败**：确保包名未被占用，版本号递增
2. **构建错误**：检查`setup.py`和项目结构
3. **依赖问题**：确保`install_requires`中列出了所有必要依赖