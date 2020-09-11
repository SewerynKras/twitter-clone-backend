"""
WSGI config for backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

from django.core.wsgi import get_wsgi_application
import os

# Load the env file
from dotenv import load_dotenv
from pathlib import Path
env = os.environ['env'].lower()
env_path = Path('.') / f'{env}.env'
load_dotenv(dotenv_path=env_path)


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

application = get_wsgi_application()
