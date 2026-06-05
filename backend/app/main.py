from fastapi import FastAPI, Depends, HTTPException, Request, Header
from fastapi.responses import RedirectResponse
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.starlette_client import OAuth
from .database import get_session
from .models import Recipe, RecipeIngredient, RecipeStep, Tag, RecipeTag, Ingredient, User, UserRecipe
from .schemas import RecipeDetail, RecipeListItem, RecipeCreate, RecipeUpdate
from .config import FRONTEND_URL, SESSION_SECRET, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, CALLBACK_URL, UPLOAD_SECRET

app = FastAPI(title="Milliways API")

app.add_middleware(SessionMiddleware, secret_key=SESSION_SECRET)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth = OAuth()
oauth.register(
    name="google",
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/auth/login")
async def login(request: Request):
    return await oauth.google.authorize_redirect(request, CALLBACK_URL)


@app.get("/auth/callback")
async def auth_callback(request: Request, session: Session = Depends(get_session)):
    token = await oauth.google.authorize_access_token(request)
    userinfo = token["userinfo"]

    user = session.exec(select(User).where(User.google_id == userinfo["sub"])).first()
    if not user:
        user = User(
            google_id=userinfo["sub"],
            email=userinfo["email"],
            name=userinfo["name"],
        )
        session.add(user)
        session.commit()
        session.refresh(user)

    request.session["user_id"] = user.id
    return RedirectResponse(url=f"{FRONTEND_URL}/recipes")


@app.get("/auth/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url=f"{FRONTEND_URL}/")


@app.get("/auth/me")
def me(request: Request, session: Session = Depends(get_session)):
    user_id = request.session.get("user_id")
    if not user_id:
        return None
    return session.get(User, user_id)


@app.get("/recipes", response_model=list[RecipeListItem])
def get_recipes(session: Session = Depends(get_session)):
    statement = select(Recipe).order_by(Recipe.name).options(selectinload(Recipe.tags))
    return session.execute(statement).scalars().all()


@app.get("/recipes/ingredients/all")
def get_all_ingredients(request: Request, session: Session = Depends(get_session)):
    user_id = request.session.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Not Logged In")
    return session.exec(select(Ingredient)).all()


@app.get("/recipes/tags/all")
def get_all_tags(request: Request, session: Session = Depends(get_session)):
    user_id = request.session.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Not Logged In")
    return session.exec(select(Tag)).all()


@app.get("/recipes/{recipe_id}", response_model=RecipeDetail)
def get_recipe_details(recipe_id: int, session: Session = Depends(get_session)):
    statement = (
        select(Recipe)
        .where(Recipe.id == recipe_id)
        .options(
            selectinload(Recipe.steps),
            selectinload(Recipe.tags),
            selectinload(Recipe.ingredients).selectinload(RecipeIngredient.ingredient),
        )
    )
    recipe = session.exec(statement).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe

@app.patch("/recipes/{recipe_id}")
def edit_recipe_details(recipe_id: int, recipe: RecipeUpdate, request: Request, session: Session = Depends(get_session)):
    user_id = request.session.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Not Logged In")

    db_recipe = session.get(Recipe, recipe_id)
    if not db_recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    if db_recipe.user_id is not None and db_recipe.user_id != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")

    update_data = recipe.model_dump(exclude_unset=True, exclude={"ingredients", "steps", "tags"})
    for key, value in update_data.items():
        setattr(db_recipe, key, value)
    session.add(db_recipe)

    if recipe.ingredients is not None:
        for ri in session.exec(select(RecipeIngredient).where(RecipeIngredient.recipe_id == recipe_id)).all():
            session.delete(ri)
        session.flush()
        for ing in recipe.ingredients:
            ingredient = session.exec(select(Ingredient).where(Ingredient.name == ing.ingredient_name)).first()
            if not ingredient:
                ingredient = Ingredient(name=ing.ingredient_name)
                session.add(ingredient)
                session.flush()
            session.add(RecipeIngredient(
                recipe_id=recipe_id,
                ingredient_id=ingredient.id,
                quantity=ing.quantity,
                unit=ing.unit,
                notes=ing.notes,
            ))

    if recipe.steps is not None:
        for step in session.exec(select(RecipeStep).where(RecipeStep.recipe_id == recipe_id)).all():
            session.delete(step)
        session.flush()
        for step in recipe.steps:
            session.add(RecipeStep(recipe_id=recipe_id, order=step.order, instruction=step.instruction))

    if recipe.tags is not None:
        for rt in session.exec(select(RecipeTag).where(RecipeTag.recipe_id == recipe_id)).all():
            session.delete(rt)
        session.flush()
        for tag_name in recipe.tags:
            tag = session.exec(select(Tag).where(Tag.name == tag_name)).first()
            if not tag:
                tag = Tag(name=tag_name)
                session.add(tag)
                session.flush()
            session.add(RecipeTag(recipe_id=recipe_id, tag_id=tag.id))

    session.commit()
    return {"id": recipe_id}

@app.delete("/recipes/{recipe_id}")
def delete_recipe(recipe_id: int, request: Request, session: Session = Depends(get_session)):
    user_id = request.session.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Not Logged In")

    db_recipe = session.get(Recipe, recipe_id)
    if not db_recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    if db_recipe.user_id is not None and db_recipe.user_id != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")

    for ri in session.exec(select(RecipeIngredient).where(RecipeIngredient.recipe_id == recipe_id)).all():
        session.delete(ri)
    for step in session.exec(select(RecipeStep).where(RecipeStep.recipe_id == recipe_id)).all():
        session.delete(step)
    for rt in session.exec(select(RecipeTag).where(RecipeTag.recipe_id == recipe_id)).all():
        session.delete(rt)
    for ur in session.exec(select(UserRecipe).where(UserRecipe.recipe_id == recipe_id)).all():
        session.delete(ur)

    session.delete(db_recipe)
    session.commit()
    return {"ok": True}

@app.post("/recipes")
def add_recipe(recipe: RecipeCreate, request: Request, session: Session = Depends(get_session)):
    user_id = request.session.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Not Logged In")

    db_recipe = Recipe(
        name=recipe.name,
        description=recipe.description,
        servings=recipe.servings,
        prep_time_minutes=recipe.prep_time_minutes,
        cook_time_minutes=recipe.cook_time_minutes,
        source_url=recipe.source_url,
        author=recipe.author,
        image_url=recipe.image_url,
        is_public=recipe.is_public,
        user_id=user_id,
    )
    session.add(db_recipe)
    session.flush()

    for ing in recipe.ingredients:
        normalized_name = ing.ingredient_name.lower().strip()
        ingredient = session.exec(select(Ingredient).where(Ingredient.name == normalized_name)).first()
        if not ingredient:
            ingredient = Ingredient(name=normalized_name)
            session.add(ingredient)
            session.flush()
        session.add(RecipeIngredient(
            recipe_id=db_recipe.id,
            ingredient_id=ingredient.id,
            quantity=ing.quantity,
            unit=ing.unit,
            notes=ing.notes,
        ))

    for step in recipe.steps:
        session.add(RecipeStep(recipe_id=db_recipe.id, order=step.order, instruction=step.instruction))

    for tag_name in recipe.tags:
        normalized_tag = tag_name.lower().strip()
        tag = session.exec(select(Tag).where(Tag.name == normalized_tag)).first()
        if not tag:
            tag = Tag(name=normalized_tag)
            session.add(tag)
            session.flush()
        session.add(RecipeTag(recipe_id=db_recipe.id, tag_id=tag.id))

    session.commit()
    return {"id": db_recipe.id}

@app.post("/recipes/upload")
def accept_uploaded_recipe(recipe: RecipeCreate, authorization: str = Header(...), session: Session = Depends(get_session)):
    if authorization != f"Bearer {UPLOAD_SECRET}":
        raise HTTPException(status_code=401, detail="Unauthorized")

    db_recipe = Recipe(
        name=recipe.name,
        description=recipe.description,
        servings=recipe.servings,
        prep_time_minutes=recipe.prep_time_minutes,
        cook_time_minutes=recipe.cook_time_minutes,
        source_url=recipe.source_url,
        author=recipe.author,
        image_url=recipe.image_url,
        is_public=recipe.is_public,
    )
    session.add(db_recipe)
    session.flush()

    for ing in recipe.ingredients:
        normalized_name = ing.ingredient_name.lower().strip()
        ingredient = session.exec(select(Ingredient).where(Ingredient.name == normalized_name)).first()
        if not ingredient:
            ingredient = Ingredient(name=normalized_name)
            session.add(ingredient)
            session.flush()
        session.add(RecipeIngredient(
            recipe_id=db_recipe.id,
            ingredient_id=ingredient.id,
            quantity=ing.quantity,
            unit=ing.unit,
            notes=ing.notes,
        ))

    for step in recipe.steps:
        session.add(RecipeStep(recipe_id=db_recipe.id, order=step.order, instruction=step.instruction))

    for tag_name in recipe.tags:
        normalized_tag = tag_name.lower().strip()
        tag = session.exec(select(Tag).where(Tag.name == normalized_tag)).first()
        if not tag:
            tag = Tag(name=normalized_tag)
            session.add(tag)
            session.flush()
        session.add(RecipeTag(recipe_id=db_recipe.id, tag_id=tag.id))

    session.commit()
    return {"id": db_recipe.id}




