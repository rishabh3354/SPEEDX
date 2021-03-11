import time
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal
from login_helper import get_login_and_save_token, check_for_local_token, get_signup_user


class LoggingInThread(QtCore.QThread):
    change_value_login = pyqtSignal(dict)

    def __init__(self, data, parent=None):
        super(LoggingInThread, self).__init__(parent)
        self.data = data

    def run(self):
        token_path = get_login_and_save_token(self.data)
        self.change_value_login.emit(token_path)


class RefreshButtonThread(QtCore.QThread):
    change_value_refresh = pyqtSignal(str)

    def __init__(self, parent=None):
        super(RefreshButtonThread, self).__init__(parent)

    def run(self):
        token = check_for_local_token()
        time.sleep(1)
        self.change_value_refresh.emit(token)


class SignUpThread(QtCore.QThread):
    change_value_signup = pyqtSignal(dict)

    def __init__(self, data, parent=None):
        super(SignUpThread, self).__init__(parent)
        self.data = data

    def run(self):
        message = get_signup_user(self.data)
        self.change_value_signup.emit(message)
