from fastapi import APIRouter, HTTPException, status
from .models import Recipe
from .database import Database
import uuid

db = Database()


router = APIRouter()

@router.delete("/{recipe_id}")
def delete_recipe(recipe_id: uuid.UUID):
    try:
        # Assuming db.delete_recipe() properly handles the deletion
        deleted = db.delete_recipe(recipe_id)
        
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")
        
    except Exception as e:
        # It's better to log the actual exception for debugging
        print(f"Error deleting recipe: {e}")

        # Raise a more generic message to the user
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error occurred while deleting the recipe")

@router.put("/update/{recipe_id}")
def update_recipe(recipe_id: uuid.UUID, data: dict):
    try:
        updated = db.update_fields(recipe_id, data)

        if not updated:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")
    
    except Exception as e:
        # It's better to log the actual exception for debugging
        print(f"Error editing recipe: {e}")

        # Raise a more generic message to the user
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error occurred while editing the recipe")



