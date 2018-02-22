#!/usr/bin/env python
#
import json
import pytest
import doctest

# Кодировка
ENCODING = 'utf-8'

# конвертируем сообщение в байты
def to_bytes(dmessage):
    '''
    >>> some_dict = {'value' : '500'}
    >>> to_bytes(some_dict)
    b'{"value" : "500"}'
    '''
    # Преобразуем словарь в json
    jmessage = json.dumps(dmessage)
    # Переводим json в байты
    bmessage = jmessage.encode(ENCODING)
    # Возвращаем байты
    return bmessage

# конвертируем сообщение в словарь
def to_dict(bmessage):
    # Получаем из байтов json
    jmessage = bmessage.decode(ENCODING)
    # Получаем  из json словарь
    dmessage = json.loads(jmessage)
    # Возвращаем словарь
    return dmessage

# посылаем сообщение
def send_msg(socket, message):
    bmsg = to_bytes(message)    # словарь в байты
    socket.send(bmsg)           # отправка

# принимаем сообщение
def get_msg(socket):
    gmsg = socket.recv(1024)    # принимаем байты
    response = to_dict(gmsg)    # конвертируем в словарь
    return response             # возвращаем словарь

'''
тестируем с помощью pytest
'''
def setup():
    print ("01. setup Установка окружения по умолчанию в модуле")

def teardown():
    print ("02. teardown Сброс окружения по умолчанию в модуле")

##  тест проходит нормально
def test_to_bytes():
    print('test_to_bytes')
    some_dict = {"value":"500"}
    assert to_bytes(some_dict) == b'{"value": "500"}'


##  тест проходит нормально
def test_to_dict():
    print('test_to_dict')
    some_dict = b'{"value":"500"}'
    assert to_dict(some_dict) == {"value":"500"}

doctest.testmod()