from flask import Flask, request, jsonify
from config.config import Config
from services import services as service
import logging

app = Flask(__name__)

# Configura el registro de errores
logging.basicConfig(level=logging.INFO)

@app.route('/Webhook', methods=['GET'])
def verify_token():
    try:
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        if token == Config.token_verify and challenge is not None:
            return challenge
        else:
            return 'Wrong token!', 403
    except Exception as e:
        logging.error(f"Error in verify_token: {e}")
        return jsonify({"error": str(e)}), 403

@app.route('/Webhook', methods=['POST'])
def receive_messages():
    try:
        body = request.get_json()
        logging.info(f"Received request body: {body}")
        
        entry = body['entry'][0]
        changes = entry['changes'][0]
        value = changes['value']
        
        if 'messages' not in value:
            return jsonify({"status": "No messages field found"}), 200
        
        message = value['messages'][0]
        number = message['from']
        id_message = message['id']
        contacts = value['contacts'][0]
        name = contacts['profile']['name']
        text = service.get_message(message)
        print(f' == INICIO JSON == \n {body} \n == FINAL JSON ==')
        
        if text == 'enter_date':
            service.send_message({
                "messaging_product": "whatsapp",
                "to": number,
                "text": {
                    "body": "Por favor ingresa la fecha en el formato DD/MM/AAAA."
                }
            })
        else:
            service.manage_chatbot(text, number, id_message, name)
        
        return jsonify({"status": "success"}), 200
    except Exception as e:
        logging.error(f"Error in receive_messages: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
