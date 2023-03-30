import telebot
from telebot import types
import csv
import datetime
import time

bot = telebot.TeleBot("6290776101:AAEsU7xSYtxu2zWeGqjfh3wJ06tr9RPaiYA")

users_data = {}

def save_to_csv(user_id, username, decision):
    with open('data.csv', mode='a', newline='') as data_file:
        data_writer = csv.writer(data_file)
        data_writer.writerow([user_id, username, decision])

def update_user_data(user_id, stage, time):
    if user_id not in users_data:
        users_data[user_id] = {'stage': stage, 'time': time}
    else:
        users_data[user_id]['stage'] = stage
        users_data[user_id]['time'] = time

def check_and_send_reminders():
    now = datetime.datetime.now()
    for user_id, data in users_data.items():
        elapsed_time = now - data['time']
        if elapsed_time > datetime.timedelta(days=1) and data['stage'] != 'решение 3':
            bot.send_message(user_id, text='Привет! Не забудь завершить игру! Попробуй еще раз.')

@bot.message_handler(commands=['start'])
def start(message):
    button_1 = types.InlineKeyboardButton('Решение 1(да)', callback_data='решение 1')
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(button_1)

    update_user_data(message.chat.id, 'start', datetime.datetime.now())

    bot.send_message(message.chat.id, text=f'Привет, {message.from_user.first_name} ! Начнем игру?.', reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    user_id = call.from_user.id
    username = call.from_user.username
    now = datetime.datetime.now()

    if call.data == 'решение 1':
        save_to_csv(user_id, username, 'решение 1')
        update_user_data(user_id, 'решение 1', now)

        button_2 = types.InlineKeyboardButton('Решение 2(да)', callback_data='решение 2')
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(button_2)

        bot.send_message(call.message.chat.id, text=f'Вы выбрали "Решение 1(да)". Хороший выбор! А теперь выберите еще одну опцию:', reply_markup=keyboard)

    elif call.data == 'решение 2':
        save_to_csv(user_id, username, 'решение 2')
        update_user_data(user_id, 'решение 2', now)

        button_3 = types.InlineKeyboardButton('Решение 3(да)', callback_data='решение 3')
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(button_3)

        bot.send_message(call.message.chat.id, text=f'Отлично, теперь выберите еще одну опцию:', reply_markup=keyboard)

    elif call.data == 'решение 3':
        save_to_csv(user_id, username, 'решение 3')
        update_user_data(user_id, 'решение 3', now)

        bot.send_message(call.message.chat.id, text='Вы выбрали "Решение 3(да)". Поздравляем, вы выиграли!', reply_markup=types.ReplyKeyboardRemove())

def polling_with_reminders():
    while True:
        try:
            bot.polling(none_stop=True, interval=0, timeout=20)
        except Exception as e:
            print(e)
            time.sleep(10)
        finally:
            check_and_send_reminders()

if __name__ == '__main__':
    polling_with_reminders()
