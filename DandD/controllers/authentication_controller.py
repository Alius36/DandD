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
                print usr[0]
                if username == usr[0]:
                    logger.error('Username giá usato! Cambialo.')
                    return make_response('Username giá usato! Cambialo.', 409)
            User.insert_new_user(dbsession, new_user)
            return make_response('Registrazione completata!', 200)
        except WrongInput, e:
            logger.error(e)
            return make_response('I dati sono sbagliati! Controllali.', 406)
        except DuplicateValue, e:
            logger.error(e)
            return make_response('Questo username é giá usato! Provane un\'altro.', 409)

    @classmethod
    def login(cls, request, dbsession, username, password):

        user = User.get_user_by_username(dbsession, username)

        if user:
            saving_user = {
                'id': user.id,
                'nome': user.nome,
                'cognome': user.cognome,
                'username': user.username,
                'role': user.fk_role.value
            }

            if request.authenticated_userid is not None and username != request.authenticated_userid:
                return make_response('Sei giá loggato con un\'altra utenza. Effettua il logout prima di autenticarti '
                                     'nuovamente.'.format(request.authenticated_userid), 409)
            elif request.authenticated_userid is not None and username == request.authenticated_userid:
                return make_response('Sei giá loggato.', 409)

            if check_password(password, user.password):
                logger.debug('CHECK PASSWORD completata!')

                headers = remember(request, username)
                request.response.headers = headers

                logger.debug('Salvataggio informazioni dell\'utente dentro la sessione.')
                request.session['user'] = saving_user
                return make_response('Success!', 200)
            else:
                return make_response('Password errata! Riprova.', 406)
        else:
            return make_response('Questo utente non esiste! Riprova o registrati e poi loggati.', 406)
