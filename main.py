
from VK_api import VK_api as VK
from Yadisk_api import Yadisk_api as Yadisk
import datetime

class Backup:

    def __init__(self,VK_access_token,VK_user_id, yandex_api_token) -> None:
    
        self.VK_access_token = VK_access_token
        self.VK_id = VK_user_id
        self.ya_token = yandex_api_token
        self.vk_api = VK(access_token=self.VK_access_token, user_id=self.VK_id)
        self.yadisk_api = Yadisk(self.ya_token)
        self.do_backup()

        
    def do_backup (self):

        folder_name = f'backup_{datetime.date.today()}'
        folder_name = self.yadisk_api.create_folder(folder_name)
        self.yadisk_api.upload(folder_name, self.get_photo_list(self.vk_api.get_photos()))

        pass


    def get_photo_list(self, vk_photos):


        photos_list = []

        for res in vk_photos:
            for photo in res['response']['items']:
                photos_list.append({str(photo['likes']['count']) + '.jpg':(photo['sizes'][-1]['url'])})
        
        renamed_photos_list = []
        counter = 1                
        while len(photos_list) > 0:
            element = photos_list.pop(0)
            for i in photos_list:
                if list(i.keys())[0] == list(element.keys())[0]:
                    key = (list(i.keys())[0])
                    value = list(i.values())[0]
                    renamed_photos_list.append({key[:key.find('.')] + f'_{str(counter)}' + '.jpg': value})
                    counter += 1
                    photos_list.remove(i)

            if len(photos_list) == 1 and list(photos_list[0].keys())[0] == list(element.keys())[0]:
                key = (list(photos_list[0].keys())[0])
                value = list(photos_list[0].values())[0]
                renamed_photos_list.append({key[:key.find('.')] + f'_{str(counter)}' + '.jpg': value})
                counter += 1
                photos_list.pop(0)
            renamed_photos_list.append(element)
            counter = 1
        
        return renamed_photos_list

if __name__ == '__main__':
    vk_token = '' # Токен вк
    ya_token = '' # токен яндекс диска
    vk_id = '' # Вк id профиля

    b = Backup(vk_token,vk_id,ya_token)
    print(b.get_photo_list(b.vk_api.get_photos()))
 

    