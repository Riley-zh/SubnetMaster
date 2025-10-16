# subnet_gui.py
import sys
from math import log2, ceil
import ipaddress
from pathlib import Path

from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                               QTabWidget, QLabel, QLineEdit, QComboBox, QTextEdit,
                               QRadioButton, QButtonGroup, QPushButton, QTreeWidget,
                               QTreeWidgetItem, QFileDialog, QMessageBox, QGroupBox,
                               QMenuBar, QStatusBar, QAction)
from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtGui import QFont, QPalette, QColor


class SubnetCalculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("子网计算器v5.0")
        self.resize(1000, 780)

        # 默认：清晰字体 + 浅色主题
        self.dark_theme = False
        self.apply_theme()

        self.init_ui()

    # --------------------------------------------------
    def apply_theme(self):
        app = QApplication.instance()
        if self.dark_theme:
            dark = QPalette()
            dark.setColor(QPalette.Window, QColor(30, 30, 30))
            dark.setColor(QPalette.WindowText, Qt.white)
            dark.setColor(QPalette.Base, QColor(42, 42, 42))
            dark.setColor(QPalette.Text, Qt.white)
            dark.setColor(QPalette.Button, QColor(53, 53, 53))
            dark.setColor(QPalette.ButtonText, Qt.white)
            app.setPalette(dark)
        else:
            app.setStyle("Fusion")          # 在所有平台下字体清晰
            app.setPalette(app.style().standardPalette())

        # 统一字体（防止系统 DPI 缩放导致模糊）
        font = QFont("Segoe UI", 10)
        if sys.platform == "darwin":
            font = QFont("SF Pro", 12)
        elif sys.platform.startswith("linux"):
            font = QFont("Noto Sans", 10)
        app.setFont(font)

    # --------------------------------------------------
    def init_ui(self):
        self.create_menu()
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.status.showMessage("就绪")

        tabs = QTabWidget()
        self.setCentralWidget(tabs)

        self.tab_basic = BasicCalcWidget(self)
        self.tab_subnet = SubnetWidget(self)
        self.tab_super = SupernetWidget(self)

        tabs.addTab(self.tab_basic, "基本计算")
        tabs.addTab(self.tab_subnet, "子网划分")
        tabs.addTab(self.tab_super, "超网计算")

    def create_menu(self):
        menu = self.menuBar()
        file_menu = menu.addMenu("文件")
        file_menu.addAction("保存结果", self.save_all_results)
        file_menu.addSeparator()
        file_menu.addAction("退出", QApplication.quit)

        view_menu = menu.addMenu("视图")
        toggle_theme = QAction("切换浅色/暗色主题", self)
        toggle_theme.triggered.connect(self.toggle_theme)
        view_menu.addAction(toggle_theme)

        help_menu = menu.addMenu("帮助")
        help_menu.addAction("使用说明", self.show_help)
        help_menu.addAction("关于", self.show_about)

    def toggle_theme(self):
        self.dark_theme = not self.dark_theme
        self.apply_theme()

    def save_all_results(self):
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
            Path(path).write_text(content, encoding="utf-8")
            self.status.showMessage(f"已保存到 {path}")

    def show_help(self):
        QMessageBox.information(self, "使用说明",
                                "功能与原版一致，界面升级到 PyQt5。\n"
                                "通过菜单“视图→切换浅色/暗色主题”可更换外观。")

    def show_about(self):
        QMessageBox.information(self, "关于",
                                "高级子网计算器 v5.0\n"
                                "作者：Sven\n"
                                "PyQt5 重构版本")


