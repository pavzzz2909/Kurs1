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
    url_api_vk = 'https://api.vk.com/method/'
    p0 = f'photos.getAlbums?'
    p1 = f'owner_id={owner_id}&'
    p2 = f'need_system=1&'
    p3 = f'need_covers=1&'
    p4 = f'access_token={token_vkontakte}&'
    p5 = f'v=5.81'
    params = p0 + p1 + p2 + p3 + p4 + p5
    url = url_api_vk + params
    data = {}
    responses = requests.get(url = url).json()['response']['items']
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

def get_url_pic_vk(token_vkontakte, owner_id, users_album, count = 5):
    album_ids = ['profile','wall','saved']
    extended = 1
    photo_sizes = 1
    urls = {}
    for album_id in album_ids:
        url_api_vk = 'https://api.vk.com/method/'
        p0 = f'photos.get?'
        p1 = f'owner_id={owner_id}&'
        p2 = f'album_id={album_id}&'
        p3 = f'extended={extended}&'
        p4 = f'photo_sizes={photo_sizes}&'
        p5 = f'count={count}&'
        p6 = f'access_token={token_vkontakte}&'
        p7 = f'v=5.81'
        params = p0 + p1 + p2 + p3 + p4 + p5 + p6 + p7  #
        url = url_api_vk + params
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
    url_images = get_url_pic_vk(token_vkontakte, owner_id, users_album)
    print(f'Завершено получение фотографий пользователя, всего найдено {len(url_images["vk"])} фотографий')
    return url_images
