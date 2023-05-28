import datetime
import os

import psutil
import py7zr

from config import AppConfig


def get_numero_seance():
    """Inputs the seance number."""
    while True:
        n = int(input("Numéro de séance [1, 5] (0 pour annuler) ? "))
        if n == 0:
            return None
        elif n < 1 or n > 5:
            print("Numéro incorrect.")
        else:
            return n


def get_nbre_labos():
    """Inputs the number of working labs."""
    while True:
        nbr_labos = int(input("Nombre de labos [1, 10] (0 pour annuler) ? "))
        if nbr_labos == 0:
            return None
        elif nbr_labos < 0 or nbr_labos > 10:
            print("Nombre de labos incorrect.")
        else:
            return nbr_labos


def get_numero_labo():
    """Inputs the working lab."""
    while True:
        num_labo = int(
            input(f"Numéro de labo [1, {AppConfig.NBRE_LABOS}] (0 pour annuler) ? "))
        if num_labo == 0:
            return None
        elif num_labo < 0 or num_labo > AppConfig.NBRE_LABOS:
            print("Nombre de labos incorrect.")
        else:
            return num_labo


def get_action_confirm(msg, options=['O', 'N', 'A'], default=0, cancel_option=2):
    while True:
        rep = input(
            f"{msg} ({' / '.join(('[' if idx == default else '') + option + (']' if idx == default else '') for idx, option in enumerate(options))}) ? ").upper()
        if rep == "":
            rep = options[default]
        if cancel_option != -1 and rep == options[cancel_option]:
            return None
        if rep in options:
            return rep
        print("Réponse incorrecte.")


def get_date(today):
    """Inputs a date using a pattern."""
    print(f"Date système : {today}")
    while True:
        rep = input("Voulez-vous utiliser cette date ([O] / N / A) ? ").upper()
        if rep == "A":
            return None
        elif rep == "N":
            return get_valid_date()
        elif rep in ("", "O"):
            return today
        if rep not in 'NO':
            print("Réponse incorrecte.")


def get_valid_date(default_date):
    """Inputs a valid formatted date"""
    date_format = '%Y-%m-%d'
    while True:
        try:
            new_date = input(
                f"Entrer une date (YYYY-MM-DD) [{default_date}] ? ")
            if new_date == "":
                new_date = default_date
            dateObject = datetime.datetime.strptime(
                new_date, date_format).date()
            return dateObject.isoformat()
        except ValueError:
            print("Format de date incorrect, doit être au format YYYY-MM-DD")


def get_folder(curr_folder=AppConfig.LOCAL_BACKUP_FOLDER):
    """Inputs a folder name."""
    while True:
        base_folder = input(f"Chemin du dossier [{curr_folder}] ? ")
        if base_folder == "":
            base_folder = curr_folder
        if os.path.exists(base_folder) and os.path.isdir(base_folder):
            return base_folder
        else:
            print("Dossier incorrect.")


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


def search_for_labos(folderpath):
    """Search for labos in removable storage."""
    labos = []
    for file in os.listdir(folderpath):
        if file.startswith("Labo") and file[-2:].isdigit():
            dirpath = os.path.join(folderpath, file)
            if not os.path.isdir(dirpath):
                continue
            labos.append({
                "name": file,
                "path": dirpath,
                "seances": search_for_seances_in_labo(dirpath)
            })
    labos.sort(key=lambda labo: labo["name"])
    return labos


def search_for_seances_in_labo(labopath):
    """Searches for seances in labopath."""
    seances = []
    for file in os.listdir(labopath):
        if file.startswith("Séance") and file[-2:].isdigit():
            dirpath = os.path.join(labopath, file)
            if not os.path.isdir(dirpath):
                continue
            seances.append({
                "name": file,
                "path": dirpath
            })
    seances.sort(key=lambda seance: seance["name"])
    return seances


def get_seance_folder_name(base_folder, num_labo, num_seance):
    """Returns the folder path of the folder to be created."""
    return os.path.join(base_folder, f"Labo{num_labo:02d}", f"Séance{num_seance:02d}")


