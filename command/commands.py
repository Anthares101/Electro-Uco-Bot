# coding=utf-8
import requests
import os
from heroku import bot
from telebot import util


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Buenas, ' + message.from_user.first_name)
    bot.send_message(chat.id, 'Introduce su id de usuario')

@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    bot.reply_to(message, message.text)