#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
资源管理器类定义
"""

import os
import sys
from pathlib import Path
from PyQt5.QtGui import QIcon


class ResourceManager:
    """资源管理器，用于管理应用的图标等资源"""
    
    @staticmethod
    def get_icon_path():
        """获取图标文件路径"""
        # 尝试多种可能的图标路径
        possible_paths = [
            Path(__file__).parent.parent.parent / "mask.ico",
            Path(__file__).parent.parent.parent / "resources" / "mask.ico",
            Path(__file__).parent / "mask.ico",
        ]
        
        for path in possible_paths:
            if path.exists():
                return str(path)
        
        return None
    
    @staticmethod
    def set_window_icon(window):
        """为窗口设置图标"""
        icon_path = ResourceManager.get_icon_path()
        if icon_path and os.path.exists(icon_path):
            window.setWindowIcon(QIcon(icon_path))