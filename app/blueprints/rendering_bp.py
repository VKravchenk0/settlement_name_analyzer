from flask import Blueprint, render_template

rendering_bp = Blueprint('rendering_bp', __name__, template_folder='templates')


@rendering_bp.route("/")
def index():
    return render_template('index.html')
