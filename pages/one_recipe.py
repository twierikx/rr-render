from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from .models import Recipe
from .database import db_instance
from datetime import datetime
import random
import pandas as pd
from uuid import uuid4

one_recipe_bp = Blueprint('one_recipe', __name__)

@one_recipe_bp.route('/recipe/<uuid:recipe_id>', methods=['GET'])
def get_recipe(recipe_id):
    print('\n\n\n\nCALLED\n\n\n\n')
    recipe = db_instance.get_recipe(str(recipe_id))

    if not recipe:
        return jsonify({"error": "Recipe not found"}), 404
    
    # Convert UUIDs to strings
    recipe_dict = recipe
    recipe_dict['id'] = str(recipe_dict['id'])

    print(recipe_dict)

    return render_template('one-recipe.html', recipe=recipe_dict)

@one_recipe_bp.route('/recipe/add-comment', methods=['POST'])
def add_comment():
    content = request.form.get('content')
    author = request.form.get('author', 'Anonymous')

    if content:
        comment = {
            "id": str(uuid4()),
            "added_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "content": content,
            "author": author
        }
        
    # Redirect back to the recipe page after processing the comment
    recipe_id = request.form.get('recipe_id')  # Ensure this is passed in the form
    if recipe_id:
        db_instance.add_comment(recipe_id=recipe_id, comment=comment)
        return redirect(url_for('one_recipe.get_recipe', recipe_id=recipe_id))
    
    # If recipe_id is missing, return an error response
    return jsonify({"error": "Missing recipe ID"}), 400