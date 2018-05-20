from flask import Blueprint, render_template

home_controller = Blueprint('home', __name__)


@home_controller.route('/', defaults={'path': ''})
def home(path):
    return render_template("index.html")


@home_controller.route('/<path:path>')
def static_proxy(path):
    return home_controller.send_static_file(path)
