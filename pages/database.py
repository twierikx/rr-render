import firebase_admin
from firebase_admin import credentials, firestore
from pydantic import BaseModel
from .models import Recipe
import os
import uuid
import datetime as dt
from flask import Blueprint
import os

if os.getenv("CURRENT_ENV") == 'PROD':
    print("Running on Production")
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'/etc/secrets/recipe-randomize-6b9879079236.json'
    collection_name = 'recipes'
else:
    # Local testing configuration
    print("Running locally")
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'secrets\recipe-randomize-6b9879079236.json'
    collection_name = 'recipes-dev'

# Application Default credentials are automatically created.
app = firebase_admin.initialize_app()
db = firestore.client()

class Database():

    def __init__(self, rec_collection_name: str = 'recipes-dev'):
        self.rec_collection_name = rec_collection_name
        self.rec_col = self.get_collection(self.rec_collection_name)

    def get_client(self):
        return firestore.Client()

    def get_collection(self, collection_name):
        client = self.get_client()
        return client.collection(collection_name)

    def add_recipe(self, recipe_dict: dict):
        recipe_id = str(uuid.uuid4())

        # Add the UUID and the current time to the recipe data
        recipe_dict['id'] = recipe_id
        recipe_dict['added_at'] = dt.datetime.now()

        # Create a document reference with the UUID
        doc_ref = self.rec_col.document(recipe_id)

        # Set the recipe data in the document
        doc_ref.set(recipe_dict)

        # Optionally, return the recipe ID or the complete recipe data
        return recipe_dict

    def update_fields(self, recipe_id: uuid.UUID, update_dict: dict):
        doc_ref = self.rec_col.document(recipe_id)
        doc_ref.set(update_dict, merge=True)
    
    def add_comment(self, recipe_id: uuid.UUID, comment: dict):
        doc_ref = self.rec_col.document(recipe_id)
        doc_ref.update({
        "comments": firestore.ArrayUnion([comment])
        })

    def get_recipe(self, recipe_id):
        doc_ref = self.rec_col.document(recipe_id)
        doc = doc_ref.get()
        return doc.to_dict()
    
    def delete_recipe(self, recipe_id: uuid.UUID):
        doc_ref = self.rec_col.document(str(recipe_id))
        doc_ref.delete()
        return True
    
    def list_recipes(self):
        # return [recipe.to_dict() for recipe in self.rec_col.stream()]
        recipes = []
        for recipe in self.rec_col.stream():
            recipe_data = recipe.to_dict()
            # Provide default values for missing fields
            if 'added_at' not in recipe_data:
                recipe_data['added_at'] = None
            recipes.append(Recipe(**recipe_data))
        return recipes
    
db_instance = Database(rec_collection_name=collection_name)