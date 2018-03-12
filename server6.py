#!/usr/bin/env python
#
# проект чат-сервера, первые шаги
'''
Функции ​​сервера:​
- принимает ​с​ообщение ​к​лиента (приветствие - presense);
- формирует ​​ответ ​к​лиенту (response код);
- отправляет ​​ответ ​к​лиенту (response код);
- принимает сообщение от клиента для других пользователей (msg)
- отправляет полученное сообщение всем подключенным пользователям (кроме присылающего)
Имеет ​​параметры ​к​омандной ​с​троки:
- -p ​​<port> ​-​ ​​TCP-порт ​​для ​​работы ​(​по ​у​молчанию ​​использует ​​порт ​​7777);
- -a ​​<addr> ​-​ ​I​P-адрес ​​для ​​прослушивания ​(​по ​у​молчанию ​с​лушает ​​все ​​доступные ​​адреса).
'''

#from socket import socket, AF_INET, SOCK_STREAM
import time
import sys
import socket
import select

from jim.utils import to_bytes, to_dict, get_msg, send_msg
from jim.options import *
from jim.jim_msg import *
from optparse import OptionParser
from my_repo import Repo


''' Разбираем аргументы командной строки '''
parser = OptionParser()

parser.add_option('-a', '--address', dest='address', default='localhost',\
	help='ADDRESS for server', metavar='ADDRESS')

parser.add_option('-p', '--port', dest='port', type='int', default=7777,\
	help='PORT for server', metavar='PORT')

(option, args) = parser.parse_args()
print('options: {}, args: {}'.format(option, args))

###############################################################
TIMESTAMP = time.ctime(time.time())

## ПРОВЕРКА ТИПА СООБЩЕНИЙ
def check_msg(message):
    ## проверяем тип сообщения - action
    if ACTION in message:
        # вытаскиваем содержимое action
        action = message.pop(ACTION)
        if action == PRESENCE:
            return PRESENCE
        elif action == GET_CONTACTS:
            return GET_CONTACTS
        elif action == ADD_CONTACT:
            return ADD_CONTACT
        elif action == DEL_CONTACT:
            return DEL_CONTACT
        elif action == MESSAGE:
            return MESSAGE
        else:
            print('некорректный action')
    else:
        # надо прикрутить проверки более подробно
        print('нет action в сообщени..')



addres = (option.address, option.port)
resp_msg = ''
contact_list = []

## создаём серверный сокет
#server = socket(AF_INET, SOCK_STREAM)   # Создает сокет TCP
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(0)                   # Неблокирущий режим сокета
server.bind(addres)                	    # Присваивает порт (из параметра)
server.listen(5)                        # Переходит в режим ожидания запросов;
server.settimeout(0.2)                  # Таймаут необходим

## ПРИНИМАЕМ СООБЩЕНИЯ
def read_messages(write_clients, all_clients):
    messages = []
    resp_msg = ''
    for s in write_clients:
        print('write_clients: %s' %s)
        try:
            print(143)
            ##############  Получаем и обрабатываем входящие сообщения #############
            inc_msg = get_msg(s)
            # проверяем тип сообшения (поле action)
            msg_type = check_msg(inc_msg)
            print('===> тип сообшения: %s  <===' %msg_type)     #DEBUG

            ## обрабатываем получение списка контактов
            if msg_type == 'get_contacts':
                print('===> получено от клиента: %s  <===' %inc_msg)
                ## формируем контакт лист для клиента
                # print('user: %s' %user)
                contact_list = Repo.friends_lst(user)
                #print('also, contact_list:: %s: ' %contact_list)

                ## формируем контакт лист для клиента
                put_contacts['contacts_list'] = contact_list
                put_contacts[TO] = inc_msg['from']
                #resp_msg = contact_list
                resp_msg = put_contacts
                #print('сформировали ответ клиенту :%s' %contact_list)
                print('сформировали ответ клиенту :%s' % resp_msg)

            ## Если тип message - просто ставим в очередь
            if msg_type == 'message':
                resp_msg = inc_msg
            print(155)
            ## добавляем сообщение в список
            messages.append(resp_msg)
            #print('messages_query_1 {|||||} : %s' %messages)
        except Exception as e:
            print('UPS_1! клиент {}{} отключился'.format(s.fileno(),s.getpeername()))
            print(e)
            all_clients.pop(s)
    return messages     # возвращаем список сообщений

# ПОСЫЛАЕМ СООБШЕНИЯ
def send_messages(messages, read_clients, all_clients):
    #print('(|||){}'.format(write_clients))
    # Отправляем сообщения клиентам, ожидающим входящие
    for s in read_clients:
        #print('read_clients: %s' %s)
        user = inputs[s]

        for message in messages:
            contact = message[TO]
            if contact == 'to_all':
                print('сообщение для всех')     #debug
                send(s,message)
            elif user == contact:
                # направляем конкретному адресату
                send(s,message)

def send(s,message):
    ''' отправка сообщения (сокращаем немного, нужно оптимизировать) '''
    all_clients = []
    try:
        print('MESSAGE in query: {}'.format(message))   # смотрим сообщение в очереди
        send_msg(s, message)
        # print('<|||>{}'.format(messages))
        print('=== >> Послали сообщение: %s' % message)
        # print(133)
    except Exception as e:
        print('UPS_2! клиент {} {} отключился'.format(s.fileno(), s.getpeername()))
        print(e)
        s.close()
        all_clients.pop(s)

def mainloop():
    #inputs = [server]
    global inputs
    inputs = {}
    outputs = []
    global conn
    conn = ''

    ''' Основной цикл обработки запросов клиентов '''
    ##################################################

    while True:
        try:
            # принимаем запросы на соединение
            conn, addr = server.accept()
            # принимаем приветствие от клиентов
            presence = get_msg(conn)
            print('... получено приветствие от клиента: %s' % presence)  # DEBUG
            # проверяем тип сообщения
            chk_presence = check_msg(presence)
            # если тип - привествие - посылем код ответа клиенту
            if chk_presence:
                response['status'] = OK
                conn_user = presence['user']['account_name']
                response['to'] = conn_user
                print('... отправляем ответ клиенту на приветствие ...')
                print('response: %s' %response)
                send_msg(conn, response)
                global user
                user = presence['user']['account_name']
            else:
                print('<AHTUNG> some problem with presence...')

        except OSError as e:
            pass  # Таймаут вышел

        else:
            print("<<||>>  Получен запрос на соединение от {}, user: {}".format(str(addr), conn_user))
            # добавляем входящее соединение в список (словарь!)
            ## + печатаем список соединений с пользователем
            inputs.update({conn:conn_user})
            for k,u in inputs.items():
                print('INPUTS: {}:{}'.format(k,u))
        finally:
            # проверка событий ввода-вывода
            wait = 0
            readable = []
            writible = []
            try:
                readable, writable, exceptional = select.select(inputs, inputs, [], wait)
            except:
                pass    # ничего не делаем, если клиент отключился

            requests = read_messages(readable, inputs)  # принимаем сообщения
            send_messages(requests, writable, inputs)   # отправляем сообщения всем


if __name__ == '__main__':
    print('Эхо-сервер2 запущен!')
    mainloop()

