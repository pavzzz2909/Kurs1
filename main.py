from pprint import pprint

from vkontakte import *
from yandex_disk import *



if __name__ == '__main__':
    url_images = {}
    id_user_vk = input('Введите id или никнэйм vk: ')
    token_vkontakte = input('Введите токен Вконтакте: ')
    token_yandex_disk = input('Введите токен пользователя Yandex диска: ')
    url_images['vk'] = get_url_vk(token_vkontakte,id_user_vk)
    upload_Yandex(url_images,token_yandex_disk) 
