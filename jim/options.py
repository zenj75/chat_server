"""Константы для jim протокола, настройки"""
# Ключи
ACTION = 'action'
TIME = 'time'
USER = 'user'
ACCOUNT_NAME = 'account_name'
RESPONSE = 'response'
ERROR = 'error'


# Значения
PRESENCE = 'presence'
MESSAGE = 'message'
FROM = 'from'
TO = 'to'

GET_CONTACTS = 'get_contacts'
CONTACT_LIST = 'contact_list'
ADD_CONTACT = 'add_contact'
DEL_CONTACT = 'del_contact'

# Коды ответов (будут дополняться)
BASIC_NOTICE = 100
OK = 200
ACCEPTED = 202
WRONG_REQUEST = 400  # неправильный запрос/json объект
SERVER_ERROR = 500

# Кортеж из кодов ответов
RESPONSE_CODES = (BASIC_NOTICE, OK, ACCEPTED, WRONG_REQUEST, SERVER_ERROR)

# Кортеж действий
ACTIONS = (PRESENCE, MESSAGE, GET_CONTACTS, CONTACT_LIST, ADD_CONTACT, DEL_CONTACT)
