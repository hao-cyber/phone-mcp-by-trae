#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
发布到PyPI的辅助脚本

此脚本帮助用户完成Phone MCP By Trae包的构建和发布流程。
"""

import os
import sys
import subprocess
import shutil
import argparse


def run_command(command, description=None):
    """运行命令并打印结果"""
    if description:
        print(f"\n{description}...")
    
    try:
        result = subprocess.run(command, shell=True, check=True, text=True,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"错误: {e}")
        print(f"详细信息: {e.stderr}")
        return False


def clean_build_dirs():
    """清理构建目录"""
    dirs_to_clean = ['build', 'dist', '*.egg-info']
    for dir_pattern in dirs_to_clean:
        for path in [p for p in os.popen(f'find . -name "{dir_pattern}" -type d').read().strip().split('\n') if p]:
            print(f"删除: {path}")
            try:
                shutil.rmtree(path)
            except Exception as e:
                print(f"无法删除 {path}: {e}")


def build_package():
    """构建Python包"""
    return run_command("python -m build", "构建分发包")


def upload_to_test_pypi():
    """上传到测试PyPI"""
    return run_command("python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*", 
                     "上传到测试PyPI")


def upload_to_pypi():
    """上传到正式PyPI"""
    return run_command("python -m twine upload dist/*", "上传到PyPI")


def main():
    parser = argparse.ArgumentParser(description="Phone MCP By Trae PyPI发布工具")
    parser.add_argument("--clean", action="store_true", help="清理构建目录")
    parser.add_argument("--build", action="store_true", help="构建包")
    parser.add_argument("--test", action="store_true", help="上传到测试PyPI")
    parser.add_argument("--upload", action="store_true", help="上传到正式PyPI")
    parser.add_argument("--all", action="store_true", help="执行所有步骤")
    
    args = parser.parse_args()
    
    # 如果没有参数，显示帮助
    if len(sys.argv) == 1:
        parser.print_help()
        return
    
    # 检查必要的工具
    for tool in ["build", "twine"]:
        try:
            subprocess.run([sys.executable, "-m", tool, "--help"], 
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError:
            print(f"错误: 缺少必要的工具 '{tool}'。请运行 'pip install {tool}'")
            return
    
    if args.clean or args.all:
        clean_build_dirs()
    
    if args.build or args.all:
        if not build_package():
            return
    
    if args.test or args.all:
        if not upload_to_test_pypi():
            return
    
    if args.upload or args.all:
        if not upload_to_pypi():
            return
    
    if args.all:
        print("\n所有步骤已完成!")
        print("\n用户现在可以通过以下命令安装此包:")
        print("pip install phone-mcp-by-trae")


if __name__ == "__main__":
    main()