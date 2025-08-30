#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
基本计算Widget类定义
"""

from math import log2, ceil
import ipaddress
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QGroupBox,
                               QLabel, QLineEdit, QComboBox, QTreeWidget,
                               QTreeWidgetItem, QPushButton, QRadioButton,
                               QButtonGroup, QMessageBox)
from PySide6.QtCore import Qt


class BasicCalcWidget(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.build_ui()

    def build_ui(self):
        """构建用户界面"""
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)

        # 输入参数组
        input_group = QGroupBox("输入参数")
        input_layout = QVBoxLayout(input_group)
        input_layout.setSpacing(10)

        # IP地址输入
        ip_layout = QHBoxLayout()
        ip_layout.addWidget(QLabel("IP地址/网络:"), 0)
        self.ip_edit = QLineEdit()
        self.ip_edit.setPlaceholderText("例如: 192.168.1.1 或 192.168.1.0/24")
        ip_layout.addWidget(self.ip_edit, 1)
        input_layout.addLayout(ip_layout)

        # 掩码格式选择
        mask_format_layout = QHBoxLayout()
        mask_format_layout.addWidget(QLabel("掩码格式:"), 0)
        self.mask_group = QButtonGroup()
        self.radio_cidr = QRadioButton("CIDR (/24)")
        self.radio_dot = QRadioButton("点分十进制 (255.255.255.0)")
        self.mask_group.addButton(self.radio_cidr)
        self.mask_group.addButton(self.radio_dot)
        self.radio_cidr.setChecked(True)
        mask_format_layout.addWidget(self.radio_cidr)
        mask_format_layout.addWidget(self.radio_dot)
        mask_format_layout.addStretch(1)
        input_layout.addLayout(mask_format_layout)

        # 掩码输入
        mask_layout = QHBoxLayout()
        mask_layout.addWidget(QLabel("子网掩码:"), 0)
        self.mask_combo = QComboBox()
        self.mask_combo.addItems([f"/{i}" for i in range(8, 33)])
        self.mask_combo.setCurrentText("/24")
        self.mask_combo.setMinimumWidth(80)
        mask_layout.addWidget(self.mask_combo, 0)
        
        self.mask_edit = QLineEdit("255.255.255.0")
        self.mask_edit.setVisible(False)
        self.mask_edit.setMinimumWidth(120)
        mask_layout.addWidget(self.mask_edit, 0)
        mask_layout.addStretch(1)
        input_layout.addLayout(mask_layout)

        # 按钮区域
        button_layout = QHBoxLayout()
        calc_btn = QPushButton("计算")
        calc_btn.setObjectName("calculateButton")
        calc_btn.clicked.connect(self.calculate)
        clear_btn = QPushButton("清除")
        clear_btn.setObjectName("clearButton")
        clear_btn.clicked.connect(self.clear)
        example_btn = QPushButton("示例")
        example_btn.setObjectName("exampleButton")
        example_btn.clicked.connect(self.fill_example)
        button_layout.addWidget(calc_btn)
        button_layout.addWidget(clear_btn)
        button_layout.addWidget(example_btn)
        input_layout.addLayout(button_layout)

        main_layout.addWidget(input_group)

        # 结果显示组
        result_group = QGroupBox("计算结果")
        result_layout = QVBoxLayout(result_group)
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["说明", "值"])
        self.tree.setColumnWidth(0, 350)
        self.tree.setAlternatingRowColors(True)
        result_layout.addWidget(self.tree)
        main_layout.addWidget(result_group)

        # 连接信号
        self.radio_cidr.toggled.connect(self.toggle_mask)

    def toggle_mask(self):
        """切换掩码输入方式"""
        self.mask_combo.setVisible(self.radio_cidr.isChecked())
        self.mask_edit.setVisible(not self.radio_cidr.isChecked())

    def calculate(self):
        """执行计算"""
        ip = self.ip_edit.text().strip()
        if not ip:
            QMessageBox.warning(self, "提示", "请输入IP地址")
            return
        try:
            if self.radio_cidr.isChecked():
                mask = self.mask_combo.currentText()
                net = ipaddress.IPv4Network(f"{ip}{mask}", strict=False)
            else:
                mask = self.mask_edit.text().strip()
                net = ipaddress.IPv4Network(f"{ip}/{mask}", strict=False)
            self.show_result(net)
            self.parent.status.showMessage(f"基本计算完成: {net}")
        except ValueError as e:
            QMessageBox.critical(self, "错误", f"输入格式错误:\n{str(e)}")

    def show_result(self, net):
        """显示计算结果"""
        self.tree.clear()
        items = [
            ("IP地址/网络", str(net)),
            ("网络地址", str(net.network_address)),
            ("广播地址", str(net.broadcast_address)),
            ("子网掩码 (CIDR)", f"/{net.prefixlen}"),
            ("子网掩码 (点分十进制)", str(net.netmask)),
            ("地址总数", str(net.num_addresses))
        ]
        if net.prefixlen <= 30:
            items += [("可用主机范围", f"{net.network_address + 1} - {net.broadcast_address - 1}"),
                      ("可用主机数量", str(net.num_addresses - 2))]
        else:
            items.append(("可用主机范围", "N/A"))
        cls = "私有网络" if net.is_private else (
            "环回" if net.is_loopback else (
                "链路本地" if net.is_link_local else ("组播" if net.is_multicast else "公有网络")))
        items.append(("网络类别", cls))
        items.append(("IP地址 (二进制)", '.'.join(f"{int(x):08b}" for x in str(net.network_address).split('.'))))
        items.append(("子网掩码 (二进制)", '.'.join(f"{int(x):08b}" for x in str(net.netmask).split('.'))))
        for desc, val in items:
            QTreeWidgetItem(self.tree, [desc, val])

    def clear(self):
        """清除输入和结果"""
        self.ip_edit.clear()
        self.mask_combo.setCurrentText("/24")
        self.mask_edit.setText("255.255.255.0")
        self.tree.clear()

    def fill_example(self):
        """填充示例数据"""
        self.ip_edit.setText("192.168.1.100")
        self.mask_combo.setCurrentText("/24")

    def collect_text(self):
        """收集文本结果用于保存"""
        txt = ""
        for i in range(self.tree.topLevelItemCount()):
            item = self.tree.topLevelItem(i)
            txt += f"{item.text(0)}: {item.text(1)}\n"
        return txt