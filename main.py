from forms.collecte import Ui_Dialog as DialogCollecteBase
from PyQt5 import QtWidgets



class DialogCollecte(QtWidgets.QDialog):
    def __init__(self) -> None:
        super().__init__()
        self.ui = DialogCollecteBase()
        self.ui.setupUi(self)

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


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dlg = DialogCollecte()
    dlg.show()
    sys.exit(app.exec())