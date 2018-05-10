# coding=utf-8
from __future__ import unicode_literals
import requests
import os
from heroku import bot, USERNAME, PASSWORD, WORKSPACE_ID
from telebot import util
import urllib, json
import watson_developer_cloud
from model import chat

assistant = watson_developer_cloud.AssistantV1(
    username=USERNAME,
    password=PASSWORD,
    version='2018-02-16'
)

@bot.message_handler(commands=['start'])
def start(message):

	response = assistant.message(
	    workspace_id=WORKSPACE_ID
	)

	contexto = json.dumps(response['context'])
	chat.Chat.set_config(message.chat.id, 'contexto', contexto)

	bot.send_message(message.chat.id, response['output']['text'][0])

@bot.message_handler(commands=['ref'])
def ref(message):
	bot.send_message(message.chat.id, "Introduzca una referencia de un pedido para ver información relativa a ese pedido")
	bot.register_next_step_handler(message, reference)

#Funcion que pide informacion de un pedido en funcion de una referencia
def reference(message):
    referencia = message.text

    url = "https://www.ucotest.es/panel/webservice/consultabot.php?case=order&ref=" + referencia
    url2 = "https://www.ucotest.es/panel/webservice/consultabot.php?case=allProductInOrder&ref=" + referencia
    url3 = "https://www.ucotest.es/panel/webservice/consultabot.php?case=shipping&ref=" + referencia

    response = urllib.urlopen(url)
    response2 = urllib.urlopen(url2)
    response3 = urllib.urlopen(url3)

    datos = json.loads(response.read())
    datos2 = json.loads(response2.read())
    datos3 = json.loads(response3.read())

    if(datos==1 or datos2==1 or datos3==1):
        bot.send_message(message.chat.id, "Ha habido un error al realizar su consulta de pedido")
    
    elif(datos==2 or datos2==2 or datos3==2):
        bot.send_message(message.chat.id, "No se ha podido localizar su pedido")

    elif(datos==3 or datos2==3 or datos3==3):
        bot.send_message(message.chat.id, "Ha habido un error al realizar su consulta de pedido")

    elif(datos==4 or datos2==4 or datos3==4):
        bot.send_message(message.chat.id, "Ha habido un error al realizar su consulta de pedido")

    else:

        for dato in datos:
            respuesta=str("ID del pedido: " + dato["rowid"] + "\nCodigo de referencia del pedido: " + dato["ref"] + "\nFecha del pedido: " + dato["date_commande"])
        
        total = 0

        respuesta=respuesta+"\n\n\nListado de productos:\n\n"

        for dato in datos2:
            total_ttc=float(dato["total_ttc"])
            respuesta=respuesta + "- " + dato["label"] + " " + str(total_ttc) + "\u20ac\n"
            total = total + float(dato["total_ttc"])

        respuesta=(respuesta + "\n\nPrecio total: " + str(total) + "\u20ac")
        
        estados = { 0:"Borrador", 1:"En curso", 2:"Entregado" }

        for dato in datos3:
            respuesta=respuesta + "\n\nEstado del pedido: " + estados[int(dato["fk_statut"])]
        
        bot.send_message(message.chat.id, respuesta)

    return


@bot.message_handler(func=lambda message: True, content_types=['text'])
def watson_bot(message):

	contexto = chat.Chat.get_config(message.chat.id, 'contexto')

	response = assistant.message(
	    workspace_id=WORKSPACE_ID,
	    input={
	        'text': message.text
	    },
	    context=json.loads(contexto.value)
	)

	contexto = json.dumps(response['context'])
	chat.Chat.set_config(message.chat.id, 'contexto', contexto)

	bot.send_message(message.chat.id, response['output']['text'][0])
