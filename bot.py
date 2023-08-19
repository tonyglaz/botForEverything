# -*- coding: utf-8 -*-
import time

import requests
import telebot
from fysom import Fysom

import config
import response_storage
import utils

chat_id = ''
section_number = 0
# Массив финальных состояний
finals = ['first3_yes']


def create_fsm():
    # Создаем объект ДКА
    fsm = Fysom({'initial': 'waiting_start',  # начальное состояние
                 'events': [  # переходы
                     {'name': 'go_to_start', 'src': finals, 'dst': 'show_sections'},
                     {'name': 'gotstart', 'src': 'waiting_start', 'dst': 'show_sections'},
                     {'name': 'selected_first', 'src': 'show_sections', 'dst': 'first1'},
                     {'name': 'first_to_no', 'src': 'first1', 'dst': 'first1_no'},
                     {'name': 'first_to_yes', 'src': 'first1', 'dst': 'first1_yes'},
                     {'name': 'first1_to_first2', 'src': 'first1', 'dst': 'first2'},
                     {'name': 'first1_to_first4', 'src': 'first1', 'dst': 'first4'},
                     {'name': 'first2_to_yes', 'src': 'first2', 'dst': 'first2_yes'},
                     {'name': 'first2_to_no', 'src': 'first2', 'dst': 'first2_no'},
                     {'name': 'first2_to_first3', 'src': 'first2', 'dst': 'first3'},
                     {'name': 'first2_to_first4', 'src': 'first2', 'dst': 'first4_no'},
                     {'name': 'first3_to_yes', 'src': 'first3', 'dst': 'first3_yes'},
                     {'name': 'first3_to_no', 'src': 'first3', 'dst': 'first3_no'},
                     {'name': 'first3_to_first4', 'src': 'first3', 'dst': 'first4'},
                     {'name': 'first4_to_yes', 'src': 'first4', 'dst': 'first4_yes'},
                     {'name': 'first4_to_no', 'src': 'first4', 'dst': 'first4_no'},
                     {'name': 'first4_to_first5', 'src': 'first4', 'dst': 'first5'},
                     {'name': 'first5_to_yes', 'src': 'first5', 'dst': 'first5_yes'},
                     {'name': 'first5_to_no', 'src': 'first5', 'dst': 'first5_no'},
                     {'name': 'first5_to_first6', 'src': 'first5', 'dst': 'first6'},
                     {'name': 'first6_to_yes', 'src': 'first6', 'dst': 'first6_yes'},
                     {'name': 'first6_to_no', 'src': 'first6', 'dst': 'first6_no'},
                 ],
                 'callbacks': {  # Коллбеки.Указываем какой метод будет отвечать за обработку какого события
                     'onwaiting_start': onwaiting_start,
                     'onshow_sections': onshow_sections,
                     'onfirst1': onfirst1, 'onfirst1_yes': onfirst1_yes, 'onfirst1_no': onfirst1_no,
                     'onfirst2': onfirst2, 'onfirst2_yes': onfirst2_yes, 'onfirst2_no': onfirst2_no,
                     'onfirst3': onfirst3, 'onfirst3_yes': onfirst3_yes, 'onfirst3_no': onfirst3_no,
                     'onfirst4': onfirst4, 'onfirst4_yes': onfirst4_yes, 'onfirst4_no': onfirst4_no,
                     'onfirst5': onfirst5, 'onfirst5_yes': onfirst5_yes, 'onfirst5_no': onfirst5_no,
                     'onfirst6': onfirst6, 'onfirst6_yes': onfirst6_yes, 'onfirst6_no': onfirst6_no,
                 }})
    return fsm


# Метод для перехода на следующее состояние после набора команды "/start"
def change_state(state):
    if state == 'waiting_start':
        fsm.gotstart()


# Описываем работу обработчика события "onwaiting_start"
def onwaiting_start(e):
    @bot.message_handler(commands=["start"])  # атрибут отвечающие за реагирование на набор команды "/start"
    def start(message):
        bot.send_message(chat_id=message.chat.id,
                         text=response_storage.welcome_message)  # берем текст сообщения из
        # банка всех текстов(response_storage.py)
        global chat_id
        chat_id = message.chat.id
        fsm.current = 'waiting_start'  # указываем, что текущее состояние - "waiting_start"
        change_state(fsm.current)


# Описываем работу обработчика события "onshow_sections"
def onshow_sections(e):
    keyboard = utils.select_keyboard("section-number")
    bot.send_message(chat_id=chat_id,
                     text=response_storage.first_response,
                     reply_markup=keyboard)


# Дальше пошло описание действий при попадании на каждое конкретное состояние.
def onfirst1(e):
    keyboard = utils.select_keyboard("yes-no")
    bot.send_message(chat_id=chat_id,
                     text=response_storage.select_message(section_number, 1, 'question'),
                     reply_markup=keyboard)


def onfirst1_yes(e):
    bot.send_message(chat_id=chat_id,
                     text=response_storage.select_message(section_number, 1, 'answer'))
    if fsm.current in finals:  # если текущее состояние является финальным, то
        fsm.go_to_start()  # переходим снова в начало к выбору ветки
        return


def onfirst1_no(e):
    bot.send_message(chat_id=chat_id,
                     text=response_storage.select_message(section_number, 1, 'answer'))
    if fsm.current in finals:  # если текущее состояние является финальным, то
        fsm.go_to_start()  # переходим снова в начало к выбору ветки
        return


