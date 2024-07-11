import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

class Config:
    token_verify = os.getenv('TOKEN_VERIFY')
    whatsapp_token = os.getenv('WHATSAPP_TOKEN')
    whatsapp_url = os.getenv('WHATSAPP_URL')
    pdf_business = os.getenv('PDF_BUSINESS_INTELLIGENCE')
    pdf_software = os.getenv('PDF_SOFTWARE_DEVELOPMENT')
    pdf_marketing = os.getenv('PDF_MARKETING_DIGITAL')
    

