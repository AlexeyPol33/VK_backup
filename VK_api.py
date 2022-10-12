
import os
import requests
import json
import sys

class VKapi:
    def __init__(self, access_token, user_id) -> None:
        self.access_token = access_token
        self.id = user_id
        self.url = 'https://api.vk.com/method/'
        self.version = '5.131'
        self.params = {'access_token': self.access_token, 'v': self.version}

    def users_info(self):

       url = self.url +'users.get'
       params = {'user_ids': self.id}
       response = requests.get(url, params={**self.params, **params})
       return response.json()

    def __error (self):
        """
        Проверка на ошибки доступа
        """
        info = self.users_info()
        if list(info.keys())[0] == 'error':
            print('error: ' + info['error']['error_msg'])
            sys.exit()
        
        if info['response'][0]['can_access_closed']:
            return
        else:
            print('error: ' + 'Профиль закрыт')
            sys.exit()

    def get_photos (self):
        """ 
        Метод возвращает список фотографий в альбоме формата [{фотографии с профиля},{фотографии со стены}].
        """
        self.__error()

        url = self.url +'photos.get'
        params = {'owner_id': self.id, 'extended':'1'}
        response = requests.get(url = url, params={**self.params,**params, 'album_id' : 'wall'})
        response_2 = requests.get(url = url, params={**self.params, **params, 'album_id' : 'profile'})

        out = [response_2.json(), response.json()]
        return out


    

    