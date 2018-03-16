from DandD.utilities.security import RootFactory, role_finder
from pyramid.authentication import SessionAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings, root_factory=RootFactory)

    authn_policy = SessionAuthenticationPolicy(callback=role_finder)
    authz_policy = ACLAuthorizationPolicy()

    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)

    config.include('pyramid_jinja2')
    config.include('pyramid_beaker')
    config.include('.models')
    config.include('.routes')
    config.scan()
    return config.make_wsgi_app()
