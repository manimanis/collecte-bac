import os
from typing import Dict, List
from forms.collecte import Ui_Dialog as DialogCollecteBase
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QApplication, QTreeWidget, QTreeWidgetItem
from PyQt5.QtCore import Qt, QDate, QModelIndex
from src.config import AppConfig

from src.folder_funcs import copytree, human_filesize_unit, search_dir_students, search_folder_contents


class DialogCollecte(QtWidgets.QDialog):
    def __init__(self) -> None:
        super().__init__()
        self.src_dir = AppConfig.BASE_SOURCE_FOLDER
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
        self.curr_labo = AppConfig.NUM_LABO
        self.base_dest_dir = ""
        self.dest_dir = ""
        self.set_base_dest_dir(AppConfig.LOCAL_BACKUP_FOLDER)

        self.ui = DialogCollecteBase()
        self.ui.setupUi(self)
        self.initInterface()
        self.updateInterface()

    def initInterface(self):
        self.ui.txtDate.setDate(self.curr_date)
        self.ui.txtSeance.setValue(self.curr_seance)
        self.ui.txtLabo.setValue(self.curr_labo)
        self.ui.txtLabo.setMaximum(AppConfig.NBRE_LABOS)

    def updateInterface(self):
        self.ui.txtSrcCurrPath.setText(self.src_dir)
        self.ui.btnSrcSearch.setEnabled(self.src_dir != "")

        self.ui.txtNbFichiers.setText(
            f"{self.src_dir_summ['nbfiles']} Fichiers")
        self.ui.txtNbDossiers.setText(
            f"{self.src_dir_summ['nbdirs']} Dossiers")

        self.ui.txtNbMin.setText(f"Min: {self.src_dir_summ['nb_min_files']}")
        self.ui.txtNbMedian.setText(
            f"Median: {self.src_dir_summ['nb_median_files']}")
        self.ui.txtNbMax.setText(f"Max: {self.src_dir_summ['nb_max_files']}")

        self.ui.txtDestCurrPath.setText(self.base_dest_dir)
        self.ui.txtDestDir.setText(self.dest_dir)
        self.ui.btnDestSearch.setEnabled(self.base_dest_dir != "")

        self.ui.txtCurrDate.setText(self.curr_date.toString("yyyy-MM-dd"))
        self.ui.txtCurrLabo.setText(f"Labo {self.curr_labo}")
        self.ui.txtCurrSeance.setText(f"Séance {self.curr_seance}")

        self.ui.btnImportAll.setEnabled(self.can_import_files())

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
        self.updateInterface()

    def btnDestSearchClicked(self):
        dct = search_folder_contents(self.base_dest_dir)
        self.display_dest_tree(dct, self.ui.treeDestDir)

    def btnImportAllClicked(self):
        (AppConfig
         .set_num_labo(self.curr_labo)
         .set_num_seance(self.curr_seance)
         .set_date_seance(self.curr_date.toString("yyyy-MM-dd"))
         .set_base_source_folder(self.src_dir)
         .save_config())
        self.import_all_files()

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

    def treeDestDirDoubleClicked(self, modelIndex: QModelIndex):
        path = os.path.join(self.base_dest_dir, self.get_path_from_model_index(modelIndex))
        os.startfile(path)

    def treeSrcDirDoubleClicked(self, modelIndex: QModelIndex):
        path = os.path.join(self.src_dir, self.get_path_from_model_index(modelIndex))
        os.startfile(path)

    def get_path_from_model_index(self, modelIndex: QModelIndex):
        path = ""
        item, lastitem = self.ui.treeSrcDir.itemFromIndex(modelIndex), ""
        while item is not None:
            lastitem = item.text(0)
            item = item.parent()
            path = os.path.join(lastitem, path)
        return path        

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

    def display_dest_tree(self, dct: Dict, tree: QTreeWidget, tree_node: QTreeWidgetItem = None):
        if tree_node is None:
            tree.clear()
            new_node = tree
        else:
            new_node = QTreeWidgetItem(tree_node)
            new_node.setText(0, dct["dirname"])
            new_node.setText(1, "DIR")
        for dir in dct["dirs"]:
            self.display_dest_tree(dir, tree, new_node)
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
            median = nbfileslst[len(lst) // 2] if len(lst) % 2 == 1 else (
                (nbfileslst[len(lst) // 2] + nbfileslst[len(lst) // 2-1])/2)
            nb_min_files = nbfileslst[0]
            nb_max_files = nbfileslst[-1]
        return {
            "nbfiles": nbfiles,
            "nbdirs": nbdirs,
            "nb_median_files": median,
            "nb_min_files": nb_min_files,
            "nb_max_files": nb_max_files
        }
    
    def can_import_files(self):
        if self.src_dir == "" or not os.path.exists(self.src_dir):
            return False
        if self.dest_dir == "":
            return False
        return len(self.src_dir_list) > 0
    
    def import_all_files(self):
        for dir in self.src_dir_list:
            copytree(dir["dirpath"], os.path.join(self.dest_dir, dir["dirname"]))
        self.btnDestSearchClicked()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    dlg = DialogCollecte()
    dlg.show()
    sys.exit(app.exec())
