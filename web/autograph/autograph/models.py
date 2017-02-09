from sqlalchemy import create_engine,Table,Column,MetaData,Integer,String,ForeignKey,Date,Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, backref, relationship
import os

if os.path.exists("avtograf.db"):
    os.remove("avtograf.db")

engine = create_engine('sqlite:///avtograf.db', encoding='utf-8')
Session = sessionmaker()
Base = declarative_base(bind=engine)

class User(Base):
     __tablename__ = "Users"
     Login = Column(String, nullable = False,primary_key = True)
     Password = Column(String, nullable = False)
     Mail = Column(String, nullable = False)
     FirstName = Column(String, nullable = False)
     SecondName = Column(String, nullable = False)
     def __init__(self, Login, Password, Mail, FirstName, SecondName):
          self.Login = Login
          self.Password = Password
          self.Mail = Mail
          self.FirstName = FirstName
          self.SecondName = SecondName

     def __repr__(self):
          return self.Login + " " + self.Password + " " + self.Mail + " " +self.FirstName 

class Timetable(Base):
     __tablename__ = "TimeTable"
     id = Column(Integer, nullable=False, primary_key=True)
     Time = Column(String, nullable = False)
     Data = Column(String, nullable = False)
     Name_event = Column(String, nullable = False)
     About= Column(String, nullable = False)
     
     def __init__(self, Name_event, Data, Time, About):
          self.Name_event = Name_event
          self.Data = Data
          self.Time = Time
          self.About = About
       
     def __repr__(self):
          return self.Name_event + " " + self.Data + " " + self.Time + " " +self.About 

class Comments(Base):
     __tablename__ = "Comments"
     id = Column(Integer, nullable=False, primary_key=True)
     Login = Column(String, ForeignKey('Users.Login'),ForeignKey('Admins.Login'), nullable = False)
     Name_com = Column(String, nullable = False)
     Text = Column(String, nullable = False)
     Date = Column(Date, nullable = False)

     def __init__(self, Login, Name_com,Text,Date):
          self.Login = Login
          self.Name_com = Name_com
          self.Text = Text
          self.Date = Date

     def __repr__(self):
          return self.Login + " " + self.Name_com + " " + self.Text+ " " +str(self.id)

class Admins(Base):
     __tablename__ = "Admins"
     Login = Column(String, nullable = False,primary_key = True)
     Password = Column(String, nullable = False)
     Mail = Column(String, nullable = False)
     FirstName = Column(String, nullable = False)
     SecondName = Column(String, nullable = False)

     def __init__(self, Login, Password, Mail, FirstName, SecondName):
          self.Login = Login
          self.Password = Password
          self.Mail = Mail
          self.FirstName = FirstName
          self.SecondName = SecondName

     def __repr__(self):
          return self.Login + " " + self.Password + " " + self.Mail + " " +self.FirstName + " " + self.SecondName
