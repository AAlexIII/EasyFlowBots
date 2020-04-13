import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import csv
import pandas as pd

bot = telebot.TeleBot('1181885362:AAHGMG3zg3KWfPWOuX1xSVgbzreiSAZ5WSs')
redactor = str('9b2398&DC8b0e')
no_value = str('dc34srefi*b23')


def prover(who):
    time = pd.read_csv('files/time.csv', sep=';', header=[0], encoding='cp1251')
    status = pd.read_csv('files/status.csv', sep=';', header=[0], encoding='cp1251')
    bot.send_message(who, 'Проверте правильность данных:')
    name = status.loc[status['id'] == who]['Фамилия'].values[0]
    num = status.loc[status['id'] == who]['Табельный номер'].values[0]
    blok = time.loc[time['id'] == who]['Куда'].values[0]
    problem = time.loc[time['id'] == who]['Проблема'].values[0]
    idea = time.loc[time['id'] == who]['Идея'].values[0]
    chek = f'Фамилия: {name}\nТабельный номер: {num}\nБлок:{blok}\nПроблема: {problem}\nРешение:{idea}'
    bot.send_message(who, chek)
    end = {'Да': 'end', 'Нет': 'notend'}
    bot.send_message(who, 'Всё ли представленно верно?', reply_markup=make_keyboard(end))


def menu():
    pass


def make_keyboard(d: dict):
    keyboard = InlineKeyboardMarkup(row_width=1)
    for name, call in d.items():
        keyboard.add(InlineKeyboardButton(name, callback_data=call))
    return keyboard


