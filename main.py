import os
from pprint import pprint
from typing import Dict, List
from forms.collecte import Ui_Dialog as DialogCollecteBase
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QApplication, QTreeWidget, QTreeWidgetItem, QMessageBox
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
        self.dest_dir_contents = {}

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

        if "dirs" in self.dest_dir_contents:
            self.ui.txtDestNbrDirs.setText(f"{len(self.dest_dir_contents['dirs'])} Dossiers")
        if "num_files" in self.dest_dir_contents:
            self.ui.txtDestNbrTotalFiles.setText(f"{self.dest_dir_contents['num_files']} Fichiers")
        if "num_dirs" in self.dest_dir_contents:
            self.ui.txtDestNbrTotalDirs.setText(f"{self.dest_dir_contents['num_dirs']} Dossiers")

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
        self.refresh_dest_tree()

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
        self.refresh_dest_tree()

    def seanceChanged(self, newSeance):
        self.curr_seance = self.ui.txtSeance.value()
        self.update_dest_dir()
        self.updateInterface()
        self.refresh_dest_tree()

    def laboChanged(self, newLabo):
        self.curr_labo = self.ui.txtLabo.value()
        self.update_dest_dir()
        self.updateInterface()
        self.refresh_dest_tree()

    def treeDestDirDoubleClicked(self, modelIndex: QModelIndex):
        path = os.path.join(
            self.dest_dir, self.get_path_from_model_index(modelIndex))
        os.startfile(path)

    def treeSrcDirDoubleClicked(self, modelIndex: QModelIndex):
        path = os.path.join(
            self.src_dir, self.get_path_from_model_index(modelIndex))
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

    def refresh_dest_tree(self):
        self.ui.treeDestDir.clear()
        if not os.path.exists(self.dest_dir):
            return
        self.dest_dir_contents = search_folder_contents(self.dest_dir)
        self.dest_dir_summ = self.summarize_dest_dir(self.dest_dir_contents)
        pprint(self.dest_dir_summ)
        self.display_dest_tree(self.dest_dir_contents, self.ui.treeDestDir)
        self.updateInterface()

    def display_dest_tree(self, dct: Dict, tree: QTreeWidget, tree_node: QTreeWidgetItem = None, level: int = 0):
        if tree_node is None:
            new_node = tree
        else:
            new_node = QTreeWidgetItem(tree_node)
            new_node.setText(0, dct["dirname"])
            new_node.setText(1, "DIR")
            if level == 1:
                new_node.setText(
                    2,
                    f"{dct['num_files']}F" +
                    (f" / {dct['num_dirs']}D" if dct['num_dirs'] > 0 else "")
                )
        for dir in dct["dirs"]:
            self.display_dest_tree(dir, tree, new_node, level + 1)
        for file in dct["files"]:
            file_node = QTreeWidgetItem(new_node)
            file_node.setText(0, file["filename"])
            file_node.setText(1, "Fichier")
            file_node.setText(2, human_filesize_unit(file["filesize"]))
            file_node.setTextAlignment(1, Qt.AlignmentFlag.AlignRight)
        tree.expandAll()
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
    
    def summarize_dest_dir(self, dir_dict: Dict, summ_dict: Dict = None):
        if summ_dict is None:
            summ_dict = {
                "files": {}
            }
        for file in dir_dict["files"]:
            if file["filename"] not in summ_dict["files"]:
                summ_dict["files"][file["filename"]] = {
                    "count": 1,
                    "min_size": file["filesize"],
                    "max_size": file["filesize"],
                    "locations": [file["filepath"]]
                }
            else:
                summ_dict["files"][file["filename"]]["count"] += 1
                summ_dict["files"][file["filename"]]["min_size"] = min(summ_dict["files"][file["filename"]]["min_size"], file["filesize"])
                summ_dict["files"][file["filename"]]["max_size"] = max(summ_dict["files"][file["filename"]]["max_size"], file["filesize"])
                summ_dict["files"][file["filename"]]["locations"].append(file["filepath"])
        for dir in dir_dict["dirs"]:
            self.summarize_dest_dir(dir, summ_dict)
        return summ_dict

    def can_import_files(self):
        if self.src_dir == "" or not os.path.exists(self.src_dir):
            return False
        if self.dest_dir == "":
            return False
        return len(self.src_dir_list) > 0

    def import_all_files(self):
        if not os.path.exists(self.dest_dir):
            os.makedirs(self.dest_dir)
        for dir in self.src_dir_list:
            copytree(dir["dirpath"], os.path.join(
                self.dest_dir, dir["dirname"]))
        self.refresh_dest_tree()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    dlg = DialogCollecte()
    dlg.show()
    sys.exit(app.exec())


