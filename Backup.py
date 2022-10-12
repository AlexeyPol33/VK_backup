
import sys
from google_drive_api import GoogleDriveAPI
from vk_api import VKapi as VK
from yadisk_api import YaDisk 
import datetime
import os
import json

class Backup:
    def __init__(self,VK_access_token,VK_user_id, yandex_api_token=None,backup_yandex=False,backup_google=False) -> None:
    
        self.VK_access_token = VK_access_token
        self.VK_id = VK_user_id
        self.vk_api = VK(access_token=self.VK_access_token, user_id=self.VK_id)

        self.folder_name = f'backup_{datetime.date.today()}'
        self.photos = self.get_photo_list(self.vk_api.get_photos())

        if (backup_yandex and backup_google):
            self.ya_token = yandex_api_token
            self.yadisk_api = YaDisk(self.ya_token)
            self.yadisk_api.do_backup(self.folder_name,self.photos)
            GoogleDriveAPI().do_backup(self.folder_name,self.photos)
        elif backup_yandex:
            self.ya_token = yandex_api_token
            self.yadisk_api = YaDisk(self.ya_token)
            self.yadisk_api.do_backup(self.folder_name,self.photos)
        elif backup_google:
            GoogleDriveAPI().do_backup(self.folder_name,self.photos)
        else:
            sys.exit()


    def get_photo_list(self, vk_photos):


        photos_list = []

        for res in vk_photos:
            for photo in res['response']['items']:
                _name = str(photo['likes']['count']) + '.jpg'
                _url = photo['sizes'][-1]['url']
                photos_list.append({ _name : _url})
        
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
    
    def save_to_file (self) -> None:
        """
        Метод сохраняет <<content>> в json файл с названием <<file_name>> без перезаписи,
        если файл с названием <<file_name>> уже существует, создается файл с названием <<file_name>>_число 
        """
        content = self.photos 
        file_name = self.folder_name

        extension = '.json'
        counter = 1
        file_name_copy = file_name
        while os.path.exists(file_name + extension):
            file_name = file_name_copy +'_'+ str(counter)
            counter += 1
        file_name = file_name + '.json'
        with open(file_name,'w') as f:
            json.dump(content, f)
        pass


