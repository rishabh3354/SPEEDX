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
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
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
        font.setFamily("DejaVu Sans")
        font.setPointSize(11)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("border: none;\n"
" color: rgb(128, 102, 168);")
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_6.addWidget(self.label_3)
        self.label_4 = QtWidgets.QLabel(self.frame_circle_1)
        font = QtGui.QFont()
        font.setFamily("DejaVu Sans")
        font.setPointSize(11)
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
        font.setFamily("DejaVu Sans")
        font.setPointSize(11)
        self.label_7.setFont(font)
        self.label_7.setStyleSheet("border: none;\n"
" color: rgb(128, 102, 168);")
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.verticalLayout_7.addWidget(self.label_7)
        self.label_8 = QtWidgets.QLabel(self.frame_circle_2)
        font = QtGui.QFont()
        font.setFamily("DejaVu Sans")
        font.setPointSize(11)
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
        font.setFamily("DejaVu Sans")
        font.setPointSize(11)
        self.label_11.setFont(font)
        self.label_11.setStyleSheet("border: none;\n"
" color: rgb(128, 102, 168);")
        self.label_11.setAlignment(QtCore.Qt.AlignCenter)
        self.label_11.setObjectName("label_11")
        self.verticalLayout_8.addWidget(self.label_11)
        self.label_12 = QtWidgets.QLabel(self.frame_circle_3)
        font = QtGui.QFont()
        font.setFamily("DejaVu Sans")
        font.setPointSize(11)
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
        self.page_credits.setStyleSheet("background-color:  rgba(6, 60, 89, 1);\n"
"border-radius: 10px;\n"
"color:#d1d1d1;")
        self.page_credits.setObjectName("page_credits")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.page_credits)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.horizontalLayout_37 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_37.setObjectName("horizontalLayout_37")
        self.label_21 = QtWidgets.QLabel(self.page_credits)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_21.sizePolicy().hasHeightForWidth())
        self.label_21.setSizePolicy(sizePolicy)
        self.label_21.setObjectName("label_21")
        self.horizontalLayout_37.addWidget(self.label_21)
        self.verticalLayout_11.addLayout(self.horizontalLayout_37)
        self.gridLayout_11 = QtWidgets.QGridLayout()
        self.gridLayout_11.setObjectName("gridLayout_11")
        self.label_19 = QtWidgets.QLabel(self.page_credits)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_19.sizePolicy().hasHeightForWidth())
        self.label_19.setSizePolicy(sizePolicy)
        self.label_19.setObjectName("label_19")
        self.gridLayout_11.addWidget(self.label_19, 0, 1, 1, 1)
        self.horizontalSlider_2 = QtWidgets.QSlider(self.page_credits)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.horizontalSlider_2.sizePolicy().hasHeightForWidth())
        self.horizontalSlider_2.setSizePolicy(sizePolicy)
        self.horizontalSlider_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.horizontalSlider_2.setStyleSheet("")
        self.horizontalSlider_2.setMinimum(1)
        self.horizontalSlider_2.setMaximum(6)
        self.horizontalSlider_2.setSingleStep(1)
        self.horizontalSlider_2.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_2.setTickPosition(QtWidgets.QSlider.TicksBothSides)
        self.horizontalSlider_2.setObjectName("horizontalSlider_2")
        self.gridLayout_11.addWidget(self.horizontalSlider_2, 3, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_11.addItem(spacerItem, 0, 0, 1, 1)
        self.label_14 = QtWidgets.QLabel(self.page_credits)
        self.label_14.setAlignment(QtCore.Qt.AlignCenter)
        self.label_14.setObjectName("label_14")
        self.gridLayout_11.addWidget(self.label_14, 3, 4, 1, 1)
        self.label_22 = QtWidgets.QLabel(self.page_credits)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_22.sizePolicy().hasHeightForWidth())
        self.label_22.setSizePolicy(sizePolicy)
        self.label_22.setObjectName("label_22")
        self.gridLayout_11.addWidget(self.label_22, 2, 1, 1, 1)
        self.comboBox_2 = QtWidgets.QComboBox(self.page_credits)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_2.sizePolicy().hasHeightForWidth())
        self.comboBox_2.setSizePolicy(sizePolicy)
        self.comboBox_2.setStyleSheet("QComboBox {\n"
"    selection-background-color:  rgba(54,136,198,178);\n"
"    border-style: solid;\n"
"    border: 1px solid rgb(38,106,133);\n"
"    border-radius: 2px;\n"
"    padding: 5px;\n"
"    min-width: 75px;\n"
"}\n"
"\n"
"QPushButton:checked {\n"
"    background-color: rgb(38,106,133);\n"
"    border-color: #6A6969;\n"
"}\n"
"\n"
"QComboBox:hover,\n"
"QPushButton:hover,\n"
"QAbstractSpinBox:hover,\n"
"QLineEdit:hover,\n"
"QTextEdit:hover,\n"
"QPlainTextEdit:hover,\n"
"QAbstractView:hover,\n"
"QTreeView:hover {\n"
"    border: 1px solid  rgba(54,136,198,178);\n"
"    color: #eff0f1;\n"
"}\n"
"\n"
"QComboBox:on {\n"
"    padding-top: 3px;\n"
"    padding-left: 4px;\n"
"    selection-background-color: #4a4a4a;\n"
"}\n"
"\n"
"QComboBox QAbstractItemView {\n"
"    background-color: #232629;\n"
"    border-radius: 2px;\n"
"    border: 1px solid rgb(38,106,133);\n"
"    selection-background-color: #18465d;\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: top right;\n"
"    width: 15px;\n"
"    border-left-width: 0px;\n"
"    border-left-color: darkgray;\n"
"    border-left-style: solid;\n"
"    border-top-right-radius: 3px;\n"
"    border-bottom-right-radius: 3px;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    image: url(:/qss_icons/dark/down_arrow_disabled.png);\n"
"}\n"
"\n"
"QComboBox::down-arrow:on,\n"
"QComboBox::down-arrow:hover,\n"
"QComboBox::down-arrow:focus {\n"
"    image: url(:/qss_icons/dark/down_arrow.png);\n"
"}\n"
"")
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.gridLayout_11.addWidget(self.comboBox_2, 0, 2, 1, 1)
        self.label_23 = QtWidgets.QLabel(self.page_credits)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_23.sizePolicy().hasHeightForWidth())
        self.label_23.setSizePolicy(sizePolicy)
        self.label_23.setObjectName("label_23")
        self.gridLayout_11.addWidget(self.label_23, 3, 1, 1, 1)
        self.label_24 = QtWidgets.QLabel(self.page_credits)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_24.sizePolicy().hasHeightForWidth())
        self.label_24.setSizePolicy(sizePolicy)
        self.label_24.setObjectName("label_24")
        self.gridLayout_11.addWidget(self.label_24, 4, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_11.addItem(spacerItem1, 2, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_11.addItem(spacerItem2, 0, 4, 1, 1)
        self.label_15 = QtWidgets.QLabel(self.page_credits)
        self.label_15.setAlignment(QtCore.Qt.AlignCenter)
        self.label_15.setObjectName("label_15")
        self.gridLayout_11.addWidget(self.label_15, 2, 4, 1, 1)
        self.label_16 = QtWidgets.QLabel(self.page_credits)
        self.label_16.setAlignment(QtCore.Qt.AlignCenter)
        self.label_16.setObjectName("label_16")
        self.gridLayout_11.addWidget(self.label_16, 4, 4, 1, 1)
        self.horizontalSlider_3 = QtWidgets.QSlider(self.page_credits)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.horizontalSlider_3.sizePolicy().hasHeightForWidth())
        self.horizontalSlider_3.setSizePolicy(sizePolicy)
        self.horizontalSlider_3.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.horizontalSlider_3.setStyleSheet("")
        self.horizontalSlider_3.setMinimum(1)
        self.horizontalSlider_3.setMaximum(6)
        self.horizontalSlider_3.setSingleStep(1)
        self.horizontalSlider_3.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_3.setTickPosition(QtWidgets.QSlider.TicksBothSides)
        self.horizontalSlider_3.setObjectName("horizontalSlider_3")
        self.gridLayout_11.addWidget(self.horizontalSlider_3, 4, 2, 1, 1)
        self.horizontalSlider = QtWidgets.QSlider(self.page_credits)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.horizontalSlider.sizePolicy().hasHeightForWidth())
        self.horizontalSlider.setSizePolicy(sizePolicy)
        self.horizontalSlider.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.horizontalSlider.setStyleSheet("")
        self.horizontalSlider.setMinimum(1)
        self.horizontalSlider.setMaximum(6)
        self.horizontalSlider.setSingleStep(1)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setTickPosition(QtWidgets.QSlider.TicksBothSides)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.gridLayout_11.addWidget(self.horizontalSlider, 2, 2, 1, 1)
        self.label_25 = QtWidgets.QLabel(self.page_credits)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_25.sizePolicy().hasHeightForWidth())
        self.label_25.setSizePolicy(sizePolicy)
        self.label_25.setObjectName("label_25")
        self.gridLayout_11.addWidget(self.label_25, 1, 1, 1, 1)
        self.comboBox_3 = QtWidgets.QComboBox(self.page_credits)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_3.sizePolicy().hasHeightForWidth())
        self.comboBox_3.setSizePolicy(sizePolicy)
        self.comboBox_3.setStyleSheet("QComboBox {\n"
"    selection-background-color:  rgba(54,136,198,178);\n"
"    border-style: solid;\n"
"    border: 1px solid rgb(38,106,133);\n"
"    border-radius: 2px;\n"
"    padding: 5px;\n"
"    min-width: 75px;\n"
"}\n"
"\n"
"QPushButton:checked {\n"
"    background-color: rgb(38,106,133);\n"
"    border-color: #6A6969;\n"
"}\n"
"\n"
"QComboBox:hover,\n"
"QPushButton:hover,\n"
"QAbstractSpinBox:hover,\n"
"QLineEdit:hover,\n"
"QTextEdit:hover,\n"
"QPlainTextEdit:hover,\n"
"QAbstractView:hover,\n"
"QTreeView:hover {\n"
"    border: 1px solid  rgba(54,136,198,178);\n"
"    color: #eff0f1;\n"
"}\n"
"\n"
"QComboBox:on {\n"
"    padding-top: 3px;\n"
"    padding-left: 4px;\n"
"    selection-background-color: #4a4a4a;\n"
"}\n"
"\n"
"QComboBox QAbstractItemView {\n"
"    background-color: #232629;\n"
"    border-radius: 2px;\n"
"    border: 1px solid rgb(38,106,133);\n"
"    selection-background-color: #18465d;\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: top right;\n"
"    width: 15px;\n"
"    border-left-width: 0px;\n"
"    border-left-color: darkgray;\n"
"    border-left-style: solid;\n"
"    border-top-right-radius: 3px;\n"
"    border-bottom-right-radius: 3px;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    image: url(:/qss_icons/dark/down_arrow_disabled.png);\n"
"}\n"
"\n"
"QComboBox::down-arrow:on,\n"
"QComboBox::down-arrow:hover,\n"
"QComboBox::down-arrow:focus {\n"
"    image: url(:/qss_icons/dark/down_arrow.png);\n"
"}\n"
"")
        self.comboBox_3.setObjectName("comboBox_3")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.gridLayout_11.addWidget(self.comboBox_3, 1, 2, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_11.addItem(spacerItem3, 1, 4, 1, 1)
        self.verticalLayout_11.addLayout(self.gridLayout_11)
        self.horizontalLayout_36 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_36.setObjectName("horizontalLayout_36")
        self.label_20 = QtWidgets.QLabel(self.page_credits)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_20.sizePolicy().hasHeightForWidth())
        self.label_20.setSizePolicy(sizePolicy)
        self.label_20.setObjectName("label_20")
        self.horizontalLayout_36.addWidget(self.label_20)
        self.verticalLayout_11.addLayout(self.horizontalLayout_36)
        self.horizontalLayout_35 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_35.setObjectName("horizontalLayout_35")
        self.theme1_2 = QtWidgets.QPushButton(self.page_credits)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.theme1_2.sizePolicy().hasHeightForWidth())
        self.theme1_2.setSizePolicy(sizePolicy)
        self.theme1_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.theme1_2.setStyleSheet("QPushButton {\n"
"    color:white;\n"
"    border-color: #76797C;\n"
"    padding: 40px;\n"
"    border-radius: 5px;\n"
"    border-style: solid;\n"
"    border-width: 1px;\n"
"    background-color:  rgb(0, 77, 128);\n"
"}\n"
"\n"
"")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/myresource/resource/single_video.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.theme1_2.setIcon(icon)
        self.theme1_2.setIconSize(QtCore.QSize(80, 80))
        self.theme1_2.setObjectName("theme1_2")
        self.horizontalLayout_35.addWidget(self.theme1_2)
        self.theme2_2 = QtWidgets.QPushButton(self.page_credits)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.theme2_2.sizePolicy().hasHeightForWidth())
        self.theme2_2.setSizePolicy(sizePolicy)
        self.theme2_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.theme2_2.setStyleSheet("QPushButton {\n"
"    color:white;\n"
"    border-color: #76797C;\n"
"    padding: 40px;\n"
"    border-radius: 5px;\n"
"    border-style: solid;\n"
"    border-width: 1px;\n"
"background-color:  QLinearGradient( x1: 0, y1: 0,\n"
"                             x2: 1, y2: 0, \n"
"                            stop: 0 rgb(37, 37, 37),\n"
"                            stop: 1 rgb(0, 77, 128) );\n"
"}\n"
"\n"
"\n"
"")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/myresource/resource/playlist.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.theme2_2.setIcon(icon1)
        self.theme2_2.setIconSize(QtCore.QSize(80, 80))
        self.theme2_2.setObjectName("theme2_2")
        self.horizontalLayout_35.addWidget(self.theme2_2)
        self.verticalLayout_11.addLayout(self.horizontalLayout_35)
        self.stackedWidget.addWidget(self.page_credits)
        self.account_page = QtWidgets.QWidget()
        self.account_page.setStyleSheet("background-color:  rgba(6, 60, 89, 1);\n"
"border-radius: 10px;\n"
"color:#d1d1d1;")
        self.account_page.setObjectName("account_page")
        self.verticalLayout_26 = QtWidgets.QVBoxLayout(self.account_page)
        self.verticalLayout_26.setObjectName("verticalLayout_26")
        self.horizontalLayout_26 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_26.setObjectName("horizontalLayout_26")
        self.gridLayout_8 = QtWidgets.QGridLayout()
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.lineEdit_plan = QtWidgets.QLineEdit(self.account_page)
        self.lineEdit_plan.setEnabled(True)
        self.lineEdit_plan.setReadOnly(True)
        self.lineEdit_plan.setObjectName("lineEdit_plan")
        self.gridLayout_8.addWidget(self.lineEdit_plan, 1, 1, 1, 1)
        self.lineEdit_expires_on = QtWidgets.QLineEdit(self.account_page)
        self.lineEdit_expires_on.setEnabled(True)
        self.lineEdit_expires_on.setReadOnly(True)
        self.lineEdit_expires_on.setObjectName("lineEdit_expires_on")
        self.gridLayout_8.addWidget(self.lineEdit_expires_on, 2, 1, 1, 1)
        self.lineEdit_account_id = QtWidgets.QLineEdit(self.account_page)
        self.lineEdit_account_id.setEnabled(True)
        self.lineEdit_account_id.setReadOnly(True)
        self.lineEdit_account_id.setObjectName("lineEdit_account_id")
        self.gridLayout_8.addWidget(self.lineEdit_account_id, 0, 1, 1, 1)
        self.lineEdit_13 = QtWidgets.QLineEdit(self.account_page)
        self.lineEdit_13.setEnabled(False)
        self.lineEdit_13.setStyleSheet("")
        self.lineEdit_13.setObjectName("lineEdit_13")
        self.gridLayout_8.addWidget(self.lineEdit_13, 0, 0, 1, 1)
        self.label_18 = QtWidgets.QLabel(self.account_page)
        self.label_18.setText("")
        self.label_18.setObjectName("label_18")
        self.gridLayout_8.addWidget(self.label_18, 0, 2, 1, 1)
        self.lineEdit_14 = QtWidgets.QLineEdit(self.account_page)
        self.lineEdit_14.setEnabled(False)
        self.lineEdit_14.setObjectName("lineEdit_14")
        self.gridLayout_8.addWidget(self.lineEdit_14, 1, 0, 1, 1)
        self.lineEdit_15 = QtWidgets.QLineEdit(self.account_page)
        self.lineEdit_15.setEnabled(False)
        self.lineEdit_15.setObjectName("lineEdit_15")
        self.gridLayout_8.addWidget(self.lineEdit_15, 2, 0, 1, 1)
        self.horizontalLayout_26.addLayout(self.gridLayout_8)
        self.verticalLayout_26.addLayout(self.horizontalLayout_26)
        self.horizontalLayout_31 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_31.setObjectName("horizontalLayout_31")
        self.verticalLayout_28 = QtWidgets.QVBoxLayout()
        self.verticalLayout_28.setObjectName("verticalLayout_28")
        self.account_progress_bar = QtWidgets.QProgressBar(self.account_page)
        self.account_progress_bar.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.account_progress_bar.sizePolicy().hasHeightForWidth())
        self.account_progress_bar.setSizePolicy(sizePolicy)
        self.account_progress_bar.setAutoFillBackground(False)
        self.account_progress_bar.setStyleSheet("QProgressBar:horizontal {\n"
"border-radius: 5px;\n"
"background:rgba(0,0,0,0.1);\n"
"padding: 1px;\n"
"color: white;\n"
"background-color: rgba(6, 60, 89, 1);\n"
"height: 1px;\n"
"\n"
"\n"
"}\n"
"QProgressBar::chunk:horizontal {\n"
"background:rgba(69, 182, 73, 1);\n"
"border-radius: 5px;\n"
"padding: 1px;\n"
"color: white;\n"
"\n"
"}\n"
"QProgressBar \n"
"{ \n"
"color: white; \n"
"}\n"
"")
        self.account_progress_bar.setMaximum(100)
        self.account_progress_bar.setProperty("value", 100)
        self.account_progress_bar.setTextVisible(True)
        self.account_progress_bar.setObjectName("account_progress_bar")
        self.verticalLayout_28.addWidget(self.account_progress_bar)
        self.error_message = QtWidgets.QLabel(self.account_page)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.error_message.sizePolicy().hasHeightForWidth())
        self.error_message.setSizePolicy(sizePolicy)
        self.error_message.setAlignment(QtCore.Qt.AlignCenter)
        self.error_message.setObjectName("error_message")
        self.verticalLayout_28.addWidget(self.error_message)
        self.horizontalLayout_31.addLayout(self.verticalLayout_28)
        self.verticalLayout_26.addLayout(self.horizontalLayout_31)
        self.horizontalLayout_30 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_30.setObjectName("horizontalLayout_30")
        self.horizontalLayout_32 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_32.setObjectName("horizontalLayout_32")
        self.purchase_licence = QtWidgets.QPushButton(self.account_page)
        self.purchase_licence.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.purchase_licence.sizePolicy().hasHeightForWidth())
        self.purchase_licence.setSizePolicy(sizePolicy)
        self.purchase_licence.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.purchase_licence.setStyleSheet("QPushButton {\n"
"        padding: 5px;\n"
"    padding-right: 8px;\n"
"    padding-left: 8px;\n"
"    background-color: rgba(69, 182, 73, 1);\n"
"    color:black;\n"
"\n"
"}\n"
"\n"
"QPushButton:disabled {    \n"
"background-color: rgb(48,48,48);\n"
"}\n"
"\n"
"\n"
"")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/resource/resource/shopping-cart.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.purchase_licence.setIcon(icon2)
        self.purchase_licence.setIconSize(QtCore.QSize(18, 18))
        self.purchase_licence.setObjectName("purchase_licence")
        self.horizontalLayout_32.addWidget(self.purchase_licence)
        self.refresh_account = QtWidgets.QPushButton(self.account_page)
        self.refresh_account.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.refresh_account.sizePolicy().hasHeightForWidth())
        self.refresh_account.setSizePolicy(sizePolicy)
        self.refresh_account.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.refresh_account.setStyleSheet("QPushButton {\n"
"        padding: 5px;\n"
"    padding-right: 8px;\n"
"    padding-left: 8px;\n"
"    background-color: rgba(255, 170, 0, 150);\n"
"    color:black;\n"
"\n"
"\n"
"}\n"
"QPushButton:disabled {    \n"
"background-color: rgb(48,48,48);\n"
"}\n"
"\n"
"")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/resource/resource/refresh--v1.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.refresh_account.setIcon(icon3)
        self.refresh_account.setIconSize(QtCore.QSize(18, 18))
        self.refresh_account.setObjectName("refresh_account")
        self.horizontalLayout_32.addWidget(self.refresh_account)
        self.horizontalLayout_30.addLayout(self.horizontalLayout_32)
        self.verticalLayout_26.addLayout(self.horizontalLayout_30)
        self.horizontalLayout_29 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_29.setObjectName("horizontalLayout_29")
        self.developer_info = QtWidgets.QTextBrowser(self.account_page)
        self.developer_info.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.developer_info.sizePolicy().hasHeightForWidth())
        self.developer_info.setSizePolicy(sizePolicy)
        self.developer_info.setStyleSheet("")
        self.developer_info.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.developer_info.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.developer_info.setReadOnly(True)
        self.developer_info.setOpenExternalLinks(True)
        self.developer_info.setObjectName("developer_info")
        self.horizontalLayout_29.addWidget(self.developer_info)
        self.verticalLayout_26.addLayout(self.horizontalLayout_29)
        self.horizontalLayout_33 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_33.setObjectName("horizontalLayout_33")
        self.horizontalLayout_34 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_34.setObjectName("horizontalLayout_34")
        self.warlordsoft_button = QtWidgets.QPushButton(self.account_page)
        self.warlordsoft_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.warlordsoft_button.setStyleSheet("QPushButton {\n"
"    padding: 5px;\n"
"    padding-right: 10px;\n"
"    padding-left: 10px;\n"
"    background-color:rgb(0, 153, 255);\n"
"    border-radius: 5px;\n"
"    color:black;\n"
"\n"
"}\n"
"")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/resource/resource/link.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.warlordsoft_button.setIcon(icon4)
        self.warlordsoft_button.setObjectName("warlordsoft_button")
        self.horizontalLayout_34.addWidget(self.warlordsoft_button)
        self.donate_button = QtWidgets.QPushButton(self.account_page)
        self.donate_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.donate_button.setStyleSheet("QPushButton {\n"
"    padding: 5px;\n"
"    padding-right: 10px;\n"
"    padding-left: 10px;\n"
"    background-color:rgb(0, 153, 255);\n"
"    border-radius: 5px;\n"
"    color:black;\n"
"\n"
"}\n"
"")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/resource/resource/paypal.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.donate_button.setIcon(icon5)
        self.donate_button.setObjectName("donate_button")
        self.horizontalLayout_34.addWidget(self.donate_button)
        self.rate_button = QtWidgets.QPushButton(self.account_page)
        self.rate_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.rate_button.setStyleSheet("QPushButton {\n"
"    padding: 5px;\n"
"    padding-right: 10px;\n"
"    padding-left: 10px;\n"
"    background-color:rgb(0, 153, 255);\n"
"    border-radius: 5px;\n"
"    color:black;\n"
"\n"
"}\n"
"")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/resource/resource/facebook-like.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.rate_button.setIcon(icon6)
        self.rate_button.setObjectName("rate_button")
        self.horizontalLayout_34.addWidget(self.rate_button)
        self.feedback_button = QtWidgets.QPushButton(self.account_page)
        self.feedback_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.feedback_button.setStyleSheet("QPushButton {\n"
"    padding: 5px;\n"
"    padding-right: 10px;\n"
"    padding-left: 10px;\n"
"    background-color:rgb(0, 153, 255);\n"
"    border-radius: 5px;\n"
"    color:black;\n"
"\n"
"}\n"
"")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/resource/resource/person-growth.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.feedback_button.setIcon(icon7)
        self.feedback_button.setObjectName("feedback_button")
        self.horizontalLayout_34.addWidget(self.feedback_button)
        self.horizontalLayout_33.addLayout(self.horizontalLayout_34)
        self.verticalLayout_26.addLayout(self.horizontalLayout_33)
        self.stackedWidget.addWidget(self.account_page)
        self.main_home = QtWidgets.QWidget()
        self.main_home.setObjectName("main_home")
        self.verticalLayout_30 = QtWidgets.QVBoxLayout(self.main_home)
        self.verticalLayout_30.setObjectName("verticalLayout_30")
        self.verticalLayout_29 = QtWidgets.QVBoxLayout()
        self.verticalLayout_29.setObjectName("verticalLayout_29")
        self.gridLayout_10 = QtWidgets.QGridLayout()
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.setting_button = QtWidgets.QPushButton(self.main_home)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.setting_button.sizePolicy().hasHeightForWidth())
        self.setting_button.setSizePolicy(sizePolicy)
        self.setting_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.setting_button.setStyleSheet("QPushButton {\n"
"    color:white;\n"
"    border-color: #76797C;\n"
"    padding: 5px;\n"
"    border-radius: 5px;\n"
"    border-style: solid;\n"
"    border-width: 1px;\n"
"\n"
"\n"
"\n"
"}\n"
"QPushButton:hover {    \n"
"background-color:  rgb(0, 77, 128);\n"
"}\n"
"\n"
"\n"
"\n"
"")
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/resource/resource/horizontal-settings-mixer.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setting_button.setIcon(icon8)
        self.setting_button.setIconSize(QtCore.QSize(75, 75))
        self.setting_button.setObjectName("setting_button")
        self.gridLayout_10.addWidget(self.setting_button, 0, 1, 1, 1)
        self.monitor_button = QtWidgets.QPushButton(self.main_home)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.monitor_button.sizePolicy().hasHeightForWidth())
        self.monitor_button.setSizePolicy(sizePolicy)
        self.monitor_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.monitor_button.setStyleSheet("QPushButton {\n"
"    color:white;\n"
"    border-color: #76797C;\n"
"    padding: 5px;\n"
"    border-radius: 5px;\n"
"    border-style: solid;\n"
"    border-width: 1px;\n"
"\n"
"\n"
"\n"
"}\n"
"QPushButton:hover {    \n"
"background-color:  rgb(0, 77, 128);\n"
"}\n"
"\n"
"\n"
"\n"
"")
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(":/resource/resource/severity.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.monitor_button.setIcon(icon9)
        self.monitor_button.setIconSize(QtCore.QSize(73, 76))
        self.monitor_button.setObjectName("monitor_button")
        self.gridLayout_10.addWidget(self.monitor_button, 0, 0, 1, 1)
        self.account_button = QtWidgets.QPushButton(self.main_home)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.account_button.sizePolicy().hasHeightForWidth())
        self.account_button.setSizePolicy(sizePolicy)
        self.account_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.account_button.setStyleSheet("QPushButton {\n"
"    color:white;\n"
"    border-color: #76797C;\n"
"    padding: 5px;\n"
"    border-radius: 5px;\n"
"    border-style: solid;\n"
"    border-width: 1px;\n"
"\n"
"\n"
"\n"
"}\n"
"QPushButton:hover {    \n"
"background-color:  rgb(0, 77, 128);\n"
"}\n"
"\n"
"\n"
"\n"
"")
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(":/resource/resource/check-male--v1.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.account_button.setIcon(icon10)
        self.account_button.setIconSize(QtCore.QSize(76, 76))
        self.account_button.setObjectName("account_button")
        self.gridLayout_10.addWidget(self.account_button, 0, 2, 1, 1)
        self.verticalLayout_29.addLayout(self.gridLayout_10)
        self.verticalLayout_30.addLayout(self.verticalLayout_29)
        self.stackedWidget.addWidget(self.main_home)
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
        self.home_button = QtWidgets.QPushButton(self.frame_label_credits)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.home_button.sizePolicy().hasHeightForWidth())
        self.home_button.setSizePolicy(sizePolicy)
        self.home_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.home_button.setStyleSheet("QPushButton {\n"
"    padding: 5px;\n"
"    color: rgb(40, 40, 40);\n"
"    background-color: rgba(6, 60, 89, 1);\n"
"    border-radius: 10px;\n"
"}\n"
"QPushButton:hover {    \n"
"    background-color: rgb(60, 231, 195);\n"
"\n"
"}")
        self.home_button.setText("")
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap(":/resource/resource/home.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.home_button.setIcon(icon11)
        self.home_button.setIconSize(QtCore.QSize(30, 30))
        self.home_button.setObjectName("home_button")
        self.horizontalLayout_6.addWidget(self.home_button)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem4)
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
        self.verticalLayout_3.addWidget(self.drop_shadow_frame)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(2)
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
        self.label_21.setText(_translate("MainWindow", "App Settings"))
        self.label_19.setText(_translate("MainWindow", "Net Speed Unit          "))
        self.label_14.setText(_translate("MainWindow", "1"))
        self.label_22.setText(_translate("MainWindow", "Net Speed Freq          "))
        self.comboBox_2.setItemText(0, _translate("MainWindow", "MB/s | KB/s | B/s"))
        self.comboBox_2.setItemText(1, _translate("MainWindow", "mb/s | kb/s | b/s"))
        self.label_23.setText(_translate("MainWindow", "CPU Indicator Freq          "))
        self.label_24.setText(_translate("MainWindow", "RAM Indicator Freq          "))
        self.label_15.setText(_translate("MainWindow", "1"))
        self.label_16.setText(_translate("MainWindow", "1"))
        self.label_25.setText(_translate("MainWindow", "CPU Temp Unit          "))
        self.comboBox_3.setItemText(0, _translate("MainWindow", "°C  (Celsius)"))
        self.comboBox_3.setItemText(1, _translate("MainWindow", "°F  (Fahrenheit)"))
        self.label_20.setText(_translate("MainWindow", "Theme Settings"))
        self.theme1_2.setText(_translate("MainWindow", "Theme1 (Zesty-Blue)"))
        self.theme2_2.setText(_translate("MainWindow", "Theme2 (Gray-blue)"))
        self.lineEdit_plan.setText(_translate("MainWindow", "Evaluation"))
        self.lineEdit_expires_on.setText(_translate("MainWindow", "Licence Expired! Purchase a new Licence"))
        self.lineEdit_account_id.setText(_translate("MainWindow", "8fjfdjhqoifj383ld"))
        self.lineEdit_13.setText(_translate("MainWindow", "Account ID:"))
        self.lineEdit_14.setText(_translate("MainWindow", "Account Type:"))
        self.lineEdit_15.setText(_translate("MainWindow", "Account Status:"))
        self.error_message.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" color:#ef2929;\">Error Message</span></p></body></html>"))
        self.purchase_licence.setText(_translate("MainWindow", "Purchase Licence (75% OFF)"))
        self.refresh_account.setText(_translate("MainWindow", "Refresh Account"))
        self.developer_info.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><img src=\":/resource/resource/user-male--v1.png\" width=\"100\" height=\"100\" /></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#d1d1d1;\">Developed by:</span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600; color:#d1d1d1;\">Rishabh bhardwaj (S.D.E)</span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#d1d1d1;\">Email me: </span><a href=\"mailto: contact@warlordsoftwares.in\"><span style=\" text-decoration: underline; color:#d1d1d1;\">contact@warlordsoftwares.in</span></a></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#d1d1d1;\">Version: </span><span style=\" font-weight:600; color:#d1d1d1;\">0.01 | </span><span style=\" color:#d1d1d1;\">Language used: </span><span style=\" font-weight:600; color:#d1d1d1;\">Python | </span><a href=\"https://snapcraft.io/search?q=rishabh\"><span style=\" text-decoration: underline; color:#d1d1d1;\">Get more apps</span></a></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; color:#d1d1d1;\"><br /></p></body></html>"))
        self.warlordsoft_button.setText(_translate("MainWindow", "Visit @WarlordSoft"))
        self.donate_button.setText(_translate("MainWindow", "Donate"))
        self.rate_button.setText(_translate("MainWindow", "Rate"))
        self.feedback_button.setText(_translate("MainWindow", "Feedback"))
        self.setting_button.setText(_translate("MainWindow", "Settings"))
        self.monitor_button.setText(_translate("MainWindow", "Monitor"))
        self.account_button.setText(_translate("MainWindow", "Account"))
        self.frame_grip.setToolTip(_translate("MainWindow", "Resize Windows"))
import resource_rc
