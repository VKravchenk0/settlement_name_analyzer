from flask import Blueprint, send_from_directory

static_files_bp = Blueprint('static_files_bp', __name__, template_folder='templates')


# serving js files
@static_files_bp.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('templates/js', path)


# serving css files
@static_files_bp.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('templates/css', path)
