import requests
from pprint import pprint
from functools import reduce
from itertools import chain

def get_max_mg_vk(list_of_dict):
    '''
    Ищем наибольший размер картинки
    '''
    dict = list_of_dict[0]
    for item in list_of_dict:
        if item['height'] > dict['height']:
            dict.update(item)
    return dict

def format_dict_vk(urls):
    '''
    Переименовываем файлы, названные по количеству лайков добавляя в них дату в формате возращаемом API VK
    '''
    rev_dict = {}
    for key, value in urls.items():
        rev_dict.setdefault(value['filename'], set()).add(key)
    result = set(chain.from_iterable(
        values for key, values in rev_dict.items()
        if len(values) > 1))
    for i in result:
        filename = str(urls[i]['filename']).split('.')[0]+'-'+str(urls[i]['date'])+'.jpg'
        urls[i]['filename'] = filename
    return urls

def get_user_id_vk(token_vkontakte, id_vk = 'begemot_korovin'):
    '''
    Получаем ID пользователя по никнэйму
    '''
    if type(id_vk) != type(1):
        url = f'https://api.vk.com/method/utils.resolveScreenName?screen_name={id_vk}&access_token={token_vkontakte}&v=5.81'
        owner_id = str(requests.get(url = url).json()['response']['object_id'])
    else:
        owner_id = id_vk
    return owner_id

def get_user_albums_vk(token_vkontakte, owner_id):
    url = (f'https://api.vk.com/method/'
            f'photos.getAlbums?'
            f'owner_id={owner_id}&'
            f'need_system=1&'
            f'need_covers=1&'
            f'access_token={token_vkontakte}&'
            f'v=5.81')
    data = {}
    responses = requests.get(url = url).json()
    key_error = 'error'
    key_response = 'response'
    if key_error in responses:
        print(f'Социальная сеть Вконтакте\n'
              f'В процессе исполнения программы возникла ошибка с кодом {responses["error"]["error_code"]}\n'
              f'Сообщение об ошибке: {responses["error"]["error_msg"]}')
        return data
    elif key_response in responses:
        responses = responses['response']['items']
        for response in responses:
            data[response["id"]] = response["title"]
        lists = data.keys()
        print(f'Всего найдено {len(lists)} альбома(ов):')
        i = 0
        for list in lists:
            i +=1
            print(f'{i}. {data[list]}')
        print()
        return data
    else:
        print(f'В процессе исполнения программы возникла ошибка')

def get_url_pic_vk(token_vkontakte, owner_id, users_album, count = 5):
    album_ids = ['profile','wall','saved']
    extended = 1
    photo_sizes = 1
    urls = {}
    for album_id in album_ids:
        url = (f'https://api.vk.com/method/'
                f'photos.get?'
                f'owner_id={owner_id}&'
                f'album_id={album_id}&'
                f'extended={extended}&'
                f'photo_sizes={photo_sizes}&'
                f'count={count}&'
                f'access_token={token_vkontakte}&'
                f'v=5.81')
        responses = requests.get(url = url).json()
        key = 'error'
        if key not in responses:
            responses = responses['response']['items']
            album = users_album[responses[0]["album_id"]]
            for response in responses:
                response_id = response['id']
                count = response['likes']['count']
                name = str(count)+'.jpg'
                date = response['date']
                url_img = get_max_mg_vk(response['sizes'])
                size = url_img['type']
                url_capt = url_img['url']
                urls[response_id] = {'filename':name, 'likes':count, 'size':size, 'date':date, 'url':url_capt}
    url_images = format_dict_vk(urls)
    return url_images

def get_url_vk(token_vkontakte,id_user):
    owner_id = int(get_user_id_vk(token_vkontakte, id_user))
    users_album = get_user_albums_vk(token_vkontakte, owner_id)
    if len(users_album) != 0:
        url_images = get_url_pic_vk(token_vkontakte, owner_id, users_album)
        print(f'Завершено формирование списка фотографий пользователя, всего обнаружено {len(url_images)} фотография(ий)\n')
        return url_images
    else:
        return 0
