import datetime
import os
import configparser


class AppConfig:
    LOCAL_BACKUP_FOLDER = "D:\\Backup\\Bac2023"
    LOCAL_COMPRESSED_FOLDER = "D:\\Users\\hp\\Backup\\Bac2023"
    NUM_SEANCE = 1
    DATE_SEANCE = datetime.date.today().isoformat()
    NBRE_LABOS = 4

    def load_config():
        curr_dir = os.path.dirname(__file__)
        filepath = os.path.join(curr_dir, "parameters.ini")
        config = configparser.ConfigParser()
        if os.path.exists(filepath):
            config.read(filepath)
            AppConfig.NUM_SEANCE = int(config.get("params", "NUM_SEANCE", fallback=str(AppConfig.NUM_SEANCE)))
            AppConfig.DATE_SEANCE = config.get("params", "DATE_SEANCE", fallback=AppConfig.DATE_SEANCE)
            AppConfig.NBRE_LABOS = int(config.get("params", "NBRE_LABOS", fallback=str(AppConfig.NBRE_LABOS)))
            AppConfig.LOCAL_BACKUP_FOLDER = config.get("params", "LOCAL_BACKUP_FOLDER", fallback=AppConfig.LOCAL_BACKUP_FOLDER)
            AppConfig.LOCAL_COMPRESSED_FOLDER = config.get("params", "LOCAL_COMPRESSED_FOLDER", fallback=AppConfig.LOCAL_COMPRESSED_FOLDER)
        else:
            AppConfig.save_config()

    
    def save_config():
        curr_dir = os.path.dirname(__file__)
        filepath = os.path.join(curr_dir, "parameters.ini")        
        config = configparser.ConfigParser()
        config.add_section("params")
        config.set("params", "NUM_SEANCE", str(AppConfig.NUM_SEANCE))
        config.set("params", "DATE_SEANCE", AppConfig.DATE_SEANCE)
        config.set("params", "NBRE_LABOS", str(AppConfig.NBRE_LABOS))
        config.set("params", "LOCAL_BACKUP_FOLDER", AppConfig.LOCAL_BACKUP_FOLDER)
        config.set("params", "LOCAL_COMPRESSED_FOLDER", AppConfig.LOCAL_COMPRESSED_FOLDER)
        with open(filepath, 'w') as configfile:
            config.write(configfile)


AppConfig.load_config()