import requests

token = ...  # enter your token
url = 'https://cloud-api.yandex.net/v1/disk/resources'
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'OAuth {token}'
}


def creat_folder(name):
    params = {'path': name}
    response = requests.put(url, headers=headers, params=params)
    return response
