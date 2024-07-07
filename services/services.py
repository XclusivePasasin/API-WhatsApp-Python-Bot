from config.config import Config
import requests, json

def get_message(message):
    if 'type' not in message:
        text = 'Message not recognized by the system.'
        
    type_message = message['type']
    if type_message == 'text':
        text = message['text']['body']
    return text

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

def text_message(number, text):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",    
            "recipient_type": "individual",
            "to": number,
            "type": "text",
            "text": {
                "body": text
            }
        }
    )
    return data

def manage_chatbot(text, number, id_message, name):
    text = text.lower() # Message of user
    message = f'Hola {name}!, Me Presento Soy Clobi, Tu asistente virtual!'
    data = text_message(number, message)
    send_message(data)
