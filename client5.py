#!/usr/bin/env python
#
'''
Реализация простого клиента для эхо-сервера, тестируем поэтапно
Основные функции:
- формирует сообщение серверу (словарь)
- отправляет сообщение серверу (в байтах)
- принимает сообщение от сервера (статус)
'''
import time
from socket import *
from optparse import OptionParser
from jim.utils import to_bytes, to_dict, get_msg, send_msg
from jim.options import *
from jim.jim_msg import *

'''
разгребам опции командной строки
'''
parser = OptionParser()

parser.add_option('-a', '--address', dest='address', default='localhost', \
                  help='ADDRESS for server', metavar='ADDRESS')

parser.add_option('-p', '--port', dest='port', type='int', default=7771, \
                  help='PORT for server', metavar='PORT')

parser.add_option('-u', '--user', dest='user', default='some_user', \
                  help='User name', metavar='USERNAME')

parser.add_option('-r', '--read', dest='read_client', default='yes', \
                  help='This client only read messages', metavar='READ_MESSAGES')

parser.add_option('-w', '--write', dest='write_client', default='no', \
                  help='This client only write messages', metavar='WRITE_MESSAGES')

(option, args) = parser.parse_args()
print('options: {}, args: {}'.format(option, args))

timestamp = time.ctime(time.time())
user = option.user

get_contacts = {
    "action": 'get_contacts',
    "time": timestamp,
    "from": user,
}


# пробуем сделать на классах :)
class User:
    def __init__(self, name):
        self.Name = name

    def connect(self):
        '''
		организация  соединения, создание сообщения серверу
		:return:
		'''
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.connect((option.address, option.port))
        print('GOOD! соединение установлено... ')

        #	формируем json данные приветствия и посылаем их серверу
        presence[USER][ACCOUNT_NAME] = option.user
        send_msg(self.sock, presence)
        print('послали данные приветствия... ')

        # принимаем данные (подтверждение) от сервера
        response = get_msg(self.sock)
        # print('приняли ответ от сервера')
        if response:
            print("YATA! =) Принята проверка от сервера: %s\n" % response)
        else:
            print("Нет ответа от сервера, что-то пошло не так...\n")

        # проверяем ответ и возвращем его
        # result_response = check_response(response)
        return response

    def disconnect(self):
        self.sock.__exit__()

    def write_message(self):
        while True:
            # посылаем сообщение в чат (общий) в цикле
            my_msg = input('==> Вы хотите отправить сообщение (y)? Для выхода жми exit!(e): ')
            if my_msg == 'y':
                # формируем сообщение в словарь
                chat_msg[MESSAGE] = input('введите текст сообщения: ')
                # посылаем словарь серверу
                chat_msg[FROM] = option.user
                print('message_test: %s' % chat_msg)
                send_msg(self.sock, chat_msg)
            elif my_msg == 'e':
                print('EXIT!')
                self.sock.close()
                exit()
            else:
                print('ошибка при отправлении сообщения в чат\n')
                self.sock.close()
                exit()

    def get_cont(self):
        # формируем запрос севреру на получение контактов
        get_contacts[FROM] = option.user
        try:
            ## получаем контакты от сервера
            send_msg(self.sock, get_contacts)
            print('послали запрос контактов... ')
        except Exception as e:
            print('EXCP: %s' %e)

        response = get_msg(self.sock)
        print('приняли ответ от сервера на запрос контактов')
        if response:
            print("YATA! =) Принят лист контактов  от сервера: %s\n" % response)
        else:
            print("Нет ответа от сервера, что-то пошло не так...\n")
        # проверяем ответ и возвращем его
        # result_response = check_response(response)
        return response

    def write_messages(self):
        # основной цикл (работа с сообщениями)
        if option.write_client == 'yes':
            while True:
                # посылаем сообщение в чат (общий) в цикле
                my_msg = input(
                    '==> Вы хотите отправить сообщение (y)? получить лист контактов (list)? Для выхода жми exit!(e): ')
                if my_msg == 'y':
                    # формируем сообщение в словарь
                    chat_msg[MESSAGE] = input('введите текст сообщения: ')
                    # посылаем словарь серверу
                    chat_msg[FROM] = option.user
                    print('message_test: %s' % chat_msg)
                    send_msg(self.sock, chat_msg)
                # получаем список контактов
                elif my_msg == 'list':
                    try:
                        #put_contacts[TO] = option.user
                        contacts = self.get_cont()
                        print(contacts)  # debug
                    except Exception as e:
                        print(e)
                elif my_msg == 'e':
                    print('EXIT!')
                    self.sock.close()
                    exit()
                else:
                    print('ошибка при отправлении сообщения в чат\n')
                    self.sock.close()
                    exit()

        while True:
            # принимаем сообщения из чата
            if option.read_client == 'yes':
                while True:
                    print('ОК, ждём входящих')
                    response = get_msg(self.sock)
                    # print('p_1')
                    print('входящее сообщение: "%s"' % response)
            print('p_10')


