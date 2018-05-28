# Electro UCO bot 

Ejemplo de bot desplegado en Heroku para el proyecto de Sistemas de la Información.


## Instalación

Para instalar el bot y adaptarlo a las necesidades de otra empresa, se deben de seguir los siguientes pasos:

- Crear un bot en telegram: Mediante el BotFather, se puede crear un bot en telegram con tan solo especificarle el nombre y el nombre de
usuario de dicho bot. Una vez se haya finalizado el proceso de creación del bot, el BotFather proporcionará un token que se necesitará
más adelante.

- Crear una cuenta en IBM Watson: Una vez creada, solicitar el servicio de asistente virtual, y crear uno nuevo, importando el archivo
json, que seproporcionará como parte del paquete. Una vez importado el json, el asistente estaría listo.

- Activar una cuenta en heroku: Cuando se haya activado, solo habrá que crear una nueva aplicación que esté sincronizada con el
repositorio de GitHub (Se recomienda realizar un fork de este repositorio por si hubiese que realizar algun ajustes en el codigo, sobre
todo cambios relacionados con URLs).

Una vez se hayan realizado estos pasos, solo queda añadir y configurar las siguientes variables en heroku en la sección _Setting_:

	o BOT_TOKEN: Proporcionado por el BotFather.
	o DATABASE_URL: Dirección url de la base de datos proporcionada por heroku.
	o HEROKU_APP_NAME: Nombre de la aplicación de heroku, es importante que coincidan exactamente.
	o INFO_EMAIL_CONTACTO: Email de atención del cliente del que dispone la empresa.
	o INFO_NOMBRE_BOT: Nombre del bot.
	o INFO_TLFNO_CONTACTO: Teléfono de atención del cliente del que dispone la empresa.
	o INFO_WEB: Web en la que está la tienda online.
	o PASSWORD: Aparece en la pestaña deploy, en el workspace del asistente de IBM Watson.
	o SECRET_TOKEN: Token que genera Heroku para restringir los accesos a esta aplicación.
	o USERNAME: Aparece en la pestaña deploy, en el workspace del asistente de IBM Watson.
	o WEB_DOMAIN: El dominio de la web en la que se alojan los servicios que proporciona el paquete UCOShop. 
		Por ejemplo: www.example.com.
	o WORKSPACE_ID: Aparece en la pestaña deploy, en el workspace del asistente de IBM Watson.


## Configuración

Dentro del archivo `__heroku/__init.py__` se inicializan las variables necesarias para que el bot funcione.

Este archivo exporta principalmente dos variables:

* `bot`: Se debe importar en todos los archivos que quieran hacer uso de la API que ofrece la librería de _pyTelegramBotAPI_.
* `app`: Se debe importar en todos los archivos que quieran hacer uso de la API que ofrece la librería de _Flask_. 

Para configurar las variables que necesitamos en local copiar el archivo siguiente:

```
cp .env.dist .env
```

Hay algunos valores que están en blanco, su valor debe ser el mismo que aparece en Heroku (Se añadieron y configuraron en el apartado anterior). Los podemos ver dentro de la sección _Setting_ en la pagina de Heroku como se vio en el apartado de instalación.

## Ejecución

### En local

Para instalarlo en local es necesario tener instalado _python2.7_ y _virtualenv_. Por defecto lo tenemos en Ubuntu.

Para instalar _virtualenv_ hacemos lo siguiente:

```sh
sudo apt-get install virtualenv
```

A continuación necesitamos tener instaladas las herramientas de _Heroku_. En Ubuntu 17.10 se puede hacer con _snap_:

```sh
sudo snap install heroku --classic
```

O podemos seguir [las instrucciones de la web de Heroku](https://devcenter.heroku.com/articles/heroku-cli).



Ejecutar el bot en local desactiva el _webhook_. Para iniciar en modo local ejecutar lo siguiente:

```
heroku local polling
``` 

Si se quiere volver a usar el bot en el servidor, hay que volver a configurar el _webhook_ como dice el apartado siguiente.

### En el servidor

Cuando se despliega el proyecto, Heroku lo configura automáticamente. Si fuera necesario volver a ejecutar el webhook ejecutar lo siguiente:

```
heroku run webhook
```

O si tenemos configurado el _.env_:

```
python webhook.py
```

También se puede iniciar dentro del apartado _Resources_ de la web de Heroku. En este apartado es posible realizar la sincronización con 
el repositorio de Github del proyecto y desplegar una rama de dicho repositorio. También se pueden configurar despliegues automaticos de
una rama concreta para que se realice un nueve despliegue del protyecto si se realizan cambios en dicha rama aplicando asi los cambios
(ATENCIÓN: Asegurarse de que se configura esta opción sobre una rama estable para evitar problemas en la aplicación desplegada). 

## Funciones

Dentro del directorio `command` se pueden añadir nuevas funciones, ya sea en los archivos existentes o en archivos nuevos.

Las funciones de _Telegram_, ya sean comandos o expresiones regulares, irán con la anotación correspondiente que permite la librería _pyTelegramBotAPI_.

Para más información, leed la documentación de [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI).

Un template para un nuevo archivo de funciones es el siguiente:

```python
# coding=utf-8
from heroku import bot


@bot.message_handler(commands=['test'])
def test(message):
    bot.reply_to(message, "Prueba")

```

Es necesario importar el fichero en `command/__init__.py` donde se indica.


## Base de datos

En local se crea un archivo en `/tmp/flask_app.db` con la base de datos en sqlite. En remoto, se crea en una base de datos de postgresql proporcionada por Heroku.

### Esquema

Dentro del directorio `model` se ha creado una clase dentro del archivo `chat.py` que sirve de ejemplo para crear tablas dentro de la aplicación.

Para más información, leed la documentación de [Flask-SQLAlchemy](http://flask-sqlalchemy.pocoo.org/2.3/)

Un template para una nueva clase es el siguiente:

```python
from model import db

class Tabla(db.Model):
    ___table__name = 'tabla'
    id = db.Column(db.Integer, primary_key=True)
    
    # Métodos get/set
```

Es necesario importar el fichero en `model/__init__.py` donde se indica.

### Clase Chat

Se adjunta una clase Chat que permite almacenar valores en una tabla. Se puede indicar el chat asociado al dato (chat), el nombre del dato (key) y su valor (value). Si se quiere un dato que exista para cualquier chat se puede usar como identificador de chat el 0 (cero).

Un ejemplo de uso se encuentra en `commands/db.py`.


## Referencias

Para obtener APIs abiertas podeís consultar el siguiente repositorio de Github:

* [https://github.com/toddmotto/public-apis](https://github.com/toddmotto/public-apis)

Repositorio del cual se realiza el fork:

* [https://github.com/aulasoftwarelibre/hackathonbot](https://github.com/aulasoftwarelibre/hackathonbot)
