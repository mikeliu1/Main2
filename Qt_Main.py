# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Qt_Main.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(453, 317)
        self.Structure = QtWidgets.QPushButton(Form)
        self.Structure.setGeometry(QtCore.QRect(90, 120, 100, 30))
        self.Structure.setObjectName("Structure")
        self.Fluid = QtWidgets.QPushButton(Form)
        self.Fluid.setGeometry(QtCore.QRect(250, 120, 100, 30))
        self.Fluid.setObjectName("Fluid")
        self.Acoustics = QtWidgets.QPushButton(Form)
        self.Acoustics.setGeometry(QtCore.QRect(90, 180, 100, 30))
        self.Acoustics.setObjectName("Acoustics")
        self.Thermal = QtWidgets.QPushButton(Form)
        self.Thermal.setGeometry(QtCore.QRect(250, 180, 100, 30))
        self.Thermal.setObjectName("Thermal")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(250, 260, 141, 23))
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(80, 40, 301, 31))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.Structure.setText(_translate("Form", "Structure"))
        self.Fluid.setText(_translate("Form", "Fluid"))
        self.Acoustics.setText(_translate("Form", "Acoustics"))
        self.Thermal.setText(_translate("Form", "Thermal"))
        self.pushButton.setText(_translate("Form", "Work Folder Setting"))
        self.label.setText(_translate("Form", "Simulation AUTO System"))
