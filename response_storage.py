# -*- coding: utf-8 -*-
welcome_message = "Добро пожаловать в проект Робот Хаус."
first_response = "\nДля начала выберите категорию и не вздумайте лгать: \n\n" \
                 "1. У меня что-то с мизинцем на ладони\n"
section_one_questions = [
    "Он болит?",
    "Болит ли он сильно?",
    "Вы падали или ударялись рукой?",
    "Он онемел?",
    "Онемел ли безымянный палец?",
    "Онемел ли средний палец?",
    "Ведете ли вы сидячий образ жизни за компьютером?"
]
section_one_answers = [
    "Ваш мизинец сломан",
    "У вас защемление нерва руки",
    "У вас пиздос-плазмос",
]


def select_message(section, message_id, m_type):
    if section == 1:
        if m_type == 'question':
            return section_one_questions[message_id - 1]
        if m_type == 'answer':
            return section_one_answers[message_id - 1]
