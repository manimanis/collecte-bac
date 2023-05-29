from forms.collecte import Ui_Dialog as DialogCollecteBase
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QApplication


class DialogCollecte(QtWidgets.QDialog):
    def __init__(self) -> None:
        super().__init__()
        self.ui = DialogCollecteBase()
        self.ui.setupUi(self)
        self.updateInterface()

    def dateChanged(self, newDate):
        self.updateInterface()

    def seanceChanged(self, newSeance):
        self.updateInterface()

    def laboChanged(self, newLabo):
        self.updateInterface()

    def updateInterface(self):
        self.ui.txtCurrDate.setText(self.ui.txtDate.date().toString("yyyy-MM-dd"))
        self.ui.txtCurrLabo.setText(f"Labo {self.ui.txtLabo.value()}")
        self.ui.txtCurrSeance.setText(f"Séance {self.ui.txtSeance.value()}")
    
    def btnSrcDirClicked(self):
        selected_dir = QFileDialog.getExistingDirectory(
            None, 
            self.tr("Dossier source"), 
            "", 
            QFileDialog.ShowDirsOnly
        )
        if selected_dir:
            self.ui.txtSrcDir.setText(selected_dir)


    def btnDestDirClicked(self):
        pass

    def btnSrcSearchClicked(self):
        pass


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    dlg = DialogCollecte()
    dlg.show()
    sys.exit(app.exec())