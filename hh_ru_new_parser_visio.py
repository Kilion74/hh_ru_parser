import tkinter as tk
from tkinter import scrolledtext
from tkinter import font
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
                'description': item.get('snippet', {}).get('requirement', ''),  # Описание вакансии
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
    :return: Строка с информацией о зарплате или None, если информации нет.
    """
    if salary_info:
        if salary_info['from'] and salary_info['to']:
            return f"{salary_info['from']} - {salary_info['to']} {salary_info['currency']}"
        elif salary_info['from']:
            return f"От {salary_info['from']} {salary_info['currency']}"
        elif salary_info['to']:
            return f"До {salary_info['to']} {salary_info['currency']}"
    return "Зарплата не указана"


def search_vacancies():
    """
    Обрабатывает нажатие кнопки поиска и отображает вакансии.
    """
    keyword = keyword_entry.get()
    results_text.delete(1.0, tk.END)  # Очистка текстового поля перед новым запросом
    vacancies = get_vacancies(keyword)

    if vacancies:
        for vacancy in vacancies:
            result = f"Компания: {vacancy['company']}\n" \
                     f"Вакансия: {vacancy['title']}\n" \
                     f"Зарплата: {vacancy['salary']}\n" \
                     f"Обязанности: {vacancy['duties']}\n" \
                     f"Месторасположение: {vacancy['location']}\n" \
                     f"Описание: {vacancy['description']}\n" \
                     f"Ссылка: {vacancy['link']}\n\n"
            results_text.insert(tk.END, result)
    else:
        results_text.insert(tk.END, "Вакансий не найдено.")


# Настройка основного окна
root = tk.Tk()


def exit_fullscreen(event=None):
    root.attributes('-fullscreen', False)


custom_font = font.Font(family="Helvetica", size=20, weight="bold")
root.title("Поиск вакансий на HeadHunter")
root.geometry("1800x900")

# Поле для ввода ключевого слова
keyword_label = tk.Label(root, text="Введите ключевое слово:", font=custom_font)
keyword_label.pack(pady=20, padx=100)

# keyword_entry = tk.Entry(root, width=40)
# keyword_entry.pack()
keyword_entry = tk.Entry(root, width=50, font=("Helvetica", 20))  # Увеличенный шрифт
keyword_entry.pack(pady=20)

# Кнопка для поиска
search_button = tk.Button(root, text="Поиск", command=search_vacancies, font=custom_font)
search_button.pack(pady=20)

# Текстовое поле для вывода результатов
results_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=100, height=20, font=("Helvetica", 20))
results_text.pack(pady=10, padx=60)
# Устанавливаем отступы внутри текстового поля
results_text.config(padx=10, pady=10)
root.bind("<Escape>", exit_fullscreen)  # Выход из полноэкранного режима по нажатию ESC
# Запуск главного цикла
root.mainloop()
