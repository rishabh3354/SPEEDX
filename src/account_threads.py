import time
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal
from accounts import get_login_and_save_token, check_for_local_token, SignInUpdatePlan, check_internet_connection


class RefreshButtonThread(QtCore.QThread):
    change_value_refresh = pyqtSignal(dict)

    def __init__(self, product_name, parent=None):
        super(RefreshButtonThread, self).__init__(parent)
        self.product_name = product_name
        self.token = check_for_local_token()

    def run(self):
        status = {"status": False, "message": "Something went wrong!"}
        try:
            if self.token:
                if check_internet_connection():
                    response = SignInUpdatePlan(self.product_name, self.token).update_local_expiry_and_client_data()
                    if response.get("status"):
                        status["status"] = True
                        status["message"] = response.get("message")
                    else:
                        status["status"] = False
                        status["message"] = response.get("message")
                else:
                    status["status"] = False
                    status["message"] = "Please check your internet connection!"
            else:
                status["status"] = False
                status["message"] = "No Active Plan"
            self.change_value_refresh.emit(status)
        except Exception as e:
            status["message"] = str(e)
            self.change_value_refresh.emit(status)


class SaveLocalInToken(QtCore.QThread):

    def __init__(self, data, parent=None):
        super(SaveLocalInToken, self).__init__(parent)
        self.data = data

    def run(self):
        try:
            time.sleep(5)
            get_login_and_save_token(self.data)
        except Exception as e:
            pass
