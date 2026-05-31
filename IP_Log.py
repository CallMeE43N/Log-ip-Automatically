#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
此脚本用于在Linux系统启动时自动记录当前日期和IP地址到日志文件。
请按照README.md的说明进行部署。
"""

import os
import sys
import subprocess
from datetime import datetime
import re

# 配置日志文件路径
LOG_FILE_PATH = os.path.expanduser("~/.startup_log.txt")

def get_external_ip():
    """
    获取外网IP地址
    通过curl访问httpbin.org/ip服务获取公网IP
    """
    try:
        result = subprocess.run(
            ["curl", "-s", "http://httpbin.org/ip"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            # 提取JSON中的origin字段
            import json
            data = json.loads(result.stdout)
            return data.get('origin', 'N/A')
        else:
            return "N/A"
    except Exception:
        return "N/A"

def get_internal_ips():
    """
    获取内网IP地址
    使用hostname -I命令获取所有非回环IP地址
    """
    try:
        result = subprocess.run(
            ["hostname", "-I"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            # 过滤掉回环地址
            ips = result.stdout.strip().split()
            internal_ips = [ip for ip in ips if not ip.startswith('127.')]
            return ' '.join(internal_ips) if internal_ips else 'N/A'
        else:
            return "N/A"
    except Exception:
        return "N/A"

def log_startup_info():
    """
    记录启动信息到日志文件
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    external_ip = get_external_ip()
    internal_ips = get_internal_ips()
    
    log_entry = f"[{timestamp}] Boot Event\n"
    log_entry += f"  External IP: {external_ip}\n"
    log_entry += f"  Internal IPs: {internal_ips}\n"
    log_entry += "-" * 50 + "\n"
    
    # 追加到日志文件
    with open(LOG_FILE_PATH, "a", encoding="utf-8") as log_file:
        log_file.write(log_entry)

if __name__ == "__main__":
    log_startup_info()
    print(f"Startup info logged to {LOG_FILE_PATH}")
