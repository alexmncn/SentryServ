import sys

sys.path.insert(0, '/var/www/html/controlserver/flask-app/')  # Add the project route


from app import app  # Import the app from app.py
from app.services.net_and_connections import notify_new_public_ip

app = app.create_app()  # Asign aplicattion var for app


@app.before_first_request
def on_init():
    try:
        notify_new_public_ip()
    except:
        print('Init Error')