#############################################################
def check_response(response):
    if response[1] == 200:
        return OK
    else:
        print('   >> BZZ! response not "200"\n')
        return ERROR


if __name__ == '__main__':
    client = User(user)
    client.connect()
    client.write_messages()
    client.disconnect()



# OLD CODE
# print('начинаем соединение с сервером... пи-пи-пи')
# # соединяемся с сервером, получаем текущее время
# with socket(AF_INET, SOCK_STREAM) as sock: # Создаем сокет TCP в менеджере контекста
# 	sock.connect((option.address, option.port)) # Соединиться с сервером
# 	print('соединение установлено... ')
#
# 	### принимаем текущее время
# 	### tm = sock.recv(4096)
# 	### print("Текущее время: %s" % tm.decode('ascii'))
#
# 	## текущее время
# 	## timestamp = time.ctime(time.time()) + "\n"
# 	##conn.send(timestamp.encode('ascii'))
#
# 	'''	формируем json данные приветствия и посылаем их серверу  '''
# 	presence[USER][ACCOUNT_NAME] = option.user
# 	send_msg(sock, presence)
# 	print('послали данные приветствия... ')
# 	'''		принимаем данные (подтверждение) от сервера		'''
# 	response = get_msg(sock)
# 	#print('приняли ответ от сервера')
# 	if response:
# 		print("YATA! =) Принята проверка от сервера: %s\n" % response[RESPONSE])
# 	else:
# 		print("Нет ответа от сервера, что-то пошло не так...\n")
#
# 	# проверяем ответ
# 	result = check_response(response)
# 	if result == 200:
# 		# основной цикл (работа с сообщениями)
# 		if option.write_client == 'yes':
# 			while True:
# 				# посылаем сообщение в чат (общий) в цикле
# 				my_msg = input('==> Вы хотите отправить сообщение (y)? Для выхода жми exit!(e): ')
# 				if my_msg == 'y':
# 					# формируем сообщение в словарь
# 					chat_msg[MESSAGE] = input('введите текст сообщения: ')
# 					# посылаем словарь серверу
# 					chat_msg[FROM] = option.user
# 					print('message_test: %s' %chat_msg)
# 					send_msg(sock, chat_msg)
# 				elif my_msg == 'e':
# 					print('EXIT!')
# 					sock.close()
# 					exit()
# 				else:
# 					print('ошибка при отправлении сообщения в чат\n')
# 					sock.close()
# 					exit()
# 	while True:
# 		# принимаем сообщения из чата
# 		if option.read_client == 'yes':
# 			while True:
# 				print('ОК, ждём входящих')
# 				response = get_msg(sock)
# 				print('p_1')
# 				print('входящее сообщение: %s' %response)
# 		print('p_10')
#
# 	sock.close()