# ------------------------------------------------------------
class BasicCalcWidget(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.build_ui()

    def build_ui(self):
        v = QVBoxLayout(self)

        grp = QGroupBox("输入参数")
        form = QVBoxLayout(grp)

        h1 = QHBoxLayout()
        h1.addWidget(QLabel("IP地址/网络:"))
        self.ip_edit = QLineEdit()
        h1.addWidget(self.ip_edit)
        form.addLayout(h1)

        h2 = QHBoxLayout()
        self.mask_group = QButtonGroup()
        self.radio_cidr = QRadioButton("CIDR")
        self.radio_dot = QRadioButton("点分十进制")
        self.mask_group.addButton(self.radio_cidr)
        self.mask_group.addButton(self.radio_dot)
        self.radio_cidr.setChecked(True)
        h2.addWidget(self.radio_cidr)
        h2.addWidget(self.radio_dot)
        form.addLayout(h2)

        self.mask_combo = QComboBox()
        self.mask_combo.addItems([f"/{i}" for i in range(8, 33)])
        self.mask_combo.setCurrentText("/24")
        form.addWidget(self.mask_combo)

        self.mask_edit = QLineEdit("255.255.255.0")
        self.mask_edit.setVisible(False)
        form.addWidget(self.mask_edit)

        self.radio_cidr.toggled.connect(self.toggle_mask)

        btn_box = QHBoxLayout()
        calc_btn = QPushButton("计算")
        calc_btn.clicked.connect(self.calculate)
        clear_btn = QPushButton("清除")
        clear_btn.clicked.connect(self.clear)
        example_btn = QPushButton("示例")
        example_btn.clicked.connect(self.fill_example)
        btn_box.addWidget(calc_btn)
        btn_box.addWidget(clear_btn)
        btn_box.addWidget(example_btn)
        form.addLayout(btn_box)
        v.addWidget(grp)

        res_grp = QGroupBox("计算结果")
        res_v = QVBoxLayout(res_grp)
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["说明", "值"])
        self.tree.setColumnWidth(0, 350)
        res_v.addWidget(self.tree, 1)
        v.addWidget(res_grp, 1)

    def toggle_mask(self):
        self.mask_combo.setVisible(self.radio_cidr.isChecked())
        self.mask_edit.setVisible(not self.radio_cidr.isChecked())

    def calculate(self):
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
            QMessageBox.critical(self, "错误", str(e))

    def show_result(self, net):
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
        self.ip_edit.clear()
        self.mask_combo.setCurrentText("/24")
        self.mask_edit.setText("255.255.255.0")
        self.tree.clear()

    def fill_example(self):
        self.ip_edit.setText("192.168.1.100")
        self.mask_combo.setCurrentText("/24")

    def collect_text(self):
        txt = ""
        for i in range(self.tree.topLevelItemCount()):
            item = self.tree.topLevelItem(i)
            txt += f"{item.text(0)}: {item.text(1)}\n"
        return txt


