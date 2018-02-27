import datetime
import os
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from srv_models import *

def friends_lst(user):
    '''
    выводим список контактов пользователя
    :param user:
    :return:
    '''
    friends_lst = session.query(Contacts).filter_by(Contact= user)
    print('\nCписок контактов пользователя :{}:'.format(user))
    for i in friends_lst:
        if not i:
            print(' -- нет контактов --')
        else:
            print('  * %s' % i)


#Mila = User('Milarepa', 'great master')
#session.add(Mila)

#Mila.Info = ('great master, hermit')
#session.commit()

# ch_contact = session.query(User).filter_by(Name = 'Vimalakirti').first()
# ch_contact.Name = 'Вималакирти'

#
# session.add_all([
#     Contacts('Ананда','Миларепа'),
#     Contacts('Ананда','Вималакирти'),
#     Contacts('Ананда','Шантидева'),
#     Contacts('Шантидева','Вималакирти'),
#     Contacts('Шантидева', 'Марпа'),
#     Contacts('Шантидева', 'Миларепа'),
#     Contacts('Вималакирти', 'Марпа'),
#     Contacts('Вималакирти', 'Миларепа')]
# )

# print(session.new)
session.commit()

# qq1 = session.query(User).filter_by(Name = 'Миларепа').all()
# print(qq1)
#
# qq2 = session.query(User).filter_by(Name = 'Марпа').all()
# print(qq2)

# qq5 = session.query(Contacts).filter_by(Contact = 'Вималакирти').first()
# qq6 = session.query(Contacts).filter_by(Contact = 'Ананда').all()

# пример удаления строк из таблицы (по данным из запроса)
qq4 = session.query(Contacts).filter(Contacts.Id > 8)
qq4.delete()

# debug
for i in qq4:
    print(': %s' %i)

session.commit()
#############################################
print('Контакты: ')
for i in session.query(User):
    print(i)

# выводим контакты
friends_lst('Вималакирти')