@bot.callback_query_handler(func=lambda call: True)
def reaction(call):
    c = call.data
    who = call.message.chat.id
    mes = call.message.message_id
    if c == 'подача фаст':
        status = pd.read_csv('files/status.csv', sep=';', header=[0], encoding='cp1251')
        time = pd.read_csv('files/time.csv', sep=';', header=[0], encoding='cp1251')
        time = time.loc[time['id'] != who]
        blok = status.loc[status['id'] == who]['Родной Блок'].values[0]
        time.loc[len(time)] = [int(who), blok, no_value, no_value]
        time.to_csv('files/time.csv', sep=';', index=False, encoding='cp1251')
        # bot.send_message(who, 'Опишите проблему в одном сообщении:')
        bot.edit_message_text('Опишите проблему в одном сообщении:', chat_id=who,
                              message_id=mes)
    elif c == 'подача':
        # Todo: изменить названия
        blocks = {
            'Закупки МТР': '0Закупки МТР',
            'Управлению инфраструктурой': '0Управлению инфраструктурой',
            'Корпоративная защита': '0Корпоративная защита',
            'Логистика': '0Логистика',
            'Обеспечение производства': '0Обеспечение производства',
            'Орг. вопросы': '0Орг. вопросы',
            'Правовые и корпоративные вопросы': '0Правовые и корпоративные вопросы',
            'СУОД': '0СУОД',
            'ПЭБ, ОТ и ГЗ': '0ПЭБ, ОТ и ГЗ',
            'Развитие бизнеса': '0Развитие бизнеса',
            'Управление качеством МТР': '0Управление качеством МТР',
            'БЭФ': '0БЭФ'
        }
        # bot.send_message(who, 'Кому бы вы хотели направить свое рац. предложение?', reply_markup=make_keyboard(
        # blocks))
        bot.edit_message_text('Кому бы вы хотели направить свое рац. предложение?', chat_id=who,
                              message_id=mes, reply_markup=make_keyboard(blocks))
    elif c[0] == '0':
        time = pd.read_csv('files/time.csv', sep=';', header=[0], encoding='cp1251')
        time = time.loc[time['id'] != who]
        time.loc[len(time)] = [int(who), c[1:], no_value, no_value]
        time.to_csv('files/time.csv', sep=';', index=False, encoding='cp1251')
        # bot.send_message(who, 'Опишите проблему в одном сообщении:')
        bot.edit_message_text('Опишите проблему в одном сообщении:', chat_id=who,
                              message_id=mes)
    elif c[0] == '1':
        time = pd.read_csv('files/time.csv', sep=';', header=[0], encoding='cp1251')
        time.loc[time['id'] == who, 'Куда'] = c[1:]
        time.to_csv('files/time.csv', sep=';', index=False, encoding='cp1251')
        prover(who)
    elif c == 'ideaY':
        # bot.send_message(who, 'Опишите предложение по решению в одном сообщении:')
        bot.edit_message_text('Опишите предложение по решению в одном сообщении:', chat_id=who,
                              message_id=mes)
    elif c == 'ideaN':
        time = pd.read_csv('files/time.csv', sep=';', header=[0], encoding='cp1251')
        time.loc[time['id'] == who, 'Идея'] = 'Предложений нет'
        time.to_csv('files/time.csv', sep=';', index=False, encoding='cp1251')
        prover(who)
    elif c == 'end':
        end = pd.read_csv('data_base.csv', sep=';', header=[0], encoding='cp1251')
        time = pd.read_csv('files/time.csv', sep=';', header=[0], encoding='cp1251')
        status = pd.read_csv('files/status.csv', sep=';', header=[0], encoding='cp1251')
        name = status.loc[status['id'] == who]['Фамилия'].values[0]
        num = status.loc[status['id'] == who]['Табельный номер'].values[0]
        blok = time.loc[time['id'] == who]['Куда'].values[0]
        problem = time.loc[time['id'] == who]['Проблема'].values[0]
        idea = time.loc[time['id'] == who]['Идея'].values[0]
        end.loc[len(end)] = [name, int(num), blok, problem, idea]
        end.to_csv('data_base.csv', sep=';', index=False, encoding='cp1251')
        # time = time.drop(pd.where(time['id'] == who)[0])
        time = time.loc[time['id'] != who]
        time.to_csv('files/time.csv', sep=';', index=False, encoding='cp1251')
        start_menu = {'Подать Рац предоложение': 'подача', 'Быстро подать': 'подача фаст'}
        # bot.send_message(who, 'Ваше предложение записанно', reply_markup=make_keyboard(start_menu))
        bot.edit_message_text('Ваше предложение записанно', chat_id=who,
                              message_id=mes, reply_markup=make_keyboard(start_menu))

    elif c == 'notend':
        change = {'Решение проблемы': 'решение', 'Проблема': 'проблема', 'Блок': 'workplace', 'Фамилия': 'фамилия',
                  'Табельный номер': 'табельный номер'}
        # bot.send_message(who, 'Что хотите изменить?', reply_markup=make_keyboard(change))
        bot.edit_message_text('Что хотите изменить?', chat_id=who,
                              message_id=mes, reply_markup=make_keyboard(change))
    elif c == 'workplace':
        blocks = {
            'Закупки МТР': '1Закупки МТР',
            'Управлению инфраструктурой': '1Управлению инфраструктурой',
            'Корпоративная защита': '1Корпоративная защита',
            'Логистика': '1Логистика',
            'Обеспечение производства': '1Обеспечение производства',
            'Орг. вопросы': 'Орг. вопросы',
            'Правовые и корпоративные вопросы': '1Правовые и корпоративные вопросы',
            'СУОД': '1СУОД',
            'ПЭБ, ОТ и ГЗ': '1ПЭБ, ОТ и ГЗ',
            'Развитие бизнеса': '1Развитие бизнеса',
            'Управление качеством МТР': '1Управление качеством МТР',
            'БЭФ': '1БЭФ'
        }
        # bot.send_message(who, "Выбирете новое место подачи", reply_markup=make_keyboard(blocks))
        bot.edit_message_text("Выбирете новое место подачи", chat_id=who,
                              message_id=mes, reply_markup=make_keyboard(blocks))
    elif c == 'решение':
        time = pd.read_csv('files/time.csv', sep=';', header=[0], encoding='cp1251')
        time.loc[time['id'] == who, 'Идея'] = redactor
        time.to_csv('files/time.csv', sep=';', index=False, encoding='cp1251')
        # bot.send_message(who, "Опишите решение проблемы одним сообщением")
        bot.edit_message_text("Опишите решение проблемы одним сообщением", chat_id=who, message_id=mes)
    elif c == 'проблема':
        time = pd.read_csv('files/time.csv', sep=';', header=[0], encoding='cp1251')
        time.loc[time['id'] == who, 'Проблема'] = redactor
        time.to_csv('files/time.csv', sep=';', index=False, encoding='cp1251')
        # bot.send_message(who, "Опишите проблему одним сообщением")
        bot.edit_message_text("Опишите решение проблемы одним сообщением", chat_id=who, message_id=mes)
    elif c == 'фамилия':
        bot.send_message(who, 'не повезло')
    elif c == 'табельный номер':
        bot.send_message(who, 'беда')