{'dirname': 'Labo01',
 'dirpath': 'C:\\Users\\Cyberbox\\Bac2023\\2023-05-31\\Seance01\\Labo01',
 'dirs': [{'dirname': '314882',
           'dirpath': 'C:\\Users\\Cyberbox\\Bac2023\\2023-05-31\\Seance01\\Labo01\\314882',
           'dirs': [{'dirname': 'dir01',
                     'dirpath': 'C:\\Users\\Cyberbox\\Bac2023\\2023-05-31\\Seance01\\Labo01\\314882\\dir01',
                     'dirs': [],
                     'files': [{'filename': 'anotherfile.txt',
                                'filepath': 'C:\\Users\\Cyberbox\\Bac2023\\2023-05-31\\Seance01\\Labo01\\314882\\dir01\\anotherfile.txt',
                                'filesize': 301}],
                     'num_dirs': 0,
                     'num_files': 1,
                     'totalsize': 301}],
           'files': [{'filename': 'file01.txt',
                      'filepath': 'C:\\Users\\Cyberbox\\Bac2023\\2023-05-31\\Seance01\\Labo01\\314882\\file01.txt',
                      'filesize': 330},
                     {'filename': 'file02.txt',
                      'filepath': 'C:\\Users\\Cyberbox\\Bac2023\\2023-05-31\\Seance01\\Labo01\\314882\\file02.txt',
                      'filesize': 642}],
           'num_dirs': 1,
           'num_files': 3,
           'totalsize': 1273},
          {'dirname': '314883',
           'dirpath': 'C:\\Users\\Cyberbox\\Bac2023\\2023-05-31\\Seance01\\Labo01\\314883',
           'dirs': [{'dirname': 'dir05',
                     'dirpath': 'C:\\Users\\Cyberbox\\Bac2023\\2023-05-31\\Seance01\\Labo01\\314883\\dir05',
                     'dirs': [],
                     'files': [{'filename': 'anotherfile.txt',
                                'filepath': 'C:\\Users\\Cyberbox\\Bac2023\\2023-05-31\\Seance01\\Labo01\\314883\\dir05\\anotherfile.txt',
                                'filesize': 584}],
                     'num_dirs': 0,
                     'num_files': 1,
                     'totalsize': 584},
                    {'dirname': 'dir07',
                     'dirpath': 'C:\\Users\\Cyberbox\\Bac2023\\2023-05-31\\Seance01\\Labo01\\314883\\dir07',
                     'dirs': [],
                     'files': [{'filename': 'anotherfile.txt',
                                'filepath': 'C:\\Users\\Cyberbox\\Bac2023\\2023-05-31\\Seance01\\Labo01\\314883\\dir07\\anotherfile.txt',
                                'filesize': 520}],
                     'num_dirs': 0,
                     'num_files': 1,
                     'totalsize': 520}],
           'files': [{'filename': 'file01.txt',
                      'filepath': 'C:\\Users\\Cyberbox\\Bac2023\\2023-05-31\\Seance01\\Labo01\\314883\\file01.txt',
                      'filesize': 351},
                     {'filename': 'file02.txt',
                      'filepath': 'C:\\Users\\Cyberbox\\Bac2023\\2023-05-31\\Seance01\\Labo01\\314883\\file02.txt',
                      'filesize': 119}],
           'num_dirs': 2,
           'num_files': 4,
           'totalsize': 1574},
          {'dirname': '314884',
           'dirpath': 'C:\\Users\\Cyberbox\\Bac2023\\2023-05-31\\Seance01\\Labo01\\314884',
           'dirs': [{'dirname': 'dir04',
                     'dirpath': 'C:\\Users\\Cyberbox\\Bac2023\\2023-05-31\\Seance01\\Labo01\\314884\\dir04',
                     'dirs': [],
                     'files': [{'filename': 'anotherfile.txt',
                                'filepath': 'C:\\Users\\Cyberbox\\Bac2023\\2023-05-31\\Seance01\\Labo01\\314884\\dir04\\anotherfile.txt',
                                'filesize': 420}],
                     'num_dirs': 0,
                     'num_files': 1,
                     'totalsize': 420},
                    {'dirname': 'dir08',
                     'dirpath': 'C:\\Users\\Cyberbox\\Bac2023\\2023-05-31\\Seance01\\Labo01\\314884\\dir08',
                     'dirs': [],
                     'files': [{'filename': 'anotherfile.txt',
                                'filepath': 'C:\\Users\\Cyberbox\\Bac2023\\2023-05-31\\Seance01\\Labo01\\314884\\dir08\\anotherfile.txt',
                                'filesize': 155}],
                     'num_dirs': 0,
                     'num_files': 1,
                     'totalsize': 155}],
           'files': [{'filename': 'file01.txt',
                      'filepath': 'C:\\Users\\Cyberbox\\Bac2023\\2023-05-31\\Seance01\\Labo01\\314884\\file01.txt',
                      'filesize': 450},
                     {'filename': 'file02.txt',
                      'filepath': 'C:\\Users\\Cyberbox\\Bac2023\\2023-05-31\\Seance01\\Labo01\\314884\\file02.txt',
                      'filesize': 308}],
           'num_dirs': 2,
           'num_files': 4,
           'totalsize': 1333},
          {'dirname': '314885',
           'dirpath': 'C:\\Users\\Cyberbox\\Bac2023\\2023-05-31\\Seance01\\Labo01\\314885',
           'dirs': [{'dirname': 'dir09',
                     'dirpath': 'C:\\Users\\Cyberbox\\Bac2023\\2023-05-31\\Seance01\\Labo01\\314885\\dir09',
                     'dirs': [],
                     'files': [{'filename': 'anotherfile.txt',
                                'filepath': 'C:\\Users\\Cyberbox\\Bac2023\\2023-05-31\\Seance01\\Labo01\\314885\\dir09\\anotherfile.txt',
                                'filesize': 112}],
                     'num_dirs': 0,
                     'num_files': 1,
                     'totalsize': 112}],
           'files': [{'filename': 'file01.txt',
                      'filepath': 'C:\\Users\\Cyberbox\\Bac2023\\2023-05-31\\Seance01\\Labo01\\314885\\file01.txt',
                      'filesize': 398},
                     {'filename': 'file02.txt',
                      'filepath': 'C:\\Users\\Cyberbox\\Bac2023\\2023-05-31\\Seance01\\Labo01\\314885\\file02.txt',
                      'filesize': 692}],
           'num_dirs': 1,
           'num_files': 3,
           'totalsize': 1202},
          {'dirname': '314886',
           'dirpath': 'C:\\Users\\Cyberbox\\Bac2023\\2023-05-31\\Seance01\\Labo01\\314886',
           'dirs': [],
           'files': [{'filename': 'file01.txt',
                      'filepath': 'C:\\Users\\Cyberbox\\Bac2023\\2023-05-31\\Seance01\\Labo01\\314886\\file01.txt',
                      'filesize': 131},
                     {'filename': 'file02.txt',
                      'filepath': 'C:\\Users\\Cyberbox\\Bac2023\\2023-05-31\\Seance01\\Labo01\\314886\\file02.txt',
                      'filesize': 472}],
           'num_dirs': 0,
           'num_files': 2,
           'totalsize': 603},
          {'dirname': '314887',
           'dirpath': 'C:\\Users\\Cyberbox\\Bac2023\\2023-05-31\\Seance01\\Labo01\\314887',
           'dirs': [{'dirname': 'dir08',
                     'dirpath': 'C:\\Users\\Cyberbox\\Bac2023\\2023-05-31\\Seance01\\Labo01\\314887\\dir08',
                     'dirs': [],
                     'files': [{'filename': 'anotherfile.txt',
                                'filepath': 'C:\\Users\\Cyberbox\\Bac2023\\2023-05-31\\Seance01\\Labo01\\314887\\dir08\\anotherfile.txt',
                                'filesize': 446}],
                     'num_dirs': 0,
                     'num_files': 1,
                     'totalsize': 446}],
           'files': [{'filename': 'file01.txt',
                      'filepath': 'C:\\Users\\Cyberbox\\Bac2023\\2023-05-31\\Seance01\\Labo01\\314887\\file01.txt',
                      'filesize': 528},
                     {'filename': 'file02.txt',
                      'filepath': 'C:\\Users\\Cyberbox\\Bac2023\\2023-05-31\\Seance01\\Labo01\\314887\\file02.txt',
                      'filesize': 386}],
           'num_dirs': 1,
           'num_files': 3,
           'totalsize': 1360},
          {'dirname': '314888',
           'dirpath': 'C:\\Users\\Cyberbox\\Bac2023\\2023-05-31\\Seance01\\Labo01\\314888',
           'dirs': [{'dirname': 'dir05',
                     'dirpath': 'C:\\Users\\Cyberbox\\Bac2023\\2023-05-31\\Seance01\\Labo01\\314888\\dir05',
                     'dirs': [],
                     'files': [{'filename': 'anotherfile.txt',
                                'filepath': 'C:\\Users\\Cyberbox\\Bac2023\\2023-05-31\\Seance01\\Labo01\\314888\\dir05\\anotherfile.txt',
                                'filesize': 383}],
                     'num_dirs': 0,
                     'num_files': 1,
                     'totalsize': 383}],
           'files': [{'filename': 'file01.txt',
                      'filepath': 'C:\\Users\\Cyberbox\\Bac2023\\2023-05-31\\Seance01\\Labo01\\314888\\file01.txt',
                      'filesize': 469},
                     {'filename': 'file02.txt',
                      'filepath': 'C:\\Users\\Cyberbox\\Bac2023\\2023-05-31\\Seance01\\Labo01\\314888\\file02.txt',
                      'filesize': 258}],
           'num_dirs': 1,
           'num_files': 3,
           'totalsize': 1110},
          {'dirname': '314889',
           'dirpath': 'C:\\Users\\Cyberbox\\Bac2023\\2023-05-31\\Seance01\\Labo01\\314889',
           'dirs': [],
           'files': [{'filename': 'file01.txt',
                      'filepath': 'C:\\Users\\Cyberbox\\Bac2023\\2023-05-31\\Seance01\\Labo01\\314889\\file01.txt',
                      'filesize': 257},
                     {'filename': 'file02.txt',
                      'filepath': 'C:\\Users\\Cyberbox\\Bac2023\\2023-05-31\\Seance01\\Labo01\\314889\\file02.txt',
                      'filesize': 352}],
           'num_dirs': 0,
           'num_files': 2,
           'totalsize': 609},
          {'dirname': '314890',
           'dirpath': 'C:\\Users\\Cyberbox\\Bac2023\\2023-05-31\\Seance01\\Labo01\\314890',
           'dirs': [{'dirname': 'dir06',
                     'dirpath': 'C:\\Users\\Cyberbox\\Bac2023\\2023-05-31\\Seance01\\Labo01\\314890\\dir06',
                     'dirs': [],
                     'files': [{'filename': 'anotherfile.txt',
                                'filepath': 'C:\\Users\\Cyberbox\\Bac2023\\2023-05-31\\Seance01\\Labo01\\314890\\dir06\\anotherfile.txt',
                                'filesize': 701}],
                     'num_dirs': 0,
                     'num_files': 1,
                     'totalsize': 701},
                    {'dirname': 'dir09',
                     'dirpath': 'C:\\Users\\Cyberbox\\Bac2023\\2023-05-31\\Seance01\\Labo01\\314890\\dir09',
                     'dirs': [],
                     'files': [{'filename': 'anotherfile.txt',
                                'filepath': 'C:\\Users\\Cyberbox\\Bac2023\\2023-05-31\\Seance01\\Labo01\\314890\\dir09\\anotherfile.txt',
                                'filesize': 436}],
                     'num_dirs': 0,
                     'num_files': 1,
                     'totalsize': 436}],
           'files': [{'filename': 'file01.txt',
                      'filepath': 'C:\\Users\\Cyberbox\\Bac2023\\2023-05-31\\Seance01\\Labo01\\314890\\file01.txt',
                      'filesize': 203},
                     {'filename': 'file02.txt',
                      'filepath': 'C:\\Users\\Cyberbox\\Bac2023\\2023-05-31\\Seance01\\Labo01\\314890\\file02.txt',
                      'filesize': 97}],
           'num_dirs': 2,
           'num_files': 4,
           'totalsize': 1437},
          {'dirname': '314891',
           'dirpath': 'C:\\Users\\Cyberbox\\Bac2023\\2023-05-31\\Seance01\\Labo01\\314891',
           'dirs': [{'dirname': 'dir05',
                     'dirpath': 'C:\\Users\\Cyberbox\\Bac2023\\2023-05-31\\Seance01\\Labo01\\314891\\dir05',
                     'dirs': [],
                     'files': [{'filename': 'anotherfile.txt',
                                'filepath': 'C:\\Users\\Cyberbox\\Bac2023\\2023-05-31\\Seance01\\Labo01\\314891\\dir05\\anotherfile.txt',
                                'filesize': 585}],
                     'num_dirs': 0,
                     'num_files': 1,
                     'totalsize': 585}],
           'files': [{'filename': 'file01.txt',
                      'filepath': 'C:\\Users\\Cyberbox\\Bac2023\\2023-05-31\\Seance01\\Labo01\\314891\\file01.txt',
                      'filesize': 646},
                     {'filename': 'file02.txt',
                      'filepath': 'C:\\Users\\Cyberbox\\Bac2023\\2023-05-31\\Seance01\\Labo01\\314891\\file02.txt',
                      'filesize': 224}],
           'num_dirs': 1,
           'num_files': 3,
           'totalsize': 1455}],
 'files': [],
 'num_dirs': 21,
 'num_files': 31,
 'totalsize': 11956}