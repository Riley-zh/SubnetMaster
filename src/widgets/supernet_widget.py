#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
超网计算Widget类定义
"""

import ipaddress
from pathlib import Path
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QGroupBox,
                               QLabel, QTextEdit, QTreeWidget, QTreeWidgetItem,
                               QPushButton, QMessageBox, QFileDialog)
from PyQt5.QtCore import Qt


class SupernetWidget(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.build_ui()

    def build_ui(self):
        """构建用户界面"""
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)

        # 输入网络列表组
        input_group = QGroupBox("输入网络列表")
        input_layout = QVBoxLayout(input_group)
        input_layout.setSpacing(10)
        
        label = QLabel("网络地址(用逗号或换行分隔):")
        label.setWordWrap(True)
        input_layout.addWidget(label)
        
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("例如:\n192.168.1.0/24, 192.168.2.0/24\n或:\n192.168.1.0/24\n192.168.2.0/24")
        input_layout.addWidget(self.text_edit)

        # 按钮区域
        button_layout = QHBoxLayout()
        calc_btn = QPushButton("计算")
        calc_btn.setObjectName("calculateButton")
        calc_btn.clicked.connect(self.calculate)
        clear_btn = QPushButton("清除")
        clear_btn.setObjectName("clearButton")
        clear_btn.clicked.connect(self.clear)
        button_layout.addWidget(calc_btn)
        button_layout.addWidget(clear_btn)
        input_layout.addLayout(button_layout)

        main_layout.addWidget(input_group)

        # 结果显示组
        result_group = QGroupBox("超网计算结果")
        result_layout = QVBoxLayout(result_group)
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["属性", "值"])
        self.tree.setColumnWidth(0, 300)
        self.tree.setAlternatingRowColors(True)
        result_layout.addWidget(self.tree)
        main_layout.addWidget(result_group)

    def calculate(self):
        """执行超网计算"""
        txt = self.text_edit.toPlainText().strip()
        if not txt:
            QMessageBox.warning(self, "提示", "请输入网络列表")
            return
        try:
            networks = []
            invalid = []
            for part in txt.replace("\n", ",").split(","):
                part = part.strip()
                if not part:
                    continue
                try:
                    networks.append(ipaddress.IPv4Network(part))
                except ValueError:
                    invalid.append(part)
            if invalid:
                QMessageBox.warning(self, "警告", f"以下网络无效: {', '.join(invalid)}")
            if len(networks) < 2:
                QMessageBox.warning(self, "提示", "至少需要两个网络")
                return
            supernets = list(ipaddress.collapse_addresses(networks))
            self.show_result(supernets, networks)
            self.parent.status.showMessage(f"找到 {len(supernets)} 个超网")
        except ValueError as e:
            QMessageBox.critical(self, "错误", f"输入格式错误:\n{str(e)}")

    def show_result(self, supernets, original):
        """显示超网计算结果"""
        self.tree.clear()
        QTreeWidgetItem(self.tree, ["输入的网络数量", str(len(original))])
        QTreeWidgetItem(self.tree, ["原始网络列表", ", ".join(str(n) for n in original[:5]) + (", ..." if len(original) > 5 else "")])
        QTreeWidgetItem(self.tree, ["", ""])
        for idx, sn in enumerate(supernets, 1):
            QTreeWidgetItem(self.tree, [f"超网 #{idx}", str(sn)])
            QTreeWidgetItem(self.tree, ["网络地址", str(sn.network_address)])
            QTreeWidgetItem(self.tree, ["广播地址", str(sn.broadcast_address)])
            QTreeWidgetItem(self.tree, ["子网掩码 (CIDR)", f"/{sn.prefixlen}"])
            QTreeWidgetItem(self.tree, ["子网掩码 (点分十进制)", str(sn.netmask)])
            QTreeWidgetItem(self.tree, ["地址总数", str(sn.num_addresses)])
            if sn.prefixlen <= 30:
                QTreeWidgetItem(self.tree, ["可用主机范围",
                                            f"{sn.network_address + 1} - {sn.broadcast_address - 1}"])
            contained = [n for n in original if n.subnet_of(sn)]
            QTreeWidgetItem(self.tree, ["包含的原始网络", f"{len(contained)}个"])
            if idx < len(supernets):
                QTreeWidgetItem(self.tree, ["", ""])

    def clear(self):
        """清除输入和结果"""
        self.text_edit.clear()
        self.tree.clear()

    def collect_text(self):
        """收集文本结果用于保存"""
        txt = ""
        for i in range(self.tree.topLevelItemCount()):
            item = self.tree.topLevelItem(i)
            txt += f"{item.text(0)}: {item.text(1)}\n"
        return txt