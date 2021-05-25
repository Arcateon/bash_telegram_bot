import telebot
import config
import requests
from bs4 import BeautifulSoup
from telebot import types


bot = telebot.TeleBot(config.TOKEN)


def random_quote():
    """
    Возвращаем случайную цитату с баша.
    """
    url = 'https://bash.im/random'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Заменчем теги <br> на перенос строки \n.
    for j in soup.select('br'):
        j.replace_with('\n')

    quotes = soup.find_all('div', class_='quote__body', limit=1)

    # Избавляемся от оставшихся тегов, возвращаем только текст.
    for i in quotes:
        str_1 = i.text
        return str_1


"""
Пишем команду старт.
"""


@bot.message_handler(commands=['start'])
def welcome(message):
    sti = open('welcome.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)

    bot.send_message(message.chat.id, f'Добро пожаловать, {message.from_user.username}!\n'
                                      f'Я бот со случайными цитатами из bash.im\nПриятного чтения.')

    # Прикручиваем кнопку.
    markup = types.InlineKeyboardMarkup(row_width=2)
    main_button = types.InlineKeyboardButton('Случайная цитата', callback_data='random_quote')

    markup.add(main_button)

    bot.send_message(message.chat.id, f'{random_quote()}', reply_markup=markup)


"""
Пишем команду для справки.
"""


@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(message.chat.id, f'Здравствуйте!\nЭтот бот работает посредством парсинга\n'
                                      f'с помощью библиотеки <b>BeautifulSoup<b/>.\nДля старта используйте'
                                      f'команду /start.', parse_mode='html')


"""
Прописываем команду для кнопки.
"""


@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    if call.message:
        if call.data == 'random_quote':
            markup = types.InlineKeyboardMarkup(row_width=2)
            main_button = types.InlineKeyboardButton('Случайная цитата', callback_data='random_quote')

            markup.add(main_button)

            bot.send_message(call.message.chat.id, f'{random_quote()}', reply_markup=markup)

            # Заставляем исчезнуть кнопку после нажатия.
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)


bot.polling(none_stop=True)
