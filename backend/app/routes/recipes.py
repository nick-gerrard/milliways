from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import selectinload
from sqlmodel import Session, select

from ..database import get_session
from ..deps import get_current_user
from ..helpers import create_recipe_from_schema, get_or_create_tag
from ..models import Recipe, RecipeIngredient, RecipeStep, RecipeTag, Tag, User, UserRecipe
from ..schemas import RecipeCreate, RecipeUpdate

router = APIRouter(prefix="/recipes", tags=["recipes"])


@router.get("/")
def list_recipes(tag: str | None = None, session: Session = Depends(get_session)):
    query = select(Recipe).options(
        selectinload(Recipe.ingredients),
        selectinload(Recipe.steps),
        selectinload(Recipe.tags),
    )
    if tag:
        query = query.join(RecipeTag).join(Tag).where(Tag.name == tag.lower().strip())
    return session.exec(query).all()


@router.post("/")
def create_recipe(data: RecipeCreate, session: Session = Depends(get_session)):
    return create_recipe_from_schema(data, session)


@router.get("/{recipe_id}")
def get_recipe(recipe_id: int, session: Session = Depends(get_session)):
    recipe = session.exec(
        select(Recipe)
        .where(Recipe.id == recipe_id)
        .options(
            selectinload(Recipe.ingredients),
            selectinload(Recipe.steps),
            selectinload(Recipe.tags),
        )
    ).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe


@router.put("/{recipe_id}")
def update_recipe(
    recipe_id: int, data: RecipeUpdate, session: Session = Depends(get_session)
):
    recipe = session.get(Recipe, recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    for field, value in data.model_dump(exclude_unset=True, exclude={"ingredients", "steps", "tags"}).items():
        setattr(recipe, field, value)

    if data.ingredients is not None:
        session.exec(select(RecipeIngredient).where(RecipeIngredient.recipe_id == recipe_id)).all()
        for ri in session.exec(select(RecipeIngredient).where(RecipeIngredient.recipe_id == recipe_id)).all():
            session.delete(ri)
        from ..helpers import get_or_create_ingredient
        for item in data.ingredients:
            ingredient = get_or_create_ingredient(item.ingredient_name, session)
            session.add(RecipeIngredient(
                recipe_id=recipe_id, ingredient_id=ingredient.id,
                quantity=item.quantity, unit=item.unit, notes=item.notes,
            ))

    if data.steps is not None:
        for step in session.exec(select(RecipeStep).where(RecipeStep.recipe_id == recipe_id)).all():
            session.delete(step)
        for step in data.steps:
            session.add(RecipeStep(recipe_id=recipe_id, order=step.order, instruction=step.instruction))

    if data.tags is not None:
        for rt in session.exec(select(RecipeTag).where(RecipeTag.recipe_id == recipe_id)).all():
            session.delete(rt)
        for tag_name in data.tags:
            tag = get_or_create_tag(tag_name, session)
            session.add(RecipeTag(recipe_id=recipe_id, tag_id=tag.id))

    session.add(recipe)
    session.commit()
    session.refresh(recipe)
    return recipe


@router.delete("/{recipe_id}", status_code=204)
def delete_recipe(recipe_id: int, session: Session = Depends(get_session)):
    recipe = session.get(Recipe, recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    session.delete(recipe)
    session.commit()


@router.post("/{recipe_id}/save", status_code=204)
def save_recipe(
    recipe_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    if not session.get(Recipe, recipe_id):
        raise HTTPException(status_code=404, detail="Recipe not found")
    already_saved = session.exec(
        select(UserRecipe).where(
            UserRecipe.user_id == current_user.id,
            UserRecipe.recipe_id == recipe_id,
        )
    ).first()
    if not already_saved:
        session.add(UserRecipe(user_id=current_user.id, recipe_id=recipe_id))
        session.commit()


@router.delete("/{recipe_id}/save", status_code=204)
def unsave_recipe(
    recipe_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    saved = session.exec(
        select(UserRecipe).where(
            UserRecipe.user_id == current_user.id,
            UserRecipe.recipe_id == recipe_id,
        )
    ).first()
    if saved:
        session.delete(saved)
        session.commit()
