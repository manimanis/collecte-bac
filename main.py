import os
from typing import List
from forms.collecte import Ui_Dialog as DialogCollecteBase
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QApplication, QTreeWidget, QTreeWidgetItem
from PyQt5.QtCore import Qt

from src.folder_funcs import human_filesize_unit, search_dir_students


class DialogCollecte(QtWidgets.QDialog):
    def __init__(self) -> None:
        super().__init__()
        self.src_dir = ""
        self.src_dir_list = []
        self.src_dir_summ = {
            "nbfiles": 0,
            "nbdirs": 0
        }

        self.dest_path = ""

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
        self.ui.txtSrcCurrPath.setText(self.src_dir)
        self.ui.btnSrcSearch.setEnabled(self.src_dir != "")

        self.ui.txtNbFichiers.setText(f"{self.src_dir_summ['nbfiles']} Fichiers")
        self.ui.txtNbDossiers.setText(f"{self.src_dir_summ['nbdirs']} Dossiers")

        self.ui.txtCurrDate.setText(self.ui.txtDate.date().toString("yyyy-MM-dd"))
        self.ui.txtCurrLabo.setText(f"Labo {self.ui.txtLabo.value()}")
        self.ui.txtCurrSeance.setText(f"Séance {self.ui.txtSeance.value()}")
    
    def btnSrcDirClicked(self):
        selected_dir = QFileDialog.getExistingDirectory(
            None, 
            self.tr("Dossier source"), 
            self.src_dir, 
            QFileDialog.ShowDirsOnly
        )
        if selected_dir:
            self.src_dir = os.path.normpath(selected_dir)
            self.btnSrcSearchClicked()
            self.updateInterface()

    def btnDestDirClicked(self):
        pass

    def btnSrcSearchClicked(self):
        self.src_dir_list = search_dir_students(self.src_dir)
        self.src_dir_summ = self.summarize_dir_contents(self.src_dir_list)
        self.display_tree_content(self.src_dir_list, self.ui.treeSrcDir)

    def display_tree_content(self, lst: List, tree: QTreeWidget):
        tree.clear()
        for item in lst:
            nameitem = QTreeWidgetItem(tree)
            nameitem.setText(0, item["dirname"])
            nameitem.setText(1, human_filesize_unit(item["totalsize"]))
            nameitem.setTextAlignment(1, Qt.AlignmentFlag.AlignRight)
            nameitem.setText(2, f"{len(item['files'])}")
            nameitem.setTextAlignment(2, Qt.AlignmentFlag.AlignRight)
            nameitem.setText(3, f"{len(item['dirs'])}")
            nameitem.setTextAlignment(3, Qt.AlignmentFlag.AlignRight)
            for file in item["files"]:
                fileitem = QTreeWidgetItem(nameitem)
                fileitem.setText(0, file["filepath"][len(item["dirpath"])+1:])
                fileitem.setText(1, human_filesize_unit(file["filesize"]))
                fileitem.setTextAlignment(1, Qt.AlignmentFlag.AlignRight)
            tree.addTopLevelItem(nameitem)
        tree.resizeColumnToContents(0)

    def summarize_dir_contents(self, lst: List) -> List:
        nbfiles, nbdirs = 0, len(lst)
        for item in lst:
            nbfiles += len(item["files"])
        return {
            "nbfiles": nbfiles,
            "nbdirs": nbdirs
        }

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    dlg = DialogCollecte()
    dlg.show()
    sys.exit(app.exec())