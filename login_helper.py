import datetime
import json
import os
import requests
from PyQt5 import QtWidgets
from PyQt5.QtCore import QStandardPaths, QProcessEnvironment
from PyQt5.QtWidgets import QWidget
from cryptography.fernet import Fernet
from login import Ui_LoginForm

APP_NAME = "SPEEDX"

ENCRYPT_APP_NAME = {
    "PDF2GO": "wsa_pd",
    "SPEEDX": "wsa_sp"
}
try:
    HOME = QProcessEnvironment().systemEnvironment().value('SNAP_REAL_HOME')
    if HOME != '':
        HOME += '/Documents'
    else:
        HOME = QStandardPaths.writableLocation(QStandardPaths.HomeLocation)
except Exception as e:
    HOME = QStandardPaths.writableLocation(QStandardPaths.HomeLocation)

STANDARD_PATH = f'{HOME}/.app_conf'
LOCAL_EXPIRY_PATH = f'{HOME}/.linux_conf'

# API FOR LOCAL/SERVER
SERVER = "https://warlordsoftwares.in/"
LOCAL = "http://localhost/"
DOMAIN = SERVER


class LoginPage(QWidget):
    def __init__(self, login_user=False):
        QWidget.__init__(self)
        self.login_user = login_user
        self.ui = Ui_LoginForm()
        self.ui.setupUi(self)
        self.setWindowTitle("Subscription")
        self.set_default_plan_page()

    def set_default_plan_page(self):
        self.ui.log_out_button_obj_2.setVisible(False)
        self.ui.register_error_message.setVisible(False)
        self.ui.register_button_obj.setEnabled(False)
        self.ui.register_progressBar.setVisible(False)
        self.ui.login_progressBar_2.setVisible(False)
        self.ui.home_button.setEnabled(False)
        self.ui.register_password_obj.setEchoMode(QtWidgets.QLineEdit.Password)
        self.ui.register_re_password_obj.setEchoMode(QtWidgets.QLineEdit.Password)
        self.ui.login_password_obj.setEchoMode(QtWidgets.QLineEdit.Password)

        for i in range(self.ui.register_gridLayout_2.count() - 1, -1, -1):
            items = self.ui.register_gridLayout_2.itemAt(i).widget()
            if items:
                items.setVisible(False)
        for i in range(self.ui.login_gridLayout.count() - 1, -1, -1):
            items = self.ui.login_gridLayout.itemAt(i).widget()
            if items:
                items.setVisible(False)
        self.resize(500, 660)


class ApplicationStartupTask:
    def __init__(self, app_name=APP_NAME):
        self.app_name = ENCRYPT_APP_NAME[app_name]
        self.today_date = datetime.datetime.now().date()
        self.expiry_folder = f'{LOCAL_EXPIRY_PATH}/{self.app_name}/local_conf'
        self.expiry_file = f'{LOCAL_EXPIRY_PATH}/{self.app_name}/local_conf/xpd.key'
        self.expiry_file_key = f'{LOCAL_EXPIRY_PATH}/{self.app_name}/local_conf/key.key'

    def create_free_trial_offline(self):
        expiry_date = self.check_for_expiry_date()
        context = dict()
        context["product"] = APP_NAME
        context["email"] = "Please Signin/Register to see your plan details."
        context["plan"] = "Free Trial"
        context["is_active"] = True
        context["expiry_date"] = str(self.today_date + datetime.timedelta(days=15))
        context["created_on"] = str(self.today_date)

        if not expiry_date:
            try:
                os.makedirs(self.expiry_folder, exist_ok=True)
                key, cipher_text = encrypt_user_data_in_local(str(context["expiry_date"]).encode("utf-8"))
                with open(self.expiry_file, "wb+") as file:
                    file.write(cipher_text)
                with open(self.expiry_file_key, "wb+") as file:
                    file.write(key)
            except Exception as error:
                pass

            # update client cache
            save_user_data_in_client_side({"data": context})

    def is_expired_product(self):
        try:
            local_expiry_date_str = self.check_for_expiry_date()
            if local_expiry_date_str in [None, ""]:
                return True
            local_expiry_date = datetime.datetime.strptime(local_expiry_date_str, '%Y-%m-%d').date()
            if self.today_date >= local_expiry_date:
                return True
            else:
                return False
        except Exception as e:
            return False

    def check_for_expiry_date(self):
        expiry_date = None
        try:
            expiry_file = open(self.expiry_file, "rb+")
            key_file = open(self.expiry_file_key, "rb+")
            expiry = expiry_file.read()
            key = key_file.read()
            expiry_date = decrypt_user_data_in_local(expiry, key)
            if isinstance(expiry_date, bytes):
                expiry_date = expiry_date.decode('utf-8')
            else:
                expiry_date = expiry_date
        except Exception as tef:
            pass

        return expiry_date

    def update_local_expiry_and_client_data(self, new_data):
        new_expiry_date = new_data.get('expiry_date', 'N/A')
        if isinstance(new_expiry_date, bytes):
            new_expiry_date = new_expiry_date
        else:
            new_expiry_date = new_expiry_date.encode('utf-8')
        try:
            os.makedirs(self.expiry_folder, exist_ok=True)
            key, cipher_text = encrypt_user_data_in_local(new_expiry_date)
            with open(self.expiry_file, "wb+") as file:
                file.write(cipher_text)
            with open(self.expiry_file_key, "wb+") as file:
                file.write(key)
            # updating local client data
            save_user_data_in_client_side({"data": new_data})
        except Exception as error:
            pass


