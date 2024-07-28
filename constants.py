from dotenv import load_dotenv
import os


load_dotenv()

DJANGO_SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")


POSTGRES_USER=os.getenv('POSTGRES_USER')
POSTGRES_DB_NAME=os.getenv('POSTGRES_DB_NAME')
POSTGRES_PASSWORD=os.getenv('POSTGRES_PASSWORD')