import logging
import os

logger = logging.getLogger(__name__)


def rollback_upload(path_file):
    try:
        if os.path.exists(path_file):
            os.remove(path_file)
    except OSError, e:
        logger.exception('ROLLBACK UPLOAD: failed. \n', e)

def create_manuals_folder(folder):
    if not os.path.exists(folder):
        logger.info('Cartella MANUALI creata!')
        os.mkdir(folder)
