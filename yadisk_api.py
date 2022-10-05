
from unicodedata import decimal
import requests

class Yadisk_api:
    def __init__(self, token) -> None:
        self.url = 'https://cloud-api.yandex.net/v1/disk/'
        self.token = token
        self.headers = {'Authorization': f'OAuth {self.token}'}

    def create_folder (self, name) -> str: # 
        url = self.url + 'resources'
        params = dict(path = name)
        response = requests.put(url=url,headers=self.headers,params=params)

        counter = 1
        while response.status_code == 409:
            if name[-1].isdecimal() and name[-2] == '_':
                name = name[:-2]
            name = name + f'_{counter}'
            params = dict(path = name)
            response = requests.put(url=url,headers=self.headers,params=params)
            counter +=1
        get_folder_name = (requests.get(url=url,headers=self.headers,params=params)).json()['name']

        return get_folder_name

    def upload (self,folder_name, files):
        """
        Загружает фотографии по внешней url в папку folder_name, 
        параметр files представляет собой лист словарей вида: [{'Имя файл.расширение':'url'},...]
        имена не должны повторяться, иначе загрузка будет не корректна """
        url = self.url + 'resources/upload'
        

        try:
            from progress.bar import IncrementalBar #Прогресс бар
            bar = IncrementalBar('Загрузка', max = len(files))
        except:
            pass

        for i in files:
            params = {'path':f'/{folder_name}/{list(i.keys())[0]}','url':f'{list(i.values())[0]}', 'replace':'false'}
            requests.post(url=url, headers=self.headers, params=params)
            
            try:
                bar.next()
            except:
                pass

        try:
            bar.finish()
        except:
            pass
