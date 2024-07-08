from config.config import Config
import requests, json
import time

def get_message(message):
    if 'type' not in message:
        return 'Message not recognized by the system.'

    type_message = message['type']
    if type_message == 'text':
        return message['text']['body']
    elif type_message == 'interactive' and 'button_reply' in message:
        return message['interactive']['button_reply']['id']
    else:
        return 'No esta funcionado xd'

def send_message(data):
    try:
        whatsapp_token = Config.whatsapp_token
        whatsapp_url = Config.whatsapp_url
        headers = {'Content-Type': 'application/json','Authorization': 'Bearer ' + whatsapp_token}
        print("Sending data:", data)  # Print data being sent
        response = requests.post(whatsapp_url, headers=headers, data=data)
        print("Response status:", response.status_code)  # Print response status
        print("Response text:", response.text)  # Print response text
        if response.status_code == 200: 
            return 'Message sent successfully!', 200
        else:
            return 'Error sending message!', response.status_code
    except Exception as e:
        return str(e), 403

def welcome_message(number, name):
    message = f'¡Hola {name}! 👋, Déjame presentarme, soy Clobi, tu asistente virtual! 😎 \n ¿Cómo puedo ayudarte?'
    template = {
        "messaging_product": "whatsapp",
        "to": number,
        "type": "interactive",
        "interactive": {
            "type": "button",
            "header": {
                "type": "text",
                "text": "Demo Screen"
            },
            "body": {
                "text": message
            },
            "footer": {
                "text": "Clobi Technologies"
            },
            "action": {
                "buttons": [
                    {
                        "type": "reply",
                        "reply": {
                            "id": "services_button",
                            "title": "Servicios"
                        }
                    },
                    {
                        "type": "reply",
                        "reply": {
                            "id": "schedule_button",
                            "title": "Agendar Cita"
                        }
                    }
                ]
            }
        }
    }
    return json.dumps(template)

def menu_message(number):
    message = f'Haz click al catalogo'
    template = {
        "messaging_product": "whatsapp",
        "to": number,
        "type": "interactive",
        "interactive": {
            "type": "list",
            "header": {
                "type": "text",
                "text": "Nuestros Servicios"
            },
            "body": {
                "text": message
            },
            "footer": {
                "text": "Clobi Technologies"
            },
            "action": {
                "button": "Catalogo!",
                "sections": [
                    {
                        "title": "Inteligencia de Negocios",
                        "rows": [
                            {
                                "id": "row1",
                                "title": "Opt1 "
                            }
                        ]
                    },
                    {
                        "title": "Migración a la Nube",
                        "rows": [
                            {
                                "id": "row2",
                                "title": "opt2"
                            }
                        ]
                    }
                ]
            }
        }
    }
    return json.dumps(template)

def manage_chatbot(text, number, id_message, name):
    time.sleep(1)
    text = text.lower()
    if 'hola' in text:
        message = welcome_message(number,name)
        send_message(message)
    elif 'servicios' in text:
        message =  menu_message(number)
        send_message(message)
        
