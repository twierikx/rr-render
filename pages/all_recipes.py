from flask import Blueprint, request, jsonify, render_template
from .models import Recipe
from .database import db_instance
import random
import pandas as pd

all_recipes_bp = Blueprint('all_recipes', __name__)

@all_recipes_bp.route('/all-recipes')
def all_recipes():

    recipes = db_instance.list_recipes()
    recipes_data = [recipe.dict() for recipe in recipes]  # Convert each Recipe instance to a dictionary
    print(recipes_data)
    return render_template('all-recipes.html', recipes=recipes_data)




# @get_recipes_bp.route('/all', methods=['GET'])
# def get_all_recipes():
#     recipes = db_instance.list_recipes()
#     recipes_data = [recipe.dict() for recipe in recipes]  # Convert each Recipe instance to a dictionary
#     return {"data": recipes_data}

# @get_recipes_bp.route('/random-recipe', methods=['GET'])
# def get_random_recipe():
#     recipes = db_instance.list_recipes()

#     recipe_names = [recipe.name for recipe in recipes]

#     # Select a random recipe from the list of documents
#     random_recipe = random.choice(recipe_names)
#     return {"name": random_recipe}


# @get_recipes_bp.route('/random-recipe-filtered', methods=['GET'])
# def get_random_recipe_filtered():
#     time = request.args.get('time')  # Query parameter for time
#     ingredients = request.args.get('ingredients')  # Query parameter for ingredients

#     recipes = db_instance.list_recipes()

#     # Filter based on time if provided
#     if time:
#         print(f'Filtering on time, maximum of {time} minutes')
#         recipes = [recipe for recipe in recipes if recipe.time <= int(time)]

#     # Filter based on ingredients if provided
#     if ingredients:
#         ingredients_lower = ingredients.lower()
#         recipes = [
#             recipe for recipe in recipes
#             if any(ingredients_lower in ingredient.lower() for ingredient in recipe.ingredients)
#         ]

#     # Ensure there are recipes after filtering
#     if not recipes:
#         return jsonify({"error": "No recipes found matching the criteria"}), 404

#     recipe_names = [recipe.name for recipe in recipes]

#     # Select a random recipe from the list of names
#     random_recipe = random.choice(recipe_names)
#     return {"name": random_recipe}


# @get_recipes_bp.route('/get_table_data', methods=['GET'])
# def get_table_data():
#     data = db_instance.list_recipes()

#     # Convert data to a Pandas DataFrame
#     df = pd.DataFrame(data)

#     # Convert DataFrame to JSON format
#     return {"data": df.to_dict(orient="records")}


# @get_recipes_bp.route('/recipe/<int:recipe_id>', methods=['GET'])
# def get_recipe(recipe_id):
#     recipe = db_instance.get_recipe(recipe_id)

#     if not recipe:
#         return jsonify({"error": "Recipe not found"}), 404

#     return recipe
