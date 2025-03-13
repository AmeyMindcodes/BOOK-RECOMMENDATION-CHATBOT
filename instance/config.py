# Instance-specific configuration
import os

SECRET_KEY = os.environ.get('SECRET_KEY', 'aedbd5d71a43cee2052a1f4a91acdcf027e87e13a270fa24a3e585966e482b9c')
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

# API Keys
GOOGLE_BOOKS_API_KEY = os.environ.get('GOOGLE_BOOKS_API_KEY', 'AIzaSyDP3748GbW4fbYi3M9IWqetTl9DUC1jCuQ')
NYT_BOOKS_API_KEY = os.environ.get('NYT_BOOKS_API_KEY', 'fpAAq87lzX04wf2g') 