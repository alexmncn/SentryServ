"""User related services."""
from flask import redirect, url_for, flash
from flask_login import current_user
from functools import wraps
import json


def user_has_role(role):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if current_user.is_authenticated and current_user.role == role:
                return fn(*args, **kwargs)
            else:
                flash("No tienes permiso para acceder a esta página.", "danger")
                return redirect(url_for('home.home'))
        return decorated_view
    return wrapper

def get_user_ip(username):
    # Get file path
    file_path = '/var/www/html/controlserver/app/logs/users_ips_log.json'

    try:
        # Try to load existing file
        with open(file_path, 'r') as json_file:
            user_data = json.load(json_file)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        # If file does not exist or is empty, return None
        return None

    # Search for entry corresponding to username
    for entry in reversed(user_data):
        if entry["username"] == username:
            remote_host = entry["data"].get("remote_host", None)
            return remote_host

    # If username not found, return None
    return None
