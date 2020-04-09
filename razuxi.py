import telebot
from telebot.types import KeyboardButton, ReplyKeyboardMarkup,InlineKeyboardMarkup,InlineKeyboardButton
import csv
import pandas as pd


@bot.message_handler(commands=['start'])

@bot.message_handler(content_types=['text'])


bot.polling(none_stop=True)
