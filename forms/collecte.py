# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\ui\collecte.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(621, 487)
        font = QtGui.QFont()
        font.setPointSize(12)
        Dialog.setFont(font)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.lblArb = QtWidgets.QLabel(Dialog)
        self.lblArb.setStyleSheet("font-weight: bold;\n"
"font-size: 12pt;")
        self.lblArb.setAlignment(QtCore.Qt.AlignCenter)
        self.lblArb.setObjectName("lblArb")
        self.gridLayout.addWidget(self.lblArb, 5, 0, 1, 2)
        self.txtCurrDate = QtWidgets.QLabel(Dialog)
        self.txtCurrDate.setStyleSheet("font-size: 60px;\n"
"font-weight: bold;\n"
"color: rgb(85, 170, 0);")
        self.txtCurrDate.setAlignment(QtCore.Qt.AlignCenter)
        self.txtCurrDate.setObjectName("txtCurrDate")
        self.gridLayout.addWidget(self.txtCurrDate, 1, 0, 1, 2)
        self.txtCurrSeance = QtWidgets.QLabel(Dialog)
        self.txtCurrSeance.setStyleSheet("font-size: 40px;\n"
"font-weight: bold;\n"
"color: rgb(255, 85, 0);")
        self.txtCurrSeance.setAlignment(QtCore.Qt.AlignCenter)
        self.txtCurrSeance.setObjectName("txtCurrSeance")
        self.gridLayout.addWidget(self.txtCurrSeance, 4, 0, 1, 1)
        self.txtCurrLabo = QtWidgets.QLabel(Dialog)
        self.txtCurrLabo.setStyleSheet("font-size: 40px;\n"
"font-weight: bold;\n"
"color: rgb(255, 0, 127);")
        self.txtCurrLabo.setAlignment(QtCore.Qt.AlignCenter)
        self.txtCurrLabo.setObjectName("txtCurrLabo")
        self.gridLayout.addWidget(self.txtCurrLabo, 4, 1, 1, 1)
        self.dirTree = QtWidgets.QTreeWidget(Dialog)
        self.dirTree.setObjectName("dirTree")
        self.gridLayout.addWidget(self.dirTree, 6, 0, 1, 2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lblDate = QtWidgets.QLabel(Dialog)
        self.lblDate.setObjectName("lblDate")
        self.horizontalLayout.addWidget(self.lblDate)
        self.txtDate = QtWidgets.QDateEdit(Dialog)
        self.txtDate.setCurrentSection(QtWidgets.QDateTimeEdit.DaySection)
        self.txtDate.setCalendarPopup(True)
        self.txtDate.setDate(QtCore.QDate(2024, 5, 1))
        self.txtDate.setObjectName("txtDate")
        self.horizontalLayout.addWidget(self.txtDate)
        self.lblSeance = QtWidgets.QLabel(Dialog)
        self.lblSeance.setObjectName("lblSeance")
        self.horizontalLayout.addWidget(self.lblSeance)
        self.txtSeance = QtWidgets.QSpinBox(Dialog)
        self.txtSeance.setMinimum(1)
        self.txtSeance.setMaximum(5)
        self.txtSeance.setObjectName("txtSeance")
        self.horizontalLayout.addWidget(self.txtSeance)
        self.lblLabo = QtWidgets.QLabel(Dialog)
        self.lblLabo.setObjectName("lblLabo")
        self.horizontalLayout.addWidget(self.lblLabo)
        self.txtLabo = QtWidgets.QSpinBox(Dialog)
        self.txtLabo.setMinimum(1)
        self.txtLabo.setMaximum(10)
        self.txtLabo.setObjectName("txtLabo")
        self.horizontalLayout.addWidget(self.txtLabo)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 2)

        self.retranslateUi(Dialog)
        self.txtDate.dateChanged['QDate'].connect(Dialog.dateChanged) # type: ignore
        self.txtSeance.valueChanged['int'].connect(Dialog.seanceChanged) # type: ignore
        self.txtLabo.valueChanged['int'].connect(Dialog.laboChanged) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.lblArb.setText(_translate("Dialog", "Arborescence"))
        self.txtCurrDate.setText(_translate("Dialog", "2023-05-28"))
        self.txtCurrSeance.setText(_translate("Dialog", "Séance xx"))
        self.txtCurrLabo.setText(_translate("Dialog", "Labo xx"))
        self.lblDate.setText(_translate("Dialog", "Date"))
        self.lblSeance.setText(_translate("Dialog", "Séance"))
        self.lblLabo.setText(_translate("Dialog", "Laboratoire"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
