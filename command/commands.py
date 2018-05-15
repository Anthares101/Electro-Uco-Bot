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

def send_log(log_information):
    url = "https://" + WEB_DOMAIN + "/panel/webservice/consultabot.php?case=log&men=" + log_information
    urllib.urlopen(url)

    return


@bot.message_handler(commands=['start'])
def start(message):
    response = assistant.message(
        workspace_id=WORKSPACE_ID
    )

    response['context']['info_web'] = INFO_WEB
    response['context']['info_nombre_bot'] = INFO_NOMBRE_BOT
    response['context']['info_tlfno_contacto'] = INFO_TLFNO_CONTACTO
    response['context']['info_email_contacto'] = INFO_EMAIL_CONTACTO

    contexto = json.dumps(response['context'])

    chat.Chat.set_config(message.chat.id, 'contexto', contexto)

    chat.Chat.del_config(message.chat.id, 'referencia')

    bot.send_message(message.chat.id, response['output']['text'][0])


@bot.message_handler(commands=['list'])
def list(message):
    referencia = util.extract_arguments(message.text)
    if not referencia:
        referencia = chat.Chat.get_config(message.chat.id, 'referencia')
        if not referencia:
            bot.send_message(message.chat.id, "Debe indicar la referencia del pedido")
            return
        else:
            referencia = referencia.value

    url = "https://" + WEB_DOMAIN + "/panel/webservice/consultabot.php?case=allProductInOrder&ref=" + referencia

    response = urllib.urlopen(url)

    datos = json.loads(response.read())

    if (datos == 1):
        bot.send_message(message.chat.id, "Ha habido un error al realizar su consulta de pedido")

    elif (datos == 2):
        bot.send_message(message.chat.id, "No se ha podido localizar su pedido")

    elif (datos == 3):
        bot.send_message(message.chat.id, "Ha habido un error al realizar su consulta de pedido")

    elif (datos == 4):
        bot.send_message(message.chat.id, "Ha habido un error al realizar su consulta de pedido")

    else:

        chat.Chat.set_config(message.chat.id, 'referencia', referencia)

        for dato in datos:
            url2 = "https://" + WEB_DOMAIN + "/panel/webservice/consultabot.php?case=getImage&ref=" + dato['ref']
            url3 = "https://" + WEB_DOMAIN + "/panel/webservice/consultabot.php?ref=" + dato['ref'] + "&case=urlshop"

            response2 = urllib.urlopen(url2)
            response3 = urllib.urlopen(url3)

            datos2 = json.loads(response2.read())
            datos3 = json.loads(response3.read())

            if (datos2 == 1 or datos3 == 1):
                bot.send_message(message.chat.id, "Ha habido un error al realizar su consulta de pedido")

            elif (datos2 == 2 or datos3 == 2):
                bot.send_message(message.chat.id, "No se ha podido localizar su pedido")

            elif (datos2 == 3 or datos3 == 3):
                bot.send_message(message.chat.id, "Ha habido un error al realizar su consulta de pedido")

            elif (datos2 == 4 or datos3 == 4):
                bot.send_message(message.chat.id, "Ha habido un error al realizar su consulta de pedido")

            else:
                nombre = dato["label"]
                precio = float(dato["total_ttc"])
                link = datos3

                bot.send_photo(message.chat.id, datos2, caption="🛒 _" + nombre + "_" + "\n💶 *Precio:* " + str(precio) + "\u20ac", parse_mode="Markdown")
                bot.send_message(message.chat.id, link)

    var="El usuario con id " + str(message.chat.id) + " ha hecho una peticion de listado de productos del pedido con referencia " + referencia
    send_log(var)

    return


