import requests
# имортируем библиотеку Requests для запросов к сайтам по протоколу http
from bs4 import BeautifulSoup
# имортируем библиотеку для парсинга BeautifulSoup
import json
# имортируем JSON для работы с данными в JSON

import time

url = 'https://spb.superjob.ru/vacancy/search/'
# обозначаем переменную url и помещаем в нее ссылку для парсинга
response = requests.get(url)
# обозначаем переменную response и делаем GET запрос через библиотеку Requests
response.status_code
# проверяем статус соединения, успешное соединение статус - 200

soup = BeautifulSoup(response.content, 'html.parser')

# Находим нужный класс и парсим целый блок с вакансией, на каждой странице 20 блоков, всего 100 страниц
all_vacancies = soup.find_all('div', class_='_1M4pN f-test-vacancy-item _9tHug _1jkjl _26kaQ _2_p8Q')

# обозначаем переменную main_link и помещаем в нее главную ссылку для склейки с продолжением адреса на вакансии
main_link = 'https://www.superjob.ru/'

'''Проходим циклом по каждому блоку объявления на странице
             и возвращаем нужные поля после парсинга'''

for vacanciya in all_vacancies:
    # Наименование вакансии
    title = vacanciya.find('span', class_='-gENC _1TcZY Bbtm8').text
    # Предлагаемая зарплата
    salary = vacanciya.find('span', class_='_2eYAG -gENC _1TcZY mO3i1 dAWx1').text
    # Ссылка на вакансию
    link = vacanciya.find('a').attrs['href']
    vacanciya_link = main_link + link



    vacanciya_list = []

    '''Проходим циклом по каждой странице'''

    for page_number in range(1, 100):
        print(f'Parsing page #{page_number}')
        url = f'https://spb.superjob.ru/vacancy/search/?page={page_number}.html'
        response = requests.get(url)
        time.sleep(0.15) # задержка
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            all_vacancies = soup.find_all('div', class_='_1M4pN f-test-vacancy-item _9tHug _1jkjl _26kaQ _2_p8Q')

            for vacanciya in all_vacancies:
                # Наименование вакансии
                title = vacanciya.find('span', class_='-gENC _1TcZY Bbtm8').text
                # Предлагаемая зарплата
                salary = vacanciya.find('span', class_='_2eYAG -gENC _1TcZY mO3i1 dAWx1').text
                # Ссылка на вакансию
                link = vacanciya.find('a').attrs['href']
                vacanciya_link = main_link + link

                vacanciya_data = {
                    'title': title,
                    'salary': salary,
                    'vacanciya_link': vacanciya_link
                }

                vacanciya_list.append(vacanciya_data)

        else:
            print(f'Ошибка: {response.status_code}')


# Создаем новый документ, записываем в него ответ

with open('data_SJ.json', 'w', encoding='utf8') as f:
    json.dump(vacanciya_list, f, ensure_ascii=False)
