#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
子网划分Widget类定义
"""

from math import log2, ceil
import ipaddress
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QGroupBox,
                               QLabel, QLineEdit, QComboBox, QTreeWidget,
                               QTreeWidgetItem, QPushButton, QRadioButton,
                               QButtonGroup, QMessageBox)
from PySide6.QtCore import Qt


class SubnetWidget(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.build_ui()

    def build_ui(self):
        """构建用户界面"""
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)

        # 子网划分参数组
        param_group = QGroupBox("子网划分参数")
        param_layout = QVBoxLayout(param_group)
        param_layout.setSpacing(10)

        # 网络地址输入
        ip_layout = QHBoxLayout()
        ip_layout.addWidget(QLabel("网络地址:"), 0)
        self.ip_edit = QLineEdit()
        self.ip_edit.setPlaceholderText("例如: 192.168.1.0")
        ip_layout.addWidget(self.ip_edit, 1)
        param_layout.addLayout(ip_layout)

        # 子网掩码输入
        mask_layout = QHBoxLayout()
        mask_layout.addWidget(QLabel("子网掩码:"), 0)
        self.mask_combo = QComboBox()
        self.mask_combo.addItems([f"/{i}" for i in range(8, 33)])
        self.mask_combo.setCurrentText("/24")
        self.mask_combo.setMinimumWidth(80)
        mask_layout.addWidget(self.mask_combo, 0)
        mask_layout.addStretch(1)
        param_layout.addLayout(mask_layout)

        # 划分方式选择
        method_layout = QHBoxLayout()
        method_layout.addWidget(QLabel("划分方式:"), 0)
        self.method_group = QButtonGroup()
        self.radio_count = QRadioButton("按子网数量")
        self.radio_hosts = QRadioButton("按主机数量")
        self.method_group.addButton(self.radio_count)
        self.method_group.addButton(self.radio_hosts)
        self.radio_count.setChecked(True)
        method_layout.addWidget(self.radio_count)
        method_layout.addWidget(self.radio_hosts)
        method_layout.addStretch(1)
        param_layout.addLayout(method_layout)

        # 子网数量输入
        count_layout = QHBoxLayout()
        count_layout.addWidget(QLabel("子网数量:"), 0)
        self.count_edit = QLineEdit("4")
        self.count_edit.setPlaceholderText("输入需要的子网数量")
        count_layout.addWidget(self.count_edit, 0)
        count_layout.addStretch(1)
        param_layout.addLayout(count_layout)

        # 主机数量输入
        hosts_layout = QHBoxLayout()
        hosts_layout.addWidget(QLabel("每个子网的主机数:"), 0)
        self.hosts_edit = QLineEdit()
        self.hosts_edit.setPlaceholderText("输入每个子网需要的主机数量")
        self.hosts_edit.setVisible(False)
        hosts_layout.addWidget(self.hosts_edit, 0)
        hosts_layout.addStretch(1)
        param_layout.addLayout(hosts_layout)

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
        param_layout.addLayout(button_layout)

        main_layout.addWidget(param_group)

        # 结果显示组
        result_group = QGroupBox("子网划分结果")
        result_layout = QVBoxLayout(result_group)
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["网络地址", "第一个可用IP", "最后一个可用IP", "广播地址", "子网掩码"])
        for i, w in enumerate([180, 150, 150, 180, 150]):
            self.tree.setColumnWidth(i, w)
        self.tree.setAlternatingRowColors(True)
        result_layout.addWidget(self.tree)
        main_layout.addWidget(result_group)

        # 连接信号
        self.radio_count.toggled.connect(self.toggle_method)

    def toggle_method(self):
        """切换划分方法"""
        self.count_edit.setVisible(self.radio_count.isChecked())
        self.hosts_edit.setVisible(not self.radio_count.isChecked())

    def calculate(self):
        """执行子网划分计算"""
        net_addr = self.ip_edit.text().strip()
        mask = self.mask_combo.currentText()
        if not net_addr:
            QMessageBox.warning(self, "提示", "请输入网络地址")
            return
        try:
            net = ipaddress.IPv4Network(f"{net_addr}{mask}", strict=False)
            if self.radio_count.isChecked():
                count = int(self.count_edit.text())
                if count <= 0:
                    QMessageBox.warning(self, "提示", "子网数量必须大于0")
                    return
                bits = ceil(log2(count))
                new_prefix = net.prefixlen + bits
                if new_prefix > 30:
                    QMessageBox.warning(self, "警告", "子网划分太细，会导致主机数为0")
                    return
                subnets = list(net.subnets(new_prefix=new_prefix))
            else:
                hosts = int(self.hosts_edit.text())
                if hosts <= 0:
                    QMessageBox.warning(self, "提示", "主机数量必须大于0")
                    return
                bits = ceil(log2(hosts + 2))
                new_prefix = 32 - bits
                if new_prefix <= net.prefixlen:
                    QMessageBox.warning(self, "警告", "主机数超出网络容量")
                    return
                subnets = list(net.subnets(new_prefix=new_prefix))
            self.show_result(subnets)
            self.parent.status.showMessage(f"成功划分 {len(subnets)} 个子网")
        except ValueError as e:
            QMessageBox.critical(self, "错误", f"输入格式错误:\n{str(e)}")

    def show_result(self, subnets):
        """显示子网划分结果"""
        self.tree.clear()
        for sn in subnets[:100]:  # 限制显示前100个子网
            first = str(sn.network_address + 1) if sn.prefixlen <= 30 else "N/A"
            last = str(sn.broadcast_address - 1) if sn.prefixlen <= 30 else "N/A"
            QTreeWidgetItem(self.tree, [str(sn.network_address), first, last,
                                        str(sn.broadcast_address), str(sn.netmask)])

    def clear(self):
        """清除输入和结果"""
        self.ip_edit.clear()
        self.mask_combo.setCurrentText("/24")
        self.count_edit.setText("4")
        self.hosts_edit.clear()
        self.tree.clear()

    def collect_text(self):
        """收集文本结果用于保存"""
        txt = ""
        for i in range(self.tree.topLevelItemCount()):
            item = self.tree.topLevelItem(i)
            txt += f"{item.text(0)} 掩码:{item.text(4)} 可用:{item.text(1)}-{item.text(2)} 广播:{item.text(3)}\n"
        return txt