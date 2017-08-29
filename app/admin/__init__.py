from flask import Blueprint

admin = Blueprint('admin', __name__, static_folder='')

from . import views

