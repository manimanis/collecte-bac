import datetime
import os
import shutil
from typing import List, Tuple
import psutil
import py7zr

from config import AppConfig


# Fonctions génériques


def create_many_folders(folderarr):
    """Creates folders for the corresponding date, seance and number of labs"""
    n, cree = len(folderarr), 0
    for folderpath in folderarr:
        cree += create_folder(folderpath)
    return cree


def create_folder(folderpath):
    """Creates a folder for the given num_seance"""
    if not os.path.exists(folderpath):
        try:
            os.makedirs(folderpath)
            return True
        except Exception:
            return False
    return False


def folder_exists(folderpath):
    return os.path.exists(folderpath) and os.path.isdir(folderpath)


def file_exists(filepath):
    return os.path.exists(filepath) and os.path.isfile(filepath)


def copytree(src: str, dest: str, overwrite=False) -> bool:
    """Copy all of the folder contents from the usb stick to the local folder."""
    try:
        shutil.copytree(src, dest, dirs_exist_ok=overwrite)
        return True
    except Exception:
        return False


def zip_folder(input_folder, output_file, password=None):
    """Compress the input folder to an encrypted 7zip file."""
    with py7zr.SevenZipFile(output_file, 'w', password=password) as archive:
        archive.set_encrypted_header(password is not None)
        archive.writeall(input_folder, os.path.basename(input_folder))


# Fonctions relatives au lecteur amovible


def fetch_removable_drives_list() -> List:
    """Returns the list of removable drives connected to the current PC."""
    drives = []
    for partition in psutil.disk_partitions():
        if 'removable' in partition.opts.split(","):
            du = psutil.disk_usage(partition.mountpoint)
            drives.append({
                "drive": partition.mountpoint,
                "total": du.total,
                "free": du.free
            })
    return drives


def usb_ident_filepath(base_folder: str) -> str:
    """Returns the usb_identity.dat filepath."""
    return os.path.join(base_folder, "usb_identity.txt")


def write_usb_ident_file(base_folder: str, curr_date: str, num_labo: int, num_seance: int) -> bool:
    """Prepare the removable drive to accept the pupil's work."""
    id_file = usb_ident_filepath(base_folder)
    try:
        with open(id_file, "w") as f:
            f.write(str({
                "current_date": curr_date,
                "num_labo": num_labo,
                "num_seance": num_seance
            }))
        return True
    except Exception:
        return False


def read_usb_ident_file(base_folder: str) -> dict:
    """Read information from the removable drive.
    Returns current_date, num_labo, num_seance, or None if failed."""
    if not has_usb_ident_file(base_folder):
        return None
    id_file = usb_ident_filepath(base_folder)
    with open(id_file, "rb") as f:
        dct = eval(f.read())
    return dct


def has_usb_ident_file(base_folder: str) -> bool:
    """Returns if identification file exists on the specified path."""
    id_file = usb_ident_filepath(base_folder)
    return folder_exists(base_folder) and file_exists(id_file)


def usb_work_dirpath(base_folder: str) -> str:
    """Returns the students works based on identification file.
    If no identification file returns None."""
    if not has_usb_ident_file(base_folder):
        return None
    id = read_usb_ident_file(base_folder)
    return os.path.join(base_folder, f"Labo{id['num_labo']:02d}", f"Séance{id['num_seance']:02d}")


def usb_work_dir_exists(base_folder: str) -> bool:
    """Returns True if the students dir exists on removable storage, False otherwise."""
    dirpath = usb_work_dirpath(base_folder)
    return folder_exists(base_folder) and folder_exists(dirpath)


def usb_work_dir_create(base_folder: str) -> bool:
    """Create the students work directory on removable storage.
    Return True if successfully created or already exists."""
    dirpath = usb_work_dirpath(base_folder)
    return usb_work_dir_exists(base_folder) or create_folder(dirpath)


def usb_work_dir_contents(base_folder: str) -> List:
    """Return a list of all of the students directory contents."""
    file_list = []
    if not usb_work_dir_exists(base_folder):
        return file_list
    dirpath = usb_work_dirpath(base_folder)
    for basepath, dirnames, filenames in os.walk(dirpath):
        dct = {
            "folder": basepath,
            "dirs": dirnames,
            "files": []
        }
        for filename in filenames:
            filepath = os.path.join(basepath, filename)
            filesize = os.path.getsize(filepath)
            dct["files"].append({
                "filename": filename,
                "size": filesize
            })
        file_list.append(dct)
    return file_list


