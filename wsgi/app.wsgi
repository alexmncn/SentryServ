# /var/www/html/controlserver/wsgi/app_ssl.wsgi
import sys
import site

sys.path.insert(0, '/var/www/html/controlserver')  # Add the project route

from app import app  # Import the app from app.py

application = app.create_app()  # Asign aplicattion var for app
