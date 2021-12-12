from pprint import pprint

from soc_vkontakte import *
from soc_odnoklassniki import *
from soc_instagram import *

from disk_yandex_disk import *
from disk_google_drive import *




if __name__ == '__main__':
    dict_soc = ['Нетология','vk','instagram','ok']
    social = int(input('Выберите социальную сеть (необходимо ввести число соответствующее социальной сети из списка):\n1. Вконтакте\n2. Instagram\n3. Одноклассники\n'))
    url_images = {}
    if social == 1:
        '''
        Вконтакте
        '''
        sistem = 'Вконтакте'
        id_user_vk = input('Введите id или никнэйм {sistem}')
        token_vkontakte = input('Введите токен {sistem}')
        url_images['vk'] = get_url_vk(token_vkontakte,id_user_vk)
        if url_images['vk'] == 0:
            url_images = {}
    elif social == 2:
        '''
        Instagram
        '''
        sistem = 'Instagram'
        access_token = input(f'Введите токен {sistem}: ')
        url_images['instagram'] = get_media_inst(access_token)
        if url_images['instagram'] == 0:
            url_images = {}
    elif social == 3:
        '''
        Одноклассники
        '''
        sistem = 'Одноклассники'
        id_user_ok = input(f'Введите id {sistem}')
        application_secret_key_ok = input(f'Введите application_secret_key {sistem}: ')
        application_id_ok = input(f'Введите application_id {sistem}: ')
        access_token_ok = input(f'Введите access_token {sistem}: ')
        application_key_ok = input(f'Введите application_key {sistem}: ')
        session_secret_key_ok = input(f'Введите session_secret_key {sistem}: ')
        url_images['ok'] = get_url_ok(application_secret_key_ok, application_id_ok, access_token_ok, application_key_ok, id_user_ok, session_secret_key_ok)
        if url_images['vk'] == 0:
            url_images = {}
    else:
        print('Вы ввели неверное значение социальной сети, попробуйте еще раз')

    if url_images != {}:
        disk = int(input('\nВыберите облочное хранилище (необходимо ввести число соответствующее облочному хранилищу из списка):\n1. YandexDisk\n2. GoogleDrive\n'))
        if disk == 1:
            token_yandex_disk = input('Введите токен пользователя Yandex диска\n')
            upload_Yandex(url_images,token_yandex_disk)
        elif disk == 2:
            SERVICE_ACCOUNT_FILE = input('Введите путь до json файла с данными сервисного аккаунта Google\n')
            upload_google(url_images,SERVICE_ACCOUNT_FILE)
            #clear_google(SERVICE_ACCOUNT_FILE,dict_soc) # Оставлю посколько апи гугла не видит удаление сделанное ручками
            pass
        else:
            print('Вы ввели неверное значение облачного хранилища, попробуйте еще раз')
