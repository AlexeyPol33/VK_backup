
import json
from Backup import Backup
import os
import sys

def change_settings(settings = None):

    if settings == None:
        settings = {'vk_access' : '',
                    'vk_id' : '',
                    'ya_access_token' : '',
                    'client_secrets' : {}}
        settings['vk_access'] = input('vk_access=> ').lower()
        settings['vk_id'] = input('vk_id=> ').lower()
        settings['ya_access_token'] = input('ya_access_token=> ').lower()
    else:
        print('Какой атребут вы хотите изменить?(цифра)')
        user_answer = input ('1) vk_access\n2) vk_id\n3) ya_access_token\n=> ')
        if user_answer == '1':
            settings['vk_access'] = input('vk_access=> ').lower()
        if user_answer == '2':
            settings['vk_id'] = input('vk_id=> ').lower()
        if user_answer == '3':
            settings['ya_access_token'] = input('ya_access_token=> ').lower()

    with open('settings.json','w',encoding='utf-8') as f:
        json.dump(settings, f)

def load_settings ():
    vk_access = ''
    vk_id = ''
    ya_access_token = ''
    client_secrets = {}

    if os.path.isfile('settings.json'):
        settings = {}
        with open('settings.json', 'r') as f:
            settings = json.load(f)
        
        vk_access = settings['vk_access']
        vk_id = settings['vk_id']
        ya_access_token = settings['ya_access_token']
        client_secrets = settings['client_secrets']
    else:
        user_answer = input ('Файл с данными отсутствует, создать новый файл?(y/n)').lower()
        if user_answer == 'y':
            change_settings()
            settings = load_settings()
        else:
            print('Завершение работы программы')
            sys.exit()


    if vk_access.strip() == '':
        print('Отсутствует токен вк требуется ручное заполнение')
        user_answer = input('Введите токен вк: ')
        settings['vk_access'] = user_answer
    if vk_id.strip() == '':
        print('Отсутствует id пользователя требуется ручное заполнение')
        user_answer = input('Введите токен вк: ')
        settings['vk_id']
    if ya_access_token.strip() == '':
        print('Отсутствует токен яндекс диска, загрузка на яндекс диск не возможна.')
        settings['ya_access_token'] = None
    if not os.path.isfile('client_secrets.json'):
        if str(client_secrets).strip() =='':
            print('отстутствует файл clien_secrets.json')
            print('Пожалуйста добавьте файл в католог или добавьте содержимое в файл settings.json')
            print ('загрузка в гугл диск не доступна')
            settings['client_secrets'] = None
        else:
            with open ('client_secrets.json','w') as f:
                json.dump(client_secrets,f)
    print ('Файл settings загружен')
    return settings


if __name__ == '__main__':
    while True:

        yandex_disk = False
        google_drive = False
        settings = load_settings()
        print ('Желаете изменить settings?')
        if input('(y/n)').lower() == 'y':
            change_settings(settings)
            settings = load_settings()
            continue

        print('Сделать Backup:\n',
        '1)YandexDisk\n',
        '2)GoogleDrive\n',
        '3)YandexDisk и GoogleDrive\n')
        user_answer = input('1/2/3: ')
        if user_answer == '1':
            if(settings['ya_access_token']) == None:
                print('Отсутствует токен Яндекс Диска, загрузка не возможно')
                continue
            yandex_disk = True
        elif user_answer == '2':
            if (settings['client_secrets']) == None:
                print('Отсутствует файл client_secrets.json ',
                'и/или параметра client_secrets в файле settings.json')
                continue
            google_drive = True
        elif user_answer == '3':
            if (settings['client_secrets']) == None:
                print('Отсутствует файл client_secrets.json ',
                'и/или параметра client_secrets в файле settings.json')
                google_drive = False
            else:
                google_drive = True

            if(settings['ya_access_token']) == None:
                print('Отсутствует токен Яндекс Диска, загрузка не возможно')
                yandex_disk = False
            else:
                yandex_disk = True

            if not(yandex_disk or google_drive):
                print('Ни один из облачных сервисов не авторизован, загрузка не возможна.')
                sys.exit()
        else:
            print('Ответ не распознан')
            continue

        backup = Backup(VK_access_token=settings['vk_access'],
        VK_user_id=settings['vk_id'],
        yandex_api_token=settings['ya_access_token'],
        backup_yandex=yandex_disk,backup_google=google_drive)

        print ('Сохранить информацию по фотографиям в json-файл?')
        if input('(y/n): ').lower() == 'y':
            backup.save_to_file()
        break

    print('завершена работа программы')
