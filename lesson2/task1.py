"""Необходимо собрать информацию о вакансиях на вводимую должность (используем input или через аргументы)
с сайтов Superjob и HH.
Приложение должно анализировать несколько страниц сайта (также вводим через input или аргументы).
Получившийся список должен содержать в себе минимум:
Наименование вакансии.
Предлагаемую зарплату (отдельно минимальную и максимальную).
Ссылку на саму вакансию.
Сайт, откуда собрана вакансия.
По желанию можно добавить ещё параметры вакансии (например, работодателя и расположение).
Структура должна быть одинаковая для вакансий с обоих сайтов.
Общий результат можно вывести с помощью dataFrame через pandas. Сохраните в json либо csv."""
import requests
import pandas as pd
import time

from bs4 import BeautifulSoup as bs
from fp.fp import FreeProxy
from datetime import date

pd.set_option('display.max_columns', 10)
pd.set_option('display.width', 320)

url = f"https://hh.ru/search/vacancy"
headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
           "Chrome/89.0.4389.114 Safari/537.36"}
proxies = {'http': f'{FreeProxy().get()}'}


def get_vacancy(url, vacancy, headers, proxies, page):
    params = {
        "L_save_area": "true",
        "clusters": "true",
        "enable_snippets": "true",
        "salary": {"st": "searchVacancy"},
        "text": f'{vacancy}',
        "showClusters": "true",
        "page": f"{page}",
    }
    r = requests.get(url, headers=headers, params=params, proxies=proxies)
    return bs(r.text, "html.parser")


def get_vacancy_info(vacancy):
    items_info = []
    i = 0
    soup = get_vacancy(url, vacancy, headers, proxies, str(i))
    while True:
        print(f"Обработка страницы {i + 1}")
        items = soup.find_all(attrs={"class": "vacancy-serp-item"})
        print(f"Количество вакансий на странице: {len(items)}")
        for el in items:
            info = {}

            vac = el.find("a", attrs={"class": "bloko-link", "data-qa": "vacancy-serp__vacancy-title"})
            info['vacancy'] = vac.getText().replace(u'\xa0', u' ')
            info['hyperlink'] = vac.attrs["href"]
            info['input_website'] = url

            employer = el.find("a", attrs={"class": "bloko-link bloko-link_secondary",
                                           "data-qa": "vacancy-serp__vacancy-employer"})
            if employer is None:
                print(f"\033[31mНекорректные данные по работодателю: {employer}\033[0m")
                info['employer'] = ''
            else:
                info['employer'] = employer.getText().replace(u'\xa0', u' ')

            address = el.find("span", attrs={"class": "vacancy-serp-item__meta-info",
                                             "data-qa": "vacancy-serp__vacancy-address"})
            if address is None:
                print(f"\033[31mНекорректный адрес: {address}\033[0m")
                info['address'] = ''
            else:
                info['address'] = address.getText().replace(u'\xa0', u' ')

            salary = el.find("span", attrs={"data-qa": "vacancy-serp__vacancy-compensation"})
            if salary is None:
                info['salary_min'] = None
                info['salary_max'] = None
                info['currency'] = None
            else:
                salary = salary.getText().replace(u'\xa0', u'')
                salary = salary.replace('\u202f', '')
                salary = salary.replace(' – ', ' ')
                salary = salary.split()

                if salary[0] == 'от':
                    info['salary_min'] = salary[1]
                    info['salary_max'] = None
                    info['currency'] = salary[2]
                elif salary[0] == 'до':
                    info['salary_min'] = None
                    info['salary_max'] = salary[1]
                    info['currency'] = salary[2]
                else:
                    info['salary_min'] = salary[0]
                    info['salary_max'] = salary[1]
                    info['currency'] = salary[2]
            items_info.append(info)

        i += 1
        print(f'Страница {i} обработана!\n')
        time.sleep(0.005)
        if soup.find(attrs={"class": "bloko-button", "data-qa": "pager-next"}) is None:
            break
        soup = get_vacancy(url, vacancy, headers, proxies, str(i))
    print()
    print('Информация по всем вакансиям собрана!')
    return items_info


if __name__ == '__main__':
    vacancy = input("Введите ключевые слова для поиска вакансий: ")
    vacancy_info = get_vacancy_info(vacancy)
    df = pd.DataFrame.from_records(vacancy_info)
    df.to_csv(f'Вакансии_{vacancy}_{date.today()}.csv', sep=';', index=False, encoding='utf-8')
    # df = pd.read_csv(f'Вакансии_{vacancy}_{date.today()}.csv', sep=';')
    print(df.sample(5))
