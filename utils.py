from telebot import types


def select_keyboard(k_type):
    if k_type == "section-number":
        keyboard = types.InlineKeyboardMarkup()
        callback_button1 = types.InlineKeyboardButton(text="1", callback_data="1")
        callback_button2 = types.InlineKeyboardButton(text="2", callback_data="2")
        keyboard.add(callback_button1, callback_button2)
        return keyboard
    if k_type == "yes-no":
        keyboard = types.InlineKeyboardMarkup()
        callback_button1 = types.InlineKeyboardButton(text="Да", callback_data="1")
        callback_button2 = types.InlineKeyboardButton(text="Нет", callback_data="2")
        keyboard.add(callback_button1, callback_button2)
        return keyboard

    if k_type == "yes-no-maybe":
        keyboard = types.InlineKeyboardMarkup()
        callback_button1 = types.InlineKeyboardButton(text="Да", callback_data="1")
        callback_button2 = types.InlineKeyboardButton(text="Нет", callback_data="2")
        callback_button3 = types.InlineKeyboardButton(text="Может быть", callback_data="3")
        keyboard.add(callback_button1, callback_button2, callback_button3)
        return keyboard

    if k_type == "back_to_start":
        keyboard = types.InlineKeyboardMarkup()
        callback_button1 = types.InlineKeyboardButton(text="Начать сначала", callback_data="to_start")
        keyboard.add(callback_button1)
        return keyboard
