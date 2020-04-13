import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import csv
import pandas as pd

bot = telebot.TeleBot('1181885362:AAHGMG3zg3KWfPWOuX1xSVgbzreiSAZ5WSs')


def prover(who):
    time = pd.read_csv('files/time.csv', sep=';', header=[0], encoding='cp1251')
    status = pd.read_csv('files/status.csv', sep=';', header=[0], encoding='cp1251')
    bot.send_message(who, 'Проверте правильность данных:')
    name = status.loc[status['id'] == who]['Фамилия'].values[0]
    num = status.loc[status['id'] == who]['Табельный номер'].values[0]
    blok = time.loc[time['id'] == who]['Куда'].values[0]
    problem = time.loc[time['id'] == who]['Проблема'].values[0]
    idea = time.loc[time['id'] == who]['Идея'].values[0]
    chek = f'Фамилия: {name}\nТабельный номер: {num}\nБлок:{blok}Проблема: {problem}\nРешение:{idea}'
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
    if c == 'подача фаст':
        status = pd.read_csv('files/status.csv', sep=';', header=[0], encoding='cp1251')
        time = pd.read_csv('files/time.csv', sep=';', header=[0], encoding='cp1251')
        blok = status.loc[status['id'] == who]['Родной Блок'].values[0]
        time.loc[len(time)] = [int(who), blok, '0', '0']
        time.to_csv('files/time.csv', sep=';', index=False, encoding='cp1251')
        bot.send_message(who, 'Опишите проблему в одном сообщении:')
    elif c == 'подача':
        # Todo: изменить названия
        blocks = {'Блок закупок МТР': 'Блок закупок МТР',
                  'Блок по управлению инфраструктурой': 'Блок по управлен',
                  'Блок корпоративной защиты': 'Блок корпо',
                  'Блок логистики (Складская и транспортная)': 'Блок логистики (Складская ',
                  'Блок обеспечения производства': 'Блок обеспечения ',
                  'Блок организационных вопросов': 'Блок организацион',
                  'Блок правовых и корпоративных вопросов': 'Блок право',
                  'Блок программ по операционной эффективности': 'Блок програм',
                  'Блок ПЭБ, ОТ и ГЗ': 'Блок ПЭБ, ОТ и ГЗ',
                  'Блок Развития бизнеса': 'Блок Развития бизнеса',
                  'Блок Центр мониторинга бизнес-процессов проектной и закупочной деятельности': 'Блок Ц',
                  'Блок Центр управления качеством МТР': 'Блок Центр уп',
                  'Блок эффективности (БЭФ)': 'Блок эффективности (БЭФ)'}
        bot.send_message(who, 'Кому бы вы хотели направить свое рац. предложение?', reply_markup=make_keyboard(blocks))

    elif c[:4] == 'Блок':
        time = pd.read_csv('files/time.csv', sep=';', header=[0], encoding='cp1251')

        time.loc[len(time)] = [int(who), c, '0', '0']
        time.to_csv('files/time.csv', sep=';', index=False, encoding='cp1251')
        bot.send_message(who, 'Опишите проблему в одном сообщении:')
    elif c[:4] == '1Бло':
        time = pd.read_csv('files/time.csv', sep=';', header=[0], encoding='cp1251')
        time.loc[time['id'] == who, 'Куда'] = c[1:]
        time.to_csv('files/time.csv', sep=';', index=False, encoding='cp1251')
        prover(who)
    elif c == 'ideaY':
        bot.send_message(who, 'Опишите предложение по решению в одном сообщении:')
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
        end.loc[len(end)] = [name, num, blok, problem, idea]
        end.to_csv('data_base.csv', sep=';', index=False, encoding='cp1251')
        # time = time.drop(pd.where(time['id'] == who)[0])
        time = time.loc[time['id'] != who]
        time.to_csv('files/time.csv', sep=';', index=False, encoding='cp1251')
        start_menu = {'Подать Рац предоложение': 'подача', 'Быстро подать': 'подача фаст'}
        bot.send_message(who, 'Ваше предложение записанно', reply_markup=make_keyboard(start_menu))
        # Todo: создать дата фрейм и начать заново

    elif c == 'notend':
        change = {'Решение проблемы': 'решение', 'Проблема': 'проблема','Блок':'workplace', 'Фамилия': 'фамилия',
                  'Табельный номер': 'табельный номер'}
        bot.send_message(who, 'Что хотите изменить?', reply_markup=make_keyboard(change))
        # Todo: добавить изменение Места работы
    elif c =='workplace':
        blocks = {'Блок закупок МТР': '1Блок закупок МТР',
                  'Блок по управлению инфраструктурой': '1Блок по управлен',
                  'Блок корпоративной защиты': '1Блок корпо',
                  'Блок логистики (Складская и транспортная)': '1Блок логистики (Складская ',
                  'Блок обеспечения производства': '1Блок обеспечения ',
                  'Блок организационных вопросов': '1Блок организацион',
                  'Блок правовых и корпоративных вопросов': '1Блок право',
                  'Блок программ по операционной эффективности': '1Блок програм',
                  'Блок ПЭБ, ОТ и ГЗ': 'Блок ПЭБ, ОТ и ГЗ',
                  'Блок Развития бизнеса': '1Блок Развития бизнеса',
                  'Блок Центр мониторинга бизнес-процессов проектной и закупочной деятельности': '1Блок Ц',
                  'Блок Центр управления качеством МТР': '1Блок Центр уп',
                  'Блок эффективности (БЭФ)': '1Блок эффективности (БЭФ)'}
        bot.send_message(who, "Выбирете новое место подачи",  reply_markup=make_keyboard(blocks))
    elif c == 'решение':
        time = pd.read_csv('files/time.csv', sep=';', header=[0], encoding='cp1251')
        time.loc[time['id'] == who, 'Идея'] = '1'
        time.to_csv('files/time.csv', sep=';', index=False, encoding='cp1251')
        bot.send_message(who, "Опишите решение проблемы одним сообщением")
    elif c == 'проблема':
        time = pd.read_csv('files/time.csv', sep=';', header=[0], encoding='cp1251')
        time.loc[time['id'] == who, 'Проблема'] = '1'
        time.to_csv('files/time.csv', sep=';', index=False, encoding='cp1251')
        bot.send_message(who, "Опишите проблему одним сообщением")

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
    bot.send_message(who, f"Приветсвую", reply_markup=make_keyboard(start_menu))


