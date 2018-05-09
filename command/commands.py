# coding=utf-8
import requests
import os
from heroku import bot
from telebot import util
from model import chat


@bot.message_handler(commands=['start'])
def start(message):
	bot.reply_to(message, 'Buenas ' + message.from_user.first_name+', introduzca una referencia con /ref de un pedido para ver información relativa a ese pedido')
@bot.message_handler(commands=['ref'])
def ref(message):
	referencia = util.extract_arguments(message.text)
    if not referencia:
        bot.reply_to(message, "Debe indicar la referencia de pedido")
        return
	url = "https://www.ucotest.es/panel/webservice/consultabot.php?case=order&userID=9&ref="+referencia
	response = urllib.urlopen(url)
	data = json.loads(response.read())
	for datos in data:
		print datos['rowid']
@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    bot.reply_to(message, message.text)