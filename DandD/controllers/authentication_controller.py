# coding: utf-8
import json
import logging

import datetime

from DandD.models import User
from DandD.utilities.exception import DuplicateValue, WrongInput
from DandD.utilities.security import hash_password
from DandD.utilities.utils import make_response

logger = logging.getLogger(__name__)


class AuthenticationController:

    def __init__(self):
        pass

    @staticmethod
    def registration(dbsession, nome, cognome, password, username):
        new_user = User({
            'nome': nome,
            'cognome': cognome,
            'password': hash_password(password),
            'url_img': None,
            'iscrizione_dt': datetime.datetime.now(),
            'username': username
        })
        try:
            username_list = User.get_all_username(dbsession)

            if username in username_list:
                logger.error('Username giá usato! Cambialo.')
                return WrongInput('Username giá usato! Cambialo.', 400)
            else:
                User.insert_new_user(dbsession, new_user)
        except WrongInput, e:
            logger.error(json.dumps(e))
            return WrongInput('I dati sono sbagliati! Controllali.', 400)
        except DuplicateValue, e:
            logger.error(json.dumps(e))
            return DuplicateValue('Questo username é giá usato! Provane un\'altro.', 500)

        return make_response('Registrazione completata!', 200)
