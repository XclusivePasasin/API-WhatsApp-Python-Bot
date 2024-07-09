from config.config import Config
import requests, json
from datetime import datetime

# Diccionario para rastrear el estado de la conversación de cada usuario
conversation_states = {}

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
        response = requests.post(whatsapp_url, headers=headers, json=data)
        print("Response status:", response.status_code)  # Print response status
        print("Response text:", response.text)  # Print response text
        if response.status_code == 200:
            return 'Message sent successfully!', 200
        else:
            return 'Error sending message!', response.status_code
    except Exception as e:
        return str(e), 403

def welcome_message(number, name):
    message = f'Hi {name}! 👋, Let me introduce myself, I´m Clobi, your virtual assistant! 😎 \n How can I help you?'
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
                    },
                    {
                        "type": "reply",
                        "reply": {
                            "id": "button_id_for_survey",
                            "title": "Take Survey"
                        }
                    }
                ]
            }
        }
    }
    return template

def document_message(number, url, caption, filename):
    data = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": number,
        "type": "document",
        "document": {
            "link": url,
            "caption": caption,
            "filename": filename
        }
    }
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
    return services_template

def survey_message(number):
    message = {
        "messaging_product": "whatsapp",
        "to": number,
        "type": "interactive",
        "interactive": {
            "type": "list",
            "header": {
                "type": "text",
                "text": "Survey"
            },
            "body": {
                "text": "How would you rate the ease of use of our software?"
            },
            "footer": {
                "text": "Clobi Technologies"
            },
            "action": {
                "button": "Rate Now",
                "sections": [
                    {
                        "title": "Rate Our Service",
                        "rows": [
                            {
                                "id": "survey_excellent",
                                "title": "Excellent"
                            },
                            {
                                "id": "survey_good",
                                "title": "Good"
                            },
                            {
                                "id": "survey_average",
                                "title": "Average"
                            },
                            {
                                "id": "survey_poor",
                                "title": "Poor"
                            }
                        ]
                    }
                ]
            }
        }
    }
    return message



def manage_chatbot(text, number, id_message, name):
    text = text.lower()
    print(f"Received text: {text}, number: {number}, id_message: {id_message}, name: {name}")  # Debugging print

    # Check if the user is already in the conversation state
    if number in conversation_states:
        state = conversation_states[number]
    else:
        state = None

    if state == "awaiting_date":
        # Validate date input from the user
        try:
            appointment_date = datetime.strptime(text, '%d/%m/%Y')
            response_message = {
                "messaging_product": "whatsapp",
                "to": number,
                "type": "text",
                "text": {
                    "body": f"Your appointment is scheduled for {appointment_date.strftime('%d/%m/%Y')}. Thank you! Can i help you in any way?"
                }
            }
            send_message(response_message)
            # Reset the state
            conversation_states.pop(number, None)
        except ValueError:
            response_message = {
                "messaging_product": "whatsapp",
                "to": number,
                "type": "text",
                "text": {
                    "body": "The date format is incorrect. Please write it this way DD/MM/YYYY."
                }
            }
            send_message(response_message)
    else:
        if 'hola' in text:
            message = welcome_message(number, name)
            send_message(message)
        elif 'services' in text or text == 'button_id_for_servicios':
            message = menu_services_message(number)
            send_message(message)
        elif text == 'business_intelligence':
            pdf_url = Config.pdf_business
            pdf_caption = "Download our Business Intelligence brochure to learn more about this service. ✅"
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
        elif "schedule appointment" in text or text == "button_id_for_date":
            response_message = {
                "messaging_product": "whatsapp",
                "to": number,
                "type": "text",
                "text": {
                    "body": "Ok, let's schedule your appointment, what day will it be? Write it this way DD/MM/YYYY"
                }
            }
            send_message(response_message)
            # Set the state to awaiting date input
            conversation_states[number] = "awaiting_date"
        elif "survey" in text or text == "button_id_for_survey":
            message = survey_message(number)
            send_message(message)
        # elif "no" in text or text:
        #     response_message = {
        #         "messaging_product": "whatsapp",
        #         "to": number,
        #         "type": "text",
        #         "text": {
        #             "body": "Goood!! See you later"
        #         }
        #     }
        #     send_message(response_message)
        # elif "yes" in text:
        #     message = welcome_message(number, name)
        #     send_message(message)
        else:
            print(f"Unrecognized service ID: {text}")  # Debugging print
