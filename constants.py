from dotenv import load_dotenv
import os


load_dotenv()


DEBUG = True if os.getenv("ENV") == "dev" else False

DJANGO_SECRET_KEY = os.getenv("DJANGO_SECRET_KEY") or 'default_secret_key'


POSTGRES_USER=os.getenv('POSTGRES_USER')
POSTGRES_DB_NAME=os.getenv('POSTGRES_DB_NAME')  if DEBUG == False else "windam_pro"
POSTGRES_PASSWORD=os.getenv('POSTGRES_PASSWORD') if DEBUG == False else "lamotte"
POSTGRES_HOST=os.getenv('POSTGRES_HOST') if DEBUG == False else "localhost"
POSTGRES_PORT=os.getenv("POSTGRES_PORT") if DEBUG == False else "5432"

GMAIL_STMP_USERNAME=os.getenv('GMAIL_STMP_USERNAME')
GMAIL_STMP_PW=os.getenv('GMAIL_STMP_PW')

OTP_SECRET_KEY=os.getenv('OTP_SECRET_KEY')