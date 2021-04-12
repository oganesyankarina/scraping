"""Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя,
сохранить JSON-вывод в файле *.json; написать функцию, возвращающую список репозиториев."""

import requests
from json import dump


def get_user_repos(username):
    req = requests.get(f'https://api.github.com/users/{username}/repos')
    save_get_results(username, req.json())
    for ind, item in enumerate(req.json()):
        print(f"Репозиторий {ind + 1}: {item['name']}, {item['svn_url']}")
    return [item['name'] for item in req.json()]


def save_get_results(username, data_json):
    with open(f'{username}.json', 'w', encoding='utf-8') as write_f:
        dump(data_json, write_f)
        print(f'Файл с данными о пользователе "{username}" сохранен!')


if __name__ == '__main__':

    username = 'oganesyankarina'
    print(f'Список репозиториев пользователя {username}:\n{get_user_repos(username)}')

    pass
