import json
from json import JSONDecodeError

import telebot
from telebot.types import Message
import requests
from datetime import datetime

bot_client = telebot.TeleBot(token="6234420525:AAEnSLEtNEYm8PoirOg49eABDt_fq-_6k8Y")


@bot_client.message_handler(commands=["start"])
def start(message: Message):
    try:
        with open("users.json", "r") as file_object:
            data_from_json = json.load(file_object)
        user_id = message.from_user.id
        username = message.from_user.username

        if str(user_id) not in data_from_json:
            data_from_json[user_id] = {"username": username}
        with open("users.json", "w") as file_object:
            json.dump(data_from_json, file_object, indent=4, ensure_ascii=False)
        bot_client.reply_to(message=message, text=f"User with id {user_id} and name {username},i love you!")
    except JSONDecodeError as err:
        print("Error:", err)
        requests.post("https://api.telegram.org/bot6234420525:AAEnSLEtNEYm8PoirOg49eABDt_fq-_6k8Y"
        "/sendMessage?chat_id=1192091627&text=sample SAMPLE")


def handle_speech(message):
    bot_client.reply_to(message, text="Желаю хорошего дня!")


@bot_client.message_handler(commands=["say_speech"])
def say_speech(message: Message):
    bot_client.reply_to(message, text="Привет! Как проходит твой день?!")
    bot_client.register_next_step_handler(message,callback=handle_speech)


bot_client.polling()
