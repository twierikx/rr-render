from flask import Blueprint, jsonify, request
from .models import Recipe
from .database import Database
import uuid

db = Database()
edit_recipes_bp = Blueprint('edit_recipes', __name__)

@edit_recipes_bp.route('/<uuid:recipe_id>', methods=['DELETE'])
def delete_recipe(recipe_id):
    try:
        # Assuming db.delete_recipe() properly handles the deletion
        deleted = db.delete_recipe(recipe_id)
        
        if not deleted:
            return jsonify({"error": "Recipe not found"}), 404

        return jsonify({"message": "Recipe deleted successfully"}), 200

    except Exception as e:
        # Log the actual exception for debugging
        print(f"Error deleting recipe: {e}")
        
        # Return a generic error message
        return jsonify({"error": "An error occurred while deleting the recipe"}), 500


@edit_recipes_bp.route('/update/<uuid:recipe_id>', methods=['PUT'])
def update_recipe(recipe_id):
    try:
        # Extract JSON data from the request body
        data = request.get_json()

        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Assuming db.update_fields() handles the update logic
        updated = db.update_fields(recipe_id, data)

        if not updated:
            return jsonify({"error": "Recipe not found"}), 404

        return jsonify({"message": "Recipe updated successfully"}), 200

    except Exception as e:
        # Log the actual exception for debugging
        print(f"Error editing recipe: {e}")
        
        # Return a generic error message
        return jsonify({"error": "An error occurred while editing the recipe"}), 500
