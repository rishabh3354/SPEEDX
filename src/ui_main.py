# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_main.ui'
#
# Created by: PyQt5 UI code generator 5.14.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(880, 600)
        MainWindow.setMinimumSize(QtCore.QSize(880, 600))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.drop_shadow_layout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.drop_shadow_layout.setContentsMargins(10, 10, 10, 10)
        self.drop_shadow_layout.setObjectName("drop_shadow_layout")
        self.drop_shadow_frame = QtWidgets.QFrame(self.centralwidget)
        self.drop_shadow_frame.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(0, 0, 0, 1), stop:0.521368 rgba(6, 60, 89, 1)); \n"
"border-radius: 10px;")
        self.drop_shadow_frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.drop_shadow_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.drop_shadow_frame.setObjectName("drop_shadow_frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.drop_shadow_frame)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.title_bar = QtWidgets.QFrame(self.drop_shadow_frame)
        self.title_bar.setMaximumSize(QtCore.QSize(16777215, 50))
        self.title_bar.setStyleSheet("background-color: none;")
        self.title_bar.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.title_bar.setFrameShadow(QtWidgets.QFrame.Raised)
        self.title_bar.setObjectName("title_bar")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.title_bar)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame_title = QtWidgets.QFrame(self.title_bar)
        self.frame_title.setMinimumSize(QtCore.QSize(0, 50))
        font = QtGui.QFont()
        font.setFamily("Roboto Condensed Light")
        font.setPointSize(14)
        self.frame_title.setFont(font)
        self.frame_title.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_title.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_title.setObjectName("frame_title")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_title)
        self.verticalLayout_2.setContentsMargins(15, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_title = QtWidgets.QLabel(self.frame_title)
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(14)
        self.label_title.setFont(font)
        self.label_title.setStyleSheet("color: rgb(60, 231, 195);")
        self.label_title.setObjectName("label_title")
        self.verticalLayout_2.addWidget(self.label_title)
        self.horizontalLayout.addWidget(self.frame_title)
        self.frame_btns = QtWidgets.QFrame(self.title_bar)
        self.frame_btns.setMaximumSize(QtCore.QSize(100, 16777215))
        self.frame_btns.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_btns.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_btns.setObjectName("frame_btns")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_btns)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.btn_minimize = QtWidgets.QPushButton(self.frame_btns)
        self.btn_minimize.setMinimumSize(QtCore.QSize(16, 16))
        self.btn_minimize.setMaximumSize(QtCore.QSize(17, 17))
        self.btn_minimize.setStyleSheet("QPushButton {\n"
"    border: none;\n"
"    border-radius: 8px;        \n"
"    background-color: rgb(255, 170, 0);\n"
"}\n"
"QPushButton:hover {    \n"
"    background-color: rgba(255, 170, 0, 150);\n"
"}")
        self.btn_minimize.setText("")
        self.btn_minimize.setObjectName("btn_minimize")
        self.horizontalLayout_3.addWidget(self.btn_minimize)
        self.btn_maximize = QtWidgets.QPushButton(self.frame_btns)
        self.btn_maximize.setMinimumSize(QtCore.QSize(16, 16))
        self.btn_maximize.setMaximumSize(QtCore.QSize(17, 17))
        self.btn_maximize.setStyleSheet("QPushButton {\n"
"    border: none;\n"
"    border-radius: 8px;    \n"
"    background-color: rgb(85, 255, 127);\n"
"}\n"
"QPushButton:hover {    \n"
"    background-color: rgba(85, 255, 127, 150);\n"
"}")
        self.btn_maximize.setText("")
        self.btn_maximize.setObjectName("btn_maximize")
        self.horizontalLayout_3.addWidget(self.btn_maximize)
        self.btn_close = QtWidgets.QPushButton(self.frame_btns)
        self.btn_close.setMinimumSize(QtCore.QSize(16, 16))
        self.btn_close.setMaximumSize(QtCore.QSize(17, 17))
        self.btn_close.setStyleSheet("QPushButton {\n"
"    border: none;\n"
"    border-radius: 8px;        \n"
"    background-color: rgb(255, 0, 0);\n"
"}\n"
"QPushButton:hover {        \n"
"    background-color: rgba(255, 0, 0, 150);\n"
"}")
        self.btn_close.setText("")
        self.btn_close.setObjectName("btn_close")
        self.horizontalLayout_3.addWidget(self.btn_close)
        self.horizontalLayout.addWidget(self.frame_btns)
        self.verticalLayout.addWidget(self.title_bar)
        self.content_bar = QtWidgets.QFrame(self.drop_shadow_frame)
        self.content_bar.setStyleSheet("background-color: none;")
        self.content_bar.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.content_bar.setFrameShadow(QtWidgets.QFrame.Raised)
        self.content_bar.setObjectName("content_bar")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.content_bar)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.stackedWidget = QtWidgets.QStackedWidget(self.content_bar)
        self.stackedWidget.setStyleSheet("background-color: none;")
        self.stackedWidget.setObjectName("stackedWidget")
        self.page_home = QtWidgets.QWidget()
        self.page_home.setObjectName("page_home")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.page_home)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.frame_content_home = QtWidgets.QFrame(self.page_home)
        self.frame_content_home.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_content_home.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_content_home.setObjectName("frame_content_home")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.frame_content_home)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.frame_infos = QtWidgets.QFrame(self.frame_content_home)
        self.frame_infos.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_infos.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_infos.setObjectName("frame_infos")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.frame_infos)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.frame_circle_1 = QtWidgets.QFrame(self.frame_infos)
        self.frame_circle_1.setMinimumSize(QtCore.QSize(250, 250))
        self.frame_circle_1.setMaximumSize(QtCore.QSize(250, 250))
        self.frame_circle_1.setStyleSheet("QFrame{\n"
"    border: 5px solid rgb(60, 231, 195);\n"
"    border-radius: 125px;\n"
"}\n"
"QFrame:hover {\n"
"    border: 5px solid rgb(105, 95, 148);\n"
"}")
        self.frame_circle_1.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_circle_1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_circle_1.setObjectName("frame_circle_1")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.frame_circle_1)
        self.verticalLayout_6.setContentsMargins(10, 50, 10, 50)
        self.verticalLayout_6.setSpacing(10)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.label = QtWidgets.QLabel(self.frame_circle_1)
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setStyleSheet("border: none;\n"
"color: rgb(60, 231, 195);")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout_6.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(self.frame_circle_1)
        font = QtGui.QFont()
        font.setFamily("Sans Serif")
        font.setPointSize(48)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("border: none;\n"
"color: rgb(220,220,220);")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_6.addWidget(self.label_2)
        self.label_3 = QtWidgets.QLabel(self.frame_circle_1)
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("border: none;\n"
" color: rgb(128, 102, 168);")
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_6.addWidget(self.label_3)
        self.label_4 = QtWidgets.QLabel(self.frame_circle_1)
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("border: none;\n"
"color: rgb(60, 231, 195);")
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_6.addWidget(self.label_4)
        self.horizontalLayout_4.addWidget(self.frame_circle_1)
        self.frame_circle_2 = QtWidgets.QFrame(self.frame_infos)
        self.frame_circle_2.setMinimumSize(QtCore.QSize(250, 250))
        self.frame_circle_2.setMaximumSize(QtCore.QSize(250, 250))
        self.frame_circle_2.setStyleSheet("QFrame{\n"
"    border: 5px solid rgb(60, 231, 195);\n"
"    border-radius: 125px;\n"
"}\n"
"QFrame:hover {\n"
"    border: 5px solid rgb(105, 95, 148);\n"
"}")
        self.frame_circle_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_circle_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_circle_2.setObjectName("frame_circle_2")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.frame_circle_2)
        self.verticalLayout_7.setContentsMargins(10, 50, 10, 50)
        self.verticalLayout_7.setSpacing(10)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.label_5 = QtWidgets.QLabel(self.frame_circle_2)
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(11)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("border: none;\n"
"color: rgb(60, 231, 195);")
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_7.addWidget(self.label_5)
        self.label_6 = QtWidgets.QLabel(self.frame_circle_2)
        font = QtGui.QFont()
        font.setFamily("Sans Serif")
        font.setPointSize(48)
        self.label_6.setFont(font)
        self.label_6.setStyleSheet("border: none;\n"
"color: rgb(220,220,220);")
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_7.addWidget(self.label_6)
        self.label_7 = QtWidgets.QLabel(self.frame_circle_2)
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(10)
        self.label_7.setFont(font)
        self.label_7.setStyleSheet("border: none;\n"
" color: rgb(128, 102, 168);")
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.verticalLayout_7.addWidget(self.label_7)
        self.label_8 = QtWidgets.QLabel(self.frame_circle_2)
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(10)
        self.label_8.setFont(font)
        self.label_8.setStyleSheet("border: none;\n"
"color: rgb(60, 231, 195);")
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.verticalLayout_7.addWidget(self.label_8)
        self.horizontalLayout_4.addWidget(self.frame_circle_2)
        self.frame_circle_3 = QtWidgets.QFrame(self.frame_infos)
        self.frame_circle_3.setMinimumSize(QtCore.QSize(250, 250))
        self.frame_circle_3.setMaximumSize(QtCore.QSize(250, 250))
        self.frame_circle_3.setStyleSheet("QFrame{\n"
"    border: 5px solid rgb(60, 231, 195);\n"
"    border-radius: 125px;\n"
"}\n"
"QFrame:hover {\n"
"    border: 5px solid rgb(105, 95, 148);\n"
"}")
        self.frame_circle_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_circle_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_circle_3.setObjectName("frame_circle_3")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.frame_circle_3)
        self.verticalLayout_8.setContentsMargins(10, 50, 10, 50)
        self.verticalLayout_8.setSpacing(10)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.label_9 = QtWidgets.QLabel(self.frame_circle_3)
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(11)
        self.label_9.setFont(font)
        self.label_9.setStyleSheet("border: none;\n"
"color: rgb(60, 231, 195);")
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.verticalLayout_8.addWidget(self.label_9)
        self.label_10 = QtWidgets.QLabel(self.frame_circle_3)
        font = QtGui.QFont()
        font.setFamily("Sans Serif")
        font.setPointSize(48)
        self.label_10.setFont(font)
        self.label_10.setStyleSheet("border: none;\n"
"color: rgb(220,220,220);")
        self.label_10.setAlignment(QtCore.Qt.AlignCenter)
        self.label_10.setObjectName("label_10")
        self.verticalLayout_8.addWidget(self.label_10)
        self.label_11 = QtWidgets.QLabel(self.frame_circle_3)
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(10)
        self.label_11.setFont(font)
        self.label_11.setStyleSheet("border: none;\n"
" color: rgb(128, 102, 168);")
        self.label_11.setAlignment(QtCore.Qt.AlignCenter)
        self.label_11.setObjectName("label_11")
        self.verticalLayout_8.addWidget(self.label_11)
        self.label_12 = QtWidgets.QLabel(self.frame_circle_3)
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(10)
        self.label_12.setFont(font)
        self.label_12.setStyleSheet("border: none;\n"
"color: rgb(60, 231, 195);")
        self.label_12.setAlignment(QtCore.Qt.AlignCenter)
        self.label_12.setObjectName("label_12")
        self.verticalLayout_8.addWidget(self.label_12)
        self.horizontalLayout_4.addWidget(self.frame_circle_3)
        self.verticalLayout_9.addWidget(self.frame_infos)
        self.frame_texts = QtWidgets.QFrame(self.frame_content_home)
        self.frame_texts.setMinimumSize(QtCore.QSize(600, 0))
        self.frame_texts.setMaximumSize(QtCore.QSize(16777215, 100))
        self.frame_texts.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_texts.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_texts.setObjectName("frame_texts")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.frame_texts)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_13 = QtWidgets.QLabel(self.frame_texts)
        self.label_13.setMaximumSize(QtCore.QSize(600, 50))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(16)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_13.setFont(font)
        self.label_13.setStyleSheet("color: rgb(211, 215, 207);\n"
"font: 16pt \"Ubuntu\";\n"
"")
        self.label_13.setAlignment(QtCore.Qt.AlignCenter)
        self.label_13.setObjectName("label_13")
        self.verticalLayout_10.addWidget(self.label_13)
        self.verticalLayout_9.addWidget(self.frame_texts, 0, QtCore.Qt.AlignHCenter)
        self.verticalLayout_5.addWidget(self.frame_content_home)
        self.stackedWidget.addWidget(self.page_home)
        self.page_credits = QtWidgets.QWidget()
        self.page_credits.setObjectName("page_credits")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.page_credits)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.textBrowser = QtWidgets.QTextBrowser(self.page_credits)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textBrowser.sizePolicy().hasHeightForWidth())
        self.textBrowser.setSizePolicy(sizePolicy)
        self.textBrowser.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(0, 0, 0, 1), stop:0.521368 rgba(6, 60, 89, 1));\n"
