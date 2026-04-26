from flask import Blueprint, render_template

root_bp = Blueprint('root', __name__)


@root_bp.route('/')
def index():
    return render_template('index.html')


@root_bp.route('/badminton-scorebook')
def badminton_scorebook():
    return render_template('index (1).html')
