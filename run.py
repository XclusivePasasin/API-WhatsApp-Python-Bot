from flask import Flask, request, jsonify
from config.config import Config
from services import services as service

app = Flask(__name__)

@app.route('/Webhook', methods=['GET'])
def verify_token():
    try:
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        print(Config.token_verify)
        print(token)
        if token == Config.token_verify and challenge is not None:
            return challenge
        else:
            return 'Wrong token!', 403
    except Exception as e:
        return jsonify({"error": str(e)}), 403

@app.route('/Webhook', methods=['POST'])
def receive_messages():
    try:
        body = request.get_json()
        print(body)
        entry = body['entry'][0]
        changes = entry['changes'][0]
        value = changes['value']
        message = value['messages'][0]
        number = message['from']
        id_message = message['id']
        contacts = value['contacts'][0]
        name = contacts['profile']['name']
        text = service.get_message(message)
        # Active chatbot
        service.manage_chatbot(text, number, id_message, name)
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
