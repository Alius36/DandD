# coding: utf-8
import logging

import os

from datetime import datetime

from DandD.models.models import Manual
from DandD.utilities.exception import WrongInput
from DandD.utilities.file_system import rollback_upload, create_manuals_folder
from DandD.utilities.utils import make_response, calculate_md5

logger = logging.getLogger(__name__)


class ManualController:

    def __init__(self):
        pass

    @staticmethod
    def upload(request, file, md5):
        folder = request.registry.settings['localpath']

        try:
            filename = file.filename
            calc_md5 = calculate_md5(filename)
            file_stream = file.file

            if calc_md5 == md5:
                # la query ritorna una lista di tuple: quindi devo cercare la tupla
                if (filename,) not in Manual.get_all_title(request.dbsession):
                    path = os.path.join(folder, filename)

                    create_manuals_folder(folder)

                    server_file = open(path, 'wb')

                    while True:
                        data = file_stream.read(2 << 16)
                        if not data:
                            break
                        server_file.write(data)
                    server_file.close()
                    new_manual = Manual({
                        'title': filename,
                        'path': path,
                        'upload_dt': datetime.now(),
                        'fk_user': request.authenticated_userid
                    })
                    try:
                        Manual.insert_new_manual(request.dbsession, new_manual)
                    except WrongInput, e:
                        logger.error('UPLOAD CONTROLLER: db manual insert failed. \n{}'.format(e))
                        rollback_upload(path)
                        return make_response('Stiamo avendo dei disservizi interni. Ci scusiamo per il disagio!', 500)
                    logger.info('Caricamento completato!')
                    return make_response('Upload del file {} completato con successo'.format(filename), 200)
                else:
                    logger.error('UPLOAD FILE: esiste giá un file con questo nome!')
                    return make_response('Esiste giá un file con questo nome: perfavore cambialo!', 409)
            else:
                logger.error('UPLOAD CONTROLLER: md5 differenti. Ricevuto: {}, calcolato: {}'.format(md5, calc_md5))
                return make_response('Spiacenti ma il file risulta essere corrotto.', 406)
        except OSError, e:
            logger.error('UPLOAD OSError: {}'.format(e))
            return make_response('Siamo spiacenti ma stiamo riscontrando un momentaneo disservizio interno', 500)
        except MemoryError, e:
            logger.critical('UPLOAD MemoryError: {}'.format(e))
            return make_response('Siamo spiacenti ma al momento non abbiamo abbastanza spazio per salvare questo file.',
                                 507)
