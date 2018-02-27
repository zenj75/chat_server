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
from optparse import OptionParser


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

#  проверяем тип сообщения (приветствие) и возвращаем код реультата проверки
def check_pres(pres_msg):
    if ACTION in pres_msg and pres_msg[ACTION] == 'presence':
        # print('   >> action is "presence". yataa! :)')
        return {RESPONSE: 200}
    else:
        # print('   >> action not "presence" in this message')
        return {RESPONSE: 400}


#  проверяем тип сообщения и возвращаем код реультата проверки
def check_msg(chat_msg):
    if ACTION in chat_msg and chat_msg[ACTION] == 'msg':
        print('....>> action is "msg"! we can transmit msg to all clients :)\n')
        return {RESPONSE: 200}
    else:
        print('   >> action not "msg" in message\n')
        return {RESPONSE: 400}


addres = (option.address, option.port)

# создаём серверный сокет
#server = socket(AF_INET, SOCK_STREAM)   # Создает сокет TCP
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(0)                   # Неблокирущий режим сокета
server.bind(addres)                	    # Присваивает порт (из параметра)
server.listen(5)                        # Переходит в режим ожидания запросов;
server.settimeout(0.2)                  # Таймаут необходим

def read_messages(read_clients, all_clients):
    # входящие сообщения
    messages = []
    for s in read_clients:
        try:
            # получаем входящие сообщения и добавляем в список
            inc_msg = get_msg(s)
            messages.append(inc_msg)
            print(22)
        except:
            print('UPS! клиент {}{} отключился'.format(s.fileno(),s.getpeername()))
            all_clients.remove(s)

    return messages     # возвращаем список сообщений

def send_messages(messages, write_clients, all_clients):
    # Отправляем сообщения клиентам, ожидающим входящие
    for s in write_clients:
        for message in messages:
            try:
                send_msg(s, message)
                print(33)
            except:
                print('UPS! клиент {} {} отключился'.format(s.fileno(), s.getpeername()))
                s.close()
                all_clients.remove(s)


def mainloop():
    inputs = [server]
    outputs = []

    ''' Основной цикл обработки запросов клиентов '''
    ##################################################

    while True:
        try:
            # принимаем запросы на соединение
            conn, addr = server.accept()
            # принимаем приветствие от клиентов
            presence = get_msg(conn)
            print('presence: %s' % presence)  # DEBUG
            # проверяем тип сообщения
            response = check_pres(presence)
            # если тип - привествие - посылем код ответа клиенту
            if response:
                print('...приветствие получено. отправляем ответ клиенту')
                send_msg(conn, response)
                print(11)
            else:
                print('<AHTUNG> some problem with presence...')

        except OSError as e:
            pass  # Таймаут вышел

        else:
            print("Получен запрос на соединение от %s" % str(addr))
            # добавляем входящее соединение в список
            inputs.append(conn)
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

    #
    # # Получаем сообщение от клиента
    # presence = get_msg(client)
    # # print(presence)   # DEBUG
    # # Проверяем сообщение (приветствие) и формируем ответ
    # response = check_msg(presence)
    # # print(response)     # DEBUG
    # if response:
    #     print('всё ОК, приветствие получено. отправляем ответ клиенту')
    #     send_msg(client,response)
    # else:
    #     print('ups, что-то пошло не так :)')

# server.close()