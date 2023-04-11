import telebot
from telebot import types
import csv
import datetime
import time
import schedule
import logging
from requests.exceptions import RequestException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = telebot.TeleBot("6290776101:AAEsU7xSYtxu2zWeGqjfh3wJ06tr9RPaiYA")


class UserDataManager:
    def __init__(self):
        self.users_data = {}

    def save_to_csv(self, user_id, username, decision):
        with open('data.csv', mode='a', newline='') as data_file:
            data_writer = csv.writer(data_file)
            data_writer.writerow([user_id, username, decision])

    def update_user_data(self, user_id, stage, time):
        if user_id not in self.users_data:
            self.users_data[user_id] = {'stage': stage, 'time': time}
        else:
            self.users_data[user_id]['stage'] = stage
            self.users_data[user_id]['time'] = time

    def check_and_send_reminders(self, bot):
        now = datetime.datetime.now()
        for user_id, data in self.users_data.items():
            elapsed_time = now - data['time']
            if elapsed_time > datetime.timedelta(days=1) and data['stage'] != 'решение 3':
                bot.send_message(user_id, text='Привет! Не забудь завершить игру! Попробуй еще раз.')


@bot.message_handler(commands=['start'])
def start(message):
    button_1 = types.InlineKeyboardButton('Решение 1(да)', callback_data='решение 1')
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(button_1)

    data_manager.update_user_data(message.chat.id, 'start', datetime.datetime.now())

    bot.send_message(message.chat.id, text=f'Привет, {message.from_user.first_name} ! Начнем игру?.',
                     reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    user_id = call.from_user.id
    username = call.from_user.username
    now = datetime.datetime.now()

    if call.data == 'решение 1':
        data_manager.save_to_csv(user_id, username, 'решение 1')
        data_manager.update_user_data(user_id, 'решение 1', now)

        button_2 = types.InlineKeyboardButton('Решение 2(да)', callback_data='решение 2')
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(button_2)

        bot.send_message(call.message.chat.id, text=f'Вы выбрали "Решение 1(да)". Хороший выбор! А теперь выберите '
                                                    f'еще одну опцию:', reply_markup=keyboard)

    elif call.data == 'решение 2':
        data_manager.save_to_csv(user_id, username, 'решение 2')
        data_manager.update_user_data(user_id, 'решение 2', now)

        button_3 = types.InlineKeyboardButton('Решение 3(да)', callback_data='решение 3')
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(button_3)

        bot.send_message(call.message.chat.id, text=f'Отлично, теперь выберите еще одну опцию:', reply_markup=keyboard)

    elif call.data == 'решение 3':
        data_manager.save_to_csv(user_id, username, 'решение 3')
        data_manager.update_user_data(user_id, 'решение 3', now)

        bot.send_message(call.message.chat.id, text='Вы выбрали "Решение 3(да)". Поздравляем, вы выиграли!',
                         reply_markup=types.ReplyKeyboardRemove())


def polling_with_reminders(data_manager_instance):
    schedule.every(1).hours.do(data_manager_instance.check_and_send_reminders, bot=bot)

    backoff = 1

    while True:
        try:
            bot.infinity_polling(timeout=20)
            backoff = 1
        except RequestException as e:
            logger.error(f'RequestException: {e}')
            time.sleep(backoff)
            backoff = min(backoff * 2, 300)
        except Exception as e:
            logger.error(f'Unexpected exception: {e}')
            time.sleep(10)

        schedule.run_pending()
        time.sleep(1)


def main():
    global data_manager
    data_manager = UserDataManager()
    polling_with_reminders(data_manager)


if __name__ == '__main__':
    main()
