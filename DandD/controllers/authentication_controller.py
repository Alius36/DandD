# coding: utf-8
import logging

import datetime

from DandD.models import User
from DandD.utilities.exception import DuplicateValue, WrongInput
from DandD.utilities.security import hash_password, check_password
from DandD.utilities.utils import make_response
from pyramid.security import remember

logger = logging.getLogger(__name__)


class AuthenticationController:

    def __init__(self):
        pass

    @classmethod
    def registration(cls, dbsession, nome, cognome, password, username):
        new_user = User({
            'nome': nome,
            'cognome': cognome,
            'password': hash_password(password),
            'url_img': None,
            'iscrizione_dt': datetime.datetime.now(),
            'username': username,
            'fk_role_id': 1
        })
        try:
            username_list = User.get_all_username(dbsession)
            for usr in username_list:

                if username == usr[0]:
                    logger.error('Username giá usato! Cambialo.')
                    return make_response('Username giá usato! Cambialo.', 400)
            User.insert_new_user(dbsession, new_user)
            return make_response('Registrazione completata!', 200)
        except WrongInput, e:
            logger.error(e)
            return make_response('I dati sono sbagliati! Controllali.', 400)
        except DuplicateValue, e:
            logger.error(e)
            return make_response('Questo username é giá usato! Provane un\'altro.', 500)

    @classmethod
    def login(cls, request, dbsession, username, password):
        if request.authenticated_userid is not None and username != request.authenticated_userid:
            pass

        user = User.get_user_by_username(dbsession, username)

        if user:
            saving_user = {
                'id': user.id,
                'nome': user.nome,
                'cognome': user.cognome,
                'username': user.username,
                'role': user.fk_role.value
            }
            if check_password(password, user.password):
                print 'password corretta!'
                headers = remember(request, username)
                request.response.headers = headers

                request.session['user'] = saving_user
                logger.info('LOGIN successful!')
                return make_response('Success!', 200), headers
            else:
                return make_response('Wrong password! Check it.', 400)
        else:
            return make_response('This username doesn\'t exist! Check it and try to log in again.', 400)
