from flask import current_app, Blueprint, send_from_directory
import os

home_bp = Blueprint('home', __name__)


@home_bp.route('/', defaults={'path': ''})
@home_bp.route('/<path:path>')
def home(path):
    # Home page.
    static_folder = os.path.join(current_app.root_path, '..', 'angular-app', 'dist', 'angular-app')
    if path != "" and os.path.exists(os.path.join(static_folder, path)):
        return send_from_directory(static_folder, path)
    else:
        static_folder = os.path.join(current_app.root_path, '..', '..', 'angular-app', 'dist', 'angular-app', 'browser')
    return send_from_directory(static_folder, 'index.html')