def onfirst2(e):
    keyboard = utils.select_keyboard("yes-no")
    bot.send_message(chat_id=chat_id,
                     text=response_storage.select_message(section_number, 2, 'question'),
                     reply_markup=keyboard)


def onfirst2_yes(e):
    bot.send_message(chat_id=chat_id,
                     text=response_storage.select_message(section_number, 2, 'answer'))
    if fsm.current in finals:
        fsm.go_to_start()
        return


def onfirst2_no(e):
    bot.send_message(chat_id=chat_id,
                     text=response_storage.select_message(section_number, 3, 'answer'))
    if fsm.current in finals:
        fsm.go_to_start()
        return


def onfirst3(e):
    keyboard = utils.select_keyboard("yes-no")
    bot.send_message(chat_id=chat_id,
                     text=response_storage.select_message(section_number, 3, 'question'),
                     reply_markup=keyboard)


def onfirst3_yes(e):
    bot.send_message(chat_id=chat_id,
                     text=response_storage.select_message(section_number, 1, 'answer'))
    if fsm.current in finals:
        fsm.go_to_start()
        return


def onfirst3_no(e):
    bot.send_message(chat_id=chat_id,
                     text=response_storage.select_message(section_number, 3, 'answer'))
    if fsm.current in finals:
        fsm.go_to_start()
        return


def onfirst4(e):
    keyboard = utils.select_keyboard("yes-no")
    bot.send_message(chat_id=chat_id,
                     text=response_storage.select_message(section_number, 4, 'question'),
                     reply_markup=keyboard)


def onfirst4_yes(e):
    bot.send_message(chat_id=chat_id,
                     text=response_storage.select_message(section_number, 3, 'answer'))
    if fsm.current in finals:
        fsm.go_to_start()
        return


def onfirst4_no(e):
    bot.send_message(chat_id=chat_id,
                     text=response_storage.select_message(section_number, 3, 'answer'))
    if fsm.current in finals:
        fsm.go_to_start()
        return


def onfirst5(e):
    keyboard = utils.select_keyboard("yes-no")
    bot.send_message(chat_id=chat_id,
                     text=response_storage.select_message(section_number, 5, 'question'),
                     reply_markup=keyboard)


def onfirst5_yes(e):
    bot.send_message(chat_id=chat_id,
                     text=response_storage.select_message(section_number, 3, 'answer'))
    if fsm.current in finals:
        fsm.go_to_start()
        return


def onfirst5_no(e):
    bot.send_message(chat_id=chat_id,
                     text=response_storage.select_message(section_number, 3, 'answer'))
    if fsm.current in finals:
        fsm.go_to_start()
        return


def onfirst6(e):
    keyboard = utils.select_keyboard("yes-no")
    bot.send_message(chat_id=chat_id,
                     text=response_storage.select_message(section_number, 6, 'question'),
                     reply_markup=keyboard)


def onfirst6_yes(e):
    bot.send_message(chat_id=chat_id,
                     text=response_storage.select_message(section_number, 3, 'answer'))
    if fsm.current in finals:
        fsm.go_to_start()
        return


def onfirst6_no(e):
    bot.send_message(chat_id=chat_id,
                     text=response_storage.select_message(section_number, 4, 'answer'))
    if fsm.current in finals:
        fsm.go_to_start()
    return


# Создаем объект бота

bot = telebot.TeleBot(config.token)  # передаем в параметр уникальный токен нашего бота
fsm = create_fsm()


# Обработчик всех нажатий на кнопки
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    data = call.data  # получаем значение, соответствующее кнопки(нажал кнопку 5 - получил в call.data значение 5).
    # Далее, в соответствии с текущим состоянием(fsm.current) и значением, полученным после нажатия на кнопку,
    # указываем в какое состояние необходимо перейти
    if fsm.current == 'show_sections':
        global section_number
        section_number = int(data)
        if section_number == 1:
            fsm.selected_first()
            return

    if fsm.current == 'first1':
        if data == '1':
            fsm.first1_to_first2()
            return
        if data == '2':
            fsm.first1_to_first4()
            return
    if fsm.current == 'first2':
        if data == '1':
            fsm.first2_to_first3()
            return
        if data == '2':
            fsm.first2_to_first4()
    if fsm.current == 'first3':
        if data == '1':
            fsm.first3_to_yes()
            return
        if data == '2':
            fsm.first3_to_no()
            return
    if fsm.current == 'first4':
        if data == '1':
            fsm.first4_to_first5()
            return
        if data == '2':
            fsm.first4_to_no()
            return
    if fsm.current == 'first5':
        if data == '1':
            fsm.first5_to_yes()
            return
        if data == '2':
            fsm.first5_to_first6()
            return
    if fsm.current == 'first6':
        if data == '1':
            fsm.first6_to_yes()
            return
        if data == '2':
            fsm.first6_to_no()


if __name__ == '__main__':
    # В бесконечном цикле держмим бот в запущенном состоянии, обрабатывая возможные ошибки.
    while True:
        try:
            bot.polling(none_stop=True, timeout=1000)
        except Exception as ex:
            print("Error:", ex)
            requests.post("https://api.telegram.org/bot6234420525:AAEnSLEtNEYm8PoirOg49eABDt_fq-_6k8Y"
                          f"/sendMessage?chat_id=1192091627&text=Произошла ошибка: {ex}")
            time.sleep(10)
