import telebot
from telebot import types
from time import *
from colorama import init, Fore
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

init(autoreset=True)  # for colorama

bot = telebot.TeleBot("6290776101:AAEsU7xSYtxu2zWeGqjfh3wJ06tr9RPaiYA")

chat_id = 12345
# start command and func
@bot.message_handler(commands=['start'])  # start command
def start(message):  # start func
    current_time = strftime("%a %b %d %H:%M:%S %Y", localtime())
    print(Fore.LIGHTBLUE_EX + "/start", "спросил:", "ID", Fore.LIGHTGREEN_EX + str(message.from_user.id), "Имя:",
          Fore.LIGHTGREEN_EX +
          str(message.from_user.first_name), "Фамилия:", Fore.LIGHTGREEN_EX +
          str(message.from_user.last_name), "Ник:", Fore.LIGHTGREEN_EX +
          str(message.from_user.username), '////', Fore.LIGHTRED_EX + str(current_time))
    #bot.reply_to(message,
     #             f'Привет, {message.from_user.first_name} ! Начнем игру?.'
      #           )

    
    button_1 = types.InlineKeyboardButton('Решение 1(да)', callback_data='решение 1')
    button_2 = types.InlineKeyboardButton('Решение 2(нет)', callback_data='решение 2')

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(button_1)
    keyboard.add(button_2)
        
    bot.send_message(message.chat.id, text =  f'Привет, {message.from_user.first_name} ! Начнем игру?.', reply_markup=keyboard)

bot.polling(none_stop=True)