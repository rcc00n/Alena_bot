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
        with open('data.csv', mode='a', newline='', encoding='utf-8') as data_file:
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
    button_1 = types.InlineKeyboardButton('Смотреть первый урок', callback_data='решение 1')
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(button_1)

    data_manager.update_user_data(message.chat.id, 'start', datetime.datetime.now())

    bot.send_message(message.chat.id, text=f"""<b>📈Приветствую, инвестор!</b>

Сегодня для Вас откроются несколько тайн финансов и инвестиций, которые помогут <b>приумножить капитал💸</b>

Курс состоит из 3 уроков:

1️⃣ Первые шаги. Куда инвестировать? 

2️⃣Прибыльные стратегии на 20%+ годовых 

3️⃣Ответы на частые вопросы. Как не прогореть? 

<b>Скорее жмите на кнопку ниже, чтобы приблизить финансовую свободу👇</b>""",
                     reply_markup=keyboard, parse_mode="HTML")


@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    user_id = call.from_user.id
    username = call.from_user.username
    now = datetime.datetime.now()

    if call.data == 'решение 1':
        data_manager.save_to_csv(user_id, username, 'решение 1')
        data_manager.update_user_data(user_id, 'решение 1', now)

        button_2 = types.InlineKeyboardButton('Смотреть второй урок', callback_data='решение 2')
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(button_2)

        bot.send_message(call.message.chat.id, text=f"""<b>💰Урок 1. Первые шаги будущего миллионера. Куда инвестировать?</b>

В этом уроке:

📌Зачем нужны инвестиции?
📌Что сделать перед покупкой первой акции?
📌Где покупать активы?
📌Куда можно инвестировать? 

<b>Смотреть урок👇</b>

▶️<a href="{"https://youtu.be/SGh4PRXYpY4"}">{"УРОК ТУТ"}</a>◀️
▶️<a href="{"https://youtu.be/SGh4PRXYpY4"}">{"УРОК ТУТ"}</a>◀️
▶️<a href="{"https://youtu.be/SGh4PRXYpY4"}">{"УРОК ТУТ"}</a>◀️



После просмотра скорее переходите ко <b>второму уроку</b>, где будут конкретные <b>стратегии</b> инвестиций👇""", reply_markup=keyboard, parse_mode="HTML")

    elif call.data == 'решение 2':
        data_manager.save_to_csv(user_id, username, 'решение 2')
        data_manager.update_user_data(user_id, 'решение 2', now)

        button_3 = types.InlineKeyboardButton('Смотреть третий урок', callback_data='решение 3')
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(button_3)

        bot.send_message(call.message.chat.id, text=f"""<b>💵Урок 2. Прибыльные стратегии на 20%+ годовых</b>

В этом уроке <b>точный алгоритм действий</b>, как с минимальным рисками получать в <b>3-4 раза</b> больше, чем на банковском депозите.

<b>Смотреть урок👇</b>

▶️<a href="{"https://youtu.be/gWiTiYYk_NY"}">{"УРОК ТУТ"}</a>◀️
▶️<a href="{"https://youtu.be/gWiTiYYk_NY"}">{"УРОК ТУТ"}</a>◀️
▶️<a href="{"https://youtu.be/gWiTiYYk_NY"}">{"УРОК ТУТ"}</a>◀️

В следующем уроке вы узнаете о том, как <b>составить портфель</b>, как <b>НЕ прогореть</b> и как инвестировать в <b>криптовалюты.</b> 

<b>Смотрите его по ссылке ниже👇</b>""", reply_markup=keyboard, parse_mode="HTML")

    elif call.data == 'решение 3':
        data_manager.save_to_csv(user_id, username, 'решение 3')
        data_manager.update_user_data(user_id, 'решение 3', now)

        button_4 = types.InlineKeyboardButton('Я прошел курс и начинаю инвестировать', callback_data='решение 4')
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(button_4)

        bot.send_message(call.message.chat.id, text=f"""<b>💲Урок 3. Ответы на вопросы.</b>

<b>В этом уроке:</b>

❓Как инвестировать с нестабильным доходом?
❓Где найти деньги для инвестиций?
❓Как научиться трейдингу и зарабатывать на бирже?
❓Как не прогореть?
❓Как правильно погашать кредиты?
❓Как инвестировать в криптовалюты?

Приятного просмотра🥳""",
                         reply_markup=keyboard, parse_mode="HTML")

    elif call.data == 'решение 4':
        data_manager.save_to_csv(user_id, username, 'решение 4')
        data_manager.update_user_data(user_id, 'решение 4', now)



        bot.send_message(call.message.chat.id, text=f"""<b>Ура! Вы сделали первый шаг к финансовой свободе!</b>

📲Остаемся на связи:

<a href="{"https://t.me/alenakladko"}">{"Телеграмм-канал с новостями"}</a>

<a href="{"https://instagram.com/alena.kladko?igshid=NTc4MTIwNjQ2YQ=="}">{"Инстаграмм с полезными видео"}</a>

Отзывы, вопросы, предложения оставляйте тут 👉 @alena_kladko

С радостью все посмотрю❤️""",
                         reply_markup=types.ReplyKeyboardRemove(), parse_mode="HTML")


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
