# coding=utf-8
import requests
import os
from heroku import bot, USERNAME, PASSWORD, WORKSPACE_ID
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

	response = assistant.message(
	    workspace_id=WORKSPACE_ID
	)

	contexto = json.dumps(response['context'])
	chat.Chat.set_config(message.chat.id, 'contexto', contexto)

@bot.message_handler(func=lambda message: True, content_types=['text'])
def watson_bot(message):

	conetexto = chat.Chat.get_config(message.chat.id, 'contexto')

	response = assistant.message(
	    workspace_id=WORKSPACE_ID,
	    input={
	        'text': message.text
	    },
	    context=json.loads(contexto.value)
	)

	contexto = json.dumps(response['context'])
	chat.Chat.set_config(message.chat.id, 'contexto', contexto)

	bot.send_message(message, response['output']['text'][0])