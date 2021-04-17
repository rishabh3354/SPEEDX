import sys
import webbrowser
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QSettings, QUrl
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QStyle
from qtpy.QtGui import QDesktopServices
from speedx_threads import DummyDataThread, CpuThread, RamThread, NetSpeedThread
from src.account_threads import SaveLocalInToken, RefreshButtonThread
from src.accounts import ApplicationStartupTask, days_left, get_user_data_from_local, check_for_local_token
from style import theme_dict, button_dict
from ui_main import Ui_MainWindow
from utility import UtilsInfo

PRODUCT_NAME = "SPEEDX"
FREQUENCY_MAPPER = {1: 0.2, 2: 0.4, 3: 0.6, 4: 1, 5: 2, 6: 3}


class MainWindow(QMainWindow):
    def __init__(self):
        from ui_functions import UIFunctions
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        UIFunctions.uiDefinitions(self)
        self.settings = QSettings("warlordsoft", "speedx")
        self.net_frequency = 1
        self.cpu_frequency = 1
        self.ram_frequency = 1
        self.is_plan_active = True
        self.speed_unit = "MB/s | KB/s | B/s"
        self.temp_unit = "°C  (Celsius)"
        self.default_frequency()
        self.load_settings()
        self.ui.stackedWidget.setCurrentIndex(0)

        # home buttons
        self.ui.home_button.clicked.connect(self.credit_button_clicked)
        self.ui.monitor_button.clicked.connect(self.monitor_button_clicked)
        self.ui.setting_button.clicked.connect(self.setting_button_clicked)
        self.ui.account_button.clicked.connect(self.account_button_clicked)
        # App setting buttons
        self.ui.horizontalSlider.valueChanged.connect(self.change_frequency_net)
        self.ui.horizontalSlider_2.valueChanged.connect(self.change_frequency_cpu)
        self.ui.horizontalSlider_3.valueChanged.connect(self.change_frequency_ram)
        self.ui.comboBox_2.currentIndexChanged.connect(self.change_net_speed_unit)
        self.ui.comboBox_3.currentIndexChanged.connect(self.change_temp_unit)

        self.count = 1  # theme set counter
        self.setWindowFlags(Qt.FramelessWindowHint)

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

        # Accounts/About functionality new======================================================

        # init
        ApplicationStartupTask(PRODUCT_NAME).create_free_trial_offline()
        self.ui.error_message.clear()
        self.ui.error_message.setStyleSheet("color:red;")
        self.ui.account_progress_bar.setVisible(False)
        self.my_plan()

        # signal and slots
        self.ui.warlordsoft_button.clicked.connect(self.redirect_to_warlordsoft)
        self.ui.donate_button.clicked.connect(self.redirect_to_paypal_donation)
        self.ui.rate_button.clicked.connect(self.redirect_to_rate_snapstore)
        self.ui.feedback_button.clicked.connect(self.redirect_to_feedback_button)
        self.ui.purchase_licence.clicked.connect(self.purchase_licence)
        self.ui.refresh_account.clicked.connect(self.refresh_account)

        #  ======================Your plan functionality end=============================================

        if self.is_plan_active:
            self.load_cpu_data()
            self.load_ram_data()
            self.load_net_speed_data()
            self.show()
            self.load_annimation_data()
        else:
            self.load_cpu_data()
            self.load_ram_data()
            self.show()
            self.load_annimation_data()
            self.check_your_plan()
            self.ui.label_7.setText("Please Purchase To Unlock")
            self.ui.label_8.setText("Licence Expired !")
            self.ui.label_6.setText("0.0")

    def load_settings(self):
        if self.settings.contains("net_speed_unit"):
            self.speed_unit = self.settings.value("net_speed_unit")
            self.ui.comboBox_2.setCurrentText(self.speed_unit)
        if self.settings.contains("cpu_temp_unit"):
            self.temp_unit = self.settings.value("cpu_temp_unit")
            self.ui.comboBox_3.setCurrentText(self.temp_unit)
        if self.settings.contains("net_frequency"):
            self.net_frequency = FREQUENCY_MAPPER.get(int(self.settings.value("net_frequency")), 4)
            self.ui.horizontalSlider.setValue(int(self.settings.value("net_frequency")))
            self.ui.label_15.setText(str(FREQUENCY_MAPPER.get(int(self.settings.value("net_frequency")), "1")) + " Sec")
        if self.settings.contains("cpu_frequency"):
            self.cpu_frequency = FREQUENCY_MAPPER.get(int(self.settings.value("cpu_frequency")), 4)
            self.ui.horizontalSlider_2.setValue(int(self.settings.value("cpu_frequency")))
            self.ui.label_14.setText(str(FREQUENCY_MAPPER.get(int(self.settings.value("cpu_frequency")), "1")) + " Sec")
        if self.settings.contains("ram_frequency"):
            self.ram_frequency = FREQUENCY_MAPPER.get(int(self.settings.value("ram_frequency")), 4)
            self.ui.horizontalSlider_3.setValue(int(self.settings.value("ram_frequency")))
            self.ui.label_16.setText(str(FREQUENCY_MAPPER.get(int(self.settings.value("ram_frequency")), "1")) + " Sec")

    def save_settings(self):
        self.settings.setValue("net_speed_unit", self.ui.comboBox_2.currentText())
        self.settings.setValue("cpu_temp_unit", self.ui.comboBox_3.currentText())
        self.settings.setValue("net_frequency", self.ui.horizontalSlider.value())
        self.settings.setValue("cpu_frequency", self.ui.horizontalSlider_2.value())
        self.settings.setValue("ram_frequency", self.ui.horizontalSlider_3.value())

    def default_frequency(self):
        self.ui.horizontalSlider.setValue(4)
        self.ui.horizontalSlider_2.setValue(4)
        self.ui.horizontalSlider_3.setValue(4)
        self.ui.label_14.setText("1 Sec")
        self.ui.label_15.setText("1 Sec")
        self.ui.label_16.setText("1 Sec")

    def change_net_speed_unit(self):
        self.speed_unit = self.ui.comboBox_2.currentText()
        try:
            if self.is_plan_active:
                self.net_speed_thread.terminate()
                self.start_net_speed_thread()
        except Exception as e:
            pass

    def change_temp_unit(self):
        self.temp_unit = self.ui.comboBox_3.currentText()
        try:
            self.cpu_thread.terminate()
            self.start_cpu_thread()
        except Exception as e:
            pass

    def change_frequency_net(self):
        self.net_frequency = FREQUENCY_MAPPER.get(self.ui.horizontalSlider.value(), 4)
        self.ui.label_15.setText(str(self.net_frequency) + " Sec")
        try:
            self.net_speed_thread.terminate()
            self.start_net_speed_thread()
        except Exception as e:
            pass

    def change_frequency_cpu(self):
        self.cpu_frequency = FREQUENCY_MAPPER.get(self.ui.horizontalSlider_2.value(), 4)
        self.ui.label_14.setText(str(self.cpu_frequency) + " Sec")
        try:
            self.self.cpu_thread.terminate()
            self.start_cpu_thread()
        except Exception as e:
            pass

    def change_frequency_ram(self):
        self.ram_frequency = FREQUENCY_MAPPER.get(self.ui.horizontalSlider_3.value(), 4)
        self.ui.label_16.setText(str(self.ram_frequency) + " Sec")
        try:
            self.self.ram_thread.terminate()
            self.start_ram_thread()
        except Exception as e:
            pass

    def change_theme(self):
        if self.count == 5:
            self.count = 1
        self.ui.drop_shadow_frame.setStyleSheet(theme_dict.get(self.count))
        self.ui.pushButton.setStyleSheet(button_dict.get(self.count))
        self.ui.theme_button.setStyleSheet(button_dict.get(self.count))
        self.ui.my_plan_button.setStyleSheet(button_dict.get(self.count))
        self.ui.textBrowser.setStyleSheet(theme_dict.get(self.count))
        self.count += 1

    def closeEvent(self, event):
        self.save_settings()
        super().closeEvent(event)

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
        self.cpu_thread = CpuThread(self.cpu_frequency, self.temp_unit)
        self.cpu_thread.change_value.connect(self.setProgress_cpu)
        self.cpu_thread.start()

    def start_ram_thread(self):
        self.ram_thread = RamThread(self.ram_frequency)
        self.ram_thread.change_value.connect(self.setProgress_ram)
        self.ram_thread.start()

    def start_net_speed_thread(self):
        self.net_speed_thread = NetSpeedThread(self.net_frequency, self.speed_unit)
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
        self.ui.stackedWidget.setCurrentIndex(3)

    def monitor_button_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    def setting_button_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def account_button_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(2)

    """
        Account functionality :-
    """

    def redirect_to_warlordsoft(self):
        warlord_soft_link = "https://warlordsoftwares.in/"
        webbrowser.open(warlord_soft_link)

    def redirect_to_paypal_donation(self):
        paypal_donation_link = "https://www.paypal.com/paypalme/rishabh3354"
        webbrowser.open(paypal_donation_link)

    def redirect_to_rate_snapstore(self):
        QDesktopServices.openUrl(QUrl("snap://speedx"))

    def redirect_to_feedback_button(self):
        feedback_link = "https://warlordsoftwares.in/contact_us/"
        webbrowser.open(feedback_link)

    def purchase_licence(self):
        account_dict = get_user_data_from_local()
        if account_dict:
            account_id = str(account_dict.get("email")).split("@")[0]
            if account_id:
                warlord_soft_link = f"https://warlordsoftwares.in/warlord_soft/subscription/?product={PRODUCT_NAME}&account_id={account_id} "
            else:
                warlord_soft_link = f"https://warlordsoftwares.in/signup/"
            webbrowser.open(warlord_soft_link)
            data = dict()
            data["email"] = f"{account_id}@warlordsoft.in"
            data["password"] = f"{account_id}@warlordsoft.in"
            data["re_password"] = f"{account_id}@warlordsoft.in"
            self.save_token = SaveLocalInToken(data)
            self.save_token.start()

    def refresh_account(self):
        self.ui.error_message.clear()
        self.ui.account_progress_bar.setRange(0, 0)
        self.ui.account_progress_bar.setVisible(True)
        self.refresh_thread = RefreshButtonThread(PRODUCT_NAME)
        self.refresh_thread.change_value_refresh.connect(self.after_refresh)
        self.refresh_thread.start()

    def after_refresh(self, response_dict):
        if response_dict.get("status"):
            user_plan_data = get_user_data_from_local()
            if user_plan_data:
                self.logged_in_user_plan_page(user_plan_data)
        else:
            self.ui.error_message.setText(response_dict.get("message"))
        self.ui.account_progress_bar.setRange(0, 1)
        self.ui.account_progress_bar.setVisible(False)

    def my_plan(self):
        token = check_for_local_token()
        if token not in [None, ""]:
            user_plan_data = get_user_data_from_local()
            if user_plan_data:
                self.logged_in_user_plan_page(user_plan_data)
            else:
                user_plan_data = dict()
                user_plan_data['plan'] = "N/A"
                user_plan_data['expiry_date'] = "N/A"
                user_plan_data['email'] = "N/A"
                self.logged_in_user_plan_page(user_plan_data)
        else:
            user_plan_data = get_user_data_from_local()
            if user_plan_data:
                self.logged_in_user_plan_page(user_plan_data)

    def logged_in_user_plan_page(self, user_plan_data):
        account_email = user_plan_data.get('email')
        plan = user_plan_data.get("plan", "N/A")
        expiry_date = user_plan_data.get("expiry_date")
        if account_email:
            account_id = str(account_email).split("@")[0]
            self.ui.lineEdit_account_id.setText(account_id)
        else:
            self.ui.lineEdit_account_id.setText("N/A")
        if plan == "Free Trial":
            self.ui.lineEdit_plan.setText("Evaluation")
        elif plan == "Life Time Free Plan":
            self.ui.purchase_licence.setEnabled(False)
            self.ui.refresh_account.setEnabled(False)
            self.ui.lineEdit_plan.setText(plan)
        else:
            self.ui.lineEdit_plan.setText(plan)
        if expiry_date:
            if plan == "Life Time Free Plan":
                self.ui.lineEdit_expires_on.setText("Active")
            else:
                plan_days_left = days_left(expiry_date)
                if plan_days_left == "0 Day(s) Left":
                    self.ui.error_message.setText("Licence Expired! Purchase a new Licence")
                    self.ui.lineEdit_expires_on.setText(plan_days_left)
                    self.is_plan_active = False
                else:
                    self.is_plan_active = True
                    self.ui.lineEdit_expires_on.setText(plan_days_left)
        else:
            self.ui.lineEdit_expires_on.setText("N/A")

    def check_your_plan(self):
        if not self.is_plan_active:
            self.msg = QMessageBox()
            self.msg.setWindowFlag(QtCore.Qt.FramelessWindowHint)
            self.msg.setStyleSheet("background-color:rgb(48,48,48);color:white;")
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setText("Evaluation Period Ended!")
            self.msg.setInformativeText("Please purchase a Licence to Unlock this Feature (75% OFF for limited period)")
            close = self.msg.addButton(QMessageBox.Yes)
            purchase = self.msg.addButton(QMessageBox.Yes)
            purchase.setText('Purchase Licence')
            close.setText('Close')
            purchase.setIcon(QIcon(QApplication.style().standardIcon(QStyle.SP_DialogOkButton)))
            close.setIcon(QIcon(QApplication.style().standardIcon(QStyle.SP_BrowserStop)))
            self.msg.exec_()
            try:
                if self.msg.clickedButton() == purchase:
                    self.account_button_clicked()
                elif self.msg.clickedButton() == close:
                    pass
            except Exception as e:
                pass
            return False
        return True


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
