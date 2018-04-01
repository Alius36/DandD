# coding: utf-8
import json
import logging

from DandD.controllers.authentication_controller import AuthenticationController
from DandD.utilities.exception import WrongInput
from DandD.utilities.utils import make_response
from pyramid.httpexceptions import HTTPFound, HTTPException, HTTPBadRequest, HTTPNotAcceptable, HTTPConflict, \
    HTTPInternalServerError, HTTPOk
from pyramid.security import remember, forget
from pyramid.view import view_config

logger = logging.getLogger(__name__)


class Authentication:
    def __init__(self, request):
        self.request = request
        self.bad_request = 400
        self.conflict_request = 409
        self.not_acceptable_request = 406
        self.success_request = 200

    @view_config(route_name='registration', renderer='../templates/registration.jinja2', request_method='GET',
                 accept='text/html')
    def registration_view(self):
        return {'1': 'one'}

    @view_config(route_name='registration', renderer='json', request_method='POST', accept='application/json')
    def registration(self):
        request = self.request

        nome = request.params.get('nome', None)
        cognome = request.params.get('cognome', None)
        password = request.params.get('password', None)
        username = request.params.get('username', None)

        logger.info('REGISTRATION INPUT sono: {nome}, {cognome}, {password}, {username}'.format(nome=nome,
                                                                                               cognome=cognome,
                                                                                               password=password,
                                                                                               username=username))

        if nome is not None and nome != '':
            if cognome is not None and cognome != '':
                if password is not None and password != '':
                    if username is not None and username != '':
                        # controller
                        result = AuthenticationController.registration(request.dbsession, nome, cognome, password,
                                                                       username)
                        logger.info('REGISTRATION OUTPUT é: {}'.format(json.dumps(result)))

                        if result['code'] == self.success_request:
                            logger.info('REGISTRATION COMPLETATA!')
                            return HTTPOk(body='Registrazione completata con successo!')
                        elif result['code'] == self.not_acceptable_request:
                            logger.error('REGISTRATION FALLITA: {}'.format(result['message']))
                            return HTTPNotAcceptable(body=result['message'])
                        elif result['code'] == self.conflict_request:
                            logger.error('REGISTRATION FALLITA: {}'.format(result['message']))
                            return HTTPConflict(body=result['message'])
                        else:
                            logger.error('REGISTRATION FALLITA: errore inaspettato.')
                            logger.error('{}'.format(result['message']))
                            return HTTPInternalServerError(body='Errore inaspettato. Ci scusiamo per il disagio!')
                    else:
                        logger.error('REGISTRATION FALLITA perché manca il parametro USERNAME')
                        return HTTPNotAcceptable('Manca lo USERNAME! Controlla.')
                else:
                    logger.error('REGISTRATION FALLITA perché manca il parametro PASSWORD')
                    return HTTPNotAcceptable('Manca la PASSWORD! Controlla.')
            else:
                logger.error('REGISTRATION FALLITA perché manca il parametro COGNOME')
                return HTTPNotAcceptable('Manca il COGNOME! Controlla.')
        else:
            logger.error('REGISTRATION FALLITA perché manca il parametro NOME')
            return HTTPNotAcceptable('Manca il NOME! Controlla.')

    @view_config(route_name='home', renderer='../templates/login.jinja2', request_method='GET',
                 accept='text/html')
    @view_config(route_name='login', renderer='../templates/login.jinja2', request_method='GET',
                 accept='text/html')
    def login_view(self):
        return {'1': 'one'}

    @view_config(route_name='login', renderer='json', request_method='POST', accept='application/json')
    def login(self):
        request = self.request

        username = request.params.get('username', None)
        password = request.params.get('password', None)

        # logger.info('LOGIN: i parametri di INPUT sono {username}, {password}'.format(username=username,
        logger.info('LOGIN: i parametri di INPUT sono {username}'.format(username=username))

        if username is not None and username != '':
            if password is not None and password != '':

                result = AuthenticationController.login(request, request.dbsession, username, password)

                if result['code'] == self.success_request:
                    logger.info('LOGIN COMPLETATA! Reindirizzamento alla home.')
                    return make_response('Success', 302, url=request.route_url('pippo'))
                elif result['code'] == self.not_acceptable_request:
                    logger.error('LOGIN FALLITA: {}'.format(result['message']))
                    return HTTPNotAcceptable(body=result['message'])
                elif result['code'] == self.conflict_request:
                    logger.error('LOGIN FALLITA: {}'.format(result['message']))
                    return HTTPConflict(body=result['message'])
                else:
                    logger.error(result)
                    return HTTPInternalServerError(body='Errore inaspettato. Ci scusiamo per il disagio!')
            else:
                logger.error('LOGIN FALLITA perché manca il parametro PASSWORD')
                return HTTPNotAcceptable(body='Manca la PASSWORD! Controlla.')
        else:
            logger.error('LOGIN FALLITA perché manca il parametro USERNAME')
            return HTTPNotAcceptable(body='Manca USERNAME! Controlla.')

    @view_config(route_name='logout', renderer='json')
    def logout(self):
        request = self.request

        headers = forget(request)
        next_url = request.route_url('login')

        logger.info('LOGOUT: url = {}, headers = {}'.format(next_url, headers))

        request.response.headers = headers
        # return HTTPFound(location=next_url, headers=headers)
        return make_response('Logout successful!', 302, next_url)
