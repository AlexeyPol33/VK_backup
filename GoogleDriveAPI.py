
import os
import sys
import requests
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from progress.bar import IncrementalBar 
            

class GoogleDriveAPI:
    __BUFFER_FILE = '_temporary_buffer_file_.tbf_local'

    def __init__(self):
        self.drive = self.__get_drive() 

    def __get_drive(self):
        try:
            gauth = GoogleAuth()
            gauth.LocalWebserverAuth()
            drive = GoogleDrive(gauth)
            return drive
        except:
            print('Ошибка Аутентификации')
            sys.exit()

    def get_info (self):

        info = self.drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
        
        return info

    def __anti_repetition (self,name, count = 1):

        title_list = []
        for title in self.get_info():
            title_list.append(title['title'])

        if name in title_list:
            if name[-1].isdecimal() and name[-2] == '_':
                name = name[:-2]
            name = name + f'_{count}'
            count += 1
            name = self.__anti_repetition(name=name,count=count)

        return name

    def create_folder (self, folder_name) -> str:
        folder_name = self.__anti_repetition(folder_name)
        metadete = {
        'title': folder_name,
        'mimeType': 'application/vnd.google-apps.folder'}

        my_file = self.drive.CreateFile(metadata=metadete)
        my_file.Upload()
        return folder_name

    def __upload_files(self,folder,list_files):
        """
        Загружает фотографии по внешней url в папку folder_name, 
        параметр files представляет собой лист словарей вида: [{'Имя файл.расширение':'url'},...]
        имена не должны повторяться, иначе загрузка будет не корректна 
        """
        folder_id = ''
        for file in self.get_info():
            if file ['title'] == folder:
                folder_id = file['id']

        bar = IncrementalBar('Загрузка файлов в GoogleDrive', max = len(list_files))
        for file in list_files:
            response = requests.get(f'{list(file.values())[0]}')
            with open(self.__BUFFER_FILE,'bw') as f:
                f.write(response.content)
            metadete = {
                "parents": [{"kind": f"drive#{folder}", "id": folder_id}],
                'title': f'{list(file.keys())[0]}',
                'mimeType': 'image/jpeg'}
            file = self.drive.CreateFile(metadata=metadete)
            file.SetContentFile(self.__BUFFER_FILE)
            file.Upload()
            bar.next()
        bar.finish()

    def do_backup (self,folder_name,list_files):
        folder_name = self.create_folder(folder_name)
        self.__upload_files(folder_name,list_files)
        os.remove(self.__BUFFER_FILE)

   

    
    


