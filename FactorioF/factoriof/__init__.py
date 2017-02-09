from pyramid.config import Configurator
from pyramid.session import SignedCookieSessionFactory
from sqlalchemy import inspect
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.security import Allow, Deny
from pyramid.security import Authenticated
from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker


from models import *

my_session_factory = SignedCookieSessionFactory('FactorioF')

class MyFactory(object):
    def __init__(self, request):
        self.__acl__ = [(Allow, Authenticated, "add")]


def main(global_config, **settings):



    Base.metadata.create_all()
    DBSession = Session(bind=engine)

    new_user = User(Login="admin", Password = "admin", Mail="Administrator", FirstName="this user is administrator", SecondName ="324", Nick = "admin")
    DBSession.add(new_user)
    DBSession.commit()

    config = Configurator(settings=settings, session_factory=my_session_factory, root_factory = MyFactory)


    config.include('pyramid_jinja2')
    config.include('pyramid_sacrud')
    settings = config.registry.settings
    settings['pyramid_sacrud.models'] = (('Group1', [EndGame]),
                                     ('Group2', [Design]))

    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('endGame','/endGame.html')
    config.add_route('design','/design.html')
    config.add_route('arts','/arts.html')
    config.add_route('wiki','/wiki.html')
    config.add_route('about','/about.html')

    config.add_route('register', '/register.html')
    config.add_route('logIn', '/logIn.html')
    config.add_route('logOut', '/logOut.html')

    config.add_route('addDesign', '/addDesign.html')
    config.add_route('addEndGame', '/addEndGame.html')


    config.scan()

    authn_policy = AuthTktAuthenticationPolicy('sosecret', hashalg='sha512')
    authz_policy = ACLAuthorizationPolicy()
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)

    #inspector = inspect(engine)
    #print(inspector.get_table_names())

    return config.make_wsgi_app()
