import requests
import unittest

from ya import url, creat_folder, headers


def get_name_list(path='disk:/'):
    params = {'path': path}
    response = requests.get(url, headers=headers, params=params).json()
    items = response['_embedded']['items']
    name_list = [item['name'] for item in items]
    return name_list


def delete_folder(path):
    params = {
        'path': path,
        'permanently': 'true'
    }
    requests.delete(url, headers=headers, params=params)


class TestYandexAPI(unittest.TestCase):
    def tearDown(self):
        delete_folder('test')

    def test_creat_folder_in(self):
        creat_folder('test')
        self.assertIn('test', get_name_list())

    def test_creat_folder_code(self):
        test = creat_folder('test')
        self.assertEqual(test.status_code, 201)
