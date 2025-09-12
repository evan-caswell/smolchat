from pydantic import BaseModel


class Recipe(BaseModel):
    recipe_name: str
    ingredients: list[str]


class Event(BaseModel):
    event_name: str
    event_date: str
    participants: list[str]
