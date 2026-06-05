from sqlmodel import SQLModel
from datetime import datetime


class IngredientInput(SQLModel):
    ingredient_name: str
    quantity: float
    unit: str
    notes: str | None = None


class StepInput(SQLModel):
    order: int
    instruction: str


class RecipeCreate(SQLModel):
    name: str
    description: str | None = None
    servings: int
    prep_time_minutes: int | None = None
    cook_time_minutes: int | None = None
    source_url: str | None = None
    author: str | None = None
    image_url: str | None = None
    is_public: bool = False
    ingredients: list[IngredientInput] = []
    steps: list[StepInput] = []
    tags: list[str] = []


class RecipeUpdate(SQLModel):
    name: str | None = None
    description: str | None = None
    servings: int | None = None
    prep_time_minutes: int | None = None
    cook_time_minutes: int | None = None
    source_url: str | None = None
    author: str | None = None
    image_url: str | None = None
    is_public: bool | None = None
    ingredients: list[IngredientInput] | None = None
    steps: list[StepInput] | None = None
    tags: list[str] | None = None


class IngredientDetail(SQLModel):
    name: str


class RecipeIngredientDetail(SQLModel):
    id: int
    quantity: float
    unit: str
    notes: str | None
    ingredient: IngredientDetail


class RecipeStepDetail(SQLModel):
    id: int
    order: int
    instruction: str


class TagDetail(SQLModel):
    id: int
    name: str


class RecipeListItem(SQLModel):
    id: int
    name: str
    description: str | None
    servings: int
    prep_time_minutes: int | None
    cook_time_minutes: int | None
    image_url: str | None
    tags: list[TagDetail]


class RecipeDetail(SQLModel):
    id: int
    name: str
    description: str | None
    servings: int
    prep_time_minutes: int | None
    cook_time_minutes: int | None
    source_url: str | None
    author: str | None
    image_url: str | None
    is_public: bool
    created_at: datetime
    steps: list[RecipeStepDetail]
    tags: list[TagDetail]
    ingredients: list[RecipeIngredientDetail]


class ShoppingListRequest(SQLModel):
    recipe_ids: list[int]


class ShoppingListItem(SQLModel):
    ingredient_name: str
    quantity: float
    unit: str
