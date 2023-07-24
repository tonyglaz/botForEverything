import telebot
from telebot.types import Message

bot_client = telebot.TeleBot(token="6234420525:AAEnSLEtNEYm8PoirOg49eABDt_fq-_6k8Y")


@bot_client.message_handler(commands=["start"])
def echo(message: Message):
    # print(message.chat.id)
    bot_client.reply_to(message=message, text="answer")
    bot_client.send_message(chat_id=message.chat.id, text="answer")

bot_client.polling()
