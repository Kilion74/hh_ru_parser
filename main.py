import requests  # pip install requests
import json

while True:
    print('Вакансия...')
    work_name = input()
    BASE_URL = "https://api.hh.ru/vacancies"


    def get_vacancies(keyword, page=0, per_page=100):
        params = {
            'text': keyword,
            'page': page,
            'per_page': per_page
        }

        response = requests.get(BASE_URL, params=params)

        if response.status_code == 200:
            data = response.json()
            vacancies = []

            for item in data['items']:
                vacancy = {
                    'title': item.get('name'),
                    'salary': parse_salary(item.get('salary')),
                    'company': item.get('employer', {}).get('name'),
                    'location': item.get('area', {}).get('name'),
                    'link': item.get('alternate_url')
                }
                vacancies.append(vacancy)

            return vacancies
        else:
            # Обработка ошибки при неудачном запросе
            print("Ошибка при запросе данных с HeadHunter")
            return []


    def parse_salary(salary):
        if salary is None:
            return "Не указана"

        from_amount = salary.get('from')
        to_amount = salary.get('to')
        currency = salary.get('currency')

        if from_amount and to_amount:
            return f"{from_amount} - {to_amount} {currency}"
        elif from_amount:
            return f"от {from_amount} {currency}"
        elif to_amount:
            return f"до {to_amount} {currency}"
        else:
            return "Не указана"


    # Демонстрация работы функции
    if __name__ == "__main__":
        keyword = work_name
        vacancies = get_vacancies(keyword)
        for vacancy in vacancies:
            # print(vacancy)
            print('\n')
            print(vacancy['title'])
            print(vacancy['salary'])
            print(vacancy['company'])
            print(vacancy['location'])
            print(vacancy['link'])
