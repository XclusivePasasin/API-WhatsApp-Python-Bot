import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

class Config:
    token_verify = os.getenv('TOKEN_VERIFY')
    whatsapp_token = os.getenv('WHATSAPP_TOKEN')
    whatsapp_url = os.getenv('WHATSAPP_URL')

