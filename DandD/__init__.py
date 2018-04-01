from DandD.utilities.file_system import create_manuals_folder
from DandD.utilities.security import RootFactory, role_finder
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings, root_factory=RootFactory)

    authn_policy = AuthTktAuthenticationPolicy(settings['dandd.secret'], callback=role_finder, hashalg='sha512')
    authz_policy = ACLAuthorizationPolicy()

    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)

    config.include('pyramid_jinja2')
    config.include('.models')
    config.include('.routes')
    config.scan()

    create_manuals_folder(settings['localpath'])

    return config.make_wsgi_app()
