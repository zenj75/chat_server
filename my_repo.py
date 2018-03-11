from models import *
from server_errors import ContactDoesNotExist

class Repo:
    ''' Серверное хранилище '''
    def __init__(self, session):
        '''
        Запоминаем сессию, чтобы было удобно работать с ней
        :param session:
        '''
        self.session = session

    def add_client(self, username, info=None):
        """Добавление клиента"""
        new_item = User(username, info)
        self.session.add(new_item)
        self.session.commit()

    def client_exists(self, username):
        """Проверка, что клиент есть в базе """
        result = self.session.query(User).filter(User.Name == username).count() > 0
        return result

    # def get_client_by_username(self, username):
    #     """Получение (объекта) клиента по имени"""
    #     client = self.session.query(User).filter(User.Name == username).first()
    #     return client

    def add_contact(self, client_username, contact_username):
        """Добавление контакта"""
        contact = self.get_client_by_username(contact_username)
        if contact:
            client = self.get_client_by_username(client_username)
            if client:
                cc = Contacts(client_id=client.Id, contact_id=contact.Id)
                self.session.add(cc)
                self.session.commit()
            else:
                # raise NoneClientError(client_username)
                pass
        else:
            raise ContactDoesNotExist(contact_username)

    def friends_lst(user):
        ''' Получаем список контактов пользователя  '''
        friends_lst = session.query(Contacts).filter_by(Contact = user)
        #Sprint('\nCписок контактов пользователя :{}:'.format(user))
        flist = []
        for i in friends_lst:
            if not i:
                print(' -- нет контактов --')
            else:
                flist.append(i)
        return flist


################### ИГРАЕМСЯ С ДЕЙСТВИЯМИ С БАЗОЙ (LEARNING) ######################

#Mila = User('Milarepa', 'great master')
#session.add(Mila)

#Mila.Info = ('great master, hermit')
#session.commit()

# ch_contact = session.query(User).filter_by(Name = 'Vimalakirti').first()
# ch_contact.Name = 'Вималакирти'

# #
# session.add_all([
#     Contacts('Ananda','Milarepa'),
#     Contacts('Ananda','Vimalakirti'),
#     Contacts('Ananda','Shantideva'),
#     Contacts('Shantideva','Vimalakirti'),
#     Contacts('Shantideva', 'Marpa'),
#     Contacts('Shantideva', 'Milarepa'),
#     Contacts('Vimalakirti', 'Marpa'),
#     Contacts('Vimalakirti', 'Shantideva'),
#     Contacts('Vimalakirti', 'Milarepa')]
# )

# print(session.new)
# session.commit()

# qq1 = session.query(User).filter_by(Name = 'Миларепа').all()
# print(qq1)
#
# qq2 = session.query(User).filter_by(Name = 'Марпа').all()
# print(qq2)

# qq5 = session.query(Contacts).filter_by(Contact = 'Вималакирти').first()
# qq6 = session.query(Contacts).filter_by(Contact = 'Ананда').all()

''' 
    Пример удаления строк из таблицы (по данным из запроса):
    qq4 = session.query(Contacts).filter(Contacts.Id > 8)
    qq4.delete()

    for i in qq4:
        print(': %s' %i)
'''

#session.commit()
#############################################
#print('Контакты: ')
#for i in session.query(User):
#    print(i)

# выводим контакты
#friends_lst('Вималакирти')

