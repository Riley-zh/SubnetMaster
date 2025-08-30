#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
配置管理器类定义
"""

import json
import os
from pathlib import Path


class ConfigManager:
    """配置管理器，用于管理应用的配置信息"""
    
    def __init__(self):
        self.config_file = Path.home() / ".subnet_calculator_config.json"
        self.default_config = {
            "theme": "light",
            "window_width": 1100,
            "window_height": 800,
            "last_tab": 0
        }
        self.config = self.load_config()
    
    def load_config(self):
        """加载配置"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    # 确保所有默认配置项都存在
                    for key, value in self.default_config.items():
                        if key not in config:
                            config[key] = value
                    return config
            except Exception:
                return self.default_config.copy()
        else:
            return self.default_config.copy()
    
    def save_config(self):
        """保存配置"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
        except Exception:
            pass  # 静默处理保存错误
    
    def get(self, key, default=None):
        """获取配置项"""
        return self.config.get(key, default)
    
    def set(self, key, value):
        """设置配置项"""
        self.config[key] = value
    
    def is_dark_theme(self):
        """检查是否为暗色主题"""
        return self.config.get("theme", "light") == "dark"
    
    def set_theme(self, is_dark):
        """设置主题"""
        self.config["theme"] = "dark" if is_dark else "light"