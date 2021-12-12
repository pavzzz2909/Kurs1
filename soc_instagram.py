import requests
from pprint import pprint

def get_id(access_token):
    fields = 'id,account_type,media_count,username'
    url = (f'https://graph.instagram.com/v12.0/me'
            f'?fields={fields}'
            f'&access_token={access_token}')
    responses = requests.get(url = url).json()
    return responses['id']

def get_media_id(access_token):
    fields = 'caption,id,media_type,media_url,permalink,thumbnail_url,timestamp,username'
    user_id = get_id(access_token)
    url = (f'https://graph.instagram.com/v12.0/{user_id}/media'
                f'?fields={fields}'
                f'&access_token={access_token}')
    responses = requests.get(url = url).json()
    return responses['data']

def get_media_inst(access_token):
    fields = 'caption,id,media_type,media_url,permalink,thumbnail_url,timestamp,username'
    media_ids = get_media_id(access_token)
    urls = {}
    for id in media_ids:
        media_id = id['id']
        url = (f'https://graph.instagram.com/{media_id}'
                f'?fields={fields}'
                f'&access_token={access_token}')
        responses = requests.get(url = url).json()
        name = str(responses['id'])+'.jpg'
        date = responses['timestamp']
        url_capt = responses['media_url']
        urls[media_id] = {'filename':name, 'likes':0, 'size' :0, 'date':date, 'url':url_capt}
    print(f'Завершено формирование списка фотографий пользователя, всего обнаружено {len(urls)} фотография(ий)\n')
    return urls
