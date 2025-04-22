#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="phone-mcp-by-trae",
    version="0.1.0",
    author="Hao",
    author_email="example@example.com",
    description="一个通过ADB命令控制Android手机的MCP插件",
    keywords="android, adb, mcp, phone, control",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hao-cyber/phone-mcp-by-trae",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "mcp",
    ],
    project_urls={
        "Bug Tracker": "https://github.com/hao-cyber/phone-mcp/issues",
        "Documentation": "https://github.com/hao-cyber/phone-mcp",
        "Source Code": "https://github.com/hao-cyber/phone-mcp",
    },
    entry_points={
        "console_scripts": [
            "phone-mcp-by-trae=phone_mcp_by_trae:main",
            "phone-cli-by-trae=phone_mcp_by_trae:cli_main",
        ],
    },
    license="MIT",
    license_files=["LICENSE"],
)