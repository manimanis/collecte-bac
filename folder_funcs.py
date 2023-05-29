import datetime
import os
import re
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


# 
def search_dir_students(base_dir):
    lst = []
    for dirpath, dirnames, filenames in os.walk(base_dir):
        for dirname in dirnames:
            if re.match(r"/\d{6,}/gm", dirname):
                pathname = os.path.join(dirpath, dirname)
                lst.append(pathname)
    return pathname
        