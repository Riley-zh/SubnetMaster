#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
子网计算器主应用文件
"""

import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt, QCoreApplication

from widgets.main_window import SubnetCalculator
from utils.style_manager import StyleManager
from utils.config_manager import ConfigManager


def main():
    """主函数"""
    QCoreApplication.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    
    # 加载配置
    config = ConfigManager()
    
    # 应用主题
    if config.is_dark_theme():
        StyleManager.apply_dark_styles()
    else:
        StyleManager.apply_styles()
    
    # 创建并显示主窗口
    window = SubnetCalculator(config)
    window.show()
    
    # 运行应用
    exit_code = app.exec()
    
    # 保存配置
    config.save_config()
    
    sys.exit(exit_code)


if __name__ == "__main__":
    main()