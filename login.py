# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created by: PyQt5 UI code generator 5.14.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_LoginForm(object):
    def setupUi(self, LoginForm):
        LoginForm.setObjectName("LoginForm")
        LoginForm.resize(545, 1212)
        font = QtGui.QFont()
        font.setFamily("Sans")
        LoginForm.setFont(font)
        LoginForm.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(6, 60, 89, 1), stop:0.521368 rgba(6, 60, 89, 1));\n"
"border-radius: 10px;")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(LoginForm)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 0, 1, 1, 1)
        self.home_button = QtWidgets.QPushButton(LoginForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.home_button.sizePolicy().hasHeightForWidth())
        self.home_button.setSizePolicy(sizePolicy)
        self.home_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.home_button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.home_button.setStyleSheet("QPushButton {\n"
"    padding: 5px;\n"
"    border-radius: 10px;\n"
"    background-color: rgb(27, 154, 171);\n"
"    color: white;\n"
"}\n"
"QPushButton:hover {    \n"
"    background-color: rgba(50, 168, 50, 1);\n"
"}\n"
"QPushButton:disabled {    \n"
"    background-color: rgb(109, 117, 130);\n"
"}")
        self.home_button.setObjectName("home_button")
        self.gridLayout_2.addWidget(self.home_button, 0, 0, 1, 1)
        self.warlord_software_button = QtWidgets.QPushButton(LoginForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.warlord_software_button.sizePolicy().hasHeightForWidth())
        self.warlord_software_button.setSizePolicy(sizePolicy)
        self.warlord_software_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.warlord_software_button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.warlord_software_button.setStyleSheet("QPushButton {\n"
"    padding: 5px;\n"
"    border-radius: 10px;\n"
"    background-color: rgb(27, 154, 171);\n"
"    color: white;\n"
"}\n"
"QPushButton:hover {    \n"
"    background-color: rgba(50, 168, 50, 1);\n"
"}\n"
"QPushButton:disabled {    \n"
"    background-color: rgb(109, 117, 130);\n"
"}")
        self.warlord_software_button.setObjectName("warlord_software_button")
        self.gridLayout_2.addWidget(self.warlord_software_button, 0, 2, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout_2)
        self.your_plan_gridLayout = QtWidgets.QGridLayout()
        self.your_plan_gridLayout.setObjectName("your_plan_gridLayout")
        self.purchase_plan_obj_2 = QtWidgets.QLabel(LoginForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.purchase_plan_obj_2.sizePolicy().hasHeightForWidth())
        self.purchase_plan_obj_2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setBold(True)
        font.setWeight(75)
        self.purchase_plan_obj_2.setFont(font)
        self.purchase_plan_obj_2.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.purchase_plan_obj_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.purchase_plan_obj_2.setStyleSheet("color: rgb(238, 238, 236);\n"
"font-weight:600;\n"
"qproperty-alignment: AlignCenter;\n"
"padding: 5px;\n"
"border: 1px solid white;\n"
"    border-radius: 0px;\n"
"\n"
"")
        self.purchase_plan_obj_2.setObjectName("purchase_plan_obj_2")
        self.your_plan_gridLayout.addWidget(self.purchase_plan_obj_2, 4, 2, 1, 1)
        self.expire_on_obj_2 = QtWidgets.QLabel(LoginForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.expire_on_obj_2.sizePolicy().hasHeightForWidth())
        self.expire_on_obj_2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setBold(True)
        font.setWeight(75)
        self.expire_on_obj_2.setFont(font)
        self.expire_on_obj_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.expire_on_obj_2.setStyleSheet("color: rgb(238, 238, 236);\n"
"font-weight:600;\n"
"qproperty-alignment: AlignCenter;\n"
"padding: 5px;\n"
"border: 1px solid white;\n"
"    border-radius: 0px;\n"
"\n"
"")
        self.expire_on_obj_2.setObjectName("expire_on_obj_2")
        self.your_plan_gridLayout.addWidget(self.expire_on_obj_2, 7, 2, 1, 1)
        self.hello_user_email_obj_2 = QtWidgets.QLabel(LoginForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.hello_user_email_obj_2.sizePolicy().hasHeightForWidth())
        self.hello_user_email_obj_2.setSizePolicy(sizePolicy)
        self.hello_user_email_obj_2.setStyleSheet("qproperty-alignment: AlignCenter;\n"
"color: rgb(138, 226, 52);\n"
"font-weight:600;\n"
"padding: 5px;\n"
"")
        self.hello_user_email_obj_2.setObjectName("hello_user_email_obj_2")
        self.your_plan_gridLayout.addWidget(self.hello_user_email_obj_2, 1, 0, 1, 3)
        self.refresh_button = QtWidgets.QPushButton(LoginForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.refresh_button.sizePolicy().hasHeightForWidth())
        self.refresh_button.setSizePolicy(sizePolicy)
        self.refresh_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.refresh_button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.refresh_button.setStyleSheet("QPushButton {\n"
"    padding: 5px;\n"
"    background-color: rgba(243, 196, 54, 1);\n"
"    border-radius: 10px;\n"
"color: white;\n"
"}\n"
"QPushButton:hover {    \n"
"    background-color: rgba(253, 191, 2, 1);\n"
"\n"
"}")
        self.refresh_button.setObjectName("refresh_button")
        self.your_plan_gridLayout.addWidget(self.refresh_button, 12, 0, 1, 3)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.your_plan_gridLayout.addItem(spacerItem1, 13, 0, 1, 3)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.your_plan_gridLayout.addItem(spacerItem2, 10, 0, 1, 3)
        self.your_plan_2 = QtWidgets.QLabel(LoginForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.your_plan_2.sizePolicy().hasHeightForWidth())
        self.your_plan_2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Sans")
        self.your_plan_2.setFont(font)
        self.your_plan_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.your_plan_2.setStyleSheet("")
        self.your_plan_2.setObjectName("your_plan_2")
        self.your_plan_gridLayout.addWidget(self.your_plan_2, 0, 0, 1, 3)
        self.purchase_now_button_2 = QtWidgets.QPushButton(LoginForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.purchase_now_button_2.sizePolicy().hasHeightForWidth())
        self.purchase_now_button_2.setSizePolicy(sizePolicy)
        self.purchase_now_button_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.purchase_now_button_2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.purchase_now_button_2.setStyleSheet("QPushButton {\n"
"    padding: 15px;\n"
"    background-color: rgba(216, 69, 31, 1);\n"
"    border-radius: 20px;\n"
"    color: white;\n"
"    font-weight: bold;\n"
"}\n"
"QPushButton:hover {    \n"
"    background-color: rgba(255, 52, 0, 1);\n"
"\n"
"}")
        self.purchase_now_button_2.setObjectName("purchase_now_button_2")
        self.your_plan_gridLayout.addWidget(self.purchase_now_button_2, 11, 0, 1, 3)
        self.log_out_button_obj_2 = QtWidgets.QPushButton(LoginForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.log_out_button_obj_2.sizePolicy().hasHeightForWidth())
        self.log_out_button_obj_2.setSizePolicy(sizePolicy)
        self.log_out_button_obj_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.log_out_button_obj_2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.log_out_button_obj_2.setStyleSheet("QPushButton {\n"
"    padding: 5px;\n"
"    background-color: rgb(27, 154, 171);\n"
"    border-radius: 10px;\n"
"color: white;\n"
"    font-weight: bold;\n"
"\n"
"}\n"
"QPushButton:hover {    \n"
"    background-color: rgba(50, 168, 50, 1);\n"
"\n"
"}")
        self.log_out_button_obj_2.setObjectName("log_out_button_obj_2")
        self.your_plan_gridLayout.addWidget(self.log_out_button_obj_2, 18, 0, 1, 3)
        self.activation_date_obj_2 = QtWidgets.QLabel(LoginForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.activation_date_obj_2.sizePolicy().hasHeightForWidth())
        self.activation_date_obj_2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setBold(True)
        font.setWeight(75)
        self.activation_date_obj_2.setFont(font)
        self.activation_date_obj_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.activation_date_obj_2.setStyleSheet("color: rgb(238, 238, 236);\n"
"font-weight:600;\n"
"qproperty-alignment: AlignCenter;\n"
"padding: 5px;\n"
"border: 1px solid white;\n"
"    border-radius: 0px;\n"
"\n"
"")
        self.activation_date_obj_2.setObjectName("activation_date_obj_2")
        self.your_plan_gridLayout.addWidget(self.activation_date_obj_2, 6, 2, 1, 1)
        self.login_from_your_plan = QtWidgets.QPushButton(LoginForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.login_from_your_plan.sizePolicy().hasHeightForWidth())
        self.login_from_your_plan.setSizePolicy(sizePolicy)
        self.login_from_your_plan.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.login_from_your_plan.setStyleSheet("QPushButton {\n"
"    padding: 10px;\n"
"    background-color: rgba(50, 168, 50, 1);\n"
"    border-radius: 15px;\n"
"color: white;\n"
"    font-weight: bold;\n"
"\n"
"}\n"
"QPushButton:hover {    \n"
"    background-color: rgb(27, 154, 171);\n"
"\n"
"}")
        self.login_from_your_plan.setAutoDefault(False)
        self.login_from_your_plan.setObjectName("login_from_your_plan")
        self.your_plan_gridLayout.addWidget(self.login_from_your_plan, 16, 0, 1, 3)
        self.refresh_error = QtWidgets.QLabel(LoginForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.refresh_error.sizePolicy().hasHeightForWidth())
        self.refresh_error.setSizePolicy(sizePolicy)
        self.refresh_error.setAutoFillBackground(False)
        self.refresh_error.setStyleSheet("color: rgb(239, 41, 41);\n"
"qproperty-alignment: AlignCenter;\n"
"font-weight: bold;\n"
"")
        self.refresh_error.setObjectName("refresh_error")
        self.your_plan_gridLayout.addWidget(self.refresh_error, 14, 0, 1, 3)
        self.label_10 = QtWidgets.QLabel(LoginForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy)
        self.label_10.setStyleSheet("\n"
"    padding: 5px;\n"
"    background-color: rgba(6, 60, 89, 1);\n"
"border: 1px solid white;\n"
"    border-radius: 0px;")
        self.label_10.setObjectName("label_10")
        self.your_plan_gridLayout.addWidget(self.label_10, 4, 0, 1, 2)
        self.label_9 = QtWidgets.QLabel(LoginForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy)
        self.label_9.setStyleSheet("\n"
"    padding: 5px;\n"
"    background-color: rgba(6, 60, 89, 1);\n"
"border: 1px solid white;\n"
"    border-radius: 0px;")
        self.label_9.setObjectName("label_9")
        self.your_plan_gridLayout.addWidget(self.label_9, 6, 0, 1, 2)
        self.label_8 = QtWidgets.QLabel(LoginForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)
        self.label_8.setStyleSheet("\n"
"    padding: 5px;\n"
"    background-color: rgba(6, 60, 89, 1);\n"
"border: 1px solid white;\n"
"    border-radius: 0px;")
        self.label_8.setObjectName("label_8")
        self.your_plan_gridLayout.addWidget(self.label_8, 7, 0, 1, 2)
        self.product_name = QtWidgets.QLabel(LoginForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.product_name.sizePolicy().hasHeightForWidth())
        self.product_name.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setBold(True)
        font.setWeight(75)
        self.product_name.setFont(font)
        self.product_name.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.product_name.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.product_name.setStyleSheet("color: rgb(238, 238, 236);\n"
"font-weight:600;\n"
"qproperty-alignment: AlignCenter;\n"
"padding: 5px;\n"
"    border: 1px solid white;\n"
"    border-radius: 0px;\n"
"\n"
"")
        self.product_name.setObjectName("product_name")
        self.your_plan_gridLayout.addWidget(self.product_name, 3, 2, 1, 1)
        self.label_14 = QtWidgets.QLabel(LoginForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_14.sizePolicy().hasHeightForWidth())
        self.label_14.setSizePolicy(sizePolicy)
        self.label_14.setStyleSheet("\n"
"    padding: 5px;\n"
"    background-color: rgba(6, 60, 89, 1);\n"
"    border: 1px solid white;\n"
"    border-radius: 0px;")
        self.label_14.setObjectName("label_14")
        self.your_plan_gridLayout.addWidget(self.label_14, 3, 0, 1, 2)
        self.verticalLayout_2.addLayout(self.your_plan_gridLayout)
        self.register_gridLayout_2 = QtWidgets.QGridLayout()
        self.register_gridLayout_2.setObjectName("register_gridLayout_2")
        self.label_3 = QtWidgets.QLabel(LoginForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setStyleSheet("\n"
"    padding: 5px;\n"
"    background-color: rgba(6, 60, 89, 1);\n"
"")
        self.label_3.setObjectName("label_3")
        self.register_gridLayout_2.addWidget(self.label_3, 3, 0, 1, 1)
        self.register_password_obj = QtWidgets.QLineEdit(LoginForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.register_password_obj.sizePolicy().hasHeightForWidth())
        self.register_password_obj.setSizePolicy(sizePolicy)
        self.register_password_obj.setStyleSheet("QLineEdit {\n"
"    padding: 5px;\n"
"    color: rgb(40, 40, 40);\n"
"    background-color: rgb(60, 231, 195);\n"
"    font-weight: bold;\n"
"    border-radius: 12px;\n"
"}\n"
"")
        self.register_password_obj.setObjectName("register_password_obj")
        self.register_gridLayout_2.addWidget(self.register_password_obj, 4, 1, 1, 2)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.register_gridLayout_2.addItem(spacerItem3, 0, 0, 1, 3)
        self.label_11 = QtWidgets.QLabel(LoginForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_11.sizePolicy().hasHeightForWidth())
        self.label_11.setSizePolicy(sizePolicy)
        self.label_11.setStyleSheet("\n"
"    padding: 5px;\n"
"    background-color: rgba(6, 60, 89, 1);\n"
"")
        self.label_11.setObjectName("label_11")
        self.register_gridLayout_2.addWidget(self.label_11, 4, 0, 1, 1)
        self.register_progressBar = QtWidgets.QProgressBar(LoginForm)
        self.register_progressBar.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.register_progressBar.sizePolicy().hasHeightForWidth())
        self.register_progressBar.setSizePolicy(sizePolicy)
        self.register_progressBar.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.register_progressBar.setAutoFillBackground(False)
        self.register_progressBar.setStyleSheet("QProgressBar:horizontal {\n"
"border: 1px solid gray;\n"
"border-radius: 10px;\n"
"background: rgba(6, 60, 89, 1);\n"
"padding: 1px;\n"
"\n"
"}\n"
"QProgressBar::chunk:horizontal {\n"
"background: qlineargradient(x1: 0, y1: 0.5, x2: 1, y2: 0.5, stop: 0 rgb(60, 231, 195), stop: 1 rgb(60, 231, 195));\n"
"border-radius: 10px;\n"
"\n"
"}\n"
"")
        self.register_progressBar.setMinimum(0)
        self.register_progressBar.setMaximum(100)
        self.register_progressBar.setProperty("value", 0)
        self.register_progressBar.setObjectName("register_progressBar")
        self.register_gridLayout_2.addWidget(self.register_progressBar, 7, 0, 1, 3)
        self.register_re_password_obj = QtWidgets.QLineEdit(LoginForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.register_re_password_obj.sizePolicy().hasHeightForWidth())
        self.register_re_password_obj.setSizePolicy(sizePolicy)
        self.register_re_password_obj.setStyleSheet("QLineEdit {\n"
"    padding: 5px;\n"
"    color: rgb(40, 40, 40);\n"
"    background-color: rgb(60, 231, 195);\n"
"    font-weight: bold;\n"
"    border-radius: 12px;\n"
"}\n"
"")
        self.register_re_password_obj.setObjectName("register_re_password_obj")
        self.register_gridLayout_2.addWidget(self.register_re_password_obj, 5, 1, 1, 2)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.register_gridLayout_2.addItem(spacerItem4, 8, 0, 1, 3)
        self.label_12 = QtWidgets.QLabel(LoginForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_12.sizePolicy().hasHeightForWidth())
        self.label_12.setSizePolicy(sizePolicy)
        self.label_12.setStyleSheet("\n"
"    padding: 5px;\n"
"    background-color: rgba(6, 60, 89, 1);\n"
"")
        self.label_12.setObjectName("label_12")
        self.register_gridLayout_2.addWidget(self.label_12, 5, 0, 1, 1)
        self.already_registered_signin = QtWidgets.QPushButton(LoginForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.already_registered_signin.sizePolicy().hasHeightForWidth())
        self.already_registered_signin.setSizePolicy(sizePolicy)
        self.already_registered_signin.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.already_registered_signin.setFocusPolicy(QtCore.Qt.NoFocus)
        self.already_registered_signin.setStyleSheet("QPushButton {\n"
"    padding: 5px;\n"
"    background-color: rgba(50, 168, 50, 1);\n"
"    border-radius: 10px;\n"
"color: white;\n"
"}\n"
"QPushButton:hover {    \n"
"    background-color: rgb(27, 154, 171);\n"
"\n"
"}")
        self.already_registered_signin.setObjectName("already_registered_signin")
        self.register_gridLayout_2.addWidget(self.already_registered_signin, 12, 0, 1, 3)
        self.register_email_id_obj = QtWidgets.QLineEdit(LoginForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.register_email_id_obj.sizePolicy().hasHeightForWidth())
        self.register_email_id_obj.setSizePolicy(sizePolicy)
        self.register_email_id_obj.setStyleSheet("QLineEdit {\n"
"    padding: 5px;\n"
"    color: rgb(40, 40, 40);\n"
"    background-color: rgb(60, 231, 195);\n"
"    border-radius: 12px;\n"
"    font-weight: bold;\n"
"}\n"
"")
        self.register_email_id_obj.setObjectName("register_email_id_obj")
        self.register_gridLayout_2.addWidget(self.register_email_id_obj, 3, 1, 1, 2)
        self.register_button_obj = QtWidgets.QPushButton(LoginForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.register_button_obj.sizePolicy().hasHeightForWidth())
        self.register_button_obj.setSizePolicy(sizePolicy)
        self.register_button_obj.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.register_button_obj.setStyleSheet("QPushButton {\n"
"    padding: 10px;\n"
"    background-color: rgba(50, 168, 50, 1);\n"
"    border-radius: 10px;\n"
"color: white;\n"
"    font-weight: bold;\n"
"\n"
"}\n"
"QPushButton:hover {    \n"
"    background-color: rgb(27, 154, 171);\n"
"\n"
"}\n"
"\n"
"QPushButton:disabled {    \n"
"    background-color: rgb(109, 117, 130);\n"
"\n"
"}")
        self.register_button_obj.setAutoDefault(True)
        self.register_button_obj.setObjectName("register_button_obj")
        self.register_gridLayout_2.addWidget(self.register_button_obj, 11, 0, 1, 3)
        self.register_obj = QtWidgets.QLabel(LoginForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.register_obj.sizePolicy().hasHeightForWidth())
        self.register_obj.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Sans")
        self.register_obj.setFont(font)
        self.register_obj.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.register_obj.setStyleSheet("")
        self.register_obj.setObjectName("register_obj")
        self.register_gridLayout_2.addWidget(self.register_obj, 1, 0, 1, 3)
        self.register_error_message = QtWidgets.QLabel(LoginForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.register_error_message.sizePolicy().hasHeightForWidth())
        self.register_error_message.setSizePolicy(sizePolicy)
        self.register_error_message.setAutoFillBackground(False)
        self.register_error_message.setStyleSheet("color: rgb(239, 41, 41);\n"
"qproperty-alignment: AlignCenter;\n"
"font-weight: bold;\n"
"")
        self.register_error_message.setObjectName("register_error_message")
        self.register_gridLayout_2.addWidget(self.register_error_message, 6, 1, 1, 1)
        self.verticalLayout_2.addLayout(self.register_gridLayout_2)
        self.login_gridLayout = QtWidgets.QGridLayout()
        self.login_gridLayout.setObjectName("login_gridLayout")
        self.login_obj = QtWidgets.QLabel(LoginForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.login_obj.sizePolicy().hasHeightForWidth())
        self.login_obj.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Sans")
        self.login_obj.setFont(font)
        self.login_obj.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.login_obj.setStyleSheet("")
        self.login_obj.setObjectName("login_obj")
        self.login_gridLayout.addWidget(self.login_obj, 1, 0, 1, 3)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.login_gridLayout.addItem(spacerItem5, 0, 0, 1, 3)
        self.label_4 = QtWidgets.QLabel(LoginForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setStyleSheet("\n"
"    padding: 5px;\n"
"    background-color: rgba(6, 60, 89, 1);\n"
"")
        self.label_4.setObjectName("label_4")
        self.login_gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.dont_have_account_register = QtWidgets.QPushButton(LoginForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dont_have_account_register.sizePolicy().hasHeightForWidth())
        self.dont_have_account_register.setSizePolicy(sizePolicy)
        self.dont_have_account_register.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.dont_have_account_register.setFocusPolicy(QtCore.Qt.NoFocus)
        self.dont_have_account_register.setStyleSheet("QPushButton {\n"
"    padding: 5px;\n"
"    background-color: rgba(50, 168, 50, 1);\n"
"    border-radius: 10px;\n"
"color: white;\n"
"}\n"
"QPushButton:hover {    \n"
"    background-color: rgb(27, 154, 171);\n"
"\n"
"}")
        self.dont_have_account_register.setObjectName("dont_have_account_register")
        self.login_gridLayout.addWidget(self.dont_have_account_register, 9, 0, 1, 3)
        self.login_password_obj = QtWidgets.QLineEdit(LoginForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.login_password_obj.sizePolicy().hasHeightForWidth())
        self.login_password_obj.setSizePolicy(sizePolicy)
        self.login_password_obj.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.login_password_obj.setStyleSheet("QLineEdit {\n"
"    padding: 5px;\n"
"    color: rgb(40, 40, 40);\n"
"    background-color: rgb(60, 231, 195);\n"
"    font-weight: bold;\n"
"    border-radius: 12px;\n"
"}\n"
"")
        self.login_password_obj.setObjectName("login_password_obj")
        self.login_gridLayout.addWidget(self.login_password_obj, 4, 1, 1, 2)
        self.login_from_login = QtWidgets.QPushButton(LoginForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.login_from_login.sizePolicy().hasHeightForWidth())
        self.login_from_login.setSizePolicy(sizePolicy)
        self.login_from_login.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.login_from_login.setStyleSheet("QPushButton {\n"
"    padding: 10px;\n"
"    background-color: rgba(50, 168, 50, 1);\n"
"    border-radius: 10px;\n"
"color: white;\n"
"    font-weight: bold;\n"
"\n"
"}\n"
"QPushButton:hover {    \n"
"    background-color: rgb(27, 154, 171);\n"
"\n"
"}\n"
"QPushButton:disabled {    \n"
"    background-color: rgb(109, 117, 130);\n"
"\n"
"}")
        self.login_from_login.setAutoDefault(False)
        self.login_from_login.setDefault(True)
        self.login_from_login.setObjectName("login_from_login")
        self.login_gridLayout.addWidget(self.login_from_login, 8, 0, 1, 3)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.login_gridLayout.addItem(spacerItem6, 7, 0, 1, 3)
        self.login_email_obj = QtWidgets.QLineEdit(LoginForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.login_email_obj.sizePolicy().hasHeightForWidth())
        self.login_email_obj.setSizePolicy(sizePolicy)
        self.login_email_obj.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.login_email_obj.setStyleSheet("QLineEdit {\n"
"    padding: 5px;\n"
"    color: rgb(40, 40, 40);\n"
"    background-color: rgb(60, 231, 195);\n"
"    font-weight: bold;\n"
"    border-radius: 12px;\n"
"}\n"
"")
        self.login_email_obj.setClearButtonEnabled(False)
        self.login_email_obj.setObjectName("login_email_obj")
        self.login_gridLayout.addWidget(self.login_email_obj, 3, 1, 1, 2)
        self.label_13 = QtWidgets.QLabel(LoginForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_13.sizePolicy().hasHeightForWidth())
        self.label_13.setSizePolicy(sizePolicy)
        self.label_13.setStyleSheet("\n"
"    padding: 5px;\n"
"    background-color: rgba(6, 60, 89, 1);\n"
"")
        self.label_13.setObjectName("label_13")
        self.login_gridLayout.addWidget(self.label_13, 4, 0, 1, 1)
        self.login_progressBar_2 = QtWidgets.QProgressBar(LoginForm)
        self.login_progressBar_2.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.login_progressBar_2.sizePolicy().hasHeightForWidth())
        self.login_progressBar_2.setSizePolicy(sizePolicy)
        self.login_progressBar_2.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.login_progressBar_2.setAutoFillBackground(False)
        self.login_progressBar_2.setStyleSheet("QProgressBar:horizontal {\n"
"border: 1px solid gray;\n"
"border-radius: 10px;\n"
"background: rgba(6, 60, 89, 1);\n"
"padding: 1px;\n"
"\n"
"}\n"
"QProgressBar::chunk:horizontal {\n"
"background: qlineargradient(x1: 0, y1: 0.5, x2: 1, y2: 0.5, stop: 0 rgb(60, 231, 195), stop: 1 rgb(60, 231, 195));\n"
"border-radius: 10px;\n"
"\n"
"}\n"
"")
        self.login_progressBar_2.setMinimum(0)
        self.login_progressBar_2.setMaximum(100)
        self.login_progressBar_2.setProperty("value", 0)
        self.login_progressBar_2.setObjectName("login_progressBar_2")
        self.login_gridLayout.addWidget(self.login_progressBar_2, 6, 0, 1, 3)
        self.login_error_message_2 = QtWidgets.QLabel(LoginForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.login_error_message_2.sizePolicy().hasHeightForWidth())
        self.login_error_message_2.setSizePolicy(sizePolicy)
        self.login_error_message_2.setAutoFillBackground(False)
        self.login_error_message_2.setStyleSheet("color: rgb(239, 41, 41);\n"
"qproperty-alignment: AlignCenter;\n"
"font-weight: bold;\n"
"")
        self.login_error_message_2.setObjectName("login_error_message_2")
        self.login_gridLayout.addWidget(self.login_error_message_2, 5, 1, 1, 1)
        self.verticalLayout_2.addLayout(self.login_gridLayout)
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout_2.addItem(spacerItem7)

        self.retranslateUi(LoginForm)
        QtCore.QMetaObject.connectSlotsByName(LoginForm)

    def retranslateUi(self, LoginForm):
        _translate = QtCore.QCoreApplication.translate
        LoginForm.setWindowTitle(_translate("LoginForm", "Form"))
        self.home_button.setText(_translate("LoginForm", "Home"))
        self.warlord_software_button.setText(_translate("LoginForm", "© WarlordSoft"))
        self.purchase_plan_obj_2.setText(_translate("LoginForm", "<html><head/><body><p align=\"justify\"><span style=\" color:#eeeeec;\">N/A</span></p></body></html>"))
        self.expire_on_obj_2.setText(_translate("LoginForm", "<html><head/><body><p align=\"justify\"><span style=\" color:#eeeeec;\">N/A</span></p></body></html>"))
        self.hello_user_email_obj_2.setText(_translate("LoginForm", "<html><head/><body><p align=\"center\"><span style=\" color:#4e9a06;\">Please Signin/Register to see your plan details.</span></p></body></html>"))
        self.refresh_button.setText(_translate("LoginForm", "Refresh"))
        self.your_plan_2.setText(_translate("LoginForm", "<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; font-weight:600; color:#eeeeec;\">YOUR PLAN</span></p></body></html>"))
        self.purchase_now_button_2.setText(_translate("LoginForm", "BUY NOW (75% OFF)"))
        self.log_out_button_obj_2.setText(_translate("LoginForm", "SIGNOUT"))
        self.activation_date_obj_2.setText(_translate("LoginForm", "<html><head/><body><p align=\"justify\"><span style=\" color:#eeeeec;\">N/A</span></p></body></html>"))
        self.login_from_your_plan.setText(_translate("LoginForm", "SIGNIN"))
        self.refresh_error.setText(_translate("LoginForm", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600; color:#ef2929;\"><br/></span></p></body></html>"))
        self.label_10.setText(_translate("LoginForm", "<html><head/><body><p><span style=\" font-weight:600; color:#eeeeec;\">Your Plan</span></p></body></html>"))
        self.label_9.setText(_translate("LoginForm", "<html><head/><body><p><span style=\" font-weight:600; color:#eeeeec;\">Plan Activated on</span></p></body></html>"))
        self.label_8.setText(_translate("LoginForm", "<html><head/><body><p><span style=\" font-weight:600; color:#eeeeec;\">Plan Expires On</span></p></body></html>"))
        self.product_name.setText(_translate("LoginForm", "<html><head/><body><p align=\"justify\"><span style=\" color:#eeeeec;\">PDF2GO</span></p></body></html>"))
        self.label_14.setText(_translate("LoginForm", "<html><head/><body><p><span style=\" font-weight:600; color:#eeeeec;\">App Name</span></p></body></html>"))
        self.label_3.setText(_translate("LoginForm", "<html><head/><body><p align=\"justify\"><span style=\" font-weight:600; color:#eeeeec;\">Email ID</span></p></body></html>"))
        self.register_password_obj.setPlaceholderText(_translate("LoginForm", "Password"))
        self.label_11.setText(_translate("LoginForm", "<html><head/><body><p align=\"justify\"><span style=\" font-weight:600; color:#eeeeec;\">Password</span></p></body></html>"))
        self.register_re_password_obj.setPlaceholderText(_translate("LoginForm", "Re-password"))
        self.label_12.setText(_translate("LoginForm", "<html><head/><body><p align=\"justify\"><span style=\" font-weight:600; color:#eeeeec;\">Re-password</span></p></body></html>"))
        self.already_registered_signin.setText(_translate("LoginForm", "Already registered ? SIGNIN"))
        self.register_email_id_obj.setPlaceholderText(_translate("LoginForm", "Your Email"))
        self.register_button_obj.setText(_translate("LoginForm", "SIGNUP"))
        self.register_obj.setText(_translate("LoginForm", "<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; font-weight:600; color:#eeeeec;\">QUICK SIGNUP</span></p><p align=\"center\"><span style=\" font-size:8pt; font-weight:600; color:#eeeeec;\">(hardly takes 10 sec)</span></p></body></html>"))
        self.register_error_message.setText(_translate("LoginForm", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600; color:#ef2929;\"><br/></span></p></body></html>"))
        self.login_obj.setText(_translate("LoginForm", "<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; font-weight:600; color:#eeeeec;\">QUICK SIGNIN</span></p><p align=\"center\"><span style=\" font-size:16pt; font-weight:600; color:#eeeeec;\"/><span style=\" font-size:8pt; font-weight:600; color:#eeeeec;\">(hardly takes 5 sec)</span></p></body></html>"))
        self.label_4.setText(_translate("LoginForm", "<html><head/><body><p align=\"justify\"><span style=\" font-weight:600; color:#eeeeec;\">Email ID</span></p></body></html>"))
        self.dont_have_account_register.setText(_translate("LoginForm", "Don\'t have account ? REGISTER"))
        self.login_password_obj.setPlaceholderText(_translate("LoginForm", "Password"))
        self.login_from_login.setText(_translate("LoginForm", "SIGNIN"))
        self.login_email_obj.setPlaceholderText(_translate("LoginForm", "Your Email"))
        self.label_13.setText(_translate("LoginForm", "<html><head/><body><p align=\"justify\"><span style=\" font-weight:600; color:#eeeeec;\">Password</span></p></body></html>"))
        self.login_error_message_2.setText(_translate("LoginForm", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600; color:#ef2929;\"><br/></span></p></body></html>"))
