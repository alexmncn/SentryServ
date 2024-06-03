import sys
import site

sys.path.insert(0, '/var/www/html/controlserver/flask-app/')  # Add the project route

from app import app  # Import the app from app.py

app = app.create_app()  # Asign aplicattion var for app
