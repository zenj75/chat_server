import json

# Кодировка
ENCODING = 'utf-8'

# конвертируем сообщение в байты
def to_bytes(dmessage):
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