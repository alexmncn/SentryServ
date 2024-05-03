"""User related services."""
import json


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