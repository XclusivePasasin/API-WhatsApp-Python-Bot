# app/routes.py
from flask import Flask, request, jsonify
from heyoo import WhatsApp
from app import app
from app.config import TOKEN, ID_NUMERO_TELEFONO, TELEFONO_ENVIA

@app.route("/enviar/", methods=["POST", "GET"])
def enviar():
    try:
        # Mensaje a enviar
        texto_mensaje = "Que onda, Soy un bot"
        # URL de la imagen a enviar
        url_imagen = 'https://i.imgur.com/r5lhxgn.png'

        # Inicializamos envío de mensajes
        mensaje_wa = WhatsApp(TOKEN, ID_NUMERO_TELEFONO)

        # Enviamos un mensaje de texto
        mensaje_wa.send_message(texto_mensaje, TELEFONO_ENVIA)
        # Enviamos una imagen
        mensaje_wa.send_image(image=url_imagen, recipient_id=TELEFONO_ENVIA)

        return jsonify({"status": "Mensaje enviado exitosamente"})
    except Exception as e:
        return jsonify({"status": "Error", "message": str(e)})

@app.route("/")
def index():
    return "Bienvenido al Bot de WhatsApp"
