# coding=utf-8
import requests
import os
from heroku import bot
from telebot import util


@bot.message_handler(commands=['start'])
def start(message):
	if chat.Chat.get_config(chat_id, 'checkStart') != 1:
		bot.reply_to(message, 'Buenas ' + message.from_user.first_name+', usa el comando /id para introducir su id de usuario')
		chat.Chat.set_config(chat_id, 'checkStart', 1)
def id(message):
	data = util.extract_arguments(message.text)

@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    bot.reply_to(message, message.text)