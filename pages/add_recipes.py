from flask import Blueprint, request, jsonify
from .models import Recipe
from .database import Database

db = Database()
add_recipes_bp = Blueprint('recipe', __name__)

@add_recipes_bp.route('/add-recipe', methods=['POST'])
def add_recipe():
    try:
        # Parse the incoming JSON data
        recipe_dict = request.get_json()

        if not recipe_dict:
            return jsonify({"error": "No data provided"}), 400

        # If the recipe has an `id`, update the existing recipe
        if 'id' in recipe_dict and recipe_dict['id']:
            updated = db.update_fields(recipe_dict['id'], recipe_dict)
            if updated:
                return jsonify({"message": "Recipe updated successfully"}), 200
            else:
                return jsonify({"error": "Recipe not found for updating"}), 404

        # Otherwise, add a new recipe
        recipe = db.add_recipe(recipe_dict)
        return jsonify(recipe), 201  # Return the created recipe with a 201 status code

    except Exception as e:
        # Log the actual exception for debugging
        print(f"Error adding a recipe: {e}")

        # Return a generic error message
        return jsonify({"error": "An error occurred while adding the recipe"}), 500