class SignInUpdatePlan:
    def __init__(self, product_name, token):
        self.plan_api = DOMAIN + 'accounts_api/plan_dashboard/'
        self.product_name = product_name
        if isinstance(token, bytes):
            self.token = token.decode('utf-8')
        else:
            self.token = token

    def get_user_paid_plan(self):
        context = dict()
        context["status"] = False
        context["message"] = ""
        context["data"] = None
        try:
            headers = {'Authorization': f'Token {self.token}'}
            response = requests.post(self.plan_api, data={'product': self.product_name}, headers=headers)
            if response.status_code in [200, 201]:
                message = json.loads(response.text)
                if message.get("status"):
                    context["status"] = True
                    context["message"] = message.get("message")
                    context["data"] = message.get("data")
                else:
                    context["status"] = False
                    context["message"] = message.get("message")
                    context["data"] = message.get("data")
            else:
                context["status"] = False
                context["message"] = "Internal Server Error"
        except Exception as e:
            context["status"] = False
            context["message"] = "Something went wrong"

        return context

    def update_local_expiry_and_client_data(self):
        try:
            response_data = self.get_user_paid_plan()
            user_email = response_data.get("data", {}).get("data", {}).get("email")
            if response_data.get("data", {}).get("status"):
                paid_plan_data = response_data.get("data")
                ApplicationStartupTask().update_local_expiry_and_client_data(paid_plan_data.get("data"))
            update_email_on_client_data(user_email)
        except Exception as e:
            pass


def update_email_on_client_data(email):
    user_data = get_user_data_from_local()
    if user_data:
        user_data["email"] = email
    save_user_data_in_client_side({"data": user_data})


def encrypt_user_data_in_local(normal_data_str):
    key = Fernet.generate_key()
    cipher_suite = Fernet(key)
    cipher_text = cipher_suite.encrypt(normal_data_str)

    return key, cipher_text


def decrypt_user_data_in_local(cipher_data_str, key):
    cipher_suite = Fernet(key)
    plain_text = cipher_suite.decrypt(cipher_data_str)

    return plain_text


def save_token_in_client_side(token):
    file_name = None
    token = token.encode('utf-8')

    try:
        app_name = ENCRYPT_APP_NAME[APP_NAME]
        os.makedirs(f'{STANDARD_PATH}/{app_name}/token', exist_ok=True)
        file_name = f'{STANDARD_PATH}/{app_name}/token/token.key'
        key_name = f'{STANDARD_PATH}/{app_name}/token/key.key'
        key, cipher_text = encrypt_user_data_in_local(token)
        with open(file_name, "wb+") as file:
            file.write(cipher_text)
        with open(key_name, "wb+") as file:
            file.write(key)
    except OSError as error:
        pass

    return file_name


