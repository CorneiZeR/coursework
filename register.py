# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'register.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(331, 91)
        Dialog.setAutoFillBackground(False)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setText("")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout_5.addWidget(self.label)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.second_name = QtWidgets.QLineEdit(Dialog)
        self.second_name.setInputMask("")
        self.second_name.setObjectName("second_name")
        self.verticalLayout_2.addWidget(self.second_name)
        self.password = QtWidgets.QLineEdit(Dialog)
        self.password.setInputMask("")
        self.password.setText("")
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password.setCursorPosition(0)
        self.password.setClearButtonEnabled(False)
        self.password.setObjectName("password")
        self.verticalLayout_2.addWidget(self.password)
        self.gridLayout.addLayout(self.verticalLayout_2, 0, 1, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.group = QtWidgets.QLineEdit(Dialog)
        self.group.setObjectName("group")
        self.verticalLayout.addWidget(self.group)
        self.reg = QtWidgets.QPushButton(Dialog)
        self.reg.setObjectName("reg")
        self.verticalLayout.addWidget(self.reg)
        self.gridLayout.addLayout(self.verticalLayout, 0, 2, 1, 1)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.first_name = QtWidgets.QLineEdit(Dialog)
        self.first_name.setInputMask("")
        self.first_name.setText("")
        self.first_name.setObjectName("first_name")
        self.verticalLayout_3.addWidget(self.first_name)
        self.login = QtWidgets.QLineEdit(Dialog)
        self.login.setInputMask("")
        self.login.setText("")
        self.login.setObjectName("login")
        self.verticalLayout_3.addWidget(self.login)
        self.gridLayout.addLayout(self.verticalLayout_3, 0, 0, 1, 1)
        self.verticalLayout_5.addLayout(self.gridLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.second_name.setPlaceholderText(_translate("Dialog", "Фамилия"))
        self.password.setPlaceholderText(_translate("Dialog", "password"))
        self.group.setPlaceholderText(_translate("Dialog", "Группа"))
        self.reg.setText(_translate("Dialog", "Ok"))
        self.first_name.setPlaceholderText(_translate("Dialog", "Имя"))
        self.login.setPlaceholderText(_translate("Dialog", "login"))
