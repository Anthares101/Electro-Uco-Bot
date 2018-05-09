# coding=utf-8
import requests
import os
from heroku import bot
from heroku import USERNAME
from heroku import PASSWORD
from heroku import WORKSPACE_ID
from telebot import util
import json
import watson_developer_cloud
from model import chat

assistant = watson_developer_cloud.AssistantV1(
    username=USERNAME,
    password=PASSWORD,
    version='2018-02-16'
)

@bot.message_handler(commands=['start'])
def start(message):
	bot.reply_to(message, 'Illo, ' + message.from_user.first_name)

	response = assistant.message(
	    workspace_id=WORKSPACE_ID
	)

	contexto = json.dumps(response['context'])
	chat.Chat.set_config(message.chat.id, 'contexto', contexto)

	bot.reply_to(message, response['output']['text'][0])
	bot.reply_to(message, contexto)

@bot.message_handler(func=lambda message: True, content_types=['text'])
def watson_bot(message):

	contexto = chat.Chat.get_config(message.chat.id, 'contexto')
	bot.reply_to(message, "%s" % context)
	contexto = contexto.value
	bot.reply_to(message, "%s" % context.value)
	response = assistant.message(
	    workspace_id=WORKSPACE_ID,
	    input={
	        'text': message.text
	    },
	    context=chat.Chat.get_config(message.chat.id, 'contexto')
	)

	bot.reply_to(message, chat.Chat.get_config(message.chat.id, 'contexto'))

	contexto = json.dumps(response['context'])
	chat.Chat.set_config(message.chat.id, 'contexto', contexto)

	bot.reply_to(message, response['output']['text'][0])
	bot.reply_to(message, contexto)