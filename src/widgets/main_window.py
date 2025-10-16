#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
主窗口类定义
"""

import sys
from pathlib import Path
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTabWidget, 
                               QMenuBar, QStatusBar, QMessageBox, QFileDialog, QAction)
from PyQt5.QtCore import Qt

from widgets.basic_calc_widget import BasicCalcWidget
from widgets.subnet_widget import SubnetWidget
from widgets.supernet_widget import SupernetWidget
from utils.theme_manager import ThemeManager
from resources.resource_manager import ResourceManager
from utils.config_manager import ConfigManager


class SubnetCalculator(QMainWindow):
    def __init__(self, config = None):
        super().__init__()
        self.config = config or ConfigManager()
        super().__init__()
        self.config = config or ConfigManager()
        super().__init__()
        self.config = config or ConfigManager()
        self.setWindowTitle("子网计算器v5.0")
        
        # 设置窗口尺寸
        width = int(self.config.get("window_width", 1100) or 1100)
        height = int(self.config.get("window_height", 800) or 800)
        self.resize(width, height)
        
        # 设置窗口图标
        ResourceManager.set_window_icon(self)
        
        # 主题管理器
        self.theme_manager = ThemeManager(self)
        
        self.init_ui()
        
        # 设置上次使用的标签页
        last_tab = int(self.config.get("last_tab", 0) or 0)
        self.tabs.setCurrentIndex(last_tab)

    def init_ui(self):
        """初始化用户界面"""
        self.create_menu()
        self.create_status_bar()
        self.create_tabs()

    def create_menu(self):
        """创建菜单栏"""
        menu = self.menuBar()
        if menu is None:
            return
        
        # 文件菜单
        file_menu = menu.addMenu("文件")
        if file_menu is None:
            return
        save_action = QAction("保存结果", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_all_results)
        file_menu.addAction(save_action)
        file_menu.addSeparator()
        exit_action = QAction("退出", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(QApplication.quit)
        file_menu.addAction(exit_action)

        # 视图菜单
        view_menu = menu.addMenu("视图")
        if view_menu is None:
            return
        toggle_theme = QAction("切换浅色/暗色主题", self)
        toggle_theme.setShortcut("Ctrl+T")
        toggle_theme.triggered.connect(self.toggle_theme)
        view_menu.addAction(toggle_theme)

        # 帮助菜单
        help_menu = menu.addMenu("帮助")
        if help_menu is None:
            return
        help_action = QAction("使用说明", self)
        help_action.setShortcut("F1")
        help_action.triggered.connect(self.show_help)
        help_menu.addAction(help_action)
        about_action = QAction("关于", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def create_status_bar(self):
        """创建状态栏"""
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.status.showMessage("就绪")

    def create_tabs(self):
        """创建标签页"""
        self.tabs = QTabWidget()
        self.tabs.currentChanged.connect(self.on_tab_changed)
        self.setCentralWidget(self.tabs)

        self.tab_basic = BasicCalcWidget(self)
        self.tab_subnet = SubnetWidget(self)
        self.tab_super = SupernetWidget(self)

        self.tabs.addTab(self.tab_basic, "基本计算")
        self.tabs.addTab(self.tab_subnet, "子网划分")
        self.tabs.addTab(self.tab_super, "超网计算")

    def on_tab_changed(self, index):
        """标签页切换事件"""
        if self.config:
            self.config.set("last_tab", index)

    def toggle_theme(self):
        """切换主题"""
        self.theme_manager.dark_theme = not self.theme_manager.dark_theme
        self.theme_manager.apply_theme()
        if self.config:
            self.config.set_theme(self.theme_manager.dark_theme)
        self.status.showMessage("已切换到暗色主题" if self.theme_manager.dark_theme else "已切换到浅色主题")

    def save_all_results(self):
        """保存所有结果到文件"""
        content = "=== 子网计算器结果 ===\n\n"
        basic = self.tab_basic.collect_text()
        if basic:
            content += "--- 基本计算结果 ---\n" + basic + "\n"
        subnet = self.tab_subnet.collect_text()
        if subnet:
            content += "--- 子网划分结果 ---\n" + subnet + "\n"
        supernet = self.tab_super.collect_text()
        if supernet:
            content += "--- 超网计算结果 ---\n" + supernet + "\n"

        path, _ = QFileDialog.getSaveFileName(self, "保存结果", str(Path.home()), "Text Files (*.txt)")
        if path:
            try:
                Path(path).write_text(content, encoding="utf-8")
                self.status.showMessage(f"已保存到 {path}")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"保存文件失败: {str(e)}")

    def show_help(self):
        """显示帮助信息"""
        QMessageBox.information(self, "使用说明",
                                "功能与原版一致，界面升级到 PyQt5。\n"
                                "通过菜单“视图→切换浅色/暗色主题”可更换外观。\n\n"
                                "快捷键:\n"
                                "Ctrl+S: 保存结果\n"
                                "Ctrl+T: 切换主题\n"
                                "Ctrl+Q: 退出程序\n"
                                "F1: 使用说明")

    def show_about(self):
        """显示关于信息"""
        QMessageBox.information(self, "关于",
                                "高级子网计算器 v5.0\n"
                                "作者：Riley\n"
                                "PyQt5 重构版本\n\n"
                                "功能特性:\n"
                                "• 基本计算: 计算IP地址相关信息\n"
                                "• 子网划分: 按子网数量或主机数量划分\n"
                                "• 超网计算: 多个网络合并为超网\n"
                                "• 主题切换: 支持浅色和暗色主题")

    def closeEvent(self, a0):
        """窗口关闭事件"""
        # 保存窗口尺寸
        if self.config:
            self.config.set("window_width", self.width())
            self.config.set("window_height", self.height())
        if a0 is not None:
            a0.accept()