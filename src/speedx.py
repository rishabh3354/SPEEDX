import datetime
import re
import sys
import webbrowser
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from extras import ABOUT_ME
from login_helper import check_for_local_token, get_user_data_from_local, convert_date_str_for_user_data, \
    SignInUpdatePlan, delete_user_data_from_local, ApplicationStartupTask, LoginPage, your_plan_button_connects, \
    notify_for_expiry
from speedx_threads import DummyDataThread, CpuThread, RamThread, NetSpeedThread
from style import theme_dict, button_dict
from ui_main import Ui_MainWindow
from utility import UtilsInfo
from your_plan_threads import LoggingInThread, SignUpThread, RefreshButtonThread

PRODUCT_NAME = "SPEEDX"


class MainWindow(QMainWindow):
    def __init__(self):
        from ui_functions import UIFunctions
        QMainWindow.__init__(self)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        UIFunctions.uiDefinitions(self)
        self.ui.pushButton.clicked.connect(self.credit_button_clicked)
        self.ui.theme_button.clicked.connect(self.change_theme)
        self.ui.textBrowser.setText(ABOUT_ME)
        self.count = 1  # theme set counter

        def moveWindow(event):
            # RESTORE BEFORE MOVE
            if UIFunctions.returnStatus() == 1:
                UIFunctions.maximize_restore(self)

            # IF LEFT CLICK MOVE WINDOW
            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.dragPos)
                self.dragPos = event.globalPos()
                event.accept()

        self.ui.title_bar.mouseMoveEvent = moveWindow

        #  ======================Your plan functionality starts=============================================
        self.msg = QMessageBox()
        self.login_ui = LoginPage(login_user=False)
        self.ui.my_plan_button.clicked.connect(self.my_plan)
        your_plan_button_connects(self)
        # local_plan_expiry_check
        ApplicationStartupTask().create_free_trial_offline()
        # include closeEvent function also.
        # include requests, cryptography python package in snapcraft.yaml file.
        # check your check_your_plan function.
        #  ======================Your plan functionality end=============================================

        if not ApplicationStartupTask().is_expired_product():
            self.load_cpu_data()
            self.load_ram_data()
            self.load_net_speed_data()
            self.show()
            self.load_annimation_data()

        else:
            self.show()
            self.load_annimation_data()
            self.check_your_plan()

    def change_theme(self):
        pass
        # if self.count == 5:
        #     self.count = 1
        # self.ui.drop_shadow_frame.setStyleSheet(theme_dict.get(self.count))
        # self.ui.pushButton.setStyleSheet(button_dict.get(self.count))
        # self.ui.theme_button.setStyleSheet(button_dict.get(self.count))
        # self.ui.my_plan_button.setStyleSheet(button_dict.get(self.count))
        # self.ui.textBrowser.setStyleSheet(theme_dict.get(self.count))
        # self.count += 1

    def closeEvent(self, event):
        self.login_ui.hide()

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
            self.ui.textBrowser.setReadOnly(True)
            self.ui.textBrowser.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
            self.ui.textBrowser.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        else:
            self.ui.stackedWidget.setCurrentIndex(0)

    # ================Login code starts=======================================

    def my_plan(self):
        self.login_ui.show()
        token = check_for_local_token()
        if token not in [None, ""]:
            user_plan_data = get_user_data_from_local()
            if user_plan_data:
                user_plan_data = convert_date_str_for_user_data(user_plan_data)
                self.logged_in_user_plan_page(user_plan_data)
            else:
                user_plan_data = dict()
                user_plan_data['plan'] = "N/A"
                user_plan_data['expiry_date'] = "N/A"
                user_plan_data['created_on'] = "N/A"
                user_plan_data['email'] = "N/A"
                user_plan_data['product'] = PRODUCT_NAME
                self.logged_in_user_plan_page(user_plan_data)
        else:
            user_plan_data = get_user_data_from_local()
            if user_plan_data:
                user_plan_data = convert_date_str_for_user_data(user_plan_data)
                self.logged_out_user_plan_page(user_plan_data)

    def check_your_plan(self):
        if ApplicationStartupTask().is_expired_product():
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setText("Plan Expired!")
            self.msg.setInformativeText("Your trial period has expired. Please purchase a plan (75% OFF)")
            self.msg.setWindowTitle(PRODUCT_NAME)
            month_name = datetime.datetime.now().date().strftime("%B")
            self.msg.setDetailedText(f"In {month_name} month we are giving bumpher"
                                     f" discount of 75% OFF. Valid for limited period only.\nHURRY UP !!")
            self.msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Close)
            purchase_button = self.msg.button(QMessageBox.Ok)
            purchase_button.setText('Purchase Now')
            self.msg.exec_()
            if self.msg.clickedButton() == purchase_button:
                self.my_plan()
                return True
            else:
                return True
        else:
            return False

    def logged_in_user_plan_page(self, user_plan_data):
        self.login_ui.ui.product_name.setText(PRODUCT_NAME)
        self.login_ui.ui.purchase_plan_obj_2.setText(user_plan_data.get("plan", "N/A"))
        if notify_for_expiry(user_plan_data.get("expiry_date")):
            self.login_ui.ui.refresh_error.setText("YOUR PLAN HAS EXPIRED, PLEASE BUY A PLAN")
        self.login_ui.ui.expire_on_obj_2.setText(user_plan_data.get("expiry_date", "N/A"))
        self.login_ui.ui.activation_date_obj_2.setText(user_plan_data.get("created_on", "N/A"))
        self.login_ui.ui.hello_user_email_obj_2.setText(f"Welcome {user_plan_data.get('email', 'How are you today')}")
        self.login_ui.ui.log_out_button_obj_2.setVisible(True)
        self.login_ui.ui.login_from_your_plan.setVisible(False)

    def logged_out_user_plan_page(self, user_plan_data):
        self.login_ui.ui.product_name.setText(PRODUCT_NAME)
        self.login_ui.ui.purchase_plan_obj_2.setText(user_plan_data.get("plan", "N/A"))
        if notify_for_expiry(user_plan_data.get("expiry_date")):
            self.login_ui.ui.refresh_error.setText("YOUR PLAN HAS EXPIRED, PLEASE BUY A PLAN")
        self.login_ui.ui.expire_on_obj_2.setText(user_plan_data.get("expiry_date", "N/A"))
        self.login_ui.ui.activation_date_obj_2.setText(user_plan_data.get("created_on", "N/A"))
        self.login_ui.ui.hello_user_email_obj_2.setText('Please Signin/Register to see your updated plan')
        self.login_ui.ui.log_out_button_obj_2.setVisible(False)

    def logout_function(self):
        self.login_ui.ui.product_name.setText(PRODUCT_NAME)
        self.login_ui.ui.purchase_plan_obj_2.setText("N/A")
        self.login_ui.ui.expire_on_obj_2.setText("N/A")
        self.login_ui.ui.activation_date_obj_2.setText("N/A")
        self.login_ui.ui.hello_user_email_obj_2.setText("Please Signin/Register to see your plan details.")
        self.login_ui.ui.log_out_button_obj_2.setVisible(False)
        self.login_ui.ui.login_from_your_plan.setVisible(True)
        self.login_ui.ui.purchase_now_button_2.setVisible(True)
        delete_user_data_from_local()

    def sign_in_user(self):
        for i in range(self.login_ui.ui.register_gridLayout_2.count() - 1, -1, -1):
            items = self.login_ui.ui.register_gridLayout_2.itemAt(i).widget()
            if items:
                items.setVisible(False)

        for i in range(self.login_ui.ui.your_plan_gridLayout.count() - 1, -1, -1):
            items = self.login_ui.ui.your_plan_gridLayout.itemAt(i).widget()
            if items:
                items.setVisible(False)

        for i in range(self.login_ui.ui.login_gridLayout.count() - 1, -1, -1):
            items = self.login_ui.ui.login_gridLayout.itemAt(i).widget()
            if items:
                if items.objectName() != "login_progressBar_2":
                    items.setVisible(True)

        self.login_ui.ui.home_button.setEnabled(True)

    def purchase_now(self):
        if self.login_ui.ui.log_out_button_obj_2.isVisible():
            token = check_for_local_token()
            warlord_soft_link = f"https://warlordsoftwares.in/warlord_soft/subscription/?product={PRODUCT_NAME}&token={token} "
            webbrowser.open(warlord_soft_link)
        else:
            for i in range(self.login_ui.ui.your_plan_gridLayout.count() - 1, -1, -1):
                items = self.login_ui.ui.your_plan_gridLayout.itemAt(i).widget()
                if items:
                    items.setVisible(False)
            self.login_ui.ui.home_button.setEnabled(True)

            for i in range(self.login_ui.ui.login_gridLayout.count() - 1, -1, -1):
                items = self.login_ui.ui.login_gridLayout.itemAt(i).widget()
                if items:
                    items.setVisible(False)

            for i in range(self.login_ui.ui.register_gridLayout_2.count() - 1, -1, -1):
                items = self.login_ui.ui.register_gridLayout_2.itemAt(i).widget()
                if items:
                    if items.objectName() != "register_progressBar":
                        items.setVisible(True)

    def refresh_button_function(self):
        if self.login_ui.ui.log_out_button_obj_2.isVisible():
            self.login_ui.ui.refresh_error.clear()
            self.login_ui.ui.login_progressBar_2.setRange(0, 0)
            self.login_ui.ui.login_progressBar_2.setVisible(True)
            self.refresh_thread = RefreshButtonThread()
            self.refresh_thread.change_value_refresh.connect(self.after_refresh)
            self.refresh_thread.start()
        else:
            message = self.login_ui.ui.refresh_error.text()
            if message != 'Please do Signin first':
                self.login_ui.ui.refresh_error.setText("Please do Signin first")
            else:
                self.login_ui.ui.refresh_error.clear()

    def after_refresh(self, token_str):
        token_data = {'status': True, 'token': token_str}
        self.after_login_step_from_signin(token_data)
        self.login_ui.ui.login_progressBar_2.setRange(0, 1)
        self.login_ui.ui.login_progressBar_2.setVisible(False)

    def show_register_page(self):
        for i in range(self.login_ui.ui.register_gridLayout_2.count() - 1, -1, -1):
            items = self.login_ui.ui.register_gridLayout_2.itemAt(i).widget()
            if items:
                if items.objectName() != "register_progressBar":
                    items.setVisible(True)

        for i in range(self.login_ui.ui.your_plan_gridLayout.count() - 1, -1, -1):
            items = self.login_ui.ui.your_plan_gridLayout.itemAt(i).widget()
            if items:
                items.setVisible(False)

        for i in range(self.login_ui.ui.login_gridLayout.count() - 1, -1, -1):
            items = self.login_ui.ui.login_gridLayout.itemAt(i).widget()
            if items:
                items.setVisible(False)

        self.login_ui.ui.home_button.setEnabled(True)

    def register_user(self):
        data = dict()
        data["email"] = str(self.login_ui.ui.register_email_id_obj.text()).strip()
        data["password"] = str(self.login_ui.ui.register_password_obj.text()).strip()
        data["re_password"] = str(self.login_ui.ui.register_re_password_obj.text()).strip()

        self.login_ui.ui.register_progressBar.setRange(0, 0)
        self.login_ui.ui.register_progressBar.setVisible(True)

        self.login_thread = SignUpThread(data)
        self.login_thread.change_value_signup.connect(self.after_signup_step)
        self.login_thread.start()

    def after_signup_step(self, data):
        if data["status"]:
            self.login_thread = LoggingInThread(data)
            self.login_thread.change_value_login.connect(self.after_login_step)
            self.login_thread.start()
        else:
            error_message = data.get("message")
            if error_message:
                self.login_ui.ui.register_error_message.setText(error_message)
            else:
                self.login_ui.ui.register_error_message.setText("Internal Server Error")
            self.login_ui.ui.register_progressBar.setRange(0, 1)
            self.login_ui.ui.register_progressBar.setVisible(False)

    def after_login_step(self, data):
        if data["status"]:
            self.login_ui.ui.register_progressBar.setRange(0, 1)
            self.login_ui.ui.register_progressBar.setVisible(False)
            self.show_your_plan_page(data)
            token = check_for_local_token()
            warlord_soft_link = f"https://warlordsoftwares.in/warlord_soft/subscription/?product={PRODUCT_NAME}&token={token} "
            webbrowser.open(warlord_soft_link)
        else:
            error_message = data.get("message")
            if error_message:
                self.login_ui.ui.register_error_message.setText(error_message)
            else:
                self.login_ui.ui.register_error_message.setText("Internal Server Error")
            self.login_ui.ui.register_progressBar.setRange(0, 1)
            self.login_ui.ui.register_progressBar.setVisible(False)
        self.login_ui.ui.home_button.setEnabled(False)
        self.login_ui.ui.login_from_your_plan.setVisible(False)

    def after_login_step_from_signin(self, data):
        if data["status"]:
            self.login_ui.ui.login_progressBar_2.setRange(0, 1)
            self.login_ui.ui.login_progressBar_2.setVisible(False)
            self.show_your_plan_page(data, from_signin=True)
        else:
            error_message = data.get("message")
            if error_message:
                self.login_ui.ui.login_error_message_2.setText(error_message)
            else:
                self.login_ui.ui.login_error_message_2.setText("Internal Server Error")
            self.login_ui.ui.login_progressBar_2.setRange(0, 1)
            self.login_ui.ui.login_progressBar_2.setVisible(False)
        self.login_ui.ui.home_button.setEnabled(False)

    def show_home_page(self):
        for i in range(self.login_ui.ui.register_gridLayout_2.count() - 1, -1, -1):
            items = self.login_ui.ui.register_gridLayout_2.itemAt(i).widget()
            if items:
                items.setVisible(False)
        for i in range(self.login_ui.ui.login_gridLayout.count() - 1, -1, -1):
            items = self.login_ui.ui.login_gridLayout.itemAt(i).widget()
            if items:
                items.setVisible(False)

        for i in range(self.login_ui.ui.your_plan_gridLayout.count() - 1, -1, -1):
            items = self.login_ui.ui.your_plan_gridLayout.itemAt(i).widget()
            if items:
                if items.objectName() != "register_progressBar":
                    items.setVisible(True)

        self.login_ui.resize(450, 450)
        self.my_plan()

    def show_your_plan_page(self, data, from_signin=False):
        for i in range(self.login_ui.ui.register_gridLayout_2.count() - 1, -1, -1):
            items = self.login_ui.ui.register_gridLayout_2.itemAt(i).widget()
            if items:
                items.setVisible(False)
        for i in range(self.login_ui.ui.login_gridLayout.count() - 1, -1, -1):
            items = self.login_ui.ui.login_gridLayout.itemAt(i).widget()
            if items:
                items.setVisible(False)

        for i in range(self.login_ui.ui.your_plan_gridLayout.count() - 1, -1, -1):
            items = self.login_ui.ui.your_plan_gridLayout.itemAt(i).widget()
            if items:
                if items.objectName() != "register_progressBar":
                    items.setVisible(True)

        SignInUpdatePlan(PRODUCT_NAME, data.get("token")).update_local_expiry_and_client_data()
        user_plan_data = get_user_data_from_local()
        if user_plan_data:
            user_plan_data = convert_date_str_for_user_data(user_plan_data)
            self.login_ui.ui.purchase_plan_obj_2.setText(user_plan_data.get("plan", "N/A"))
            if user_plan_data.get("plan", "N/A") == 'Life Time Free Plan':
                self.login_ui.ui.purchase_now_button_2.setVisible(False)
            self.login_ui.ui.product_name.setText(str(user_plan_data.get("product", PRODUCT_NAME)).upper())
            self.login_ui.ui.expire_on_obj_2.setText(user_plan_data.get("expiry_date", "N/A"))
            self.login_ui.ui.activation_date_obj_2.setText(user_plan_data.get("created_on", "N/A"))
            self.login_ui.ui.hello_user_email_obj_2.setText(f"Welcome {user_plan_data.get('email', 'How are you today')}")
            if from_signin:
                self.login_ui.ui.login_from_your_plan.setVisible(False)

    def validate_password(self):
        if self.login_ui.ui.register_re_password_obj.text() not in [None, ""] or \
                self.login_ui.ui.register_password_obj.text() not in [None, ""]:
            if not len(self.login_ui.ui.register_password_obj.text()) > 3:
                self.login_ui.ui.register_error_message.setText("Password length is short!")
                self.login_ui.ui.register_button_obj.setEnabled(False)
            else:
                if self.login_ui.ui.register_password_obj.text() != self.login_ui.ui.register_re_password_obj.text():
                    self.login_ui.ui.register_error_message.setText("Password does not match!")
                    self.login_ui.ui.register_button_obj.setEnabled(False)
                else:
                    self.login_ui.ui.register_error_message.clear()
                    self.login_ui.ui.register_button_obj.setEnabled(True)
                    self.validate_email()

    def validate_email(self):
        if self.login_ui.ui.register_email_id_obj.text() not in [None, ""]:
            regex = '^[a-z0-9A-Z]+[\._]?[a-z0-9A-Z]+[@]\w+-?\w+[.]\w{2,3}$'
            if re.search(regex, self.login_ui.ui.register_email_id_obj.text()):
                self.login_ui.ui.register_error_message.clear()
                self.login_ui.ui.register_button_obj.setEnabled(True)
            else:
                self.login_ui.ui.register_error_message.setText("Enter valid email address!")
                self.login_ui.ui.register_button_obj.setEnabled(False)

    def validate_login_email(self):
        if self.login_ui.ui.login_email_obj.text() not in [None, ""]:
            regex = '^[a-z0-9A-Z]+[\._]?[a-z0-9A-Z]+[@]\w+-?\w+[.]\w{2,3}$'
            if re.search(regex, self.login_ui.ui.login_email_obj.text()):
                self.login_ui.ui.login_error_message_2.clear()
                if self.login_ui.ui.login_password_obj.text() != "":
                    self.login_ui.ui.login_from_login.setEnabled(True)
            else:
                self.login_ui.ui.login_error_message_2.setText("Enter valid email address!")
                self.login_ui.ui.login_from_login.setEnabled(False)

    def validate_login_password(self):
        if self.login_ui.ui.login_password_obj.text() != "":
            if self.login_ui.ui.login_email_obj.text() not in [None, ""]:
                regex = '^[a-z0-9A-Z]+[\._]?[a-z0-9A-Z]+[@]\w+-?\w+[.]\w{2,3}$'
                if re.search(regex, self.login_ui.ui.login_email_obj.text()):
                    self.login_ui.ui.login_error_message_2.clear()
                    self.login_ui.ui.login_from_login.setEnabled(True)
        else:
            self.login_ui.ui.login_error_message_2.setText("Password cannot be empty !")
            self.login_ui.ui.login_from_login.setEnabled(False)

    def after_login_show_your_plan(self):

        self.login_ui.ui.login_progressBar_2.setRange(0, 0)
        self.login_ui.ui.login_progressBar_2.setVisible(True)
        data = {"data": {"email": str(self.login_ui.ui.login_email_obj.text()).strip(),
                         "password": str(self.login_ui.ui.login_password_obj.text()).strip()}}
        self.login_thread = LoggingInThread(data)
        self.login_thread.change_value_login.connect(self.after_login_step_from_signin)
        self.login_thread.start()

    def redirect_to_warlord_softwares(self):
        warlord_soft_link = "https://warlordsoftwares.in/"
        webbrowser.open(warlord_soft_link)

    #  ==============================Login code ends==================================================


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
