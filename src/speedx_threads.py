import time
import psutil
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal
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


class DummyDataThread(QtCore.QThread):
    change_value = pyqtSignal(list)

    def __init__(self, parent=None):
        super(DummyDataThread, self).__init__(parent)

    def run(self):
        for iter in range(0, 100):
            self.change_value.emit(["{0}%".format(iter), str(iter)])
            time.sleep(0.007)


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
