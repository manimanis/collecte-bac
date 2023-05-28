import os
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.uic import loadUi
from PyQt5.QtCore import QDate, QFileSystemWatcher, QStorageInfo
from config import AppConfig
import utility_functions as uf


class ChangeSettingsDialog:
    def __init__(self) -> None:
        self.dlg = loadUi("forms/settings.ui")
        self.dlg.setModal(True)
        self.dlg.btnOk.clicked.connect(self.ok_clicked)
        self.dlg.btnCancel.clicked.connect(self.cancel_clicked)
        self.update_interface()
        self.dlg.exec()
        update_interface()

    def update_interface(self):
        date = QDate.fromString(AppConfig.DATE_SEANCE, "yyyy-MM-dd")
        self.dlg.txtDate.setDate(date)
        self.dlg.txtNumSeance.setValue(AppConfig.NUM_SEANCE)
        self.dlg.txtNbreLabos.setValue(AppConfig.NBRE_LABOS)
        self.dlg.txtLocalDir.setText(AppConfig.LOCAL_BACKUP_FOLDER)
        self.dlg.txtArchiveDir.setText(AppConfig.LOCAL_COMPRESSED_FOLDER)

    def update_settings(self):
        AppConfig.DATE_SEANCE = self.dlg.txtDate.date().toString("yyyy-MM-dd")
        AppConfig.NUM_SEANCE = self.dlg.txtNumSeance.value()
        AppConfig.NBRE_LABOS = self.dlg.txtNbreLabos.value()
        AppConfig.LOCAL_BACKUP_FOLDER = self.dlg.txtLocalDir.text()
        AppConfig.LOCAL_COMPRESSED_FOLDER = self.dlg.txtArchiveDir.text()
        AppConfig.save_config()

    def confirm_create_folder(self, folder):
        if not os.path.exists(folder):
            rep = QMessageBox.question(self.dlg,
                                       "Dossier introuvable",
                                       f"Voulez-vous créer le dossier '{folder}'",
                                       QMessageBox.Yes | QMessageBox.No)
            if rep == QMessageBox.Yes:
                if not uf.create_folder(folder):
                    QMessageBox.information(self.dlg,
                                            "Erreur",
                                            f"Impossible de créer le dossier '{folder}'")
                    return False
        return False

    def ok_clicked(self):
        local_dir = os.path.normpath(self.dlg.txtLocalDir.text())
        archive_dir = os.path.normpath(self.dlg.txtArchiveDir.text())
        if not os.path.isabs(local_dir):
            QMessageBox.warning(self.dlg, "Dossier incorrect",
                                "Vérifier le nom du dossier local.")
            return
        if not os.path.exists(local_dir) and not self.confirm_create_folder(local_dir):
            return
        if not os.path.isabs(archive_dir):
            QMessageBox.warning(self.dlg, "Dossier incorrect",
                                "Vérifier le nom du dossier d'archives.")
            return
        if not os.path.exists(archive_dir) and not self.confirm_create_folder(archive_dir):
            return
        self.update_settings()
        self.cancel_clicked()

    def cancel_clicked(self):
        self.dlg.close()


class CreateBackupDirsDialog:
    def __init__(self) -> None:
        self.dlg = loadUi("forms/backup_dir_create.ui")
        self.dlg.setModal(True)
        self.dlg.btnCancel.clicked.connect(self.cancel_clicked)
        self.dlg.btnCreateFolders.clicked.connect(self.create_dirs)
        self.dlg.btnOpenFolder.clicked.connect(self.open_folder)
        self.folders, self.new_dirs, self.existing_dirs = None, None, None
        self.update_interface()
        self.dlg.exec()

    def update_interface(self):
        self.folders = uf.get_all_labos_folders_names(
            AppConfig.LOCAL_BACKUP_FOLDER,
            AppConfig.DATE_SEANCE,
            AppConfig.NUM_SEANCE,
            AppConfig.NBRE_LABOS
        )
        self.new_dirs, self.existing_dirs = uf.get_new_and_existing_folders(
            self.folders)
        self.dlg.txtDirList.appendPlainText("")
        self.dlg.btnCreateFolders.setEnabled(len(self.new_dirs) > 0)
        self.dlg.txtDirList.appendPlainText(
            f"Dossier local : {AppConfig.LOCAL_BACKUP_FOLDER}")
        self.dlg.txtDirList.appendPlainText(
            f"Nbre de labos: {AppConfig.NBRE_LABOS:>2d}")
        if len(self.existing_dirs) > 0:
            self.dlg.txtDirList.appendPlainText("")
            self.dlg.txtDirList.appendPlainText("Dossiers existants")
            self.display_list(self.existing_dirs)
        if len(self.new_dirs) > 0:
            self.dlg.txtDirList.appendPlainText("")
            self.dlg.txtDirList.appendPlainText("Nouveaux dossiers à créer")
            self.display_list(self.new_dirs)
        else:
            self.dlg.txtDirList.appendPlainText("")
            self.dlg.txtDirList.appendPlainText("Aucun dossier à créer.")

    def display_list(self, arr):
        for item in arr:
            self.dlg.txtDirList.appendPlainText(item)

    def open_folder(self):
        os.startfile(AppConfig.LOCAL_BACKUP_FOLDER)

    def create_dirs(self):
        nbr_doss = uf.create_many_folders(self.new_dirs)
        self.dlg.txtDirList.appendPlainText("")
        self.dlg.txtDirList.appendPlainText(
            f"{nbr_doss} / {len(self.new_dirs)} dossiers créés.")
        self.update_interface()

    def cancel_clicked(self):
        self.dlg.close()


