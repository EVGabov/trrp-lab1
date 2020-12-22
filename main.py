import os
import vk
from Cryptodome.Cipher import DES
import datetime

key = b'abcdefgh'
des = DES.new(key, DES.MODE_ECB)
filePath = "D:\\authData.txt"
value = 1


def pad(text):
    while len(text) % 8 != 0:
        text += b' '
    return text


def createPost():
    message = input("Введите текст записи\n")
    response = vkApi.wall.post(message=message)
    print(response)
    return response


def deletePost():
    postId = input("Введите id записи\n")
    response = vkApi.wall.delete(post_id=postId)
    if response == 1:
        print('Запись успешно удалена')
    else:
        print('Произошла ошибка при удалении сообщения')
    return response


def getLastPosts():
    posts = input("Введите кол-во записей, которое хотите просмотреть\n")
    response = vkApi.wall.get(count=posts)
    items = response['items']
    text1 =''
    text2 =''
    for item in items:
        date = datetime.datetime.fromtimestamp(item['date']).strftime('%Y-%m-%d %H:%M:%S')
        try:
            if item['copy_history']:
                text1 = 'Эта запись содержит репост другой записи'
        except Exception:
            text1 = ''
        try:
            if item['attachments']:
                text2 = 'Эта запись содержит медиафайл'
        except Exception:
                text2 = ''
        print('post_id: '+str(item['id'])+' date: '+date+' text: '+item['text']+' ' + text1 + text2)
    return response


def editPost():
    postId = input("Введите id записи\n")
    message = input("Введите текст записи\n")
    response = vkApi.wall.edit(post_id=postId, message=message)
    if response == 1:
        print('Запись успешно изменена')
    else:
        print('Произошла ошибка при изменении записи')
    return response


def exitProgram():
    print('Завершение работы')


def exitAcc():
    os.remove(filePath)
    print('Завершение работы')


print('Это приложение предназначено для работы с записями на стене в социальной сети Вконтакте')
if(os.path.isfile(filePath)):
    with open(filePath, 'rb') as f:
        encryptedData = f.read()
    decryptedData = des.decrypt(encryptedData)
    data = decryptedData.decode('utf-8').split('!')
    name = data[0]
    login = data[1]
    password = data[2].replace(' ', '')
else:
    print('Введите свое имя, логин и пароль для входа в учётную запись Вконтакте')
    name = input("Имя: ")
    login = input("Логин: ")
    password = input("Пароль: ")
    data = name+'!'+login+'!'+password
    encryptedData = des.encrypt(pad(bytes(data, 'utf-8')))
    with open(filePath, 'wb') as f:
        f.write(encryptedData)
try:
    session = vk.AuthSession(7664147, login, password, scope='wall')
    vkApi = vk.API(session, v='5.35', lang='ru')
    print("Вы авторизовались как " + name)
except Exception:
    print('Произошла ошибка при авторизации, проверьте введённые данные')
    os.remove(filePath)
    value = -1

while value > 0 and value < 5:
    value = int(input("Список возможных действий:\n1.Просмотреть последние n записей на странице.\n2.Создать новую запись.\n3.Изменить запись.\n4.Удалить запись.\n5.Выход из программы (без выхода из аккаунта)\n6.Выход из аккаунта\n"))
    result = {
        1: getLastPosts,
        2: createPost,
        3: editPost,
        4: deletePost,
        5: exitProgram,
        6: exitAcc,
    }.get(value, exitProgram)()
