import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import csv
import pandas as pd

bot = telebot.TeleBot('1181885362:AAHGMG3zg3KWfPWOuX1xSVgbzreiSAZ5WSs')

def menu():
    pass
def make_keyboard(d: dict):
    keyboard = InlineKeyboardMarkup(row_width=1)
    for name,call in d.items():
        keyboard.add(InlineKeyboardButton(name, callback_data=call))
    return keyboard

@bot.callback_query_handler(func=lambda call: True)
def reaction(call):

    c = call.data()
    who = call.message.chat.id
    if c == 'подача':
        blocks = {'Блок закупок МТР':'Блок закупок МТР',
                  'Блок по управлению инфраструктурой':'Блок по управлению инфраструктурой',
                  'Блок корпоративной защиты':'Блок корпоративной защиты',
                  'Блок логистики (Складская и транспортная)':'Блок логистики (Складская и транспортная)',
                  'Блок обеспечения производства':'Блок обеспечения производства',
                  'Блок организационных вопросов':'Блок организационных вопросов',
                  'Блок правовых и корпоративных вопросов':'Блок правовых и корпоративных вопросов',
                  'Блок программ по операционной эффективности':'Блок программ по операционной эффективности',
                  'Блок ПЭБ, ОТ и ГЗ':'Блок ПЭБ, ОТ и ГЗ',
                  'Блок Развития бизнеса':'Блок Развития бизнеса',
                  'Блок Центр мониторинга бизнес-процессов проектной и закупочной деятельности':'Блок Центр мониторинга бизнес-процессов проектной и закупочной деятельности',
                  'Блок Центр управления качеством МТР':'Блок Центр управления качеством МТР',
                  'Блок эффективности (БЭФ)':'Блок эффективности (БЭФ)'}
        bot.send_message(who, 'Кому бы вы хотели направить свое рац. предложение?', reply_markup=make_keyboard(blocks))
    if c[:4]=='Блок':
        time = pd.read_csv('time.csv', sep=';', header=[0], encoding='cp1251')
        #
        bot.send_message(who,'Опишите проблему:')



@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Напишите вашу фамилию')
    razuxi = []
    razuxi.append(1)
    for i in razuxi:
        print('e')

@bot.message_handler(content_types=['text'])
def send_mes(message):
    t = message.text
    who = message.chat.id
    stat = pd.read_csv('status.csv', sep=';', header=[0], encoding='cp1251')
    start_menu = {'Подать Рац предоложение': 'подача', 'Быстро подать': 'подача фаст'}
    if who not in stat:
        people = pd.read_csv('people.csv', sep=';', header=[0], encoding='cp1251')
        # ищем проверка количества добовляем
        bot.send_message(who, f"Приветсвую {stat}", reply_markup=make_keyboard(start_menu))
    else:
        time = pd.read_csv('time.csv', sep=';', header=[0], encoding='cp1251')
        if who in time:
            if problrm is None:
                # добавить в проблему
                yes_no={'Да':'','Нет':''}
                bot.send_message(who,'Есть ли у вас предложения по решению проблемы?',
                                 reply_markup=make_keyboard(start_menu))
            elif idea is None:
                # добавить в идею


    bot.send_message(who, 'куку')


bot.polling(none_stop=True)
