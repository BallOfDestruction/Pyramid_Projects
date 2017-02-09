# -*- coding: utf-8 -*- 
from pyramid.config import Configurator
from autograph.resources import get_root
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

class MyFactory(object):
    def __init__(self, request):
        self.__acl__ = [(Allow, Authenticated, "add")]

my_session_factory = SignedCookieSessionFactory('autograph')

def main(global_config, **settings):
    Base.metadata.create_all()

    settings = dict(settings)
    settings.setdefault('jinja2.i18n.domain', 'autograph')

    config = Configurator(root_factory=MyFactory, settings=settings, session_factory=my_session_factory)
    config.include('pyramid_jinja2')

    config.add_static_view('static', 'static')
    config.add_route("index" , '/')
    config.add_route("timeTable", '/timeTable.html')
    config.add_route("arenda" , "/arenda.html")
    config.add_route("contacts" , "/contacts.html")
    config.add_route("responce" , "/responce.html")

    config.add_route("goodReg", "/goodReg.html")
    config.add_route("register", "/register.html")
    config.add_route("logIn", '/logIn.html')
    config.add_route("logOut", "/logOut.html")
    config.add_route("addComment", "/addComment.html")

    config.add_route("admin", "/admin")
    config.add_route("adminEditTable", "/adminEditTable")
    config.add_route("adminEditComment", "/adminEditComment")
    config.add_route("adminEditTableEdit", "/adminEditTableEdit/{id}")
    config.add_route("addTable", "/addTable")


    authn_policy = AuthTktAuthenticationPolicy('sosecret', hashalg='sha512')
    authz_policy = ACLAuthorizationPolicy()
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)

    #админ
    sessio = Session(bind = engine)
    new_admin = Admins(Login = 'admin',
    					Password = 'admin',
    					Mail = 'admin@mail.ru',
    					FirstName = 'admin',
    					SecondName = 'admin')
    sessio.add(new_admin)
    sessio.commit()

    # Парочка дефольных событий
    new_Table = Timetable(Data = u"26 декабря, понедельник",
    						Time = u"19:00",
    						Name_event = u"Театральная импровизация",
    						About = u"Театральная импровизация и что нибудь еще")
    sessio.add(new_Table)
    sessio.commit()

    new_Table = Timetable(Data = u"26 декабря, понедельник",
    						Time = u"19:00",
    						Name_event = u"Театральная импровизация",
    						About = u"Театральная импровизация и что нибудь еще")
    sessio.add(new_Table)
    sessio.commit()



    config.scan()
    return config.make_wsgi_app()
