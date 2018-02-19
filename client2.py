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
from jim.options import *

'''
разгребам опции командной строки
'''
parser = OptionParser()

parser.add_option('-a', '--address', dest='address', default='localhost',\
	help='ADDRESS for server', metavar='ADDRESS')

parser.add_option('-p', '--port', dest='port', type='int', default=7771,\
	help='PORT for server', metavar='PORT')

parser.add_option('-t', '--to', dest='TO', default='#all_users',\
	help='[MSG] TO USERS', metavar='TO')

parser.add_option('-m', '--msg', dest='MSG', default='hi friends! whats up?',\
	help='MESSAGE to chat', metavar='MSG')

parser.add_option('-u', '--user', dest='FROM', default='some_user',\
	help='USER_NAME', metavar='FROM')

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

chat_msg = {
	"action":  'msg',
	"time":  "timestamp",
	"to":  "#room_name",
	"from":  "some_account_name",
	"encoding":"ascii",
	"message":"Hi all in this room!"
}

def check_response(response):
	if response[RESPONSE] == 200:
		return 200
	else:
		print('   >> BZZ! response not "200"\n')
		return 400

# соединяемся с сервером, получаем текущее время
with socket(AF_INET, SOCK_STREAM) as sock: # Создаем сокет TCP в менеджере контекста
	sock.connect((option.address, option.port)) # Соединиться с сервером

	tm = sock.recv(4096)
	print("Текущее время: %s" % tm.decode('ascii'))


	print(5)
	'''
	формируем json данные приветствия и посылаем их серверу
	'''
	send_msg(sock, presence)
	print(6)
	'''
	принимаем данные от сервера 
	'''
	response = get_msg(sock)
	print(7)
	if response:
		print("Принята проверка от сервера: %s\n" % response)
	else:
		print("Нет ответа от сервера, что-то пошло не так...\n")

	print(11)
	# проверяем ответ
	result = check_response(response)
	if result == 200:
		print('>> посылаем сообщение в чат\n')
		# основной цикл (работа с сообщениями)
		while True:
			# посылаем сообщение в чат (общий)
			my_msg = input('==> Вы хотите отправить сообщение? (y,n,exit): ')
			if my_msg == 'y':
				# формируем сообщение в словарь
				chat_msg[MESSAGE] = input('введите текст сообщения: ')
				# посылаем словарь
				send_msg(sock, chat_msg)
			elif my_msg == 'n':
				print('ОК, ждём входящих')
				response = get_msg(sock)
				# нужно функцию делать на предложение отправки сообщения

			elif my_msg == 'exit':
				print('EXIT!')
				sock.close()
				exit()
	else:
		print('ошибка при отправлении сообщения в чат\n')

		print(12)

	sock.close()

