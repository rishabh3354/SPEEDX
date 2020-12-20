import sys
import platform
import time

import psutil
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect,
                          QSize, QTime, QUrl, Qt, QEvent, pyqtSignal)
from PyQt5.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence,
                         QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PyQt5.QtWidgets import *

# GUI FILE
from extras import ABOUT_ME
from ui_main import Ui_MainWindow

# IMPORT FUNCTIONS
from ui_functions import *
from utility import UtilsInfo


class CpuThread(QtCore.QThread):
    change_value = pyqtSignal(list)

    def __init__(self, parent=None):
        super(CpuThread, self).__init__(parent)

    def run(self):
        while True:
            percentage_cpu = UtilsInfo.get_cpu_usage_percentage(self)
            cpu_temp = UtilsInfo.get_cpu_temp(self)
            self.change_value.emit([percentage_cpu, cpu_temp])
            time.sleep(1)

class RamThread(QtCore.QThread):
    change_value = pyqtSignal(list)

    def __init__(self, parent=None):
        super(RamThread, self).__init__(parent)

    def run(self):
        while True:
            ram_usage = UtilsInfo.get_ram_usage(self)
            total_ram = UtilsInfo.get_total_ram(self)
            available_ram = UtilsInfo.get_available_ram(self)
            self.change_value.emit([ram_usage, total_ram, available_ram])
            time.sleep(1)

class NetSpeedThread(QtCore.QThread):
    change_value = pyqtSignal(list)

    def __init__(self, parent=None):
        super(NetSpeedThread, self).__init__(parent)

    def convert_to_gbit(self, value):
        return str(self.convert_bytes(value)).split("-")

    def send_stat(self, value):
        return self.convert_to_gbit(value)

    def convert_bytes(self, num):
        """
        this function will convert bytes to MB.... GB... etc
        """
        step_unit = 1000.0  # 1024 bad the size

        for x in ['B/s', 'KB/s', 'MB/s', 'GB/s', 'TB/s']:
            if num < step_unit:
                return "%3.1f-%s" % (num, x)
            num /= step_unit

    def run(self):
        old_value = 0
        while True:
            new_value = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv
            ping_data = str(UtilsInfo.check_internet_connection(self))
            if ping_data == "Connected":
                if old_value:
                    self.change_value.emit([self.send_stat(new_value - old_value), ping_data])
                old_value = new_value
            else:
                self.change_value.emit([["0", "B/s"], ping_data])
            time.sleep(1)


class DummyDataThread(QtCore.QThread):
    change_value = pyqtSignal(list)

    def __init__(self, parent=None):
        super(DummyDataThread, self).__init__(parent)

    def run(self):
        for iter in range(0, 100):
            self.change_value.emit(["{0}%".format(iter), str(iter)])
            time.sleep(0.007)


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # MOVE WINDOW
        def moveWindow(event):
            # RESTORE BEFORE MOVE
            if UIFunctions.returnStatus() == 1:
                UIFunctions.maximize_restore(self)

            # IF LEFT CLICK MOVE WINDOW
            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.dragPos)
                self.dragPos = event.globalPos()
                event.accept()

        # SET TITLE BAR
        self.ui.title_bar.mouseMoveEvent = moveWindow

        ## ==> SET UI DEFINITIONS
        UIFunctions.uiDefinitions(self)


        ## SHOW ==> MAIN WINDOW
        ########################################################################
        self.ui.pushButton.clicked.connect(self.credit_button_clicked)

        self.ui.textEdit.setText(ABOUT_ME)
        self.load_cpu_data()
        self.load_ram_data()
        self.load_net_speed_data()
        self.show()
        self.load_annimation_data()



    ## APP EVENTS
    ########################################################################
    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()

    def load_annimation_data(self):
        self.dummy_data_thread = DummyDataThread()
        self.dummy_data_thread.change_value.connect(self.setProgress_dummy_data)
        self.dummy_data_thread.start()


    def load_cpu_data(self):
        self.ui.label_3.setText(UtilsInfo.get_cpu_info(self))
        self.ui.label_13.setText(UtilsInfo.get_system_info(self))
        self.start_cpu_thread()

    def load_ram_data(self):
        self.start_ram_thread()

    def load_net_speed_data(self):
        self.start_net_speed_thread()

    def start_cpu_thread(self):
        self.cpu_thread = CpuThread()
        self.cpu_thread.change_value.connect(self.setProgress_cpu)
        self.cpu_thread.start()

    def start_ram_thread(self):
        self.ram_thread = RamThread()
        self.ram_thread.change_value.connect(self.setProgress_ram)
        self.ram_thread.start()

    def start_net_speed_thread(self):
        self.net_speed_thread = NetSpeedThread()
        self.net_speed_thread.change_value.connect(self.setProgress_net_speed)
        self.net_speed_thread.start()

    def setProgress_cpu(self, value):
        self.ui.label_2.setText(value[0])
        self.ui.label_4.setText(value[1])

    def setProgress_ram(self, value):
        self.ui.label_10.setText(value[0])
        self.ui.label_11.setText(value[1])
        self.ui.label_12.setText(value[2])

    def setProgress_net_speed(self, value):
        self.ui.label_6.setText(value[0][0])
        self.ui.label_7.setText(value[0][1])
        self.ui.label_8.setText(value[1])

    def setProgress_dummy_data(self, value):
        self.ui.label_2.setText(value[0])
        self.ui.label_10.setText(value[0])
        self.ui.label_6.setText(value[1])

    def credit_button_clicked(self):
        if self.ui.stackedWidget.currentIndex() == 0:
            self.ui.stackedWidget.setCurrentIndex(1)
            self.ui.textEdit.setReadOnly(True)
            self.ui.textEdit.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
            self.ui.textEdit.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        else:
            self.ui.stackedWidget.setCurrentIndex(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