@bot.message_handler(commands=['info'])
def info(message):
    referencia = util.extract_arguments(message.text)
    if not referencia:
        referencia = chat.Chat.get_config(message.chat.id, 'referencia')
        if not referencia:
            bot.send_message(message.chat.id, "Debe indicar la referencia del pedido")
            return
        else:
            referencia = referencia.value

    url = "https://" + WEB_DOMAIN + "/panel/webservice/consultabot.php?case=order&ref=" + referencia
    url2 = "https://" + WEB_DOMAIN + "/panel/webservice/consultabot.php?case=allProductInOrder&ref=" + referencia
    url3 = "https://" + WEB_DOMAIN + "/panel/webservice/consultabot.php?case=shipping&ref=" + referencia

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

        chat.Chat.set_config(message.chat.id, 'referencia', referencia)

        for dato in datos:
            respuesta=("📝 *Codigo de referencia del pedido:* " + str(dato["ref"]) + "\n📆 *Fecha del pedido:* " + str(dato["date_commande"]))

            total = 0

            respuesta=respuesta+"\n\n\n📋 *Listado de productos:*\n\n"

            for dato in datos2:
                total_ttc=float(dato["total_ttc"])
                respuesta=respuesta + "- " + "_" + dato["label"] + "_" + "\t\t" + "_" + str(total_ttc) + "_" + "\u20ac\n"
                total = total + float(dato["total_ttc"])

            respuesta=(respuesta + "\n\n💶 *Precio total:* " + str(total) + "\u20ac")

            estados = { 0:"_Borrador_", 1:"_En curso_", 2:"_Entregado_" }

            for dato in datos3:
                respuesta=respuesta + "\n\n🚚 *Estado del pedido:* " + estados[int(dato["fk_statut"])]

            bot.send_message(message.chat.id, respuesta, parse_mode="Markdown")

    var = "El usuario con id " + str(message.chat.id) + " ha hecho una peticion de informacion del pedido con referencia " + referencia
    send_log(var)

    return


@bot.message_handler(func=lambda message: True, content_types=['text'])
def watson_bot(message):

    contexto = chat.Chat.get_config(message.chat.id, 'contexto').value
    contexto = json.loads(contexto)

    referencia = chat.Chat.get_config(message.chat.id, 'referencia')
    if referencia:
        referencia = referencia.value
        contexto['hay_pedido'] = "true"

    response = assistant.message(
        workspace_id=WORKSPACE_ID,
        input={
            'text': message.text
        },
        context=contexto
    )

    if response['context']['mostrar_pedido'] == "true":
        url = "https://" + WEB_DOMAIN + "/panel/webservice/consultabot.php?case=order&ref=" + referencia
        url2 = "https://" + WEB_DOMAIN + "/panel/webservice/consultabot.php?case=allProductInOrder&ref=" + referencia
        url3 = "https://" + WEB_DOMAIN + "/panel/webservice/consultabot.php?case=shipping&ref=" + referencia

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

            chat.Chat.set_config(message.chat.id, 'referencia', referencia)

            for dato in datos:
                respuesta=("📝 *Codigo de referencia del pedido:* " + str(dato["ref"]) + "\n📆 *Fecha del pedido:* " + str(dato["date_commande"]))

            total = 0

            respuesta=respuesta+"\n\n\n📋 *Listado de productos:*\n\n"

            for dato in datos2:
                total_ttc=float(dato["total_ttc"])
                respuesta=respuesta + "- " + "_" + dato["label"] + "_" + "\t\t" + "_" + str(total_ttc) + "_" + "\u20ac\n"
                total = total + float(dato["total_ttc"])

            respuesta=(respuesta + "\n\n💶 *Precio total:* " + str(total) + "\u20ac")

            estados = { 0:"_Borrador_", 1:"_En curso_", 2:"_Entregado_" }

            for dato in datos3:
                respuesta=respuesta + "\n\n🚚 *Estado del pedido:* " + estados[int(dato["fk_statut"])]

            bot.send_message(message.chat.id, respuesta, parse_mode="Markdown")

        var = "El usuario con id " + str(message.chat.id) + " ha hecho una peticion de informacion del pedido con referencia " + referencia
        send_log(var)

        response['context']['mostrar_pedido'] = "false"
    else:
        bot.send_message(message.chat.id, response['output']['text'][0])

    contexto = json.dumps(response['context'])
    chat.Chat.set_config(message.chat.id, 'contexto', contexto)