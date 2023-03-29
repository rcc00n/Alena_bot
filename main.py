import telebot
from telebot import types
from time import *
from colorama import init, Fore
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

init(autoreset=True)  # for colorama

bot = telebot.TeleBot("6290776101:AAEsU7xSYtxu2zWeGqjfh3wJ06tr9RPaiYA")


# start command and func
@bot.message_handler(commands=['start'])  # start command
def start(message):  # start func
    current_time = strftime("%a %b %d %H:%M:%S %Y", localtime())
    print(Fore.LIGHTBLUE_EX + "/start", "спросил:", "ID", Fore.LIGHTGREEN_EX + str(message.from_user.id), "Имя:",
          Fore.LIGHTGREEN_EX +
          str(message.from_user.first_name), "Фамилия:", Fore.LIGHTGREEN_EX +
          str(message.from_user.last_name), "Ник:", Fore.LIGHTGREEN_EX +
          str(message.from_user.username), '////', Fore.LIGHTRED_EX + str(current_time))

    bot.reply_to(message,
                 f'Привет, {message.from_user.first_name} ! Начнем игру?.'
                 )




bot.polling(none_stop=True)
