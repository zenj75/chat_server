#!/usr/bin/env python
#
'''
Реализация простого клиента для эхо-сервера, тестируем поэтапно
Основные функции:
- формирует сообщение серверу (словарь)
- отправляет сообщение серверу (в байтах)
- принимает сообщение от сервера (статус)
'''
from socket import *
from optparse import OptionParser
from jim.utils import to_bytes, to_dict, get_msg, send_msg


'''
разгребам опции командной строки
'''
parser = OptionParser()

parser.add_option('-a', '--address', dest='address', default='localhost',\
	help='ADDRESS for server', metavar='ADDRESS')

parser.add_option('-p', '--port', dest='port', type='int', default=7777,\
	help='PORT for server', metavar='PORT')

(option, args) = parser.parse_args()
print('options: {}, args: {}'.format(option, args))


'''
формируем json сообщение для сервера (приветствие)
'''
presence = {
	"action": "presence",
	"time": "timestamp",
	"type": "status",
	"user": {
	"account_name": "ZENJ",
	"status": "Yep, I am here!"
	}
}


sock = socket(AF_INET, SOCK_STREAM) # Создать сокет TCP
sock.connect((option.address, option.port)) # Соединиться с сервером

tm = sock.recv(1024)
print("Текущее время: %s" % tm.decode('ascii'))

# '''
# посылаем немного данных серверу (debug)
# '''
# sdata = '...некоторые данные...'
# sock.sendall(sdata.encode('utf-8'))

'''
формируем json данные и посылаем их серверу
'''
send_msg(sock, presence)

'''
принимаем данные от сервера 
'''
response = get_msg(sock)
if response:
	print("Принята проверка от сервера: %s" % response)
else:
	print("Нет ответа от сервера, что-то пошло не так...")

sock.close()

