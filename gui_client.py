# Qt contact list
#
from PyQt5 import QtWidgets, uic
import sys
from models import *
from client5 import User

# создаем приложение
app = QtWidgets.QApplication(sys.argv)
# грузим главную форму
window = uic.loadUi('contact_list.ui')

# пользователь, контакты которого будут выводится
client = User(Name = 'Vimalakirti')
contact_list = client.get_contacts()

def load_contacts(contacts):
    ''' получаем список контактов '''
    # сбрасываем список
    window.listWidget_ListContacts.clear()
    for contact in session.query(User):
        print('contact: %s' %contact)
        if contact in contacts:
            # добавляем контакт в список в окне
            window.listWidget_ListContacts.addItem(contact)

# грузим контакты при запуске
load_contacts(contact_list)