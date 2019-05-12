# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'new.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_NewWindow(object):
    def setupUi(self, NewWindow):
        NewWindow.setObjectName("NewWindow")
        NewWindow.resize(682, 391)
        NewWindow.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        NewWindow.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.centralwidget = QtWidgets.QWidget(NewWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_3.setObjectName("gridLayout_3")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout_3.addItem(spacerItem, 0, 2, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(self.frame)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout_3.addWidget(self.buttonBox, 10, 3, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout_3.addItem(spacerItem1, 7, 1, 1, 1)
        self.lineE2 = QtWidgets.QLineEdit(self.frame)
        self.lineE2.setEnabled(False)
        self.lineE2.setText("")
        self.lineE2.setPlaceholderText("")
        self.lineE2.setObjectName("lineE2")
        self.gridLayout_3.addWidget(self.lineE2, 3, 2, 1, 2)
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setObjectName("label")
        self.gridLayout_3.addWidget(self.label, 1, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setObjectName("label_2")
        self.gridLayout_3.addWidget(self.label_2, 3, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setObjectName("label_3")
        self.gridLayout_3.addWidget(self.label_3, 5, 1, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout_3.addItem(spacerItem2, 2, 2, 1, 1)
        self.pushb_abrir = QtWidgets.QPushButton(self.frame)
        self.pushb_abrir.setObjectName("pushb_abrir")
        self.gridLayout_3.addWidget(self.pushb_abrir, 10, 1, 1, 1)
        self.lineE1 = QtWidgets.QLineEdit(self.frame)
        self.lineE1.setInputMask("")
        self.lineE1.setText("")
        self.lineE1.setObjectName("lineE1")
        self.gridLayout_3.addWidget(self.lineE1, 1, 2, 1, 2)
        self.line = QtWidgets.QFrame(self.frame)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout_3.addWidget(self.line, 8, 1, 1, 3)
        self.lineE3 = QtWidgets.QLineEdit(self.frame)
        self.lineE3.setText("")
        self.lineE3.setObjectName("lineE3")
        self.gridLayout_3.addWidget(self.lineE3, 5, 2, 1, 2)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout_3.addItem(spacerItem3, 4, 2, 1, 1)
        self.gridLayout.addWidget(self.frame, 0, 1, 3, 1)
        spacerItem4 = QtWidgets.QSpacerItem(200, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem4, 2, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 1, 0, 1, 1)
        NewWindow.setCentralWidget(self.centralwidget)
        self.statusBar = QtWidgets.QStatusBar(NewWindow)
        self.statusBar.setObjectName("statusBar")
        NewWindow.setStatusBar(self.statusBar)

        self.retranslateUi(NewWindow)
        QtCore.QMetaObject.connectSlotsByName(NewWindow)

    def retranslateUi(self, NewWindow):
        _translate = QtCore.QCoreApplication.translate
        NewWindow.setWindowTitle(_translate("NewWindow", "Nuevo proyecto"))
        self.label.setText(_translate("NewWindow", "Nombre"))
        self.label_2.setText(_translate("NewWindow", "Ubicacion"))
        self.label_3.setText(_translate("NewWindow", "Descripcion"))
        self.pushb_abrir.setText(_translate("NewWindow", "Abrir"))
        self.lineE1.setPlaceholderText(_translate("NewWindow", "nombre de proyecto"))
        self.lineE3.setPlaceholderText(_translate("NewWindow", "(optional)"))
        self.label_4.setText(_translate("NewWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; font-weight:600;\">WELCOME</span></p></body></html>"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    NewWindow = QtWidgets.QMainWindow()
    ui = Ui_NewWindow()
    ui.setupUi(NewWindow)
    NewWindow.show()
    sys.exit(app.exec_())

