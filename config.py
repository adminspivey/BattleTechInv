import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_default_secret_key_here')

# In the future, you can add database settings here