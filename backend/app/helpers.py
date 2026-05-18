from sqlmodel import Session, select
from .models import Ingredient, Tag, Recipe, RecipeIngredient, RecipeStep, RecipeTag
from .schemas import RecipeCreate


def get_or_create_ingredient(name: str, session: Session) -> Ingredient:
    ingredient = session.exec(
        select(Ingredient).where(Ingredient.name == name.lower().strip())
    ).first()
    if not ingredient:
        ingredient = Ingredient(name=name.lower().strip())
        session.add(ingredient)
        session.flush()
    return ingredient


def get_or_create_tag(name: str, session: Session) -> Tag:
    tag = session.exec(
        select(Tag).where(Tag.name == name.lower().strip())
    ).first()
    if not tag:
        tag = Tag(name=name.lower().strip())
        session.add(tag)
        session.flush()
    return tag


def create_recipe_from_schema(data: RecipeCreate, session: Session) -> Recipe:
    recipe = Recipe(
        name=data.name,
        description=data.description,
        servings=data.servings,
        prep_time_minutes=data.prep_time_minutes,
        cook_time_minutes=data.cook_time_minutes,
        source_url=data.source_url,
        author=data.author,
        image_url=data.image_url,
        is_public=data.is_public,
    )
    session.add(recipe)
    session.flush()

    for item in data.ingredients:
        ingredient = get_or_create_ingredient(item.ingredient_name, session)
        session.add(RecipeIngredient(
            recipe_id=recipe.id,
            ingredient_id=ingredient.id,
            quantity=item.quantity,
            unit=item.unit,
            notes=item.notes,
        ))

    for step in data.steps:
        session.add(RecipeStep(
            recipe_id=recipe.id,
            order=step.order,
            instruction=step.instruction,
        ))

    for tag_name in data.tags:
        tag = get_or_create_tag(tag_name, session)
        session.add(RecipeTag(recipe_id=recipe.id, tag_id=tag.id))

    session.commit()
    session.refresh(recipe)
    return recipe
