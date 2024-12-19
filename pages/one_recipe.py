from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from .models import Recipe
from .database import db_instance
from datetime import datetime
import random
import pandas as pd
import uuid

one_recipe_bp = Blueprint('one_recipe', __name__)

@one_recipe_bp.route('/recipe/new', methods=['GET','POST'])
def new_recipe():

    if request.method == 'POST':
        
        # Handle form submission to update recipe
        new_recipe = dict(request.form)

        # Split the ingredients by newlines, trimming extra spaces
        ingredients_list = [
            ingredient.strip() for ingredient in new_recipe['ingredients'].split('\n') if ingredient.strip()
        ]
        new_recipe['ingredients'] = ingredients_list
        new_recipe['time'] = int(new_recipe['time'])

        recipe = db_instance.add_recipe(new_recipe)  # Save changes to the database
        return redirect(f'/recipe/{recipe["id"]}')  # Redirect back to the view page after saving

    return render_template('new-recipe.html')

@one_recipe_bp.route('/recipe/<uuid:recipe_id>', methods=['GET'])
def get_recipe(recipe_id):
    recipe = db_instance.get_recipe(str(recipe_id))

    if not recipe:
        return jsonify({"error": "Recipe not found"}), 404
    
    # Convert UUIDs to strings
    recipe_dict = recipe
    recipe_dict['id'] = str(recipe_dict['id'])
    recipe_dict['added_at'] = recipe_dict['added_at'].strftime("%d %b %Y")
    return render_template('one-recipe.html', recipe=recipe_dict)

@one_recipe_bp.route('/recipe/<uuid:recipe_id>/edit', methods=['GET', 'POST'])
def edit_recipe(recipe_id):
    recipe = db_instance.get_recipe(str(recipe_id))

    if not recipe:
        return jsonify({"error": "Recipe not found"}), 404

    if request.method == 'POST':

        # Handle form submission to update recipe
        updated_name = request.form.get('name')
        updated_ingredients = request.form.get('ingredients')  # Get the multiline string

        # Split the ingredients by newlines, trimming extra spaces
        updated_ingredients_list = [
            ingredient.strip() for ingredient in updated_ingredients.split('\n') if ingredient.strip()
        ]

        recipe['name'] = updated_name
        recipe['ingredients'] = updated_ingredients_list

        db_instance.update_fields(str(recipe_id), recipe)  # Save changes to the database
        return redirect(f'/recipe/{recipe_id}')  # Redirect back to the view page after saving

    return render_template('one-recipe.html', recipe=recipe, mode="edit")


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