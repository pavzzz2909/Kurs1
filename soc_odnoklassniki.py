import requests
from pprint import pprint
from functools import reduce
from itertools import chain
import hashlib

def format_dict(urls):
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

def get_user_albums(application_secret_key_ok, application_key_ok, access_token_ok, owner_id, session_secret_key_ok):
    session_secret = access_token_ok+application_secret_key_ok
    session_secret_key_ok = hashlib.md5((session_secret).encode()).hexdigest()
    sig = f'application_key={application_key_ok}fid={owner_id}format=jsonmethod=photos.getAlbums{session_secret_key_ok}'
    sig_ok = hashlib.md5(sig.encode()).hexdigest()
    url = (f'https://api.ok.ru/fb.do?'
            f'application_key={application_key_ok}&'
            f'fid={owner_id}&'
            f'format=json&'
            f'method=photos.getAlbums&'
            f'sig={sig_ok}&'
            f'access_token={access_token_ok}')
    data = {}
    responses = requests.get(url = url).json()
    for response in responses['albums']:
        data[str(response["aid"])] = response["title"]
    lists = data.keys()
    print(f'Всего найдено {len(lists)} альбома(ов):')
    i = 0
    for list in lists:
        i +=1
        print(f'{i}. {data[list]}')
    return data

def get_id_pic_ok(application_secret_key_ok, application_key_ok, access_token_ok, owner_id, session_secret_key_ok):#), users_album, count = 5):
    album_ids = get_user_albums(application_secret_key_ok, application_key_ok, access_token_ok, owner_id, session_secret_key_ok).keys()
    ids_photos = []
    for album_id in album_ids:
        session_secret = access_token_ok+application_secret_key_ok
        session_secret_key_ok = hashlib.md5((session_secret).encode()).hexdigest()
        sig = f'aid={album_id}application_key={application_key_ok}fid={owner_id}format=jsonmethod=photos.getPhotos{session_secret_key_ok}'
        sig_ok = hashlib.md5(sig.encode()).hexdigest()
        url = (f'https://api.ok.ru/fb.do?'
                f'aid={album_id}&'
                f'application_key={application_key_ok}&'
                f'fid={owner_id}&'
                f'format=json&'
                f'method=photos.getPhotos&'
                f'sig={sig_ok}&'
                f'access_token={access_token_ok}')
        responses = requests.get(url = url).json()
        for photo in responses['photos']:
            ids_photos.append(photo['id'])
    return ids_photos

def get_url_pic_ok(application_secret_key_ok, application_key_ok, access_token_ok, owner_id, session_secret_key_ok):
    ids_photos = get_id_pic_ok(application_secret_key_ok, application_key_ok, access_token_ok, owner_id, session_secret_key_ok)
    urls = {}
    for id in ids_photos:
        session_secret = access_token_ok+application_secret_key_ok
        session_secret_key_ok = hashlib.md5((session_secret).encode()).hexdigest()
        sig = f'application_key={application_key_ok}fields=photo.album_id, photo.like_summary,photo.created_ms,photo.crop_height,photo.crop_size,photo.crop_width,photo.pic_maxformat=jsonmethod=photos.getPhotoInfophoto_id={id}{session_secret_key_ok}'
        sig_ok = hashlib.md5(sig.encode()).hexdigest()
        url = (f'https://api.ok.ru/fb.do?'
                f'application_key={application_key_ok}&'
                f'fields=photo.album_id, photo.like_summary,photo.created_ms,photo.crop_height,photo.crop_size,photo.crop_width,photo.pic_max&'
                f'format=json&'
                f'method=photos.getPhotoInfo&'
                f'photo_id={id}&'
                f'sig={sig_ok}&'
                f'access_token={access_token_ok}')
        responses = requests.get(url = url).json()
        responses = responses['photo']
        count = responses['like_summary']['count']
        name = str(count)+'.jpg'
        date = responses['created_ms']
        url_capt = responses['pic_max']
        urls[id] = {'filename':name, 'likes':count, 'date':date, 'url':url_capt}
    url_images = format_dict(urls)
    return url_images

def get_url_ok(application_secret_key_ok, application_id, access_token_ok, application_key_ok, owner_id, session_secret_key_ok):
    print(f'ID выбранного пользователя {owner_id}')
    url_images = get_url_pic_ok(application_secret_key_ok,application_key_ok, access_token_ok, owner_id,session_secret_key_ok)
    print(f'Завершено формирование списка фотографий пользователя, всего обнаружено {len(url_images)} фотография(ий)\n')
    return url_images
