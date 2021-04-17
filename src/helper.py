from PyQt5.QtNetwork import QNetworkConfigurationManager


def check_internet_connection():
    try:
        if QNetworkConfigurationManager().isOnline():
            return True
    except Exception as e:
        pass
    return False