from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from .models import Recipe
from .database import Database
import random
import pandas as pd


db = Database()

router = APIRouter()

@router.get("/random-recipe")
def get_random_recipe():
    recipes = db.list_recipes()
    recipe_names = [recipe.name for recipe in recipes]

    # Select a random recipe from the list of documents
    random_recipe = random.choice(recipe_names)
    return {"name":random_recipe}

@router.get("/random-recipe-filtered")
def get_random_recipe(time: str = Query(None), ingredients: str = Query(None)):
    recipes = db.list_recipes()

    # Filter based on time if it's provided
    if time:
        print(f'Filtering on time, maximum of {time} minutes')
        recipes = [recipe for recipe in recipes if recipe.time <= int(time)]

    # Filter based on ingredients if they are provided
    if ingredients:
        ingredients_lower = ingredients.lower()
        recipes = [recipe for recipe in recipes if any(ingredients_lower in ingredient.lower() for ingredient in recipe.ingredients)]

    # Ensure there are recipes after filtering
    if not recipes:
        return {"error": "No recipes found matching the criteria"}

    recipe_names = [recipe.name for recipe in recipes]

    # Select a random recipe from the list of names
    random_recipe = random.choice(recipe_names)
    return {"name": random_recipe}

@router.get("/get_table_data")
def get_table_data():
    data = db.list_recipes()
    df = pd.DataFrame(data)

    return JSONResponse(content={"data": df.to_dict(orient="records")})

@router.get("/all")
def all_recipes():
    recipes = db.list_recipes()
    return {"data":recipes}

@router.get("/recipe/{recipe_id}")
def get_recipe(recipe_id):
    recipe = db.get_recipe(recipe_id)
    return recipe
    

