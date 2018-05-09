# coding=utf-8
import requests
import os
from heroku import bot
from telebot import util
from model import chat


@bot.message_handler(commands=['start'])
def start(message):
	bot.reply_to(message, 'Buenas ' + message.from_user.first_name+', usa el comando /id para introducir su ID de usuario')

@bot.message_handler(commands=['id'])
def id(message):
	saved = chat.Chat.get_config(message.chat.id, 'memory')
	if saved:
		bot.reply_to(message, "Ya ha introducido una id de usuario")
		return
	data = util.extract_arguments(message.text)
	if not data:
		bot.reply_to(message, "Debe indicar una ID de usuario")
		return
	chat.Chat.set_config(message.chat.id, 'memory', data)
	bot.reply_to(message, "ID de usuario guardado, si desea consultarla use /check_id")

@bot.message_handler(commands=['check_id'])
def check_id(message):
    data = chat.Chat.get_config(message.chat.id, 'memory')
    if not data:
        bot.reply_to(message, "Aún no ha introducido una ID de usuario")
        return
    bot.reply_to(message, "Su ID de usuario es: %s" % data.value)

@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    bot.reply_to(message, message.text)