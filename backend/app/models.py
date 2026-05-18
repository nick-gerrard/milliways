from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Relationship


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    google_id: str = Field(unique=True)
    email: str = Field(unique=True)
    name: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    recipes: list["Recipe"] = Relationship(back_populates="created_by")


class Ingredient(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str


class RecipeTag(SQLModel, table=True):
    recipe_id: int = Field(foreign_key="recipe.id", primary_key=True)
    tag_id: int = Field(foreign_key="tag.id", primary_key=True)


class UserRecipe(SQLModel, table=True):
    user_id: int = Field(foreign_key="user.id", primary_key=True)
    recipe_id: int = Field(foreign_key="recipe.id", primary_key=True)
    saved_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class RecipeIngredient(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    recipe_id: int = Field(foreign_key="recipe.id")
    ingredient_id: int = Field(foreign_key="ingredient.id")
    quantity: float
    unit: str
    notes: str | None = None
    recipe: "Recipe" = Relationship(back_populates="ingredients")
    ingredient: "Ingredient" = Relationship()

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
    is_public: bool = Field(default=False)
    user_id: int | None = Field(default=None, foreign_key="user.id")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    created_by: User | None = Relationship(back_populates="recipes")
    ingredients: list[RecipeIngredient] = Relationship(back_populates="recipe")
    steps: list[RecipeStep] = Relationship(back_populates="recipe")
    tags: list[Tag] = Relationship(back_populates="recipes", link_model=RecipeTag)
    saved_by: list[User] = Relationship(link_model=UserRecipe)


class ParseJob(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    source_filename: str
    status: str = "pending"  # pending | processing | complete | failed
    error: str | None = None
    recipe_id: int | None = Field(default=None, foreign_key="recipe.id")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
