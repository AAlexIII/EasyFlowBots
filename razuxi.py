import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import csv
import pandas as pd

bot = telebot.TeleBot('1181885362:AAHGMG3zg3KWfPWOuX1xSVgbzreiSAZ5WSs')


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
    if c == 'подача':
        # Todo: изменить названия
        blocks = {'Блок закупок МТР': 'Блок закупок МТР',
                  'Блок по управлению инфраструктурой': 'Блок по управлению инфраструктурой',
                  'Блок корпоративной защиты': 'Блок корпоративной защиты',
                  'Блок логистики (Складская и транспортная)': 'Блок логистики (Складская ',
                  'Блок обеспечения производства': 'Блок обеспечения производства',
                  'Блок организационных вопросов': 'Блок организационных вопросов',
                  'Блок правовых и корпоративных вопросов': 'Блок правовых и корпора',
                  'Блок программ по операционной эффективности': 'Блок программ по операционн',
                  'Блок ПЭБ, ОТ и ГЗ': 'Блок ПЭБ, ОТ и ГЗ',
                  'Блок Развития бизнеса': 'Блок Развития бизнеса',
                  'Блок Центр мониторинга бизнес-процессов проектной и закупочной деятельности': 'Блок Ц',
                  'Блок Центр управления качеством МТР': 'Блок Центр управления качеством МТР',
                  'Блок эффективности (БЭФ)': 'Блок эффективности (БЭФ)'}
        bot.send_message(who, 'Кому бы вы хотели направить свое рац. предложение?', reply_markup=make_keyboard(blocks))

    elif c[:4] == 'Блок':
        time = pd.read_csv('time.csv', sep=';', header=[0], encoding='cp1251')
        # Todo: возможно копировать из статуса значения
        time.append({'id': who, 'Куда': c, 'Проблема': None, 'Идея': None})
        bot.send_message(who, 'Опишите проблему в одном сообщении:')
    elif c == 'ideaY':
        bot.send_message(who, 'Опишите предложение по решению в одном сообщении:')
    elif c == 'ideaN':
        time = pd.read_csv('files/time.csv', sep=';', header=[0], encoding='cp1251')
        status = pd.read_csv('status.csv', sep=';', header=[0], encoding='cp1251')
        time.loc[time['id'] == who]['Идея'][0] = 'Предложений по решению нет'
        bot.send_message(who, 'Проверте правильность данных:')
        name = status.loc['id' == who]['Фамилия'].values[0]
        num = status.loc['id' == who]['Табельный номер'].values[0]
        problem = time.loc['id' == who]['Проблема'].values[0]
        idea = time.loc['id' == who]['Идея'].values[0]
        chek = f'Фамилия: {name}\nТабельный номер: {num}\n Проблема: {problem}\n Решение:{idea}'
        bot.send_message(who, chek)
        end = {'Да': 'end', 'Нет': 'not end'}
        bot.send_message(who, 'Всё ли представленно верно?', reply_markup=make_keyboard(end))
    elif c == 'end':
        # Todo: создать дата фрейм и начать заново
        pass
    elif c == 'notend':
        # Todo: настроить изменения + клава под каждое
        pass


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Напишите вашу фамилию')


@bot.message_handler(content_types=['text'])
def send_mes(message):
    t = message.text
    who = message.chat.id
    status = pd.read_csv('files/status.csv', sep=';', header=[0], encoding='cp1251')
    start_menu = {'Подать Рац предоложение': 'подача', 'Быстро подать': 'подача фаст'}
    # Todo: пропуск выбора блока
    if who not in status['id'].values:
        people = pd.read_csv('people.csv', sep=';', header=[0], encoding='cp1251')
        names = people.loc['Фамилия' == t.strip()]['Фамилия'].values
        if len(names) == 1:
            status.append({'id': who, 'Фамилия': names[0],
                           'Табельный номер': people.loc['Фамилия' == t.strip()]['Табельный номер'].values[0],
                           'Родной Блок': people.loc['Фамилия' == t.strip()]['Место работы'].values[0],
                           'Статус': 0})
            bot.send_message(who, f"Приветсвую {names[0]}", reply_markup=make_keyboard(start_menu))
        elif not names:
            bot.send_message(who, "Вас нет в списке пользователей обратитесь к @gasadaser")
        # Todo: много одинаковых фамилий

    else:
        time = pd.read_csv('time.csv', sep=';', header=[0], encoding='cp1251')
        if who in time['id']:
            if time.loc[time['id'] == who]['Проблема'][0] is None:

                time.loc[time['id'] == who]['Проблема'] = t
                yes_no = {'Да': 'ideaY', 'Нет': 'ideaY'}
                bot.send_message(who, 'Есть ли у вас предложения по решению проблемы?',
                                 reply_markup=make_keyboard(yes_no))
            elif time.loc[time['id'] == who]['Идея'][0] is None:
                # добавить в идею
                time.loc[time['id'] == who]['Идея'][0] = t
                bot.send_message(who, 'Проверте правильность данных:')
                name = status.loc['id' == who]['Фамилия'].values[0]
                num = status.loc['id' == who]['Табельный номер'].values[0]
                blok = time.loc['id' == who]['Куда'].values[0]
                problem = time.loc['id' == who]['Проблема'].values[0]
                idea = time.loc['id' == who]['Идея'].values[0]
                chek = f'Фамилия: {name}\nТабельный номер: {num}\nБлок:{blok} Проблема: {problem}\n Решение:{idea}'
                bot.send_message(who, chek)
                end = {'Да': 'end', 'Нет': 'not end'}
                bot.send_message(who, 'Всё ли представленно верно?', reply_markup=make_keyboard(end))


# Todo: найти функцию которая возращает значение сразу
# Todo: создать файлы
print('go')
bot.polling(none_stop=True)
