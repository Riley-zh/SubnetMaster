#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
主题管理器类定义
"""

import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette, QColor, QFont

from utils.style_manager import StyleManager


class ThemeManager:
    def __init__(self, parent):
        self.parent = parent
        self.dark_theme = False

    def apply_theme(self):
        """应用当前主题"""
        app = QApplication.instance()
        if self.dark_theme:
            # 应用暗色主题调色板
            dark = QPalette()
            dark.setColor(QPalette.ColorRole.Window, QColor(45, 45, 48))
            dark.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
            dark.setColor(QPalette.ColorRole.Base, QColor(51, 51, 55))
            dark.setColor(QPalette.ColorRole.AlternateBase, QColor(61, 61, 64))
            dark.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.white)
            dark.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
            dark.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
            dark.setColor(QPalette.ColorRole.Button, QColor(61, 61, 64))
            dark.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
            dark.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
            dark.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
            dark.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
            dark.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black)
            app.setPalette(dark)
            
            # 应用暗色主题样式
            StyleManager.apply_dark_styles()
        else:
            # 应用浅色主题
            app.setStyle("Fusion")
            app.setPalette(app.style().standardPalette())
            
            # 应用浅色主题样式
            StyleManager.apply_styles()

        # 统一字体（防止系统 DPI 缩放导致模糊）
        font = QFont("Microsoft YaHei", 9)
        if sys.platform == "darwin":
            font = QFont("SF Pro", 10)
        elif sys.platform.startswith("linux"):
            font = QFont("Noto Sans", 9)
        app.setFont(font)

    def toggle_theme(self):
        """切换主题"""
        self.dark_theme = not self.dark_theme
        self.apply_theme()
        self.parent.status.showMessage("已切换到暗色主题" if self.dark_theme else "已切换到浅色主题")