import requests

while True:
    print('Введи название вакансии...')
    work_name = input()
    # Определяем базовый URL для API HeadHunter
    BASE_URL = "https://api.hh.ru/vacancies"


    def get_vacancies(keyword, page=0, per_page=100):
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
                    'duties': item.get('snippet', {}).get('responsibility', ''),  # Обязанности
                    'company': item.get('employer', {}).get('name'),  # Название компании
                    'location': item.get('area', {}).get('name'),  # Месторасположение
                    'link': item.get('alternate_url')  # Ссылка на вакансию
                }
                vacancies.append(vacancy)

            return vacancies
        else:
            print(f"Ошибка при запросе данных: {response.status_code}")
            return []


    def parse_salary(salary_info):
        """
        Парсит информацию о зарплате.

        :param salary_info: Словарь с информацией о зарплате.
        :return: Строка с информацией о зарплате.
        """
        if not salary_info:
            return "Не указана"

        if salary_info.get('from') and salary_info.get('to'):
            return f"{salary_info['from']} - {salary_info['to']} {salary_info['currency']}"
        elif salary_info.get('from'):
            return f"От {salary_info['from']} {salary_info['currency']}"
        elif salary_info.get('to'):
            return f"До {salary_info['to']} {salary_info['currency']}"
        else:
            return "Не указана"


    # Пример использования
    if __name__ == "__main__":
        keyword = work_name  # Замените на любое другое ключевое слово, если необходимо
        vacancies = get_vacancies(keyword)

        for vacancy in vacancies:
            print(f"Название: {vacancy['title']}")
            print(f"Зарплата: {vacancy['salary']}")
            print(f"Обязанности: {vacancy['duties']}")
            # print(f"Описание: {vacancy['description']}")
            print(f"Компания: {vacancy['company']}")
            print(f"Месторасположение: {vacancy['location']}")
            print(f"Ссылка: {vacancy['link']}")
            print("=" * 40)
