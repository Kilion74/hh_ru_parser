import csv

import requests

# Определяем базовый URL для API HeadHunter
BASE_URL = "https://api.hh.ru/vacancies"


def get_vacancies(keyword, page=0, per_page=100):
    """
    Получает список вакансий с HeadHunter по заданному ключевому слову.

    :param keyword: Ключевое слово для поиска вакансий.
    :param page: Номер страницы для получения вакансий (по умолчанию 0).
    :param per_page: Количество вакансий на странице (по умолчанию 10).
    :return: Список вакансий.
    """
    params = {
        'text': keyword,
        'page': page,
        'per_page': per_page,
        'only_with_salary': True  # Не включать вакансии без зарплаты
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        vacancies = []

        for item in data.get('items', []):
            vacancy = {
                'title': item.get('name'),  # Название вакансии
                'salary': parse_salary(item.get('salary')),  # Парсинг зарплаты
                'description': item.get('snippet', {}).get('responsibility', ''),  # Описание вакансии
                'company': item.get('employer', {}).get('name'),  # Название компании
                'location': item.get('area', {}).get('name'),  # Месторасположение
                'link': item.get('alternate_url')  # Ссылка на вакансии
            }
            vacancies.append(vacancy)

        return vacancies
    else:
        print(f"Ошибка при запросе данных: {response.status_code}")
        return []


def parse_salary(salary):
    """
    Парсит информацию о зарплате.

    :param salary: словарь с информацией о зарплате.
    :return: строка с зарплатой или текст о ее отсутствии.
    """
    if salary is None:
        return "Не указана"

    from_amount = salary.get('from', None)
    to_amount = salary.get('to', None)
    currency = salary.get('currency', 'RUR')

    if from_amount and to_amount:
        return f"{from_amount} - {to_amount} {currency}"
    elif from_amount:
        return f"От {from_amount} {currency}"
    elif to_amount:
        return f"До {to_amount} {currency}"
    else:
        return "Не указана"


if __name__ == "__main__":
    print("Введите ключевое слово для поиска вакансий: ")
    keyword = input().lower()
    vacancies = get_vacancies(keyword)

    for idx, vacancy in enumerate(vacancies, start=1):
        print(f"{idx}. Название: {vacancy['title']}")
        name = (f"{idx}. Название: {vacancy['title']}")
        print(f"    Зарплата: {vacancy['salary']}")
        salary = (f"   Зарплата: {vacancy['salary']}")
        print(f"   Описание: {vacancy['description']}")
        profy = (f"   Описание: {vacancy['description']}")
        print(f"   Компания: {vacancy['company']}")
        company = (f"   Компания: {vacancy['company']}")
        print(f"   Месторасположение: {vacancy['location']}")
        location = (f"   Месторасположение: {vacancy['location']}")
        print(f"   Ссылка: {vacancy['link']}")
        link = (f"   Ссылка: {vacancy['link']}")
        print()

        storage = {'name': name, 'selary': salary, 'vacancy': profy, 'company': company, 'location': location,
                   'url': link}

        with open(f'{keyword}.csv', 'a+', encoding='utf-16') as f:
            pisar = csv.writer(f, delimiter=';', lineterminator='\r')
            pisar.writerow(
                [storage['name'], storage['selary'], storage['vacancy'], storage['company'], storage['location'],
                 storage['url']])
