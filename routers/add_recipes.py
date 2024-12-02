from fastapi import APIRouter, HTTPException
from .models import Recipe
from .database import Database


db = Database()


router = APIRouter()

@router.post("/add-recipe")
def add_recipe(recipe_dict: dict):
    print(recipe_dict)
    if recipe_dict['id']:
        db.update_fields(recipe_dict['id'], recipe_dict)
        return
    try:
        recipe = db.add_recipe(recipe_dict)    
        return recipe
    except Exception as e:
        raise HTTPException(f'Adding a recipe went wrong;\n{e}')