class CreateRemovableDirsDialog:
    def __init__(self) -> None:
        self.dlg = loadUi("forms/removable_dir_create.ui")
        self.dlg.setModal(True)
        self.dlg.btnCancel.clicked.connect(self.cancel_clicked)
        self.dlg.btnCreateFolders.clicked.connect(self.create_dirs)
        self.dlg.btnOpenFolder.clicked.connect(self.open_folder)
        self.dlg.btnUpdateList.clicked.connect(self.update_removable_drives)
        self.dlg.cmbDrives.currentIndexChanged.connect(self.user_input_changed)
        self.dlg.txtNumLabo.valueChanged.connect(self.user_input_changed)
        self.folders, self.new_dirs, self.existing_dirs = None, None, None
        self.drive = None
        self.update_interface()
        self.dlg.exec()

    def user_input_changed(self):
        if self.dlg.cmbDrives.currentIndex() == -1:
            self.dlg.btnCreateFolders.setEnabled(False)
            return
        self.drive = self.drives[self.dlg.cmbDrives.currentIndex()]['drive']
        self.folder_path = uf.get_seance_folder_name(self.drive, self.dlg.txtNumLabo.value(), AppConfig.NUM_SEANCE)
        self.dlg.txtTargetDir.setText(self.folder_path)

    def update_removable_drives(self):
        self.drives = uf.fetch_removable_drives_list()
        self.dlg.cmbDrives.clear()
        for drive in self.drives:
            self.dlg.cmbDrives.addItem(
                f"{drive['drive']}\t(Libre : {drive['free']//1024**2}MB)\t(Libre : {drive['total']//1024**2}MB)"
            )

    def display_list(self, arr):
        for item in arr:
            self.dlg.txtDirList.appendPlainText(item)

    def update_interface(self):
        self.update_removable_drives()
        self.dlg.txtNumLabo.setMaximum(AppConfig.NBRE_LABOS)

    def cancel_clicked(self):
        self.dlg.close()

    def create_dirs(self):
        drive = self.drives[self.dlg.cmbDrives.currentIndex()]['drive']
        folder_path = uf.get_seance_folder_name(drive, self.dlg.txtNumLabo.value(), AppConfig.NUM_SEANCE)
        new_dirs, existing_dirs = uf.get_new_and_existing_folders([folder_path])
        if len(existing_dirs) > 0:
            self.dlg.txtDirList.appendPlainText("Dossiers existants")
            self.display_list(existing_dirs)
        if len(new_dirs) > 0:
            self.dlg.txtDirList.appendPlainText("Nouveaux dossiers à créer")
            self.display_list(new_dirs)
            
            nbr_doss = uf.create_many_folders(new_dirs)
            if nbr_doss != 0:
                self.dlg.txtDirList.appendPlainText("Dossier créé.")
            else:
                self.dlg.txtDirList.appendPlainText("Erreur lors de la création du dossier.")
        else:
            self.dlg.txtDirList.appendPlainText("Aucun dossier à créer.")

    def open_folder(self):
        os.startfile(self.drives[self.dlg.cmbDrives.currentIndex()]['drive'])


def create_backup_dirs():
    _ = CreateBackupDirsDialog()


def change_settings():
    _ = ChangeSettingsDialog()


def create_removable_dirs():
    _ = CreateRemovableDirsDialog()


def update_interface():
    win_main.txtDate.setText(AppConfig.DATE_SEANCE)
    win_main.txtSeance.setText(str(AppConfig.NUM_SEANCE))
    win_main.txtNbreLabos.setText(str(AppConfig.NBRE_LABOS))
    win_main.txtLocalDir.setText(AppConfig.LOCAL_BACKUP_FOLDER)
    win_main.txtArchiveDir.setText(AppConfig.LOCAL_COMPRESSED_FOLDER)


# PP
app = QApplication([])
win_main = loadUi("forms/mainwindow.ui")
win_main.show()
win_main.btnChangeDefaults.clicked.connect(change_settings)
win_main.btnCreateBackupFolders.clicked.connect(create_backup_dirs)
win_main.btnCreateRemovableFolders.clicked.connect(create_removable_dirs)
update_interface()
app.exec()
