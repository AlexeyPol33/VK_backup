
import requests

class Yadisk_api:
    def __init__(self, token) -> None:
        self.url = 'https://cloud-api.yandex.net/v1/disk/'
        self.token = token
        self.headers = {'Authorization': f'OAuth {self.token}'}

    def create_folder (self, name): # TODO Реализовать проверку на конфликты имен папок
        url = self.url + 'resources'
        params = dict(path = name)
        response = requests.put(url=url,headers=self.headers,params=params)
        return response

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
