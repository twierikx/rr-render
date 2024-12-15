from flask import Blueprint
from .all_recipes import get_recipes_bp
from .edit_recipes import edit_recipes_bp
from .add_recipes import add_recipes_bp

api_bp = Blueprint('API', __name__)

api_bp.register_blueprint(get_recipes_bp,url_prefix='/get-recipe')
api_bp.register_blueprint(edit_recipes_bp,url_prefix='/edit-recipe')
api_bp.register_blueprint(add_recipes_bp,url_prefix='/add-recipe')

