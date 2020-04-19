import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import pandas as pd

bot = telebot.TeleBot('1181885362:AAHGMG3zg3KWfPWOuX1xSVgbzreiSAZ5WSs')
redactor = str('9b2398&DC8b0e')
no_value = str('dc34srefi*b23')


def make_keyboard(d: dict):
    keyboard = InlineKeyboardMarkup(row_width=1)
    for name, call in d.items():
        keyboard.add(InlineKeyboardButton(name, callback_data=call))
    return keyboard


def menu(who):
    start_menu = {'Подать рац. предложение': 'подача',
                  'Посмотреть': "результаты", "Оценить предложения": 'оценкалайт'}
    bot.send_message(who, "Выбирете дальнейшие действие:", reply_markup=make_keyboard(start_menu))


def make_keyboard_2(type=0):
    keyboard = InlineKeyboardMarkup()
    if type == 1:
        keyboard.add(InlineKeyboardButton('👍🏻', callback_data='like'),
                     InlineKeyboardButton('👎🏻', callback_data='dislike'))
    keyboard.add(InlineKeyboardButton("Закончить оценку", callback_data='endlook'))
    return keyboard


def prover(who):
    time = pd.read_csv('files/time.csv', sep=';', header=[0], encoding='cp1251')
    status = pd.read_csv('files/status.csv', sep=';', header=[0], encoding='cp1251')
    bot.send_message(who, 'Проверьте правильность данных:')
    name = status.loc[status['id'] == who]['Фамилия'].values[0]
    num = status.loc[status['id'] == who]['Табельный номер'].values[0]
    blok = time.loc[time['id'] == who]['Куда'].values[0]
    problem = time.loc[time['id'] == who]['Проблема'].values[0]
    idea = time.loc[time['id'] == who]['Идея'].values[0]
    chek = f'\033[1m Фамилия: \033[0m{name}\n\033[1mТабельный номер: \033[0m{num}\n\033[1mБлок: \033[0m{blok}\n\033[1mПроблема: \033[0m{problem}\n\033[1mРешение: \033[0m{idea}'
    bot.send_message(who, chek)
    end = {'Да': 'end', 'Нет': 'notend'}
    bot.send_message(who, 'Всё ли представлено верно?', reply_markup=make_keyboard(end))


