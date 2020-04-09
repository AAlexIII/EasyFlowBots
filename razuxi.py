import telebot
from telebot.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
import csv
import pandas as pd

bot = telebot.TeleBot('1181885362:AAHGMG3zg3KWfPWOuX1xSVgbzreiSAZ5WSs')


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.id, 'Напишите вашу фамилию')


@bot.message_handler(content_types=['text'])
def send_mes(message):
    bot.send_message(message.id, 'куку')


bot.polling(none_stop=True)