def check_for_local_token():
    plain_text = None
    try:
        app_name = ENCRYPT_APP_NAME[APP_NAME]
        token_file = open(f'{STANDARD_PATH}/{app_name}/token/token.key', "rb+")
        token_key_file = open(f'{STANDARD_PATH}/{app_name}/token/key.key', "rb+")
        token = token_file.read()
        key = token_key_file.read()
        plain_text = decrypt_user_data_in_local(token, key)
        if isinstance(plain_text, bytes):
            plain_text = plain_text.decode('utf-8')
        else:
            plain_text = plain_text
    except OSError as error:
        pass
    except Exception as tef:
        pass

    return plain_text


def save_user_data_in_client_side(data_dict):
    try:
        app_name = ENCRYPT_APP_NAME[APP_NAME]
        os.makedirs(f'{STANDARD_PATH}/{app_name}/user_data', exist_ok=True)
        file_name = f'{STANDARD_PATH}/{app_name}/user_data/user_data.json'
        key_file = f'{STANDARD_PATH}/{app_name}/user_data/key.key'
        data = json.dumps(data_dict.get("data", {})).encode('utf-8')
        key, cipher_text = encrypt_user_data_in_local(data)
        with open(file_name, "wb+") as file:
            file.write(cipher_text)
        with open(key_file, "wb+") as file:
            file.write(key)
    except Exception as ee:
        pass


def delete_user_data_from_local():
    app_name = ENCRYPT_APP_NAME[APP_NAME]
    token_path = f"{STANDARD_PATH}/{app_name}/token/token.key"
    token_key_path = f"{STANDARD_PATH}/{app_name}/token/key.key"
    try:
        os.remove(token_path)
        os.remove(token_key_path)
    except OSError as e:
        return False

    return True


def get_user_data_from_local():
    plain_text = None
    try:
        app_name = ENCRYPT_APP_NAME[APP_NAME]
        user_data_file = open(f'{STANDARD_PATH}/{app_name}/user_data/user_data.json', "rb+")
        user_key_file = open(f'{STANDARD_PATH}/{app_name}/user_data/key.key', "rb+")
        data = user_data_file.read()
        key = user_key_file.read()
        plain_text = decrypt_user_data_in_local(data, key)
        plain_text = json.loads(plain_text)
    except Exception as error:
        pass
    return plain_text


def get_login_and_save_token(data):
    login_api = DOMAIN + "accounts_api/login_api/"
    context = dict()
    context["status"] = False
    context["token"] = ""
    context["token_path"] = ""
    context["message"] = ""
    try:
        if check_internet_connection():
            response = requests.post(login_api, data=data.get("data", {}))
            if response.status_code in [200, 201]:
                message = json.loads(response.text)
                if message["status"]:
                    context["token"] = json.loads(message['message']).get("token", "")
                    context["token_path"] = save_token_in_client_side(context["token"])
                    context["status"] = True
                    context["message"] = "Login success"
                else:
                    context["status"] = False
                    context["message"] = message.get("message")

            else:
                context["status"] = False
                context["message"] = "Internal Server Error"
        else:
            context["message"] = "Please check your internet connection"
    except Exception as e:
        context["status"] = False
        context["message"] = "Login Failed"

    return context


def get_signup_user(data):
    signup_api = DOMAIN + 'accounts_api/signup_api/'
    context = dict()
    context["status"] = False
    context["message"] = ""
    context["data"] = data

    if data["password"] == data["re_password"]:
        if check_internet_connection():
            try:
                response = requests.post(signup_api, data=data)
                if response.status_code in [200, 201]:
                    message = json.loads(response.text)
                    if message.get("status"):
                        context["status"] = True
                        context["message"] = message.get("message")
                    else:
                        context["status"] = False
                        context["message"] = message.get("message")
                else:
                    context["status"] = False
                    context["message"] = "Internal Server Error"
            except Exception as e:
                context["status"] = False
                context["message"] = "Something went wrong"
        else:
            context["message"] = "Please check your internet connection"
    else:
        context["message"] = "Password does not match!"

    return context