def show_res(mes, who):
    status = pd.read_csv('files/status.csv', sep=';', header=[0], encoding='cp1251')
    data = pd.read_csv('data_base.csv', sep=';', header=[0], encoding='cp1251')
    which = status.loc[status['id'] == who]['Статус'].values[0]
    if which == len(data):
        q = 0
        s = 'Вы оценили все предложения.'
    else:
        l = ['\033[1mФамилия: \033[0m', '\033[1mТабельный номер: \033[0m', '\033[1mНаправление: \033[0m', '\033[1mОписание проблемы: \033[0m',
             '\033[1mПредложение по решению: \033[0m']
        s = ''
        for index, row in data.iterrows():
            if index == which:
                s += str(index) + ' из ' + str(len(data)-1) + '\n' + l[0] + str(row['Фамилия']) + '\n' + l[1] + str(
                    row['Табельный номер']) + '\n' + l[2] + str(row['Направление']) + '\n' + l[3] + str(
                    row['Описание проблемы']) + '\n' + l[4] + str(row['Предложение по решению']) + '\n\n'
        q = 1
    bot.edit_message_text(s, chat_id=who,
                          message_id=mes, reply_markup=make_keyboard_2(type=q))


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
        # bot.send_message(who, 'Егор С ДР 🎊🎉')
        bot.edit_message_text('Опишите проблему в одном сообщении:', chat_id=who, message_id=mes)
    elif c == 'подача':
        # Todo: изменить названия
        blocks = {
            'Закупки МТР': '0Закупки МТР',
            'Управлению инфраструктурой': '0Управлению инфраструктурой',
            'Корпоративная защита': '0Корпоративная защита',
            'Логистика': '0Логистика',
            'Обеспечение производства': '0Обеспечение производства',
            'Орг. вопросы (HR)': '0Орг. вопросы',
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
    elif c == 'результаты':
        l = ['\033[1mФамилия: \033[0m', '\033[1mТабельный номер: \033[0m',
             '\033[1mНаправление: \033[0m', '\033[1mОписание проблемы: \033[0m',
             '\033[1mПредложение по решению: \033[0m', '\033[1mЗа принятие: \033[0m',
             '\033[1mПротив принятия: \033[0m']
        status = pd.read_csv('data_base.csv', sep=';', header=[0], encoding='cp1251')
        s = ''
        for index, row in status.iterrows():
            if index != 0:
                s += l[0] + str(row['Фамилия']) + '\n' + l[1] + str(row['Табельный номер']) + '\n' + l[2] + str(
                    row['Направление']) + '\n' + l[3] + str(row['Описание проблемы']) + '\n' + l[4] + str(
                    row['Предложение по решению']) + '\n' + l[5] + str(row['За принятие']) + '\n' + l[6] + str(
                    row['Против принятия']) + '\n\n'

        bot.answer_callback_query(call.id)
        bot.send_message(who, s)
        menu(who)
    elif c == 'оценкалайт':
        bot.answer_callback_query(call.id)
        show_res(mes, who)
    elif c[0] == '0':  # выбор блока
        time = pd.read_csv('files/time.csv', sep=';', header=[0], encoding='cp1251')
        time = time.loc[time['id'] != who]
        time.loc[len(time)] = [int(who), c[1:], no_value, no_value]
        time.to_csv('files/time.csv', sep=';', index=False, encoding='cp1251')
        # bot.send_message(who, 'Опишите проблему в одном сообщении:')
        bot.edit_message_text('Опишите проблему в одном сообщении:', chat_id=who,
                              message_id=mes)
    elif c[0] == '1':  # Редактирование блока
        time = pd.read_csv('files/time.csv', sep=';', header=[0], encoding='cp1251')
        time.loc[time['id'] == who, 'Куда'] = c[1:]
        time.to_csv('files/time.csv', sep=';', index=False, encoding='cp1251')
        prover(who)
    elif c == 'ideaY':  # идеи решения есть
        # bot.send_message(who, 'Опишите предложение по решению в одном сообщении:')
        bot.edit_message_text('Опишите предложение по решению проблемы в одном сообщении:', chat_id=who,
                              message_id=mes)
    elif c == 'ideaN':  # идеи решения нет
        time = pd.read_csv('files/time.csv', sep=';', header=[0], encoding='cp1251')
        time.loc[time['id'] == who, 'Идея'] = 'Предложений нет'
        time.to_csv('files/time.csv', sep=';', index=False, encoding='cp1251')
        prover(who)
    elif c == 'end':  # запись в файл
        end = pd.read_csv('data_base.csv', sep=';', header=[0], encoding='cp1251')
        time = pd.read_csv('files/time.csv', sep=';', header=[0], encoding='cp1251')
        status = pd.read_csv('files/status.csv', sep=';', header=[0], encoding='cp1251')
        name = status.loc[status['id'] == who]['Фамилия'].values[0]
        num = status.loc[status['id'] == who]['Табельный номер'].values[0]
        blok = time.loc[time['id'] == who]['Куда'].values[0]
        problem = time.loc[time['id'] == who]['Проблема'].values[0]
        idea = time.loc[time['id'] == who]['Идея'].values[0]
        end.loc[len(end)] = [name, int(num), blok, problem, idea, int(0), int(0)]
        end.to_csv('data_base.csv', sep=';', index=False, encoding='cp1251')
        # time = time.drop(pd.where(time['id'] == who)[0])
        time = time.loc[time['id'] != who]
        time.to_csv('files/time.csv', sep=';', index=False, encoding='cp1251')
        #start_menu = {'Подать РАЦ Предложение': 'подача',
        #             'Посмотреть': "результаты", "Оценить предложения": 'оценкалайт'}
        # bot.send_message(who, 'Ваше предложение записанно', reply_markup=make_keyboard(start_menu))
        bot.edit_message_text('Ваше предложение записано', chat_id=who,
                              message_id=mes)
        menu(who)

    elif c == 'notend':  # редактирование меню
        change = {'Проблема': 'проблема', 'Решение проблемы': 'решение', 'Блок': 'workplace',
                  'Фамилия (сбросит результат)': 'фамилия', 'Табельный номер': 'табельный номер'}
        # bot.send_message(who, 'Что хотите изменить?', reply_markup=make_keyboard(change))
        bot.edit_message_text('Что хотите изменить?', chat_id=who,
                              message_id=mes, reply_markup=make_keyboard(change))
    elif c == 'workplace':  # редактирование место подачи
        blocks = {
            'Закупки МТР': '1Закупки МТР',
            'Управлению инфраструктурой': '1Управлению инфраструктурой',
            'Корпоративная защита': '1Корпоративная защита',
            'Логистика': '1Логистика',
            'Обеспечение производства': '1Обеспечение производства',
            'Орг. вопросы (HR)': 'Орг. вопросы',
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
    elif c == 'решение':  # редактирование
        time = pd.read_csv('files/time.csv', sep=';', header=[0], encoding='cp1251')
        time.loc[time['id'] == who, 'Идея'] = redactor
        time.to_csv('files/time.csv', sep=';', index=False, encoding='cp1251')
        # bot.send_message(who, "Опишите решение проблемы одним сообщением")
        bot.edit_message_text("Опишите предложение по решению проблемы в одном сообщении", chat_id=who, message_id=mes)
    elif c == 'проблема':  # редактирование
        time = pd.read_csv('files/time.csv', sep=';', header=[0], encoding='cp1251')
        time.loc[time['id'] == who, 'Проблема'] = redactor
        time.to_csv('files/time.csv', sep=';', index=False, encoding='cp1251')
        # bot.send_message(who, "Опишите проблему одним сообщением")
        bot.edit_message_text("Опишите проблему в одном сообщении", chat_id=who, message_id=mes)
    elif c == 'фамилия':  # редактирование
        bot.send_message(who, 'Назовите вашу фамилию')
        status = pd.read_csv('files/status.csv', sep=';', header=[0], encoding='cp1251')
        status = status.loc[status['id'] != who]
        time = pd.read_csv('files/time.csv', sep=';', header=[0], encoding='cp1251')
        time = time.loc[time['id'] != who]
        status.to_csv('files/status.csv', sep=';', index=False, encoding='cp1251')
        time.to_csv('files/time.csv', sep=';', index=False, encoding='cp1251')

    elif c == 'табельный номер':  # редактирование
        bot.send_message(who, 'Табельный номер напрямую связан с фамилией, попробуйте сбросить и '
                              'выбрать свою, если это не решит '
                              'проблему обратитесь @gasadaser')
        prover(who)
    # оценка
    elif c == "like":
        bot.answer_callback_query(call.id)
        data = pd.read_csv('data_base.csv', sep=';', header=[0], encoding='cp1251')
        status = pd.read_csv('files/status.csv', sep=';', header=[0], encoding='cp1251')
        index = status.loc[status['id'] == who]['Статус'].values[0]
        data.at[index, 'За принятие'] += 1
        status.loc[status['id'] == who, 'Статус'] += 1
        data.to_csv('data_base.csv', sep=';', index=False, encoding='cp1251')
        status.to_csv('files/status.csv', sep=';', index=False, encoding='cp1251')
        show_res(mes, who)

    elif c == 'dislike':
        bot.answer_callback_query(call.id)
        data = pd.read_csv('data_base.csv', sep=';', header=[0], encoding='cp1251')
        status = pd.read_csv('files/status.csv', sep=';', header=[0], encoding='cp1251')
        index = status.loc[status['id'] == who]['Статус'].values[0]
        data.at[index, 'Против принятия'] += 1
        status.loc[status['id'] == who, 'Статус'] += 1
        data.to_csv('data_base.csv', sep=';', index=False, encoding='cp1251')
        status.to_csv('files/status.csv', sep=';', index=False, encoding='cp1251')
        bot.answer_callback_query(call.id)
        show_res(mes, who)

    elif c == 'next':
        status = pd.read_csv('files/status.csv', sep=';', header=[0], encoding='cp1251')
        status.loc[status['id'] == who, 'Статус'] += 1
        status.to_csv('files/status.csv', sep=';', index=False, encoding='cp1251')
        bot.answer_callback_query(call.id)
        show_res(mes, who)

    elif c == 'last':
        status = pd.read_csv('files/status.csv', sep=';', header=[0], encoding='cp1251')
        if status.loc[status['id'] == who]['Статус'].values[0] > 0:
            status.loc[status['id'] == who, 'Статус'] -= 1
        status.to_csv('files/status.csv', sep=';', index=False, encoding='cp1251')
        bot.answer_callback_query(call.id)
        show_res(mes, who)

    elif c == 'endlook':
        bot.answer_callback_query(call.id)
        menu(who)


@bot.message_handler(commands=['start'])
def start(message):
    who = message.chat.id
    status = pd.read_csv('files/status.csv', sep=';', header=[0], encoding='cp1251')
    start_menu = {'Подать рац. предложение': 'подача',
                  'Посмотреть': "результаты", "Оценить предложения": 'оценкалайт'}
    if who not in status['id'].values:
        bot.send_message(message.chat.id, 'Напишите вашу фамилию')
    else:
        f = status.loc[status['id'] == who]['Фамилия'].values[0]
        bot.send_message(who, f"Приветствую, {f}", reply_markup=make_keyboard(start_menu))


@bot.message_handler(content_types=['text'])
def send_mes(message):
    t = message.text
    who = message.chat.id
    status = pd.read_csv('files/status.csv', sep=';', header=[0], encoding='cp1251')
    start_menu = {'Подать рац. предложение': 'подача',
                  'Посмотреть': "результаты", "Оценить предложения": 'оценкалайт'}
    # Todo: возможноcть копировать из статуса значения
    # Todo: Фамилия и имя
    if who not in status['id'].values:  # проверка пользовался или нет
        status.loc[len(status)] = [int(who), t,
                                   ' ',
                                   123,
                                   "Дом", 1]
        status.to_csv('files/status.csv', sep=';', index=False, encoding='cp1251')
        bot.send_message(who, f"Приветствую {t}, что вас интересует?", reply_markup=make_keyboard(start_menu))

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
            bot.send_message(who, "Приветствую, что вас интересует?", reply_markup=make_keyboard(start_menu))


# Todo: найти функцию которая возращает значение сразу

print('go')
bot.polling(none_stop=True)
