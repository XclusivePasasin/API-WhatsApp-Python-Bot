from config.config import Config
import requests, json

def get_message(message):
    if 'type' not in message:
        return 'Message not recognized by the system.'

    type_message = message['type']
    if type_message == 'text':
        return message['text']['body']
    elif type_message == 'interactive' and 'button_reply' in message['interactive']:
        return message['interactive']['button_reply']['id']
    elif type_message == 'reaction':
        return message['reaction']['message_id']
    elif type_message == 'interactive' and 'list_reply' in message['interactive']:
        return message['interactive']['list_reply']['id']
    else:
        return 'Message type not supported.'

def send_message(data):
    try:
        whatsapp_token = Config.whatsapp_token
        whatsapp_url = Config.whatsapp_url
        headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + whatsapp_token}
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
                "text": "Python - Bot"
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
                            "id": "button_id_for_servicios",
                            "title": "Services"
                        }
                    },
                    {
                        "type": "reply",
                        "reply": {
                            "id": "button_id_for_date",
                            "title": "Schedule Appointment"
                        }
                    }
                ]
            }
        }
    }
    return json.dumps(template)

def document_message(number, url, caption, filename):
    data = json.dumps({
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": number,
        "type": "document",
        "document": {
            "link": url,
            "caption": caption,
            "filename": filename
        }
    })
    return send_message(data)

def menu_services_message(number):
    services_template = {
        "messaging_product": "whatsapp",
        "to": number,
        "type": "interactive",
        "interactive": {
            "type": "list",
            "header": {
                "type": "text",
                "text": "Python - Bot"
            },
            "body": {
                "text": "Select one of our services:"
            },
            "footer": {
                "text": "Clobi Technologies"
            },
            "action": {
                "button": "View Services",
                "sections": [
                    {
                        "title": "Business Intelligence",
                        "rows": [
                            {
                                "id": "business_intelligence",
                                "title": "Business Intelligence"
                            }
                        ]
                    },
                    {
                        "title": "Software Development",
                        "rows": [
                            {
                                "id": "software_development",
                                "title": "Software Development"
                            }
                        ]
                    },
                    {
                        "title": "Marketing Digital",
                        "rows": [
                            {
                                "id": "marketing_digital",
                                "title": "Marketing Digital"
                            }
                        ]
                    }
                ]
            }
        }
    }
    return json.dumps(services_template)

def manage_chatbot(text, number, id_message, name):
    text = text.lower()
    print(f"Received text: {text}, number: {number}, id_message: {id_message}, name: {name}")  # Debugging print
    if 'hola' in text:
        message = welcome_message(number, name)
        send_message(message)
    elif 'services' in text or text == 'button_id_for_servicios':  
        message = menu_services_message(number)
        send_message(message)
    elif text == 'business_intelligence':
        pdf_url = Config.pdf_business
        pdf_caption = "Download our Business Intelligence to learn more about this service. ✅"
        pdf_filename = "Business Intelligence.pdf"
        message = document_message(number, pdf_url, pdf_caption, pdf_filename)
        send_message(message)
    elif text == 'software_development':
        pdf_url = Config.pdf_software
        pdf_caption = "Download our Software Development brochure to learn more about this service. ✅"
        pdf_filename = "Software Development.pdf"
        message = document_message(number, pdf_url, pdf_caption, pdf_filename)
        send_message(message)
    elif text == 'marketing_digital':
        pdf_url = Config.pdf_marketing
        pdf_caption = "Download our Marketing Digital brochure to learn more about this service. ✅"
        pdf_filename = "Marketing Digital.pdf"
        message = document_message(number, pdf_url, pdf_caption, pdf_filename)
        send_message(message)
    else:
        print(f"Unrecognized service ID: {text}")  # Debugging print
