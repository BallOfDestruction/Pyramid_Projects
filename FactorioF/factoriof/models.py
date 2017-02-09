from sqlalchemy import Table, Column, Integer, Text, create_engine, String, ForeignKey, DateTime, Date, Float, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, backref, relationship

from pyramid.security import (
Allow,
Everyone,
)

engine = create_engine('sqlite:///FactorioF.db')
Session = sessionmaker()
Base = declarative_base(bind=engine)

class User(Base):
  __tablename__ = "Users"
  id = Column(Integer, nullable = False, primary_key = True)
  Login = Column(String, nullable = False)
  Password = Column(String, nullable = False)
  Mail = Column(String, nullable = False)
  FirstName = Column(String, nullable = False)
  SecondName = Column(String, nullable = False)
  Nick = Column(String, nullable = False)
  def __init__(self, Login, Password, Mail, FirstName, SecondName, Nick):
    super(User, self).__init__()
    self.Login = Login
    self.Password = Password
    self.Mail = Mail
    self.FirstName = FirstName
    self.SecondName = SecondName
    self.Nick = Nick

  def __repr__(self):
    return self.Login + " " + self.Password + " " + self.Mail + " " +self.FirstName + " " + self.Nick
    
class Design(Base):
  __tablename__ = "Design"
  id = Column(Integer, nullable= False, primary_key = True)
  Picture = Column(String, nullable = False)
  Name = Column(String, nullable = False)
  Description = Column(String)
  Price = Column(Float, nullable = False)
  Nick_autor = Column(String, nullable = False)
  def __init__(self, Picture, Name, Description, Price, Nick_autor):
    super(Design, self).__init__()
    self.Picture = Picture
    self.Name = Name
    self.Description = Description
    self.Price = Price
    self.Nick_autor = Nick_autor

class EndGame(Base):
  __tablename__ = "EndGame"
  id = Column(Integer, nullable= False, primary_key = True)
  Picture = Column(String, nullable = False)
  Name = Column(String, nullable = False)
  Description = Column(String)
  Nick_autor = Column(String, nullable = False)
  def __init__(self, Picture, Name, Description, Nick_autor):
    super(EndGame, self).__init__()
    self.Picture = Picture
    self.Name = Name
    self.Description = Description
    self.Nick_autor = Nick_autor

class Accsess(Base):
  __tablename__ = "Accsess"
  id = Column(Integer, primary_key = True, nullable = False)
  id_user = Column(Integer, ForeignKey('Users.id'), nullable = False)
  id_design = Column(Integer, ForeignKey('Design.id'), nullable = False)
  def __init__(self, id_user, id_design):
    super(Accsess, self).__init__()
    self.id_user = id_user
    self.id_design = id_design

class Arts(Base):
  __tablename__ = "Arts"
  id = Column(Integer, primary_key = True, nullable = False)
  Path = Column(String, nullable = False)
  def __init__(self, Path):
    self.Path = Path