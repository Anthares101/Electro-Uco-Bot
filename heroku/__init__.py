# coding=utf-8
from flask import Flask
from telebot import TeleBot
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.environ.get('BOT_TOKEN')
if not TOKEN:
    raise Exception('No se ha definido BOT_TOKEN')

SECRET_TOKEN = os.environ.get('SECRET_TOKEN', False)
if not SECRET_TOKEN:
    raise Exception('No se ha definido SECRET_TOKEN')

HEROKU_APP_NAME = os.environ.get('HEROKU_APP_NAME', False)
if not HEROKU_APP_NAME:
    raise Exception('No se ha definido HEROKU_APP_NAME')

DATABASE_URL = os.environ.get('DATABASE_URL', False)
if not DATABASE_URL:
    raise Exception('No se ha definido DATABASE_URL')

WORKSPACE_ID = os.environ.get('WORKSPACE_ID', False)
if not WORKSPACE_ID:
    raise Exception('No se ha definido WORKSPACE_ID')

USERNAME = os.environ.get('USERNAME', False)
if not USERNAME:
    raise Exception('No se ha definido USERNAME')

PASSWORD = os.environ.get('PASSWORD', False)
if not PASSWORD:
    raise Exception('No se ha definido PASSWORD')

WEB_DOMAIN = os.environ.get('WEB_DOMAIN', False)
if not WEB_DOMAIN:
    raise Exception('No se ha definido WEB_DOMAIN')

INFO_WEB = os.environ.get('INFO_WEB', False)
if not INFO_WEB:
    raise Exception('No se ha definido INFO_WEB')

INFO_NOMBRE_BOT = os.environ.get('INFO_NOMBRE_BOT', False)
if not INFO_NOMBRE_BOT:
    raise Exception('No se ha definido INFO_NOMBRE_BOT')

INFO_TLFNO_CONTACTO = os.environ.get('INFO_TLFNO_CONTACTO', False)
if not INFO_TLFNO_CONTACTO:
    raise Exception('No se ha definido INFO_TLFNO_CONTACTO')

INFO_EMAIL_CONTACTO = os.environ.get('INFO_EMAIL_CONTACTO', False)
if not INFO_EMAIL_CONTACTO:
    raise Exception('No se ha definido INFO_EMAIL_CONTACTO')


bot = TeleBot(TOKEN, os.environ.get('POLLING', False))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

import command
