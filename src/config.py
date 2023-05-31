import datetime
import os
import configparser
import sys


class AppConfig:
    LOCAL_BACKUP_FOLDER = ""
    LOCAL_COMPRESSED_FOLDER = ""
    BASE_SOURCE_FOLDER = ""
    ANNEE_SCOLAIRE = 2023
    NUM_SEANCE = 1
    NUM_LABO = 1
    DATE_SEANCE = datetime.date.today().isoformat()
    NBRE_LABOS = 4

    def set_local_backup_folder(newFolder: str):
        AppConfig.LOCAL_BACKUP_FOLDER = newFolder
        return AppConfig

    def set_local_compressed_folder(newFolder: str):
        AppConfig.LOCAL_COMPRESSED_FOLDER = newFolder
        return AppConfig
    
    def set_num_seance(newNum: int):
        AppConfig.NUM_SEANCE = newNum
        return AppConfig
    
    def set_num_labo(newNum: int):
        AppConfig.NUM_LABO = newNum
        return AppConfig
    
    def set_nbre_labos(newNbre: int):
        AppConfig.NBRE_LABOS = newNbre
        return AppConfig
    
    def set_date_seance(newDate: str):
        AppConfig.DATE_SEANCE = newDate
        return AppConfig

    def set_base_source_folder(newFolder: str):
        AppConfig.BASE_SOURCE_FOLDER = newFolder
        return AppConfig
    
    def default_config_windows():
        AppConfig.LOCAL_BACKUP_FOLDER = f"D:\\Backup\\Bac{AppConfig.ANNEE_SCOLAIRE}"
        AppConfig.LOCAL_COMPRESSED_FOLDER = f"D:\\Users\\hp\\Backup\\Bac{AppConfig.ANNEE_SCOLAIRE}"
        AppConfig.BASE_SOURCE_FOLDER = ""
    
    def default_config_linux():
        home_dir = os.path.expanduser("~")
        AppConfig.LOCAL_BACKUP_FOLDER = os.path.join(home_dir, f"Bac{AppConfig.ANNEE_SCOLAIRE}")
        AppConfig.LOCAL_COMPRESSED_FOLDER = os.path.join(home_dir, "archive", f"Bac{AppConfig.ANNEE_SCOLAIRE}")
        AppConfig.BASE_SOURCE_FOLDER = ""
    
    def load_config():
        if sys.platform == "win32":
            AppConfig.default_config_windows()
        else:
            AppConfig.default_config_linux()
        curr_dir = os.path.dirname(__file__)
        filepath = os.path.join(curr_dir, f"{sys.platform}-parameters.ini")
        config = configparser.ConfigParser()
        if os.path.exists(filepath):
            config.read(filepath)
            AppConfig.NUM_SEANCE = int(config.get("params", "NUM_SEANCE", fallback=str(AppConfig.NUM_SEANCE)))
            AppConfig.NUM_LABO = int(config.get("params", "NUM_LABO", fallback=str(AppConfig.NUM_LABO)))
            AppConfig.DATE_SEANCE = config.get("params", "DATE_SEANCE", fallback=AppConfig.DATE_SEANCE)
            AppConfig.NBRE_LABOS = int(config.get("params", "NBRE_LABOS", fallback=str(AppConfig.NBRE_LABOS)))
            AppConfig.BASE_SOURCE_FOLDER = config.get("params", "BASE_SOURCE_FOLDER", fallback=AppConfig.BASE_SOURCE_FOLDER)
            AppConfig.LOCAL_BACKUP_FOLDER = config.get("params", "LOCAL_BACKUP_FOLDER", fallback=AppConfig.LOCAL_BACKUP_FOLDER)
            AppConfig.LOCAL_COMPRESSED_FOLDER = config.get("params", "LOCAL_COMPRESSED_FOLDER", fallback=AppConfig.LOCAL_COMPRESSED_FOLDER)
        else:
            AppConfig.save_config()
    
    def save_config():
        curr_dir = os.path.dirname(__file__)
        filepath = os.path.join(curr_dir, f"{sys.platform}-parameters.ini")        
        config = configparser.ConfigParser()
        config.add_section("params")
        config.set("params", "NUM_SEANCE", str(AppConfig.NUM_SEANCE))
        config.set("params", "NUM_LABO", str(AppConfig.NUM_LABO))
        config.set("params", "DATE_SEANCE", AppConfig.DATE_SEANCE)
        config.set("params", "NBRE_LABOS", str(AppConfig.NBRE_LABOS))
        config.set("params", "BASE_SOURCE_FOLDER", AppConfig.BASE_SOURCE_FOLDER)
        config.set("params", "LOCAL_BACKUP_FOLDER", AppConfig.LOCAL_BACKUP_FOLDER)
        config.set("params", "LOCAL_COMPRESSED_FOLDER", AppConfig.LOCAL_COMPRESSED_FOLDER)
        with open(filepath, 'w') as configfile:
            config.write(configfile)


AppConfig.load_config()