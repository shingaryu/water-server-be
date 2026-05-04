from flask import Blueprint, redirect, render_template, request

from common.scorebook_links import scorebook_local_path

root_bp = Blueprint('root', __name__)


@root_bp.route('/')
def index():
    return render_template('index.html')


@root_bp.route('/badminton-scorebook')
def badminton_scorebook():
    return render_template('index (1).html')


@root_bp.route('/water-cooler-scorebook')
def water_cooler_scorebook():
    return redirect(scorebook_local_path(tab=request.args.get("tab")))
