import datetime
import os
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class User(Base):
    """ Пользователь (контакт) """
    __tablename__ = 'users'
    Id = Column(Integer, primary_key=True)
    Name = Column(String, unique=True)
    Info = Column(String, nullable=True)

    def __init__(self, name,info=None):
        self.Name = name
        if info:
            self.Info = info

    def __repr__(self):
        #return "<User: '%s'; %s>" % (self.Name, self.Info)
        return "'%s'" %self.Name


class Contacts(Base):
    """ Контакты (друзья пользователя) """
    __tablename__ = 'contacts'
    Id = Column(Integer, primary_key=True)
    Contact = Column(Integer, ForeignKey('users.Id'))
    Friend = Column(Integer, ForeignKey('users.Id'))

    def __init__(self, contact, friend):
        self.Contact = contact
        self.Friend  = friend

    def __repr__(self):
        return "'%s'" % (self.Friend)

class Messages(Base):
    ''' Хранилище сообщений пользователей '''
    __tablename__ = 'messages'
    Id = Column(Integer, primary_key=True)
    Contact = Column(Integer, ForeignKey('users.Id'))
    Timestamp = Column(DateTime)
    From = Column(String)
    Message = Column(String)

    def __init__(self,contact, timestamp, from_contact, message):
        self.Contact = contact
        self.Timestamp = timestamp
        self.From = from_contact
        self.Message = message

        def __repr__(self):
            return "coобщение от '%s' для ''%s': %s" %from_contact %contact %message



# путь до папки c модулем
DB_FOLDER_PATH = os.path.dirname(os.path.abspath(__file__))
# путь до файла базы данных
DB_PATH = os.path.join(DB_FOLDER_PATH, 'chat_server.db')

#создаем движок
engine = create_engine('sqlite:///{}'.format(DB_PATH), echo=False)
# Создаём структуру базы данных (!)
Base.metadata.create_all(engine)

# Создаем сессию для работы
Session = sessionmaker(bind=engine)
session = Session()
# Рекомендуется брать 1 сессию и передавать параметром куда нам надо
session = session
