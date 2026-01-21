import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'weather app password')

    OPENWEATHER_API_KEY = os.environ.get('OPENWEATHER_API_KEY', 'write your api key')
