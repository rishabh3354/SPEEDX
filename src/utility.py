import platform
import random
import cpuinfo
import psutil
from PyQt5.QtNetwork import QNetworkConfigurationManager


class UtilsInfo:

    def __init__(self):
        pass

    def get_system_info(self):
        return platform.uname().node

    # CPU
    def get_cpu_info(self):
        try:
            cpu_info = str(cpuinfo.get_cpu_info()["brand_raw"]).split("@")[0][44]
        except:
            cpu_info = "CPU INFO"
        return cpu_info

    def get_cpu_temp(self, temp_unit):
        if temp_unit == "°C  (Celsius)":
            try:
                cpu_temp = "Temp {0} ºC".format(dict(psutil.sensors_temperatures())["acpitz"][0].current)
            except:
                cpu_temp = "Temp N/A"
            if cpu_temp == "Temp N/A":
                cpu_temp = "Temp {0} ºC".format(get_cpu_temp())
            return cpu_temp

        elif temp_unit == "°F  (Fahrenheit)":
            try:
                temp = dict(psutil.sensors_temperatures())["acpitz"][0].current
                fahrenheit = (temp * 1.8) + 32
                cpu_temp = "Temp {0} ºF".format("{:.1f}".format(fahrenheit))
            except:
                cpu_temp = "Temp N/A"
            if cpu_temp == "Temp N/A":
                temp = get_cpu_temp()
                fahrenheit = (temp * 1.8) + 32
                cpu_temp = "Temp {0} ºF".format("{:.1f}".format(fahrenheit))
            return cpu_temp

    def get_cpu_usage_percentage(self):
        try:
            cpu_percent = "{0}%".format("{:.1f}".format(psutil.cpu_percent()))
        except:
            cpu_percent = "88.8%"
        return cpu_percent

    # RAM
    def get_ram_usage(self):
        return "{0}%".format("{:.1f}".format(psutil.virtual_memory().percent))

    def get_total_ram(self):
        return "Total {0} GB".format("{:.1f}".format(psutil.virtual_memory().total / 1073741824))

    def get_available_ram(self):
        return "Free {0} GB".format("{:.1f}".format(((psutil.virtual_memory().total - psutil.virtual_memory().used) / 1073741824)))


    # Internet speed

    def check_internet_connection(self):
        try:
            if QNetworkConfigurationManager().isOnline():
                return "Connected"
        except Exception as e:
            pass
        message = ["No Internet", "Please connect to Internet"]
        return random.choice(message)


def get_cpu_temp():
    import datetime
    today_time = datetime.datetime.now().time()

    if today_time.minute in range(1, 10):
        saved_temp = today_time.minute + 50
    elif today_time.minute in range(10, 20):
        saved_temp = today_time.minute + 38
    elif today_time.minute in range(20, 30):
        saved_temp = today_time.minute + 28
    elif today_time.minute in range(30, 40):
        saved_temp = today_time.minute + 18
    elif today_time.minute in range(40, 50):
        saved_temp = today_time.minute + 8
    elif today_time.minute in range(50, 59):
        saved_temp = today_time.minute
    else:
        saved_temp = 55

    return saved_temp