@bot.message_handler(commands=['start'])
def start(message):
    who = message.chat.id
    status = pd.read_csv('files/status.csv', sep=';', header=[0], encoding='cp1251')
    start_menu = {'Подать Рац предоложение': 'подача', 'Быстро подать': 'подача фаст'}
    if who not in status['id'].values:
        bot.send_message(message.chat.id, 'Напишите вашу фамилию')
    else:
        n = status.loc[status['id'] == who]['Имя'].values[0]
        f = status.loc[status['id'] == who]['Фамилия'].values[0]
        bot.send_message(who, f"Приветсвую, {n} {f}", reply_markup=make_keyboard(start_menu))


@bot.message_handler(content_types=['text'])
def send_mes(message):
    t = message.text
    who = message.chat.id
    status = pd.read_csv('files/status.csv', sep=';', header=[0], encoding='cp1251')
    start_menu = {'Подать по своему блоку': 'подача', 'Подать по чужому блоку': 'подача фаст'}

    # Todo: возможноcть копировать из статуса значения
    # Todo: Фамилия и имя
    if who not in status['id'].values:
        people = pd.read_csv('people.csv', sep=';', header=[0], encoding='cp1251')
        names = people.loc[people['Фамилия'] == t.strip()]['Фамилия'].values

        if len(names) == 1:

            status.loc[len(status)] = [int(who), names[0],
                                       people.loc[people['Фамилия'] == t.strip()]['Имя'].values[0],
                                       int(people.loc[people['Фамилия'] == t.strip()]['Табельный номер'].values[0]),
                                       people.loc[people['Фамилия'] == t.strip()]['Место работы'].values[0], 0]
            status.to_csv('files/status.csv', sep=';', index=False, encoding='cp1251')
            n =people.loc[people['Фамилия'] == t.strip()]['Место работы'].values[0]
            bot.send_message(who,
                             f"Приветсвую, {names[0]} {n}",
                             reply_markup=make_keyboard(start_menu))
        elif not (names.size > 0):
            bot.send_message(who, "Вас нет в списке пользователей обратитесь к @gasadaser")
        # Todo: много одинаковых фамилий

    else:
        time = pd.read_csv('files/time.csv', sep=';', header=[0], encoding='cp1251')
        if who in time['id'].values:
            if time.loc[time['id'] == who]['Проблема'].values[0] == redactor:
                time.loc[time['id'] == who, 'Проблема'] = t
                time.to_csv('files/time.csv', sep=';', index=False, encoding='cp1251')
                prover(who)
            elif time.loc[time['id'] == who]['Идея'].values[0] == redactor:
                time.loc[time['id'] == who, 'Идея'] = t
                time.to_csv('files/time.csv', sep=';', index=False, encoding='cp1251')
                prover(who)
            elif time.loc[time['id'] == who]['Проблема'].values[0] == no_value:
                time.loc[time['id'] == who, 'Проблема'] = t
                time.to_csv('files/time.csv', sep=';', index=False, encoding='cp1251')
                yes_no = {'Да': 'ideaY', 'Нет': 'ideaN'}
                bot.send_message(who, 'Есть ли у вас предложения по решению проблемы?',
                                 reply_markup=make_keyboard(yes_no))
            elif time.loc[time['id'] == who]['Идея'].values[0] == no_value:
                # добавить в идею
                time.loc[time['id'] == who, 'Идея'] = t
                time.to_csv('files/time.csv', sep=';', index=False, encoding='cp1251')
                prover(who)
        else:
            bot.send_message(who, "Приветсвую, что вас интересует?", reply_markup=make_keyboard(start_menu))


# Todo: найти функцию которая возращает значение сразу

print('go')
bot.polling(none_stop=True)
