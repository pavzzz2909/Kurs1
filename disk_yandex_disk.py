import requests
from pprint import pprint
import json

class YaUploader:
    def __init__(self, token: str, file_path: str, path: str):
        self.token = token
        self.path = path
        self.file_path = file_path

    def get_headers(self):
        return {
                'Content-Type':'application/json',
                'Accept': 'application/json',
                'Authorization':'OAuth {}'.format(self.token)
        }

    def get_params(self):
        return {
                'path':self.path,
                'url':self.file_path
        }

    def upload_file(self, file_path: str, path: str):
        '''
        Метод загружает файл c url-адреса на яндекс диск
        '''
        files_url='https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = self.get_headers()
        params = self.get_params()
        response = requests.post(url=files_url, headers=headers, params=params)
        return response.status_code

class Yafolder_files:
    def __init__(self, token: str, path: str):
        self.token = token
        self.path = path

    def get_headers(self):
        return {
                'Accept':'application/json',
                'Authorization':'OAuth {}'.format(self.token)
        }

    def get_params(self):
        return {
                'path':self.path
        }

    def create(self):
        '''
        Метод загружает файл c url-адреса на яндекс диск
        '''
        files_url='https://cloud-api.yandex.net/v1/disk/resources'
        headers = self.get_headers()
        params = self.get_params()
        response = requests.get(url=files_url, headers=headers, params=params).json()
        return response




class Yafolder:
    def __init__(self, token: str, path: str):
        self.token = token
        self.path = path

    def get_headers(self):
        return {
                'Content-Type':'application/json',
                'Authorization':'OAuth {}'.format(self.token)
        }

    def get_params(self):
        return {
                'path':self.path
        }

    def create(self):
        '''
        Метод загружает файл c url-адреса на яндекс диск
        '''
        files_url='https://cloud-api.yandex.net/v1/disk/resources'
        headers = self.get_headers()
        params = self.get_params()
        response = requests.put(url=files_url, headers=headers, params=params)
        return response.status_code

def upload_Yandex(dict_urls,token):
    for dir in dict_urls:
        json_file = []
        filename = 'filenames_'+dir+'.json'
        created = Yafolder(token,dir)
        result_create = created.create()
        if result_create == 409:
            print('Папка уже ранее была создана')
        for key in dict_urls[dir]:
            res = {}
            path = dir+'/'+dict_urls[dir][key]['filename']
            file_path = dict_urls[dir][key]['url']
            folder = path.split('/')[0]
            in_files = Yafolder_files(token,path)
            res = in_files.create()
            print(res)
            if 'error' in res.keys():
                folder = Yafolder(token,folder)
                upload = YaUploader(token,file_path,path)
                in_json=[]
                if 'size' in dict_urls[dir][key].keys():
                    size = dict_urls[dir][key]['size']
                else:
                    size = 0
                result = upload.upload_file(file_path,path)
                if result == 202:
                    print(f'Файл {dict_urls[dir][key]["filename"]} успешно загружен')
                in_json = {'filename': dict_urls[dir][key]['filename'],"size":size}
                json_file.append(in_json)
            else:
                print(f'файл {dict_urls[dir][key]["filename"]} уже существует')
        json.dump(json_file,open(filename,'w+'))
