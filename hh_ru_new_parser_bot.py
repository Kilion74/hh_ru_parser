import telebot
import requests
import time

# Здесь нужно вставить токен вашего бота
API_TOKEN = '#'
bot = telebot.TeleBot(API_TOKEN)


# Приветственное сообщение
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Введите название вакансии для поиска:")


# Обработка сообщений с запросом вакансий
@bot.message_handler(func=lambda message: True)
def send_vacancies(message):
    search_query = message.text
    vacancies = search_vacancies(search_query)

    if vacancies:
        for vacancy in vacancies:
            bot.send_message(message.chat.id, format_vacancy(vacancy))
    else:
        bot.send_message(message.chat.id, "Вакансий по данному запросу не найдено.")

    # Снова просим ввести запрос для поиска
    bot.send_message(message.chat.id, "Введите название вакансии для поиска:")


def search_vacancies(query):
    url = 'https://api.hh.ru/vacancies'
    params = {'text': query, 'per_page': 5}  # Ограничим результаты до 5 вакансий для примера
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json().get('items', [])
    else:
        return []


def format_vacancy(vacancy):
    title = vacancy.get('name', 'Нет данных')
    salary = vacancy.get('salary')
    company = vacancy.get('employer', {}).get('name', 'Нет данных')
    location = vacancy.get('area', {}).get('name', 'Нет данных')
    url = vacancy.get('alternate_url', 'Нет данных')
    description = vacancy.get('snippet', {}).get('responsibility', 'Нет данных')

    if salary:
        salary_from = salary.get('from')
        salary_to = salary.get('to')
        currency = salary.get('currency', 'RUR')
        if salary_from and salary_to:
            salary_str = f"{salary_from} - {salary_to} {currency}"
        elif salary_from:
            salary_str = f"От {salary_from} {currency}"
        elif salary_to:
            salary_str = f"До {salary_to} {currency}"
        else:
            salary_str = "Не указана"
    else:
        salary_str = "Не указана"

    return (f"*Название вакансии:* {title}\n"
            f"*Зарплата:* {salary_str}\n"
            f"*Описание:* {description}\n"
            f"*Компания:* {company}\n"
            f"*Локация:* {location}\n"
            f"*Ссылка:* [Перейти]({url})")


while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(f"Ошибка: {e}")
        time.sleep(15)  # Подождем 15 секунд перед повторным запуском
