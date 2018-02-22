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

parser.add_option('-u', '--user', dest='user', default='some_user',\
 	help='User name', metavar='USERNAME')

parser.add_option('-r', '--read', dest='read_client', default='yes'  ,\
	help='This client only read messages', metavar='READ_MESSAGES')

parser.add_option('-w', '--write', dest='write_client', default='no',\
	help='This client only write messages', metavar='WRITE_MESSAGES')

(option, args) = parser.parse_args()
print('options: {}, args: {}'.format(option, args))


''' формируем json сообщение для сервера (приветствие) '''

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
	"encoding": "ascii",
	"message": "Hi all in this room!"
}

def check_response(response):
	if response[RESPONSE] == 200:
		return 200
	else:
		print('   >> BZZ! response not "200"\n')
		return 400

if __name__ == '__main__':
	print('начинаем соединение с сервером... пи-пи-пи')
	# соединяемся с сервером, получаем текущее время
	with socket(AF_INET, SOCK_STREAM) as sock: # Создаем сокет TCP в менеджере контекста
		sock.connect((option.address, option.port)) # Соединиться с сервером
		print('соединение установлено... ')

		# принимаем текущее время
		# tm = sock.recv(4096)
		# print("Текущее время: %s" % tm.decode('ascii'))

		'''	формируем json данные приветствия и посылаем их серверу  '''
		presence[USER][ACCOUNT_NAME] = option.user
		send_msg(sock, presence)
		print('послали данные приветствия... ')
		'''		принимаем данные (подтверждение) от сервера		'''
		response = get_msg(sock)
		#print('приняли ответ от сервера')
		if response:
			print("YATA! =) Принята проверка от сервера: %s\n" % response[RESPONSE])
		else:
			print("Нет ответа от сервера, что-то пошло не так...\n")

		# проверяем ответ
		result = check_response(response)
		if result == 200:
			# основной цикл (работа с сообщениями)
			if option.write_client == 'yes':
				while True:
					# посылаем сообщение в чат (общий) в цикле
					my_msg = input('==> Вы хотите отправить сообщение (y)? Для выхода жми exit!(e): ')
					if my_msg == 'y':
						# формируем сообщение в словарь
						chat_msg[MESSAGE] = input('введите текст сообщения: ')
						# посылаем словарь серверу
						send_msg(sock, chat_msg)
					elif my_msg == 'e':
						print('EXIT!')
						sock.close()
						exit()
					else:
						print('ошибка при отправлении сообщения в чат\n')
						sock.close()
						exit()
		while True:
			# принимаем сообщения из чата
			if option.read_client == 'yes':
				while True:
					print('ОК, ждём входящих')
					response = get_msg(sock)
					print('p_1')
					print('входящее сообщение: %s' %response)
			print('p_10')

		sock.close()

