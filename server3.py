#!/usr/bin/env python
#
# проект чат-сервера, первые шаги
'''
Функции ​​сервера:​
- принимает ​с​ообщение ​к​лиента;
- формирует ​​ответ ​к​лиенту;
- отправляет ​​ответ ​к​лиенту;
- имеет ​​параметры ​к​омандной ​с​троки:
- -p ​​<port> ​-​ ​​TCP-порт ​​для ​​работы ​(​по ​у​молчанию ​​использует ​​порт ​​7777);
- -a ​​<addr> ​-​ ​I​P-адрес ​​для ​​прослушивания ​(​по ​у​молчанию ​с​лушает ​​все ​​доступные ​​адреса).
'''

from socket import socket, AF_INET, SOCK_STREAM
import time
import sys
from jim.utils import to_bytes, to_dict, get_msg, send_msg

from optparse import OptionParser

'''
разбираем аргументы командной строки
'''
parser = OptionParser()

parser.add_option('-a', '--address', dest='address', default='localhost',\
	help='ADDRESS for server', metavar='ADDRESS')

parser.add_option('-p', '--port', dest='port', type='int', default=7777,\
	help='PORT for server', metavar='PORT')

(option, args) = parser.parse_args()
print('options: {}, args: {}'.format(option, args))

#####
addr = (option.address, option.port)

server = socket(AF_INET, SOCK_STREAM)  # Создает сокет TCP
server.bind(addr)                	  # Присваивает порт (из параметра)
server.listen(5)                       # Переходит в режим ожидания запросов;
                                  # одновременно обслуживает не более
                                  # 5 запросов.
action = ''

def check_msg(pres_msg):
    if action in pres_msg and pres_msg[action] == 'presence':
        print('   >> action is presence. yataa! :)')
        return {RESPONSE: 200}
    else:
        print('   >> action not presence in message, some wrong')
        return {RESPONSE: 400}


print('pin0')
while True:
    client, addr = server.accept()     # Принять запрос на соединение
    print("Получен запрос на соединение от %s" % str(addr))

    '''
    тестируем тайм-сервер
    '''
    timestr = time.ctime(time.time()) + "\n"
    # Обратите внимание, дальнейшая работа ведётся с сокетом клиента
    client.send(timestr.encode('ascii'))  # <-по сети должны передаваться байты,поэтому выполняется кодирование строки

    # '''
    # получаем данные от клиента (debug)
    # '''
    # rec = client.recv(1024)
    # rc_mess = rec.decode('utf-8')
    #
    # if rec:
    #    print('>> получено от клиента: {} <<'.format(rc_mess))
    # else:
    #    print('нет данных от клиента_1')

    # Получаем сообщение от клиента
    presence = get_msg(client)
    print(presence)
    # Проверяем сообщение (приветствие) и формируем ответ
    response = check_msg(presence)
    print(response)
    # if response:
    #     print('всё ОК, приветствие получено')
    # else:
    #     print('ups, что-то пошло не так :)')

server.close()