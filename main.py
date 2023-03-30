import telebot
from telebot import types
from colorama import init, Fore
import csv
import time
import schedule

init(autoreset=True)  # for colorama

bot = telebot.TeleBot("6290776101:AAEsU7xSYtxu2zWeGqjfh3wJ06tr9RPaiYA")

def save_to_csv(user_id, username, decision):
    with open('data.csv', mode='a', newline='') as data_file:
        data_writer = csv.writer(data_file)
        data_writer.writerow([user_id, username, decision])

@bot.message_handler(commands=['start'])
def start(message):
    button_1 = types.InlineKeyboardButton('Решение 1(да)', callback_data='решение 1')
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(button_1)

    bot.send_message(message.chat.id, text=f'Привет, {message.from_user.first_name} ! Начнем игру?.', reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    user_id = call.from_user.id
    username = call.from_user.username

    if call.data == 'решение 1':
        save_to_csv(user_id, username, 'решение 1')
        button_2 = types.InlineKeyboardButton('Решение 2(да)', callback_data='решение 2')
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(button_2)

        bot.send_message(call.message.chat.id, text=f'Вы выбрали "Решение 1(да)". Хороший выбор! А теперь выберите еще одну опцию:', reply_markup=keyboard)

    elif call.data == 'решение 2':
        save_to_csv(user_id, username, 'решение 2')
        button_3 = types.InlineKeyboardButton('Решение 3(да)', callback_data='решение 3')
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(button_3)

        bot.send_message(call.message.chat.id, text=f'Отлично, теперь выберите еще одну опцию:', reply_markup=keyboard)

    elif call.data == 'решение 3':
        save_to_csv(user_id, username, 'решение 3')
        bot.send_message(call.message.chat.id, text='Вы выбрали "Решение 3(да)". Поздравляем, вы выиграли!', reply_markup=types.ReplyKeyboardRemove())


bot.polling(none_stop=True)
