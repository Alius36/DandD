import logging

import datetime

from DandD.models import User
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
        # try:
        #     User.insert_new_user(dbsession, new_user)
        # except Exception, e:
        #     return make_response(666, 'Registration failed! Please try again.')
        User.insert_new_user(dbsession, new_user)
        return make_response(200, 'Registration complete!')
