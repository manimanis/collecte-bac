import os
from typing import List
from forms.collecte import Ui_Dialog as DialogCollecteBase
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QApplication, QTreeWidget, QTreeWidgetItem
from PyQt5.QtCore import Qt, QDate
from src.config import AppConfig

from src.folder_funcs import human_filesize_unit, search_dir_students


class DialogCollecte(QtWidgets.QDialog):
    def __init__(self) -> None:
        super().__init__()
        self.src_dir = ""
        self.src_dir_list = []
        self.src_dir_summ = {
            "nbfiles": 0,
            "nbdirs": 0,
            "nb_median_files": None,
            "nb_min_files": None,
            "nb_max_files": None
        }
        
        self.curr_date = QDate.fromString(AppConfig.DATE_SEANCE, "yyyy-MM-dd")
        self.curr_seance = AppConfig.NUM_SEANCE
        self.curr_labo = 1
        self.base_dest_dir = ""
        self.dest_dir = ""
        self.set_base_dest_dir(AppConfig.LOCAL_BACKUP_FOLDER)

        self.ui = DialogCollecteBase()
        self.ui.setupUi(self)
        self.updateInterface()

    def dateChanged(self, newDate):
        self.curr_date = self.ui.txtDate.date()
        self.update_dest_dir()
        self.updateInterface()

    def seanceChanged(self, newSeance):
        self.curr_seance = self.ui.txtSeance.value()
        self.update_dest_dir()
        self.updateInterface()

    def laboChanged(self, newLabo):
        self.curr_labo = self.ui.txtLabo.value()
        self.update_dest_dir()
        self.updateInterface()

    def updateInterface(self):
        self.ui.txtSrcCurrPath.setText(self.src_dir)
        self.ui.btnSrcSearch.setEnabled(self.src_dir != "")

        self.ui.txtNbFichiers.setText(f"{self.src_dir_summ['nbfiles']} Fichiers")
        self.ui.txtNbDossiers.setText(f"{self.src_dir_summ['nbdirs']} Dossiers")

        self.ui.txtNbMin.setText(f"Min: {self.src_dir_summ['nb_min_files']}")
        self.ui.txtNbMedian.setText(f"Median: {self.src_dir_summ['nb_median_files']}")
        self.ui.txtNbMax.setText(f"Max: {self.src_dir_summ['nb_max_files']}")

        self.ui.txtDestCurrPath.setText(self.base_dest_dir)
        self.ui.txtDestDir.setText(self.dest_dir)

        self.ui.txtCurrDate.setText(self.curr_date.toString("yyyy-MM-dd"))
        self.ui.txtCurrLabo.setText(f"Labo {self.curr_labo}")
        self.ui.txtCurrSeance.setText(f"Séance {self.curr_seance}")
    
    def btnSrcDirClicked(self):
        selected_dir = QFileDialog.getExistingDirectory(
            self, 
            self.tr("Dossier source"), 
            self.src_dir, 
            QFileDialog.ShowDirsOnly
        )
        if selected_dir:
            self.src_dir = os.path.normpath(selected_dir)
            self.btnSrcSearchClicked()
            self.updateInterface()

    def btnDestDirClicked(self):
        selected_dir = QFileDialog.getExistingDirectory(
            self,
            self.tr("Dossier destination"),
            self.base_dest_dir,
            QFileDialog.ShowDirsOnly
        )
        if selected_dir:
            self.base_dest_dir = os.path.normpath(selected_dir)
            self.updateInterface()

    def btnSrcSearchClicked(self):
        self.src_dir_list = search_dir_students(self.src_dir)
        self.src_dir_summ = self.summarize_dir_contents(self.src_dir_list)
        self.display_tree_content(self.src_dir_list, self.ui.treeSrcDir)

    def get_base_dest_dir(self):
        return self.base_dest_dir
    
    def set_base_dest_dir(self, dest_dir: str):
        self.base_dest_dir = dest_dir
        self.update_dest_dir()

    def update_dest_dir(self):
        self.dest_dir = os.path.join(self.base_dest_dir, 
                                     self.curr_date.toString("yyyy-MM-dd"),
                                     f"Seance{self.curr_seance:02d}",
                                     f"Labo{self.curr_labo:02d}")

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
        nbfiles, nbdirs, nb = 0, len(lst), len(lst)
        nbfileslst = []
        for item in lst:
            nbfiles += len(item["files"])
            nbfileslst.append(len(item["files"]))
        nbfileslst.sort()
        median = None
        nb_min_files = None
        nb_max_files = None
        if nb > 0:
            median = nbfileslst[len(lst) // 2] if len(lst) % 2 == 1 else ((nbfileslst[len(lst) // 2] + nbfileslst[len(lst) // 2-1])/2)
            nb_min_files = nbfileslst[0]
            nb_max_files = nbfileslst[-1]
        return {
            "nbfiles": nbfiles,
            "nbdirs": nbdirs,
            "nb_median_files": median,
            "nb_min_files": nb_min_files,
            "nb_max_files": nb_max_files
        }

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    dlg = DialogCollecte()
    dlg.show()
    sys.exit(app.exec())