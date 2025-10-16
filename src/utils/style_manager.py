#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
样式管理器类定义
"""

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtWidgets import QApplication


class StyleManager:
    """样式管理器，用于统一界面样式"""
    
    @staticmethod
    def apply_styles():
        """应用统一样式"""
        app = QApplication.instance()
        
        # 设置全局字体
        font = QFont("Microsoft YaHei", 9)
        app.setFont(font)
        
        # 设置样式表
        app.setStyleSheet("""
            QWidget {
                font-family: "Microsoft YaHei", "Segoe UI", sans-serif;
                font-size: 9pt;
            }
            
            QGroupBox {
                font-weight: bold;
                border: 1px solid #CCCCCC;
                border-radius: 4px;
                margin-top: 1ex;
                padding-top: 10px;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            
            QPushButton {
                padding: 6px 15px;
                border-radius: 4px;
                background-color: #E0E0E0;
                border: 1px solid #CCCCCC;
                min-width: 70px;
            }
            
            QPushButton:hover {
                background-color: #D0D0D0;
            }
            
            QPushButton:pressed {
                background-color: #C0C0C0;
            }
            
            QPushButton#calculateButton {
                background-color: #0078D4;
                color: white;
                border: 1px solid #005A9E;
            }
            
            QPushButton#calculateButton:hover {
                background-color: #005A9E;
            }
            
            QPushButton#calculateButton:pressed {
                background-color: #004578;
            }
            
            QPushButton#clearButton {
                background-color: #F0F0F0;
                border: 1px solid #CCCCCC;
            }
            
            QPushButton#exampleButton {
                background-color: #F0F0F0;
                border: 1px solid #CCCCCC;
            }
            
            QLineEdit, QComboBox, QTextEdit {
                padding: 6px;
                border: 1px solid #CCCCCC;
                border-radius: 4px;
                background-color: white;
            }
            
            QLineEdit:focus, QComboBox:focus, QTextEdit:focus {
                border: 1px solid #0078D4;
                outline: none;
            }
            
            QTreeWidget {
                border: 1px solid #CCCCCC;
                border-radius: 4px;
                alternate-background-color: #F8F8F8;
                selection-background-color: #0078D4;
                selection-color: white;
            }
            
            QTreeWidget::item {
                padding: 4px;
            }
            
            QTreeWidget::item:selected {
                background-color: #0078D4;
                color: white;
            }
            
            QTabWidget::pane {
                border: 1px solid #CCCCCC;
                border-radius: 4px;
            }
            
            QTabBar::tab {
                padding: 8px 15px;
                border: 1px solid #CCCCCC;
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                background-color: #F0F0F0;
            }
            
            QTabBar::tab:selected {
                background-color: white;
                border-bottom: 1px solid white;
            }
            
            QTabBar::tab:!selected {
                margin-top: 2px;
            }
            
            QMenuBar {
                background-color: #F0F0F0;
                border-bottom: 1px solid #CCCCCC;
                padding: 2px;
            }
            
            QMenuBar::item {
                padding: 5px 10px;
                background: transparent;
                border-radius: 4px;
            }
            
            QMenuBar::item:selected {
                background-color: #D0D0D0;
            }
            
            QMenuBar::item:pressed {
                background-color: #C0C0C0;
            }
            
            QMenu {
                border: 1px solid #CCCCCC;
                border-radius: 4px;
                background-color: white;
            }
            
            QMenu::item {
                padding: 5px 20px;
            }
            
            QMenu::item:selected {
                background-color: #0078D4;
                color: white;
            }
            
            QRadioButton {
                spacing: 5px;
            }
            
            QRadioButton::indicator {
                width: 16px;
                height: 16px;
            }
            
            QRadioButton::indicator:unchecked {
                border: 1px solid #888888;
                border-radius: 8px;
                background-color: white;
            }
            
            QRadioButton::indicator:checked {
                border: 1px solid #0078D4;
                border-radius: 8px;
                background-color: white;
            }
            
            QRadioButton::indicator:checked::after {
                border-radius: 4px;
                background-color: #0078D4;
            }
        """)

    @staticmethod
    def apply_dark_styles():
        """应用暗色主题样式"""
        app = QApplication.instance()
        
        # 设置样式表
        app.setStyleSheet("""
            QWidget {
                font-family: "Microsoft YaHei", "Segoe UI", sans-serif;
                font-size: 9pt;
                color: #E0E0E0;
                background-color: #2D2D30;
            }
            
            QGroupBox {
                font-weight: bold;
                border: 1px solid #555555;
                border-radius: 4px;
                margin-top: 1ex;
                padding-top: 10px;
                background-color: #2D2D30;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #E0E0E0;
            }
            
            QPushButton {
                padding: 6px 15px;
                border-radius: 4px;
                background-color: #3D3D40;
                border: 1px solid #555555;
                color: #E0E0E0;
                min-width: 70px;
            }
            
            QPushButton:hover {
                background-color: #4D4D50;
            }
            
            QPushButton:pressed {
                background-color: #5D5D60;
            }
            
            QPushButton#calculateButton {
                background-color: #0078D4;
                color: white;
                border: 1px solid #005A9E;
            }
            
            QPushButton#calculateButton:hover {
                background-color: #005A9E;
            }
            
            QPushButton#calculateButton:pressed {
                background-color: #004578;
            }
            
            QPushButton#clearButton {
                background-color: #3D3D40;
                border: 1px solid #555555;
            }
            
            QPushButton#exampleButton {
                background-color: #3D3D40;
                border: 1px solid #555555;
            }
            
            QLineEdit, QComboBox, QTextEdit {
                padding: 6px;
                border: 1px solid #555555;
                border-radius: 4px;
                background-color: #333337;
                color: #E0E0E0;
            }
            
            QLineEdit:focus, QComboBox:focus, QTextEdit:focus {
                border: 1px solid #0078D4;
                outline: none;
            }
            
            QTreeWidget {
                border: 1px solid #555555;
                border-radius: 4px;
                background-color: #333337;
                alternate-background-color: #3D3D40;
                selection-background-color: #0078D4;
                selection-color: white;
                color: #E0E0E0;
            }
            
            QTreeWidget::item {
                padding: 4px;
            }
            
            QTreeWidget::item:selected {
                background-color: #0078D4;
                color: white;
            }
            
            QTabWidget::pane {
                border: 1px solid #555555;
                border-radius: 4px;
            }
            
            QTabBar::tab {
                padding: 8px 15px;
                border: 1px solid #555555;
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                background-color: #3D3D40;
                color: #E0E0E0;
            }
            
            QTabBar::tab:selected {
                background-color: #2D2D30;
                border-bottom: 1px solid #2D2D30;
            }
            
            QTabBar::tab:!selected {
                margin-top: 2px;
            }
            
            QMenuBar {
                background-color: #3D3D40;
                border-bottom: 1px solid #555555;
                padding: 2px;
                color: #E0E0E0;
            }
            
            QMenuBar::item {
                padding: 5px 10px;
                background: transparent;
                border-radius: 4px;
                color: #E0E0E0;
            }
            
            QMenuBar::item:selected {
                background-color: #4D4D50;
            }
            
            QMenuBar::item:pressed {
                background-color: #5D5D60;
            }
            
            QMenu {
                border: 1px solid #555555;
                border-radius: 4px;
                background-color: #2D2D30;
                color: #E0E0E0;
            }
            
            QMenu::item {
                padding: 5px 20px;
            }
            
            QMenu::item:selected {
                background-color: #0078D4;
                color: white;
            }
            
            QRadioButton {
                spacing: 5px;
                color: #E0E0E0;
            }
            
            QRadioButton::indicator {
                width: 16px;
                height: 16px;
            }
            
            QRadioButton::indicator:unchecked {
                border: 1px solid #888888;
                border-radius: 8px;
                background-color: #333337;
            }
            
            QRadioButton::indicator:checked {
                border: 1px solid #0078D4;
                border-radius: 8px;
                background-color: #333337;
            }
            
            QRadioButton::indicator:checked::after {
                border-radius: 4px;
                background-color: #0078D4;
            }
            
            QMessageBox {
                background-color: #2D2D30;
            }
            
            QMessageBox QLabel {
                color: #E0E0E0;
            }
        """)