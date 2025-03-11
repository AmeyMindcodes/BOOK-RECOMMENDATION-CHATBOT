# Instance-specific configuration
import os

SECRET_KEY = os.environ.get('SECRET_KEY', 'your_secret_key_here')
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

# API Keys
GOOGLE_BOOKS_API_KEY = os.environ.get('GOOGLE_BOOKS_API_KEY', '')
NYT_BOOKS_API_KEY = os.environ.get('NYT_BOOKS_API_KEY', '') 