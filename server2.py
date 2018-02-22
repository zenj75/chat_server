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

from socket import socket, AF_INET, SOCK_STREAM
import time
import sys
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
        print('   >> action is "msg". we can transmit msg to all clients :)\n')
        return {RESPONSE: 200}
    else:
        print('   >> action not "msg" in message\n')
        return {RESPONSE: 400}

# создаём серверный сокет
def new_listen_socket(addr):
    server = socket(AF_INET, SOCK_STREAM)   # Создает сокет TCP
    server.bind(addr)                	    # Присваивает порт (из параметра)
    server.listen(5)                        # Переходит в режим ожидания запросов;
    server.settimeout(0.2)                  # Таймаут необходим
    server.setblocking(0)                   # Неблокирущий режим сокета
    return  server

def mainloop():
    addres = (option.address, option.port)
    clients = []
    sock = new_listen_socket(addres)

    ''' Основной цикл обработки запросов клиентов '''
    ##############################################################
    # сам цикл проверки
    while True:
        try:
            # Принять запрос на соединение
            conn, addr = sock.accept()
                ## посылаем текущее время
                ## timestamp = time.ctime(time.time()) + "\n"
                ## conn.send(timestamp.encode('ascii'))
            # принимаем сообщение от клиентов (presence)
            presence = get_msg(conn)
            print('presence: %s' % presence)        # DEBUG
            # проверяем тип сообщения
            response = check_pres(presence)
            # если тип - привествие - посылем код ответа клиенту
            if response:
                # print('...приветствие получено. отправляем ответ клиенту')
                send_msg(conn, response)
            else:
                print('ups, что-то пошло не так :)')
        except OSError as e:
            pass                            #  Таймаут вышел
        else:
            print("Получен запрос на соединение от %s" % str(addr))
            clients.append(conn)            # Добавляем соединения в список
            print(10)   # DEBUG
        finally:
            # Проверка наличия соединений (ввод-вывод) без таймаута
            outputs = []
            inputs = [sock]
             try:
                r, w, e = select.select(inputs, clients, inputs)
            except Exception as e:
                pass    # Ничего не делаем, если клиент отключится

            #print(11)
            # Обходим список клиентов, посылающих данные в сокет
            for w_client in w:
                print('current write connect: %s' % w_client)     # DEBUG
                try:
                    # принимаем сообщение от клиента (для чата)
                    input_msg = get_msg(w_client)
                    # проверяем тип сообщения (msg_chat)
                    resp_msg = check_msg(input_msg)
                    print('bzz2: %s' % resp_msg)     # DEBUG
                    if resp_msg:
                        #print('YATAA! :) входящее сообщение (raw): %s\n' % input_msg)
                        print('-------------------------- TADA! New message ---------------------------------')
                        print('from:  %s' % input_msg[FROM])
                        print('to: %s'% input_msg[TO])
                        print('time:  %s' % TIMESTAMP)
                        print('------- body message --------')
                        print('     MESSAGE: %s' % input_msg[MESSAGE])
                        print('--------------------------- END message  -----------------------------------')
                        # теперь надо переслать всем клиентам из списка подключенных :)
                    else:
                        print('нет ответа от клиента')
                except:
                    # Удаляем клиента, который отключился
                    clients.remove(w_client)
                    #print(13)

            # Проверка соединений, читающих сообщения из сокета
            for r_client in r:
                print('current read connect: %s' % r_client)     # DEBUG
                # отсылаем сообщения всем клиентам, читающим из сокета
                try:
                    # принимаем сообщение от клиента (для чата)
                    input_msg = get_msg(r_client)
                    # проверяем тип сообщения (msg_chat)
                    resp_msg = check_msg(input_msg)
                    if input_msg:
                        print('посылаем сообщения списку')
                        send_msg(r_client,input_msg)
                    else:
                        print('не можем послать сообщения. список пуст?')
                except:
                    # Удаляем клиента, который отключился
                    clients.remove(r_client)
            #print(13)

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