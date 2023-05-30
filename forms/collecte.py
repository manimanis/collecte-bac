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
        Dialog.resize(900, 500)
        font = QtGui.QFont()
        font.setPointSize(12)
        Dialog.setFont(font)
        self.gridLayout_4 = QtWidgets.QGridLayout(Dialog)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout.setSpacing(10)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.txtCurrSeance = QtWidgets.QLabel(Dialog)
        self.txtCurrSeance.setStyleSheet("font-size: 30px;\n"
"font-weight: bold;\n"
"color: rgb(255, 85, 0);")
        self.txtCurrSeance.setAlignment(QtCore.Qt.AlignCenter)
        self.txtCurrSeance.setObjectName("txtCurrSeance")
        self.gridLayout_3.addWidget(self.txtCurrSeance, 8, 1, 1, 1)
        self.btnImportAll = QtWidgets.QPushButton(Dialog)
        self.btnImportAll.setObjectName("btnImportAll")
        self.gridLayout_3.addWidget(self.btnImportAll, 15, 1, 1, 2)
        self.txtCurrLabo = QtWidgets.QLabel(Dialog)
        self.txtCurrLabo.setStyleSheet("font-size: 30px;\n"
"font-weight: bold;\n"
"color: rgb(255, 0, 127);")
        self.txtCurrLabo.setAlignment(QtCore.Qt.AlignCenter)
        self.txtCurrLabo.setObjectName("txtCurrLabo")
        self.gridLayout_3.addWidget(self.txtCurrLabo, 8, 2, 1, 1)
        self.lblDestination = QtWidgets.QLabel(Dialog)
        self.lblDestination.setStyleSheet("font-weight: bold;\n"
"font-size: 12pt;")
        self.lblDestination.setAlignment(QtCore.Qt.AlignCenter)
        self.lblDestination.setObjectName("lblDestination")
        self.gridLayout_3.addWidget(self.lblDestination, 2, 1, 1, 2)
        self.txtCurrDate = QtWidgets.QLabel(Dialog)
        self.txtCurrDate.setStyleSheet("font-size: 40px;\n"
"font-weight: bold;\n"
"color: rgb(85, 170, 0);")
        self.txtCurrDate.setAlignment(QtCore.Qt.AlignCenter)
        self.txtCurrDate.setObjectName("txtCurrDate")
        self.gridLayout_3.addWidget(self.txtCurrDate, 7, 1, 1, 2)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.txtDestDir = QtWidgets.QLabel(Dialog)
        self.txtDestDir.setText("")
        self.txtDestDir.setObjectName("txtDestDir")
        self.horizontalLayout_4.addWidget(self.txtDestDir)
        self.gridLayout_3.addLayout(self.horizontalLayout_4, 11, 1, 1, 2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.txtDestCurrPath = QtWidgets.QLabel(Dialog)
        self.txtDestCurrPath.setText("")
        self.txtDestCurrPath.setObjectName("txtDestCurrPath")
        self.horizontalLayout_3.addWidget(self.txtDestCurrPath)
        self.btnDestDir = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnDestDir.sizePolicy().hasHeightForWidth())
        self.btnDestDir.setSizePolicy(sizePolicy)
        self.btnDestDir.setObjectName("btnDestDir")
        self.horizontalLayout_3.addWidget(self.btnDestDir)
        self.gridLayout_3.addLayout(self.horizontalLayout_3, 3, 1, 1, 2)
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
        self.gridLayout_3.addLayout(self.horizontalLayout, 6, 1, 1, 2)
        self.btnDestSearch = QtWidgets.QPushButton(Dialog)
        self.btnDestSearch.setObjectName("btnDestSearch")
        self.gridLayout_3.addWidget(self.btnDestSearch, 4, 1, 1, 2)
        self.progressBar = QtWidgets.QProgressBar(Dialog)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setTextVisible(False)
        self.progressBar.setInvertedAppearance(False)
        self.progressBar.setObjectName("progressBar")
        self.gridLayout_3.addWidget(self.progressBar, 14, 1, 1, 2)
        self.treeDestDir = QtWidgets.QTreeWidget(Dialog)
        self.treeDestDir.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.treeDestDir.setRootIsDecorated(True)
        self.treeDestDir.setExpandsOnDoubleClick(False)
        self.treeDestDir.setObjectName("treeDestDir")
        self.gridLayout_3.addWidget(self.treeDestDir, 5, 1, 1, 2)
        self.gridLayout.addLayout(self.gridLayout_3, 0, 1, 1, 1)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.txtNbFichiers = QtWidgets.QLabel(Dialog)
        self.txtNbFichiers.setText("")
        self.txtNbFichiers.setAlignment(QtCore.Qt.AlignCenter)
        self.txtNbFichiers.setObjectName("txtNbFichiers")
        self.horizontalLayout_5.addWidget(self.txtNbFichiers)
        self.txtNbDossiers = QtWidgets.QLabel(Dialog)
        self.txtNbDossiers.setText("")
        self.txtNbDossiers.setAlignment(QtCore.Qt.AlignCenter)
        self.txtNbDossiers.setObjectName("txtNbDossiers")
        self.horizontalLayout_5.addWidget(self.txtNbDossiers)
        self.txtNbMin = QtWidgets.QLabel(Dialog)
        self.txtNbMin.setText("")
        self.txtNbMin.setAlignment(QtCore.Qt.AlignCenter)
        self.txtNbMin.setObjectName("txtNbMin")
        self.horizontalLayout_5.addWidget(self.txtNbMin)
        self.txtNbMedian = QtWidgets.QLabel(Dialog)
        self.txtNbMedian.setText("")
        self.txtNbMedian.setAlignment(QtCore.Qt.AlignCenter)
        self.txtNbMedian.setObjectName("txtNbMedian")
        self.horizontalLayout_5.addWidget(self.txtNbMedian)
        self.txtNbMax = QtWidgets.QLabel(Dialog)
        self.txtNbMax.setText("")
        self.txtNbMax.setAlignment(QtCore.Qt.AlignCenter)
        self.txtNbMax.setObjectName("txtNbMax")
        self.horizontalLayout_5.addWidget(self.txtNbMax)
        self.gridLayout_2.addLayout(self.horizontalLayout_5, 5, 0, 1, 1)
        self.lblSource = QtWidgets.QLabel(Dialog)
        self.lblSource.setStyleSheet("font-weight: bold;\n"
"font-size: 12pt;")
        self.lblSource.setAlignment(QtCore.Qt.AlignCenter)
        self.lblSource.setObjectName("lblSource")
        self.gridLayout_2.addWidget(self.lblSource, 0, 0, 1, 1)
        self.treeSrcDir = QtWidgets.QTreeWidget(Dialog)
        self.treeSrcDir.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.treeSrcDir.setAlternatingRowColors(True)
        self.treeSrcDir.setUniformRowHeights(True)
        self.treeSrcDir.setAllColumnsShowFocus(True)
        self.treeSrcDir.setExpandsOnDoubleClick(False)
        self.treeSrcDir.setObjectName("treeSrcDir")
        self.treeSrcDir.headerItem().setTextAlignment(1, QtCore.Qt.AlignLeading|QtCore.Qt.AlignVCenter)
        self.treeSrcDir.headerItem().setTextAlignment(2, QtCore.Qt.AlignLeading|QtCore.Qt.AlignVCenter)
        self.treeSrcDir.headerItem().setTextAlignment(3, QtCore.Qt.AlignLeading|QtCore.Qt.AlignVCenter)
        self.treeSrcDir.header().setSortIndicatorShown(True)
        self.gridLayout_2.addWidget(self.treeSrcDir, 4, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.txtSrcCurrPath = QtWidgets.QLabel(Dialog)
        self.txtSrcCurrPath.setText("")
        self.txtSrcCurrPath.setObjectName("txtSrcCurrPath")
        self.horizontalLayout_2.addWidget(self.txtSrcCurrPath)
        self.btnSrcDir = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnSrcDir.sizePolicy().hasHeightForWidth())
        self.btnSrcDir.setSizePolicy(sizePolicy)
        self.btnSrcDir.setObjectName("btnSrcDir")
        self.horizontalLayout_2.addWidget(self.btnSrcDir)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)
        self.btnSrcSearch = QtWidgets.QPushButton(Dialog)
        self.btnSrcSearch.setObjectName("btnSrcSearch")
        self.gridLayout_2.addWidget(self.btnSrcSearch, 2, 0, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_2, 0, 0, 1, 1)
        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 1)
        self.gridLayout_4.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        self.txtDate.dateChanged['QDate'].connect(Dialog.dateChanged) # type: ignore
        self.txtSeance.valueChanged['int'].connect(Dialog.seanceChanged) # type: ignore
        self.txtLabo.valueChanged['int'].connect(Dialog.laboChanged) # type: ignore
        self.btnSrcDir.clicked.connect(Dialog.btnSrcDirClicked) # type: ignore
        self.btnSrcSearch.clicked.connect(Dialog.btnSrcSearchClicked) # type: ignore
        self.btnDestDir.clicked.connect(Dialog.btnDestDirClicked) # type: ignore
        self.btnImportAll.clicked.connect(Dialog.btnImportAllClicked) # type: ignore
        self.btnDestSearch.clicked.connect(Dialog.btnDestSearchClicked) # type: ignore
        self.treeDestDir.doubleClicked['QModelIndex'].connect(Dialog.treeDestDirDoubleClicked) # type: ignore
        self.treeSrcDir.doubleClicked['QModelIndex'].connect(Dialog.treeSrcDirDoubleClicked) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.btnSrcDir, self.btnSrcSearch)
        Dialog.setTabOrder(self.btnSrcSearch, self.btnDestDir)
        Dialog.setTabOrder(self.btnDestDir, self.txtDate)
        Dialog.setTabOrder(self.txtDate, self.txtSeance)
        Dialog.setTabOrder(self.txtSeance, self.txtLabo)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "BacUp"))
        self.txtCurrSeance.setText(_translate("Dialog", "Séance xx"))
        self.btnImportAll.setText(_translate("Dialog", "Importer tout..."))
        self.txtCurrLabo.setText(_translate("Dialog", "Labo xx"))
        self.lblDestination.setText(_translate("Dialog", "Dossier Destination"))
        self.txtCurrDate.setText(_translate("Dialog", "2023-05-28"))
        self.btnDestDir.setText(_translate("Dialog", "Choisir..."))
        self.lblDate.setText(_translate("Dialog", "Date"))
        self.lblSeance.setText(_translate("Dialog", "Séance"))
        self.lblLabo.setText(_translate("Dialog", "Labo"))
        self.btnDestSearch.setText(_translate("Dialog", "Recherche"))
        self.treeDestDir.headerItem().setText(0, _translate("Dialog", "Nom"))
        self.treeDestDir.headerItem().setText(1, _translate("Dialog", "Type"))
        self.lblSource.setText(_translate("Dialog", "Dossier Source"))
        self.treeSrcDir.headerItem().setText(0, _translate("Dialog", "Dossier"))
        self.treeSrcDir.headerItem().setText(1, _translate("Dialog", "Taille"))
        self.treeSrcDir.headerItem().setText(2, _translate("Dialog", "Fichiers"))
        self.treeSrcDir.headerItem().setText(3, _translate("Dialog", "Dossiers"))
        self.btnSrcDir.setText(_translate("Dialog", "Choisir..."))
        self.btnSrcSearch.setText(_translate("Dialog", "Recherche"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
