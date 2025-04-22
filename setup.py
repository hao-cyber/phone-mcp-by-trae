#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="phone-mcp",
    version="0.1.0",
    author="Hao",
    author_email="example@example.com",
    description="一个通过ADB命令控制Android手机的MCP插件",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hao-cyber/phone-mcp",
    packages=find_packages(),
    py_modules=["phone_mcp"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "mcp",
    ],
    entry_points={
        "console_scripts": [
            "phone-mcp=phone_mcp:main",
            "phone-cli=phone_mcp:cli_main",
        ],
    },
)