"border-radius: 10px;")
        self.textBrowser.setReadOnly(False)
        self.textBrowser.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByKeyboard|QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextBrowserInteraction|QtCore.Qt.TextEditable|QtCore.Qt.TextEditorInteraction|QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.textBrowser.setOpenExternalLinks(True)
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout_11.addWidget(self.textBrowser)
        self.stackedWidget.addWidget(self.page_credits)
        self.verticalLayout_4.addWidget(self.stackedWidget)
        self.verticalLayout.addWidget(self.content_bar)
        self.credits_bar = QtWidgets.QFrame(self.drop_shadow_frame)
        self.credits_bar.setMaximumSize(QtCore.QSize(16777215, 30))
        self.credits_bar.setStyleSheet("background-color: none;")
        self.credits_bar.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.credits_bar.setFrameShadow(QtWidgets.QFrame.Raised)
        self.credits_bar.setObjectName("credits_bar")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.credits_bar)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.frame_label_credits = QtWidgets.QFrame(self.credits_bar)
        self.frame_label_credits.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_label_credits.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_label_credits.setObjectName("frame_label_credits")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.frame_label_credits)
        self.horizontalLayout_6.setContentsMargins(15, 0, 0, 0)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.pushButton = QtWidgets.QPushButton(self.frame_label_credits)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton.setStyleSheet("QPushButton {\n"
"    padding: 5px;\n"
"    color: rgb(40, 40, 40);\n"
"    background-color: rgba(6, 60, 89, 1);\n"
"    border-radius: 10px;\n"
"}\n"
"QPushButton:hover {    \n"
"    background-color: rgb(60, 231, 195);\n"
"\n"
"}")
        self.pushButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/resource/resource/speedx.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon)
        self.pushButton.setIconSize(QtCore.QSize(30, 30))
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_6.addWidget(self.pushButton)
        self.my_plan_button = QtWidgets.QPushButton(self.frame_label_credits)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.my_plan_button.sizePolicy().hasHeightForWidth())
        self.my_plan_button.setSizePolicy(sizePolicy)
        self.my_plan_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.my_plan_button.setStyleSheet("QPushButton {\n"
"    padding: 5px;\n"
"    color: rgb(40, 40, 40);\n"
"    background-color: rgba(6, 60, 89, 1);\n"
"    border-radius: 10px;\n"
"}\n"
"QPushButton:hover {    \n"
"    background-color: rgb(60, 231, 195);\n"
"\n"
"}")
        self.my_plan_button.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/resource/resource/my_plan.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.my_plan_button.setIcon(icon1)
        self.my_plan_button.setIconSize(QtCore.QSize(30, 30))
        self.my_plan_button.setObjectName("my_plan_button")
        self.horizontalLayout_6.addWidget(self.my_plan_button)
        self.theme_button = QtWidgets.QPushButton(self.frame_label_credits)
        self.theme_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.theme_button.setStyleSheet("QPushButton {\n"
"    padding: 5px;\n"
"    color: rgb(40, 40, 40);\n"
"    background-color: rgba(6, 60, 89, 1);\n"
"    border-radius: 10px;\n"
"}\n"
"QPushButton:hover {    \n"
"    background-color: rgb(60, 231, 195);\n"
"\n"
"}")
        self.theme_button.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/resource/resource/change-theme.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.theme_button.setIcon(icon2)
        self.theme_button.setIconSize(QtCore.QSize(30, 30))
        self.theme_button.setObjectName("theme_button")
        self.horizontalLayout_6.addWidget(self.theme_button)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem)
        self.horizontalLayout_2.addWidget(self.frame_label_credits)
        self.frame_grip = QtWidgets.QFrame(self.credits_bar)
        self.frame_grip.setMinimumSize(QtCore.QSize(30, 30))
        self.frame_grip.setMaximumSize(QtCore.QSize(30, 30))
        self.frame_grip.setAutoFillBackground(False)
        self.frame_grip.setStyleSheet("padding: 5px;\n"
"background-color: rgb(33, 33, 75);")
        self.frame_grip.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_grip.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_grip.setObjectName("frame_grip")
        self.horizontalLayout_2.addWidget(self.frame_grip)
        self.verticalLayout.addWidget(self.credits_bar)
        self.drop_shadow_layout.addWidget(self.drop_shadow_frame)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_title.setText(_translate("MainWindow", "SpeedX™"))
        self.btn_minimize.setToolTip(_translate("MainWindow", "Minimize"))
        self.btn_maximize.setToolTip(_translate("MainWindow", "Maximize"))
        self.btn_close.setToolTip(_translate("MainWindow", "Close"))
        self.label.setText(_translate("MainWindow", "CPU USAGE"))
        self.label_2.setText(_translate("MainWindow", "25%"))
        self.label_3.setText(_translate("MainWindow", "Intel | i9 9900k"))
        self.label_4.setText(_translate("MainWindow", "Temp: 45Cº"))
        self.label_5.setText(_translate("MainWindow", "INTERNET SPEED"))
        self.label_6.setText(_translate("MainWindow", "8.8"))
        self.label_7.setText(_translate("MainWindow", "MB/S"))
        self.label_8.setText(_translate("MainWindow", "No Internet"))
        self.label_9.setText(_translate("MainWindow", "RAM USAGE"))
        self.label_10.setText(_translate("MainWindow", "80%"))
        self.label_11.setText(_translate("MainWindow", "Total: 16 GB"))
        self.label_12.setText(_translate("MainWindow", "FREE 2.0 GB"))
        self.label_13.setText(_translate("MainWindow", "Hello how are you today!"))
        self.frame_grip.setToolTip(_translate("MainWindow", "Resize Windows"))
import resource_rc