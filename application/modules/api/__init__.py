from flask import Blueprint

api_blueprint = Blueprint(__name__, 'api_blueprint', url_prefix='/api/v1.0')

from .blocs import *
from .users import *
