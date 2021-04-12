"""Зарегистрироваться на https://openweathermap.org/api и написать функцию, которая получает погоду в данный момент
для города, название которого получается через input. https://openweathermap.org/current"""


import requests
from pprint import pprint


def get_my_key(file_name):
    with open(file_name, encoding='utf-8') as f:
        return [line.strip() for line in f][0]


key = get_my_key('key.txt')

if __name__ == '__main__':
    city_name = input('Введите название города латинскими буквами: ')
    try:
        req = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={key}')
        pprint(req.json())
    except Exception as e:
        print(e)
