# coding: utf-8
import json
import logging

from DandD.controllers.authentication_controller import AuthenticationController
from DandD.utilities.exception import WrongInput
from DandD.utilities.utils import make_response
from pyramid.httpexceptions import HTTPFound, HTTPException, HTTPBadRequest, HTTPNotAcceptable, HTTPConflict, \
    HTTPInternalServerError
from pyramid.security import remember
from pyramid.view import view_config

logger = logging.getLogger(__name__)


class Authentication:
    def __init__(self, request):
        self.request = request
        self.bad_request = 400
        self.conflict_request = 409
        self.not_acceptable_request = 406
        self.success_request = 200


    @view_config(route_name='registration', renderer='json', request_method='POST')
    def registration(self):
        request = self.request

        nome = request.params.get('nome', None)
        cognome = request.params.get('cognome', None)
        password = request.params.get('password', None)
        username = request.params.get('username', None)

        logger.info('Registration input are: {nome}, {cognome}, {password}, {username}'.format(nome=nome,
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
                        logger.info('Registration OUTPUT is: {}'.format(json.dumps(result)))
                        return result

                    else:
                        logger.error('Registration failed because missing param USERNAME')
                        return make_response('Missing USERNAME! Check it.', 400)
                else:
                    logger.error('Registration failed because missing param PASSWORD')
                    return make_response('Missing PASSWORD! Check it.', 400)
            else:
                logger.error('Registration failed because missing param COGNOME')
                return make_response('Missing COGNOME! Check it.', 400)
        else:
            logger.error('Registration failed because missing param NOME')
            return make_response('Missing NOME! Check it.', 400)

    @view_config(route_name='home', renderer='../templates/login.jinja2', request_method='GET')
    @view_config(route_name='login_view', renderer='../templates/login.jinja2', request_method='GET')
    def login_view(self):
        return {'1': 'one'}

    @view_config(route_name='login', renderer='json', request_method='POST')
    def login(self):
        request = self.request

        username = request.params.get('username', None)
        password = request.params.get('password', None)

        logger.info('LOGIN input params are {username}, {password}'.format(username=username, password=password))

        if username is not None and username != '':
            if password is not None and password != '':
                result = AuthenticationController.login(request, request.dbsession, username, password)
                print 'LOGIN RESULT: ', result
                if result['code'] == 200:
                    return make_response('Success', 302, url=request.route_url('pippo'))
                elif result['code'] == 406:
                    return HTTPNotAcceptable(body=result['message'])
                elif result['code'] == 409:
                    return HTTPConflict(body=result['message'])
                else:
                    logger.error(result)
                    return HTTPInternalServerError(body=json.dumps('Unexpected error.'))
            else:
                logger.error('LOGIN failed because missing param PASSWORD')
                return HTTPNotAcceptable(body=json.dumps('Missing PASSWORD! Check it.'))
        else:
            logger.error('LOGIN failed because missing param USERNAME')
            return HTTPNotAcceptable(body=json.dumps('Missing USERNAME! Check it.'))

    @view_config(route_name='registration_view', renderer='../templates/registration.jinja2', request_method='GET')
    def registration_view(self):
        return {'1': 'one'}
