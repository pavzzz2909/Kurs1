from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload,MediaFileUpload,MediaInMemoryUpload
from googleapiclient.discovery import build
from pprint import pprint
import io
import json
import requests

def create_files(folder_id,name,file_path,SERVICE_ACCOUNT_FILE):
    SCOPES = ['https://www.googleapis.com/auth/drive']
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('drive', 'v3', credentials=credentials)
    file_metadata = {
                    'name': name,
                    'mimeType': 'image/jpeg',
                    'parents': [folder_id]
                }
    media = MediaInMemoryUpload(requests.post(file_path).content, mimetype='image/jpeg', resumable=True)
    r = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    return r

def working_google(SERVICE_ACCOUNT_FILE):
    SCOPES = ['https://www.googleapis.com/auth/drive']
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('drive', 'v3', credentials=credentials)
    results = service.files().list(pageSize=100, fields="nextPageToken, files(id, name, mimeType)").execute()
    names = []
    for files in results['files']:
        if files['name'] not in names:
            names.append(files['name'])
    return names

def files_for_delete_google(SERVICE_ACCOUNT_FILE,names):
    SCOPES = ['https://www.googleapis.com/auth/drive']
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('drive', 'v3', credentials=credentials)
    results = service.files().list(pageSize=100, fields="nextPageToken, files(id, name, mimeType)").execute()
    names.append('Нетология')
    deleted = []
    for files in results['files']:
        if files['name'] not in names:
            deleted.append(files['id'])
    return deleted


def new_dir_google(SERVICE_ACCOUNT_FILE, dir):
    SCOPES = ['https://www.googleapis.com/auth/drive']
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('drive', 'v3', credentials=credentials)
    results = service.files().list(pageSize=100, fields="nextPageToken, files(id, name, mimeType)").execute()
    k = ''
    for i in results['files']:
        if i['name'] == dir:
            k = i['id']
    return k

def del_folser_dir(SERVICE_ACCOUNT_FILE,dir):
    SCOPES = ['https://www.googleapis.com/auth/drive']
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('drive', 'v3', credentials=credentials)
    service.files().delete(fileId=dir).execute()

def create_folder_google(SERVICE_ACCOUNT_FILE, dir):
    SCOPES = ['https://www.googleapis.com/auth/drive']
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('drive', 'v3', credentials=credentials)
    folder_id = working_google(SERVICE_ACCOUNT_FILE)
    name = dir
    file_metadata = {
        'name': name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [folder_id]
        }
    r = service.files().create(body=file_metadata,fields='id').execute()

def upload_google(dict_urls,SERVICE_ACCOUNT_FILE):
    files = working_google(SERVICE_ACCOUNT_FILE)
    for dir in dict_urls:
        json_file = []
        filename = 'filenames'+dir+'.json'
        folder = new_dir_google(SERVICE_ACCOUNT_FILE,dir)
        if folder == '':
            create_folder_google(SERVICE_ACCOUNT_FILE, dir)
            print('Папка создана')
        else:
            print(f'Папка {dir} уже существует')
        for key in dict_urls[dir]:
            in_json=[]
            filename = dict_urls[dir][key]['filename']
            file_path = dict_urls[dir][key]['url']
            if 'size' in dict_urls[dir][key].keys():
                size = dict_urls[dir][key]['size']
            else:
                size = 0
            if filename not in files:
                result = create_files(folder,filename,file_path,SERVICE_ACCOUNT_FILE)
                print(result)
                if result != None:
                    print(f'Файл {dict_urls[dir][key]["filename"]} успешно загружен')
                in_json = {'filename': dict_urls[dir][key]['filename'],"size":size}
                json_file.append(in_json)
            else:
                print(f'Файл {dict_urls[dir][key]["filename"]} имеется на Google Drive')
        json.dump(json_file,open(filename,'w+'))

def clear_google(SERVICE_ACCOUNT_FILE,dict_soc):
    files = files_for_delete_google(SERVICE_ACCOUNT_FILE,dict_soc)
    for file in files:
        del_folser_dir(SERVICE_ACCOUNT_FILE, file)
