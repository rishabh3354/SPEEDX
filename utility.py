import platform
import random

import cpuinfo
import psutil
import urllib.request

import speedtest


class UtilsInfo:

    def __init__(self):
        pass

    def get_system_info(self):
        return platform.uname().node

    # CPU
    def get_cpu_info(self):
        return str(cpuinfo.get_cpu_info()["brand_raw"]).split("@")[0]

    def get_cpu_temp(self):
        return "Temp {0} ºC".format(dict(psutil.sensors_temperatures())["acpitz"][0].current)

    def get_cpu_usage_percentage(self):
        return "{0}%".format("{:.1f}".format(psutil.cpu_percent()))

    # RAM
    def get_ram_usage(self):
        return "{0}%".format("{:.1f}".format(psutil.virtual_memory().percent))

    def get_total_ram(self):
        return "Total {0} GB".format("{:.1f}".format(psutil.virtual_memory().total / 1073741824))

    def get_available_ram(self):
        return "Free {0} GB".format("{:.1f}".format(psutil.virtual_memory().free / 1073741824))


    # Internet speed

    def check_internet_connection(self):
        try:
            urllib.request.urlopen("http://google.com")
            return "Connected"
        except:
            message = ["No Internet", "Please connect to Internet"]
            return random.choice(message)