def get_all_labos_folders_names(base_folder, date, num_seance, nbr_labos):
    """Returns the folders names for the specified date, num_seance and nbr_labos"""
    return [os.path.join(base_folder, date, f"Séance{num_seance:02d}", f"Labo{i:02d}") for i in range(1, nbr_labos + 1)]


def get_new_and_existing_folders(folders):
    """Returns a list of new folders to be created and a list of old created folders."""
    existing_dirs = set()
    for folder in folders:
        if os.path.exists(folder):
            existing_dirs.add(folder)
    new_dirs = set(folders) - existing_dirs
    return sorted(new_dirs), sorted(existing_dirs)


def show_new_and_existing_folders(new_dirs, existing_dirs):
    """Show a list of new and existing directories."""
    if len(new_dirs) > 0:
        print("Nouveaux dossiers")
        for dir in new_dirs:
            print(f"+ {dir}")

    if len(existing_dirs) > 0:
        print("Dossies existants")
        for dir in existing_dirs:
            print(f"- {dir}")


def show_labos_folders_info(folders_dict):
    """Shows labos informations in the removable storage.
    [{'name': 'Labo01', 'path': 'E:\\Labo01', 'seances': [{'name': 'Séance02', 'path': 'E:\\Labo01\\Séance02'}]}]"""
    for idx1, dct in enumerate(folders_dict):
        print()
        print(f"{dct['name']}")
        print("-"*(len(dct['name']) * 2))
        for idx2, seance in enumerate(dct["seances"]):
            print(f"{idx1+1}.{idx2+1}. {seance['name']}")
    print()


def fetch_removable_drives_list():
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


def show_removable_drives(drives):
    print("-"*50)
    print("Liste des disques amovibles")
    print("-"*50)
    if len(drives) == 0:
        print("Aucun disque amovible trouvé.")
    else:
        print("N° " + "Lecteur".ljust(10, ' ') + "  Free (MB) Total (MB)")
        for index, drive in enumerate(drives):
            print(
                f"{index+1:>2d} {drive['drive']:<10} {drive['free']//1024**2:>10} {drive['total']//1024**2:>10}")


def is_removable_drive(drive, drives):
    return len([drv['drive'] for drv in drives if drv['drive'] == drive]) > 0


def get_drive_name(drives):
    sel_drive = ""
    while not is_removable_drive(sel_drive, drives):
        n = int(input(f"Numéro du lecteur (0 pour annuler) ? "))
        if n == 0:
            return None
        elif n < 1 or n > len(drives):
            print("Numéro de lecteur incorrect.")
        else:
            sel_drive = drives[n-1]['drive']
    return sel_drive


def fetch_folders_list(basefolder):
    folders = []
    for file in os.listdir(basefolder):
        filepath = os.path.join(basefolder, file)
        if os.path.isdir(filepath):
            folders.append(filepath)
    return folders


def show_folders_list(basefolder, folders):
    print("-"*60)
    print(f"Liste des dossiers dans {basefolder}")
    print("-"*60)
    print()
    nbre_dirs = len(folders)
    idx_size = max(len(str(nbre_dirs)), 3)
    print("N°".rjust(idx_size+1) + " Nom du dossier")
    for index, file in enumerate(folders):
        dirname = os.path.basename(file)
        print(f"{index+1:>{idx_size}d}. {dirname}")


def get_folder_name(folders):
    while True:
        numfolder = int(input("Numéro du dossier (0 pour annuler) ? "))
        if numfolder == 0:
            return None
        elif numfolder < 1 or numfolder > len(folders):
            print("Dossier incorrect.")
        else:
            return folders[numfolder-1]


def zip_folder(input_folder, output_file, password=None):
    """Compress the input folder to an encrypted 7zip file."""
    with py7zr.SevenZipFile(output_file, 'w', password=password) as archive:
        archive.set_encrypted_header(password is not None)
        archive.writeall(input_folder, os.path.basename(input_folder))
