import logging

from DandD.controllers.authentication_controller import AuthenticationController
from DandD.utilities.utils import make_response
from pyramid.view import view_config

logger = logging.getLogger(__name__)


class Authentication:
    success = 200
    failed = 666

    def __init__(self, request):
        self.request = request

    # ../templates/login.jinja2
    @view_config(route_name='registration', renderer='json', request_method='POST')
    def registration(self):
        request = self.request

        nome = request.params.get('nome', None)
        cognome = request.params.get('cognome', None)
        password = request.params.get('password', None)
        username = request.params.get('username', None)

        logger.info('Login input are: {nome}, {cognome}, {password}, {username}'.format(nome=nome, cognome=cognome,
                                                                                        password=password,
                                                                                        username=username))

        if nome is not None and nome != '':
            if cognome is not None and cognome != '':
                if password is not None and password != '':
                    if username is not None and username != '':
                        # controller
                        result = AuthenticationController.registration(request.dbsession, nome, cognome, password,
                                                                       username)
                        print 'FINE: ', result
                        return result

                    else:
                        logger.error('Login failed because param beacuse missed param USERNAME')
                else:
                    logger.error('Login failed because param beacuse missed param PASSWORD')
            else:
                logger.error('Login failed because param beacuse missed param COGNOME')
        else:
            logger.error('Login failed because param beacuse missed param NOME')

    @view_config(route_name='home', renderer='../templates/login.jinja2', request_method='GET')
    @view_config(route_name='login_view', renderer='../templates/login.jinja2', request_method='GET')
    def login_view(self):
        return {'1': 'one'}

    @view_config(route_name='registration_view', renderer='../templates/registration.jinja2', request_method='GET')
    def registration_view(self):
        return {'1': 'one'}
