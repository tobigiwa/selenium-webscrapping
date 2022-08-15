import logging
import os

def creating_log(script_name:str):

    log_folder_path = 'log_folder'

    if os.path.exists(log_folder_path):
        for files in os.scandir(log_folder_path):
            os.remove(files)
    else:
        os.makedirs(log_folder_path)

    log_path = os.path.join(os.getcwd(), log_folder_path, 'riviera.log')

    logger = logging.getLogger(script_name)
    logger.setLevel(logging.DEBUG)
    log_handler = logging.FileHandler(log_path)
    log_format = logging.Formatter('%(asctime)s -- %(name)s -- %(levelname)s -- %(message)s \n')
    log_handler.setFormatter(log_format)
    logger.addHandler(log_handler)
    logger.info('Log reporting is instantiated.')

    return logger