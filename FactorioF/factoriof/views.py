from pyramid.view import view_config
from sqlalchemy import Table, Column, Integer, Text, create_engine, String, ForeignKey, DateTime, Date, Float, MetaData

from pyramid.response import Response
from models import *
import re
import os
import uuid
import shutil

from pyramid.security import (
remember,
forget,
)

from pyramid.httpexceptions import (
HTTPFound,
HTTPNotFound,
)

@view_config(route_name='home', renderer='templates/home.jinja2')
def home(request):
    return {'username' : request.authenticated_userid }

@view_config(route_name='endGame', renderer='templates/endGame.jinja2')
def endGame(request):
    return {'username' : request.authenticated_userid,
    		'games' : Session(bind = engine).query(EndGame).all()}

@view_config(route_name='design', renderer='templates/data_design.jinja2')
def design(request):
    return {'username' : request.authenticated_userid,
    		'games' : Session(bind = engine).query(Design).all() }
    
@view_config(route_name='arts', renderer='templates/arts.jinja2')
def arts(request):
	ses = Session(bind=engine)
	if request.method == "POST":
		if request.params['picture'] == "":
			return {'username' : request.authenticated_userid,
					'images' : ses.query(Arts).all(),
					'first' : ses.query(Arts).first() }
		filename = request.POST['picture'].filename
		input_file = request.POST["picture"].file
		file_path = os.path.join( 'factoriof/static/images/Arts', filename)
		with open(file_path, 'wb') as output_file:
			shutil.copyfileobj(input_file, output_file)
		file_path = re.split(r'[/]', file_path, maxsplit = 1)[1]
		art = Arts(Path = file_path)
		ses.add(art)
		ses.commit()
		return {'username' : request.authenticated_userid,
    			'images' : ses.query(Arts).all(),
    			'first' : ses.query(Arts).first()}
	else:
	    return {'username' : request.authenticated_userid,
    			'images' : ses.query(Arts).all(),
    			'first' : ses.query(Arts).first()}

@view_config(route_name='wiki', renderer='templates/wiki.jinja2')
def wiki(request):
    return {'username' : request.authenticated_userid }

@view_config(route_name='about', renderer='templates/about.jinja2')
def about(request):
    return {'username' : request.authenticated_userid }

@view_config(route_name='addDesign', renderer='templates/addDesign.jinja2', permission = 'add')
def addDesign(request):
	if request.method == 'POST':
		ses = Session(bind=engine)
		if request.params['picture'] == "":
			return {'username' : request.authenticated_userid }
		filename = request.POST['picture'].filename
		input_file = request.POST["picture"].file
		file_path = os.path.join( 'factoriof/static/images/uploads', filename)
		with open(file_path, 'wb') as output_file:
			shutil.copyfileobj(input_file, output_file)
		file_path = re.split(r'[/]', file_path, maxsplit = 1)[1]
		try:
			new_design = Design(Name = request.params["name"],
					Picture = file_path,
					Description = request.params["description"],
					Nick_autor = request.authenticated_userid,
					Price = request.params['price'])
			ses.add(new_design)
			ses.commit()
		except:
			return { 'username' : request.authenticated_userid }
		return HTTPFound(location = request.route_url("design", _query = {"username" : request.authenticated_userid}))
	else:
	    return {'username' : request.authenticated_userid }

@view_config(route_name='addEndGame', renderer='templates/addEndGame.jinja2', permission = 'add')
def addEndGame(request):
	if request.method == 'POST':
		ses = Session(bind=engine)
		if request.params['picture'] == "":
			return {'username' : request.authenticated_userid }
		filename = request.POST['picture'].filename
		input_file = request.POST["picture"].file
		file_path = os.path.join( 'factoriof/static/images/uploads', filename)
		with open(file_path, 'wb') as output_file:
			shutil.copyfileobj(input_file, output_file)
		file_path = re.split(r'[/]', file_path, maxsplit = 1)[1]
		new_game = EndGame(Name = request.params["name"],
				Picture = file_path,
				Description = request.params["description"],
				Nick_autor = request.authenticated_userid)
		ses.add(new_game)
		ses.commit()
		return HTTPFound(location = request.route_url("endGame", _query = {"username" : request.authenticated_userid}))
	else:
	    return {'username' : request.authenticated_userid }

@view_config(route_name='logOut')
def logOut(request):
	if request.method == 'POST':
		headers = forget(request)
		return HTTPFound(location = '/', headers = headers)
	else:
		return HTTPNotFound()

@view_config(route_name='logIn')
def logIn(request):
	if request.method == 'POST':
		ses = Session(bind=engine)
		user = ses.query(User).filter_by(Login = request.params['login']).first()
		if(user != None and user.Password == request.params['password']):
			headers = remember(request, user.Nick)			
			return HTTPFound(location = '/', headers = headers)
	else:
		return HTTPNotFound()

@view_config(route_name='register', renderer = 'templates/register.jinja2')
def register(request):
	print(request)
	if request.method == 'POST':
		ses = Session(bind=engine)
		errors = []
		if(len(request.params['login']) < 6):
			errors.append("Min length login is 6")
		if(len(request.params['password']) < 6):
			errors.append("Min length password is 6")
		if(len(request.params['mail']) == 0):
			errors.append("Enter mail, please")
		if(len(request.params['firstName']) == 0):
			errors.append("Enter first name, please")
		if(len(request.params['secondName']) == 0):
			errors.append("Enter second name, please")
		if(len(request.params['nick']) == 0):
			errors.append("Enter nickName, please")
		if(request.params['password'] != request.params['confirm_password']):
			errors.append('Passwords are not equals')
		user = ses.query(User).filter_by(Login = request.params['login']).first()
		if(user != None):
			errors.append('Login already exists')
		user = ses.query(User).filter_by(Mail = request.params['mail']).first()
		if(user != None):
			errors.append("E-mail already exists")
		user = ses.query(User).filter_by(Nick = request.params['nick']).first()
		if(user != None):
			errors.append("Nick already exists")
		if(len(errors) != 0):
			return { 'errors' : errors,
						'firstName' :request.params['firstName'],
						'secondName': request.params['secondName'],
						'mail' : request.params['mail'],
						'nick' : request.params['nick'],
						'login' : request.params['login'],
						'username' : request.authenticated_userid}
		new_user = User(Login = request.params['login'], Password = request.params['password'], Mail = request.params['mail'], FirstName = request.params['firstName'] , SecondName = request.params['secondName'], Nick = request.params['nick'])
		ses.add(new_user)
		ses.commit()
		return HTTPFound(location=request.route_url("home", _query={'username': request.authenticated_userid}))
	else:
		return { 'username' : request.authenticated_userid}