@bot.message_handler(content_types=['text'])
def send_mes(message):
    t = message.text
    who = message.chat.id
    status = pd.read_csv('files/status.csv', sep=';', header=[0], encoding='cp1251')
    start_menu = {'Подать Рац предоложение': 'подача', 'Быстро подать': 'подача фаст'}
    # Todo: пропуск выбора блока
    # Todo: возможноcть копировать из статуса значения
    # Todo: Фамилия и имя
    if who not in status['id'].values:
        people = pd.read_csv('people.csv', sep=';', header=[0], encoding='cp1251')
        names = people.loc[people['Фамилия'] == t.strip()]['Фамилия'].values

        if len(names) == 1:
            status.loc[len(status)] = [int(who), names[0],
                                       int(people.loc[people['Фамилия'] == t.strip()]['Табельный номер'].values[0]),
                                       people.loc[people['Фамилия'] == t.strip()]['Место работы'].values[0], 0]
            status.to_csv('files/status.csv', sep=';', index=False, encoding='cp1251')
            bot.send_message(who, f"Приветсвую {names[0]}", reply_markup=make_keyboard(start_menu))
        elif not (names.size > 0):
            bot.send_message(who, "Вас нет в списке пользователей обратитесь к @gasadaser")
        # Todo: много одинаковых фамилий

    else:
        time = pd.read_csv('files/time.csv', sep=';', header=[0], encoding='cp1251')
        if who in time['id'].values:
            if time.loc[time['id'] == who]['Проблема'][0] == 1:
                time.loc[time['id'] == who, 'Проблема'] = t
                time.to_csv('files/time.csv', sep=';', index=False, encoding='cp1251')
                prover(who)
            elif time.loc[time['id'] == who]['Идея'][0] == 1:
                time.loc[time['id'] == who, 'Идея'] = t
                time.to_csv('files/time.csv', sep=';', index=False, encoding='cp1251')
                prover(who)
            elif time.loc[time['id'] == who]['Проблема'][0] == 0:
                time.loc[time['id'] == who, 'Проблема'] = t
                time.to_csv('files/time.csv', sep=';', index=False, encoding='cp1251')
                yes_no = {'Да': 'ideaY', 'Нет': 'ideaN'}
                bot.send_message(who, 'Есть ли у вас предложения по решению проблемы?',
                                 reply_markup=make_keyboard(yes_no))
            elif time.loc[time['id'] == who]['Идея'][0] == 0:
                # добавить в идею
                print(t)
                time.loc[time['id'] == who, 'Идея'] = t
                time.to_csv('files/time.csv', sep=';', index=False, encoding='cp1251')
                prover(who)
        else:
            bot.send_message(who, "Приветсвую, что вас интересует?", reply_markup=make_keyboard(start_menu))


# Todo: найти функцию которая возращает значение сразу

# Todo: сделать дроп
# Todo: дописать функцию

print('go')
bot.polling(none_stop=True)
