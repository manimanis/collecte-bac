import datetime
import os
import re
import shutil
from typing import List, Tuple
import psutil
import py7zr

from .config import AppConfig


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
def human_filesize_unit(filesize):
    unit = ["B", "KB", "MB", "GB"]
    i = 0
    while filesize > 512:
        filesize /= 1024
        i += 1
    return f"{filesize:3.1f}{unit[i]}"


def search_dir_students(base_dir):   
    def find_students_folders(dirpath):
        lst = []
        for filename in os.listdir(base_dir):
            pathname = os.path.join(dirpath, filename)
            if folder_exists(pathname) and re.match(r"\d{6,}", filename):
                dct = {
                    "dirname": filename,
                    "dirpath": pathname,
                    "files": [],
                    "dirs": [],
                    "totalsize": 0
                }
                lst.append(dct)
        return lst
    
    def find_elements(lst):
        for item in lst:
            for dirpath, dirnames, filenames in os.walk(item["dirpath"]):
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    dct = {
                        "filename": filename,
                        "filepath": filepath,
                        "filesize": os.path.getsize(filepath)
                    }
                    item["files"].append(dct)
                    item["totalsize"] += dct["filesize"]
                for dirname in dirnames:
                    item["dirs"].append(dirname)


    lst = find_students_folders(base_dir)
    find_elements(lst)
    return lst
    
