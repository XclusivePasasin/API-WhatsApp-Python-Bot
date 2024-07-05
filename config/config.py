from dotenv import load_dotenv
import os

# Cargar las variables de entorno desde el archivo .env
load_dotenv()
# Acceder a las variables de entorno
TOKEN = os.getenv('TOKEN')
ID_NUMERO_TELEFONO = os.getenv('ID_NUMERO_TELEFONO')
TELEFONO_ENVIA = os.getenv('TELEFONO_ENVIA')
