from pydantic import BaseModel, validator
from typing import List, Optional
import datetime as dt
import uuid

class Ingredient(BaseModel):
    name: str
    quantity: int 
    unit: str

class Recipe(BaseModel):
    id: Optional[uuid.UUID]  # Corrected to uuid.UUID
    name: str
    time: Optional[int] = None
    ingredients: List[str] = []
    added_at: Optional[dt.datetime]  # Optional is correct here
    link: str = ''
    comments: list = []
    
    @validator('time')
    def convert_time(cls, value):
        return int(value)
    
    @validator('ingredients')
    def convert_ingredients(cls, value):
        if isinstance(value, str):
            parts = value.split(',')
        else:
            parts = value
        ingredients = [part.strip().capitalize() for part in parts]
        return ingredients
    
    def to_text(self):
        return str(
            [f"{k}: {v}" for k,v in self.__dict__.items()]
        )

class Comment(BaseModel):
    id: Optional[uuid.UUID]  # Corrected to uuid.UUID
    added_at: Optional[dt.datetime]
    content: str
    author: Optional[str]

