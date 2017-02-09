# -*- coding: utf-8 -*- 
from pyramid.view import view_config
from pyramid.response import Response
from models import *
import re
from datetime import *


from pyramid.security import (
remember,
forget,
)

from pyramid.httpexceptions import (
HTTPFound,
HTTPNotFound,
)

#добавляет при посте
@view_config(route_name='addTable', renderer='templates/addTable.jinja2', permission = 'add')
def addTable(request):
	if request.method == 'POST':
		session = Session(bind = engine)
		timetable = Timetable(Name_event = request.params["Name_event"],
								Data = request.params["Data"],
								Time = request.params["Time"],
								About = request.params["About"])
		session.add(timetable)
		session.commit()
		return HTTPFound(location = request.route_url('adminEditTable', _query={'username': request.authenticated_userid}))
	else:
		return {'username': request.authenticated_userid }

#редактирует при посте
@view_config(route_name='adminEditTableEdit', renderer='templates/adminEditTableEdit.jinja2', permission = 'add')
def adminEditTableEdit(request):
	session = Session(bind = engine)
	if request.method == 'POST':
		timetable = session.query(Timetable).filter(Timetable.id == request.matchdict['id']).first()
		session.delete(timetable)
		session.commit()
		timetable = Timetable(Name_event = request.params["Name_event"],
								Data = request.params["Data"],
								Time = request.params["Time"],
								About = request.params["About"])
		session.add(timetable)
		session.commit()
		times = session.query(Timetable).all()
		return HTTPFound(location = request.route_url('adminEditTable', _query={'username': request.authenticated_userid}))
	else:
		return {'username': request.authenticated_userid,
				"timeTable" : Session(bind=engine).query(Timetable).filter(Timetable.id == request.matchdict['id']).first()}

#Удаляет при посте
@view_config(route_name='adminEditTable', renderer='templates/adminEditTable.jinja2', permission = 'add')
def adminEditTable(request):
	if request.method == 'POST':
		session = Session(bind = engine)
		timetable = session.query(Timetable).filter(Timetable.id == request.params['id']).first()
		session.delete(timetable)
		session.commit()
		return {'username': request.authenticated_userid,
				"timeTables" : Session(bind=engine).query(Timetable).all()}
	else:
		return {'username': request.authenticated_userid,
				"timeTables" : Session(bind=engine).query(Timetable).all()}


@view_config(route_name='adminEditComment', renderer='templates/adminEditComment.jinja2', permission = 'add')
def adminEditComment(request):
	if request.method == 'POST':
		session = Session(bind = engine)
		comment = session.query(Comments).filter(Comments.id == request.params['id']).first()
		session.delete(comment)
		session.commit()
		return {'username': request.authenticated_userid,
				"comments" : Session(bind=engine).query(Comments).all()}
	else:
		return {'username': request.authenticated_userid,
				"comments" : Session(bind=engine).query(Comments).all()}


@view_config(route_name='admin', renderer='templates/admin.jinja2')
def admin(request):
	if request.method == 'POST':
		user = Session(bind=engine).query(Admins).filter(Admins.Login == request.params['login']).first()
		if user != None and user.Password == request.params['password']:
			headers = remember(request, user.Login)			
			return HTTPFound(location = '/adminEditComment', headers = headers)
		else:
			return {'error': u"Введены неверные данные", 'username': request.authenticated_userid }
	else:
		return {'username' : request.authenticated_userid }


@view_config(route_name='timeTable', renderer='templates/timeTable.jinja2')
def timeTable(request):
	return {'username': request.authenticated_userid,
					"timeTables" : Session(bind=engine).query(Timetable).all()}

@view_config(route_name='index', renderer='templates/index.jinja2')
def index(request):
    return {'username': request.authenticated_userid}


@view_config(route_name='arenda', renderer='templates/arenda.jinja2')
def arenda(request):
    return {'username': request.authenticated_userid}


@view_config(route_name='contacts', renderer='templates/contacts.jinja2')
def contacts(request):
    return {'username': request.authenticated_userid}


@view_config(route_name='addComment', renderer='templates/addComment.jinja2')
def addComment(request):
	if request.method == "POST":
		session = Session(bind = engine)
		new_comment = Comments(Login = request.authenticated_userid,
								Name_com = request.params['name'],
								Text = request.params['comment'],
								Date = datetime.now())
		session.add(new_comment)
		session.commit()
		return HTTPFound(location = request.route_url('responce', _query={'username': request.authenticated_userid}))
	else:
		return { 'username': request.authenticated_userid }

@view_config(route_name='responce', renderer='templates/responce.jinja2')
def responce(request):
	return {'username': request.authenticated_userid,
    		"comments" : Session(bind=engine).query(Comments).all()}

@view_config(route_name='register', renderer='templates/register.jinja2')
def register(request):
	if request.method == 'POST':
		session = Session(bind=engine)
		errors = []
		if(len(request.params['name']) <=3):
			errors.append(u"Введите имя")
		if(len(request.params['login']) <6):
			errors.append(u"Введите логин")
		if(len(request.params['password']) <=5):
			errors.append(u"Введите пароль")
		if(len(request.params['passwordTwo']) <=5):
			errors.append(u"Введите подтверждение пароля")
		if(request.params['password']!= request.params['passwordTwo']):
			errors.append(u'Пароли не совпадают')
		if(session.query(User).filter_by(Login=request.params['login']).count() != 0):
			errors.append(u'Такой логин уже существует')
		if(len(errors) != 0):
			return { 'errors' : errors ,
					 'name' : request.params['name'],
					 'login' : request.params['login'],
					 'mail' : request.params['mail'],
					 'secondName' : request.params['secondName'],
					 'username': request.authenticated_userid }
		else:
			new_user = User(request.params['login'],
							request.params['password'],
							request.params['mail'],
							request.params['name'],
							request.params['secondName']);
			session.add(new_user)
			session.commit()
			return HTTPFound(location = request.route_url('goodReg', goodReg='great', _query={'login' : request.params['login']}))
	else:
		return { 'username': request.authenticated_userid }

@view_config(route_name='logIn', renderer='templates/logIn.jinja2')
def logIn(request):
	if request.method == 'POST':
		user = Session(bind=engine).query(User).filter(User.Login == request.params['login']).first()
		if user != None and user.Password == request.params['password']:
			headers = remember(request, user.Login)			
			return HTTPFound(location = '/', headers = headers)
		else:
			return {'error': u"Введены неверные данные", 'username': request.authenticated_userid }
	else:
		return {'username' : request.authenticated_userid }

@view_config(route_name='logOut')
def logOut(request):
	headers = forget(request)
	return HTTPFound(location = '/', headers = headers)

@view_config(route_name='goodReg', renderer='templates/goodReg.jinja2')
def goodReg(request):
    return {'username': request.authenticated_userid,
    		'login' : request.params['login'] }
