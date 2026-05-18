from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Relationship


class Ingredient(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str


class RecipeTag(SQLModel, table=True):
    recipe_id: int = Field(foreign_key="recipe.id", primary_key=True)
    tag_id: int = Field(foreign_key="tag.id", primary_key=True)


class RecipeIngredient(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    recipe_id: int = Field(foreign_key="recipe.id")
    ingredient_id: int = Field(foreign_key="ingredient.id")
    quantity: float
    unit: str
    notes: str | None = None
    recipe: "Recipe" = Relationship(back_populates="ingredients")


class RecipeStep(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    recipe_id: int = Field(foreign_key="recipe.id")
    order: int
    instruction: str
    recipe: "Recipe" = Relationship(back_populates="steps")


class Tag(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    recipes: list["Recipe"] = Relationship(back_populates="tags", link_model=RecipeTag)


class Recipe(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    description: str | None = None
    servings: int
    prep_time_minutes: int | None = None
    cook_time_minutes: int | None = None
    source_url: str | None = None
    author: str | None = None
    image_url: str | None = None
    ingredients: list[RecipeIngredient] = Relationship(back_populates="recipe")
    steps: list[RecipeStep] = Relationship(back_populates="recipe")
    tags: list[Tag] = Relationship(back_populates="recipes", link_model=RecipeTag)


class ParseJob(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    file_path: str
    status: str = "pending"
    error: str | None = None
    recipe_id: int | None = Field(default=None, foreign_key="recipe.id")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
