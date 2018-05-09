# coding=utf-8
import requests
import os
from heroku import bot
from telebot import util
from model import chat

@bot.message_handler(commands=['start'])
def start(message):
	bot.sendMessage(message.chat.id, 'Buenas, introduzca una referencia de un pedido para ver información relativa a ese pedido')
	#bot.register_next_step_handler(message, ref)

"""def ref(message):
	referencia = message.text

	url = "https://www.ucotest.es/panel/webservice/consultabot.php?case=order&userID=9&ref="+referencia
	response = urllib.urlopen(url)
	data = json.loads(response.read())
	for datos in data:
		print datos['rowid']"""

@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    bot.reply_to(message, message.text)