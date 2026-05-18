from collections import defaultdict

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import selectinload
from sqlmodel import Session, select

from ..database import get_session
from ..models import Ingredient, Recipe, RecipeIngredient
from ..schemas import ShoppingListItem, ShoppingListRequest

router = APIRouter(prefix="/shopping-list", tags=["shopping"])


@router.post("/", response_model=list[ShoppingListItem])
def build_shopping_list(data: ShoppingListRequest, session: Session = Depends(get_session)):
    if not data.recipe_ids:
        return []

    recipe_ingredients = session.exec(
        select(RecipeIngredient)
        .where(RecipeIngredient.recipe_id.in_(data.recipe_ids))
    ).all()

    if len(recipe_ingredients) == 0:
        recipes = session.exec(select(Recipe).where(Recipe.id.in_(data.recipe_ids))).all()
        if len(recipes) != len(data.recipe_ids):
            raise HTTPException(status_code=404, detail="One or more recipes not found")

    # Aggregate by ingredient + unit, summing quantities
    totals: dict[tuple[int, str], float] = defaultdict(float)
    for ri in recipe_ingredients:
        totals[(ri.ingredient_id, ri.unit)] += ri.quantity

    ingredient_ids = {ingredient_id for ingredient_id, _ in totals}
    ingredients = {
        i.id: i for i in session.exec(
            select(Ingredient).where(Ingredient.id.in_(ingredient_ids))
        ).all()
    }

    return [
        ShoppingListItem(
            ingredient_name=ingredients[ingredient_id].name,
            quantity=quantity,
            unit=unit,
        )
        for (ingredient_id, unit), quantity in sorted(totals.items())
    ]