def usb_work_dir_delete(base_folder: str) -> bool:
    """Remove the usb work folder after saving successfully all of the students works."""
    usb_path = usb_work_dirpath(base_folder)
    if usb_path is None:
        return False
    try:
        shutil.rmtree(usb_path)
        return True
    except Exception:
        return False


def local_work_day_dirpath(local_folder: str = None, date: str = None) -> str:
    """Returns the local dir without séances where the students work will be backup.
    base_folder defaults to AppConfig.LOCAL_BACKUP_FOLDER
    date defaults to AppConfig.DATE_SEANCE"""
    if local_folder is None:
        local_folder = AppConfig.LOCAL_BACKUP_FOLDER
    if date is None:
        date = AppConfig.DATE_SEANCE
    return os.path.join(local_folder, date)


def local_work_dirpath(local_folder: str = None, date: str = None, num_seance: int = None):
    """Returns the local dir where the students work will be backup.
    base_folder defaults to AppConfig.LOCAL_BACKUP_FOLDER
    date defaults to AppConfig.DATE_SEANCE
    num_seance defaults to AppConfig.NUM_SEANCE"""
    if num_seance is None:
        num_seance = AppConfig.NUM_SEANCE
    return os.path.join(local_work_day_dirpath(local_folder, date), f"Séance{num_seance:02d}")


def local_dir_work_to_student_work_backup(base_folder: str) -> str:
    """Returns the dir path where the students works should be saved to from the usb stick.
    Return None if no usb memory is attached."""
    ident = read_usb_ident_file(base_folder)
    if ident is None:
        return None
    return os.path.join(
        local_work_dirpath(date=ident['current_date'],
                           num_seance=ident['num_seance']),
        f"Labo{ident['num_labo']}"
    )


def local_dir_work_create(base_folder: str) -> bool:
    """Creates the local folder where the students work should be saved.
    Return True if the operation succeeds or False otherwise."""
    localdir = local_dir_work_to_student_work_backup(base_folder)
    if folder_exists(localdir):
        return True
    return create_folder(localdir)


def local_dir_work_copy_info(base_folder: str) -> Tuple:
    """Returns a tuple that indicate which folder of usb stick would be copied to which local folder."""
    usb_path = usb_work_dirpath(base_folder)
    local_path = local_dir_work_to_student_work_backup(base_folder)
    return usb_path, local_path


def local_dir_work_copy(base_folder: str, overwite: bool = False) -> bool:
    """Copy all of the folder contents from the usb stick to the local folder.
    If overwrite is False the operation will fails if the local folder exists.
    If overwrite is True the local folder will be overwritten with the new data from the usb stick."""
    usb_path, local_path = local_dir_work_copy_info(base_folder)
    return copytree(usb_path, local_path, overwite)


def archive_dir_filepath(archive_folder, date) -> str:
    return os.path.join(archive_folder, f"{date}.7z")


def archive_dir_compress(local_folder=None, date=None, archive_folder=None, password=None) -> bool:
    if local_folder is None:
        local_folder = AppConfig.LOCAL_BACKUP_FOLDER
    if date is None:
        date = AppConfig.DATE_SEANCE
    if archive_folder is None:
        archive_folder = AppConfig.LOCAL_COMPRESSED_FOLDER
    localdir = local_work_day_dirpath(local_folder, date)
    dest_file = archive_dir_filepath(archive_folder, date)
    try:
        zip_folder(localdir, dest_file, password)
        return dest_file
    except Exception:
        return ""


drives = fetch_removable_drives_list()
if len(drives) == 0:
    exit()
drive = drives[0]['drive']
if has_usb_ident_file(drive):
    print("Identification file found.")
    dct = read_usb_ident_file(drive)
    print(dct)
else:
    print("Identification file not found.")
    write_usb_ident_file(drive, datetime.date.today().isoformat(), 1, 1)
    exit()
if not usb_work_dir_exists(drive):
    print("Student folder absent.")
    usb_work_dir_create(drive)
    exit()
else:
    print(usb_work_dir_contents(drive))
    print("Students work to be transferred to:",
          local_dir_work_to_student_work_backup(drive))
    if local_dir_work_copy(drive):
        print("Copy success.")
    else:
        print("Copy failed.")
    file = archive_dir_compress()
    if file != "":
        print("Compressed successfully in:", file)
    else:
        print("Compressing failed.")
