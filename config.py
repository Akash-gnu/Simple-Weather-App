import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'weather-app-secret-key')
    OPENWEATHER_API_KEY = os.environ.get('OPENWEATHER_API_KEY', 'dfd26ba5cfabdc6f7b53ea3f36f4c1ed')