def plan_dashboard_api(data):
    dashboard_api = DOMAIN + 'accounts_api/plan_dashboard/'
    context = dict()
    context["status"] = False
    context["message"] = ""
    if isinstance(data.get("token"), bytes):
        context["token"] = data.get("token").decode('utf-8')
    else:
        context["token"] = data.get("token")
    context["data"] = None

    try:
        headers = {'Authorization': f'Token {context["token"]}'}
        response = requests.post(dashboard_api, data=data, headers=headers)

        if response.status_code in [200, 201]:
            message = json.loads(response.text)
            if message.get("status"):
                context["status"] = True
                context["message"] = message.get("message")
                context["data"] = message.get("data")
            else:
                context["status"] = False
                context["message"] = message.get("message")
                context["data"] = message.get("data")
        else:
            context["status"] = False
            context["message"] = "Internal Server Error"
    except Exception as e:
        context["status"] = False
        context["message"] = "Something went wrong"

    return context


def login_from_token_local(token):
    login_api = DOMAIN + "accounts_api/get_user_from_token/"
    context = dict()
    context["status"] = False
    context["message"] = "Something went wrong!"
    context["user_id"] = None

    try:
        if check_internet_connection():
            response = requests.post(login_api, data={"token": token})
            if response.status_code in [200, 201]:
                message = json.loads(response.text)
                if message["status"]:
                    context["user_id"] = json.loads(message['message']).get("user_id")
                    context["status"] = True
                    context["message"] = "Successfully got user with this token!"
                else:
                    context["status"] = False
                    context["message"] = message.get("message")

            else:
                context["status"] = False
                context["message"] = "Internal Server Error"
        else:
            context["status"] = False
            context["message"] = "Please check your internet connection"
    except Exception as e:
        context["status"] = False
        context["message"] = "Unable to get userid from token"

    return context


def convert_date_str_for_user_data(user_data):
    beautify_data = user_data
    try:
        if user_data:
            expiry_date = user_data.get("expiry_date")
            created_on = user_data.get("created_on")
            plan = user_data.get("plan")
            if plan == "Life Time Free Plan":
                user_data["expiry_date"] = "Life Time"
            elif expiry_date:
                user_data["expiry_date"] = convert_date_str(expiry_date)
            if created_on:
                user_data["created_on"] = convert_date_str(created_on)
    except Exception as e:
        return beautify_data

    return user_data


def check_internet_connection():
    try:
        requests.get("http://www.google.com", timeout=5)
        return True
    except (requests.ConnectionError, requests.Timeout):
        return False


def convert_date_str(date_str):
    date = "-/-/-"
    date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
    date = datetime.datetime.strftime(date_obj, "%d %b %Y")

    return date


def your_plan_button_connects(self):
    # signin
    self.login_ui.ui.login_from_login.clicked.connect(self.after_login_show_your_plan)
    # signout
    self.login_ui.ui.log_out_button_obj_2.clicked.connect(self.logout_function)
    # purchase now
    self.login_ui.ui.purchase_now_button_2.clicked.connect(self.purchase_now)
    # refresh button
    self.login_ui.ui.refresh_button.clicked.connect(self.refresh_button_function)
    # validation
    self.login_ui.ui.register_re_password_obj.textChanged.connect(self.validate_password)
    self.login_ui.ui.register_password_obj.textChanged.connect(self.validate_password)
    self.login_ui.ui.register_email_id_obj.textChanged.connect(self.validate_email)
    self.login_ui.ui.login_email_obj.textChanged.connect(self.validate_login_email)
    self.login_ui.ui.register_button_obj.clicked.connect(self.register_user)
    self.login_ui.ui.login_from_your_plan.clicked.connect(self.sign_in_user)
    self.login_ui.ui.already_registered_signin.clicked.connect(self.sign_in_user)
    self.login_ui.ui.dont_have_account_register.clicked.connect(self.show_register_page)
    self.login_ui.ui.home_button.clicked.connect(self.show_home_page)
    self.login_ui.ui.warlord_software_button.clicked.connect(self.redirect_to_warlord_softwares)
