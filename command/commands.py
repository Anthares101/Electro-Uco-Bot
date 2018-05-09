# coding=utf-8
from __future__ import unicode_literals
import requests
import os
import urllib, json
from heroku import bot
from telebot import util
from model import chat

@bot.message_handler(commands=['start'])
def start(message):
	bot.send_message(message.chat.id, "Buenas, "+message.from_user.first_name)
	bot.send_message(message.chat.id, "Introduzca una referencia de un pedido para ver información relativa a ese pedido")
	bot.register_next_step_handler(message, ref)

#Funcion que pide informacion de un pedido en funcion de una referencia
def ref(message):
    referencia = message.text

    url = "https://www.ucotest.es/panel/webservice/consultabot.php?case=order&userID=9&ref=" + referencia
    url2 = "https://www.ucotest.es/panel/webservice/consultabot.php?case=allProductInOrder&ref=" + referencia
    response = urllib.urlopen(url)
    response2 = urllib.urlopen(url2)
    datos = json.loads(response.read())

    for dato in datos:
        respuesta="ID del pedido: " + dato["rowid"] + "\nCodigo de referencia del pedido: " + dato["ref"] + "\nFecha del pedido: " + dato["date_commande"]

    datos = json.loads(response2.read())
    total = 0

    respuesta+="\n\nListado de productos:\n"

    for dato in datos:
        respuesta+=" - " + dato["label"] + float(dato["total_ttc"]) + "\u20ac\n"
        total = total + float(dato["total_ttc"])

    respuesta+="\nPrecio total: " + total + "\u20ac"

    bot.send_message(message.chat.id, respuesta)

    """url = "https://www.ucotest.es/panel/webservice/consultabot.php?case=order&userID=9&ref="+referencia
	response = urllib.urlopen(url)
	data = json.loads(response.read())
	for datos in data:
		bot.send_message(message.chat.id, datos['rowid'])"""

@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    bot.reply_to(message, message.text)