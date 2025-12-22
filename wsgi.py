from app import create_app
from dotenv import load_dotenv

load_dotenv()

# WSGI callable
app = create_app()