# ------------------------------------------------------------
class SubnetWidget(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.build_ui()

    def build_ui(self):
        v = QVBoxLayout(self)

        grp = QGroupBox("子网划分参数")
        form = QVBoxLayout(grp)

        h1 = QHBoxLayout()
        h1.addWidget(QLabel("网络地址:"))
        self.ip_edit = QLineEdit()
        h1.addWidget(self.ip_edit)
        form.addLayout(h1)

        h2 = QHBoxLayout()
        h2.addWidget(QLabel("子网掩码:"))
        self.mask_combo = QComboBox()
        self.mask_combo.addItems([f"/{i}" for i in range(8, 33)])
        self.mask_combo.setCurrentText("/24")
        h2.addWidget(self.mask_combo)
        form.addLayout(h2)

        h3 = QHBoxLayout()
        self.method_group = QButtonGroup()
        self.radio_count = QRadioButton("按子网数量")
        self.radio_hosts = QRadioButton("按主机数量")
        self.method_group.addButton(self.radio_count)
        self.method_group.addButton(self.radio_hosts)
        self.radio_count.setChecked(True)
        h3.addWidget(self.radio_count)
        h3.addWidget(self.radio_hosts)
        form.addLayout(h3)

        self.count_edit = QLineEdit("4")
        form.addWidget(QLabel("子网数量:"))
        form.addWidget(self.count_edit)

        self.hosts_edit = QLineEdit()
        self.hosts_edit.setVisible(False)
        form.addWidget(QLabel("每个子网的主机数:"))
        form.addWidget(self.hosts_edit)

        self.radio_count.toggled.connect(self.toggle_method)

        btn_box = QHBoxLayout()
        calc_btn = QPushButton("计算")
        calc_btn.clicked.connect(self.calculate)
        clear_btn = QPushButton("清除")
        clear_btn.clicked.connect(self.clear)
        btn_box.addWidget(calc_btn)
        btn_box.addWidget(clear_btn)
        form.addLayout(btn_box)
        v.addWidget(grp)

        res_grp = QGroupBox("子网划分结果")
        res_v = QVBoxLayout(res_grp)
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["网络地址", "第一个可用IP", "最后一个可用IP", "广播地址", "子网掩码"])
        for i, w in enumerate([180, 150, 150, 180, 150]):
            self.tree.setColumnWidth(i, w)
        res_v.addWidget(self.tree, 1)
        v.addWidget(res_grp, 1)

    def toggle_method(self):
        self.count_edit.setVisible(self.radio_count.isChecked())
        self.hosts_edit.setVisible(not self.radio_count.isChecked())

    def calculate(self):
        net_addr = self.ip_edit.text().strip()
        mask = self.mask_combo.currentText()
        if not net_addr:
            QMessageBox.warning(self, "提示", "请输入网络地址")
            return
        try:
            net = ipaddress.IPv4Network(f"{net_addr}{mask}", strict=False)
            if self.radio_count.isChecked():
                count = int(self.count_edit.text())
                bits = ceil(log2(count))
                new_prefix = net.prefixlen + bits
                if new_prefix > 30:
                    QMessageBox.warning(self, "警告", "子网划分太细，会导致主机数为0")
                    return
                subnets = list(net.subnets(new_prefix=new_prefix))
            else:
                hosts = int(self.hosts_edit.text())
                bits = ceil(log2(hosts + 2))
                new_prefix = 32 - bits
                if new_prefix <= net.prefixlen:
                    QMessageBox.warning(self, "警告", "主机数超出网络容量")
                    return
                subnets = list(net.subnets(new_prefix=new_prefix))
            self.show_result(subnets)
            self.parent.status.showMessage(f"成功划分 {len(subnets)} 个子网")
        except ValueError as e:
            QMessageBox.critical(self, "错误", str(e))

    def show_result(self, subnets):
        self.tree.clear()
        for sn in subnets[:100]:
            first = str(sn.network_address + 1) if sn.prefixlen <= 30 else "N/A"
            last = str(sn.broadcast_address - 1) if sn.prefixlen <= 30 else "N/A"
            QTreeWidgetItem(self.tree, [str(sn.network_address), first, last,
                                        str(sn.broadcast_address), str(sn.netmask)])

    def clear(self):
        self.ip_edit.clear()
        self.mask_combo.setCurrentText("/24")
        self.count_edit.setText("4")
        self.hosts_edit.clear()
        self.tree.clear()

    def collect_text(self):
        txt = ""
        for i in range(self.tree.topLevelItemCount()):
            item = self.tree.topLevelItem(i)
            txt += f"{item.text(0)} 掩码:{item.text(4)} 可用:{item.text(1)}-{item.text(2)} 广播:{item.text(3)}\n"
        return txt


# ------------------------------------------------------------
class SupernetWidget(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.build_ui()

    def build_ui(self):
        v = QVBoxLayout(self)

        grp = QGroupBox("输入网络列表")
        form = QVBoxLayout(grp)
        form.addWidget(QLabel("网络地址(用逗号或换行分隔):"))
        self.text_edit = QTextEdit()
        form.addWidget(self.text_edit)

        btn_box = QHBoxLayout()
        calc_btn = QPushButton("计算")
        calc_btn.clicked.connect(self.calculate)
        clear_btn = QPushButton("清除")
        clear_btn.clicked.connect(self.clear)
        btn_box.addWidget(calc_btn)
        btn_box.addWidget(clear_btn)
        form.addLayout(btn_box)
        v.addWidget(grp)

        res_grp = QGroupBox("超网计算结果")
        res_v = QVBoxLayout(res_grp)
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["属性", "值"])
        self.tree.setColumnWidth(0, 300)
        res_v.addWidget(self.tree, 1)
        v.addWidget(res_grp, 1)

    def calculate(self):
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
            QMessageBox.critical(self, "错误", str(e))

    def show_result(self, supernets, original):
        self.tree.clear()
        QTreeWidgetItem(self.tree, ["输入的网络数量", str(len(original))])
        QTreeWidgetItem(self.tree, ["原始网络列表", ", ".join(str(n) for n in original)])
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
        self.text_edit.clear()
        self.tree.clear()

    def collect_text(self):
        txt = ""
        for i in range(self.tree.topLevelItemCount()):
            item = self.tree.topLevelItem(i)
            txt += f"{item.text(0)}: {item.text(1)}\n"
        return txt


# ------------------------------------------------------------
if __name__ == "__main__":
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    w = SubnetCalculator()
    w.show()
    sys.exit(app.exec())