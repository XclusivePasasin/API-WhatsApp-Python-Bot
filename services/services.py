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

def actions_menu_message(number, name):
    message = f'With great pleasure  {name}! 😎, What action do you want to perform? 🤔'
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

def action_prompt_message(number):
    message = "Would you like to perform another action? 🤓"
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
                            "id": "action_yes",
                            "title": "Yes"
                        }
                    },
                    {
                        "type": "reply",
                        "reply": {
                            "id": "action_no",
                            "title": "No"
                        }
                    }
                ]
            }
        }
    }
    return template

def farewell_message(number):
    message = "Thank you for using our service! We hope to see you soon. 😎 "
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
                            "id": "action_goodbye",
                            "title": "Sign off"
                        }
                    }
                ]
            }
        }
    }
    return template

def document_message(number, url, caption, filename):
    data = (
        {
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
    )
    return data

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

def survey_message(number, question_text, options):
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
                "text": question_text
            },
            "footer": {
                "text": "Clobi Technologies"
            },
            "action": {
                "button": "Select an option",
                "sections": [
                    {
                        "title": "Options",
                        "rows": []
                    }
                ]
            }
        }
    }

    # Add options dynamically
    for option in options:
        message["interactive"]["action"]["sections"][0]["rows"].append({
            "id": f"survey_{option.lower()}",
            "title": option
        })

    return message



# Variables for the survey
survey_responses = {}
survey_questions = [
    "How would you rate the ease of use of our software?",
    "How satisfied are you with the speed of our software?",
    "How would you evaluate the quality of the technical support we offer?",
    "How useful do you find the features and functions of our software?",
    "What opinion do you have about the graphical interface of our software?"
]

def manage_date(number, text, conversation_states):
   
    # Check if the user is already in the conversation state
    state = conversation_states.get(number)

    if state == "awaiting_date":
        # Validate date input from the user
        try:
            appointment_date = datetime.strptime(text, '%d/%m/%Y')
            template = {
                "messaging_product": "whatsapp",
                "to": number,
                "type": "text",
                "text": {
                    "body": f"Your appointment is scheduled for {appointment_date.strftime('%d/%m/%Y')}. We'll be waiting for you. 😎"
                }
            }
            # Reset the state
            conversation_states.pop(number, None)
        except ValueError:
            template = {
                "messaging_product": "whatsapp",
                "to": number,
                "type": "text",
                "text": {
                    "body": "The date format is incorrect. Please write it this way DD/MM/YYYY. 👀"
                }
            }
        return template

    return None

def mark_read_message(id_message):
    
    data = {
        "messaging_product": "whatsapp",
        "status": "read",
        "message_id": id_message
    }
    
    return send_message(data)

def emoji_reaction_message(id_message, number):
    emoji = '🥵'
    data = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": number,
        "type": "reaction",
        "reaction": {
            "message_id": id_message,
            "emoji": emoji
        }
    }
    return send_message(data)


def manage_chatbot(text, number, id_message, name):
    text = text.lower()
    print(f"Received text: {text}, number: {number}, id_message: {id_message}, name: {name}")  # Debugging print
    # View Message
    mark_read_message(id_message)
    emoji_reaction_message(id_message, number)
    
    # Check if the user is already in the conversation state
    if number in conversation_states:
        state = conversation_states[number]
    else:
        state = None

    if state == "awaiting_date":
        message = manage_date(number, text, conversation_states)
        if message:
            send_message(message)
            prompt_message = action_prompt_message(number)
            send_message(prompt_message)
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
            prompt_message = action_prompt_message(number)
            send_message(prompt_message)
        elif text == 'software_development':
            pdf_url = Config.pdf_software
            pdf_caption = "Listo 😁"
            pdf_filename = "Software Development.pdf"
            message = document_message(number, pdf_url, pdf_caption, pdf_filename)
            send_message(message)
            prompt_message = action_prompt_message(number)
            send_message(prompt_message)
        elif text == 'marketing_digital':
            pdf_url = Config.pdf_marketing
            pdf_caption = "Download our Marketing Digital brochure to learn more about this service. ✅"
            pdf_filename = "Marketing Digital.pdf"
            message = document_message(number, pdf_url, pdf_caption, pdf_filename)
            send_message(message)
            prompt_message = action_prompt_message(number)
            send_message(prompt_message)
        elif "schedule appointment" in text or text == "button_id_for_date":
            response_message = {
                "messaging_product": "whatsapp",
                "to": number,
                "type": "text",
                "text": {
                    "body": "Ok, let's schedule your appointment, what day will it be? Write it this way DD/MM/YYYY. 😎📝"
                }
            }
            send_message(response_message)
            # Set the state to awaiting date input
            conversation_states[number] = "awaiting_date"
        elif "survey" in text or text == "button_id_for_survey":
            # Handle survey questions iteratively
            if number not in survey_responses:
                survey_responses[number] = 0  # Inicializar el índice de preguntas para este número

            current_question_index = survey_responses[number]

            if current_question_index < len(survey_questions):
                question_text = survey_questions[current_question_index]
                options = ["Excellent", "Good", "Average", "Poor"]
                message = survey_message(number, question_text, options)
                send_message(message)
                survey_responses[number] += 1  # Mover a la siguiente pregunta
            else:
                survey_responses.pop(number, None) 
                send_message({
                    "messaging_product": "whatsapp",
                    "to": number,
                    "type": "text",
                    "text": {
                        "body": "Thank you for completing the survey! 🥺"
                    }
                })
                prompt_message = action_prompt_message(number)
                send_message(prompt_message)
        elif "action_yes" in text:
            message = actions_menu_message(number, name)
            send_message(message)
        elif "action_no" in text:
            message = farewell_message(number)
            send_message(message)
        else:
            print(f"Unrecognized service ID: {text}")  # Debugging print

