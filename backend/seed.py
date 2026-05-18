"""
Seed the database with test recipes. Run from the backend/ directory:
    PYTHONPATH=. uv run python seed.py
"""
from app.database import engine
from app.helpers import create_recipe_from_schema
from app.schemas import IngredientInput, RecipeCreate, StepInput
from sqlmodel import Session

RECIPES: list[RecipeCreate] = [
    RecipeCreate(
        name="TEST_Classic Margarita",
        description="A clean, balanced margarita. No mix, no nonsense.",
        servings=1,
        prep_time_minutes=5,
        tags=["cocktail"],
        ingredients=[
            IngredientInput(ingredient_name="tequila blanco", quantity=2, unit="oz"),
            IngredientInput(ingredient_name="triple sec", quantity=1, unit="oz"),
            IngredientInput(ingredient_name="fresh lime juice", quantity=1, unit="oz"),
            IngredientInput(ingredient_name="kosher salt", quantity=1, unit="pinch", notes="for the rim"),
        ],
        steps=[
            StepInput(order=1, instruction="Run a lime wedge around the rim of a rocks glass and dip in salt."),
            StepInput(order=2, instruction="Combine tequila, triple sec, and lime juice in a shaker with ice."),
            StepInput(order=3, instruction="Shake well for 15 seconds."),
            StepInput(order=4, instruction="Strain over fresh ice into the prepared glass."),
        ],
    ),
    RecipeCreate(
        name="TEST_Chocolate Chip Cookies",
        description="Classic chewy cookies with crisp edges.",
        servings=24,
        prep_time_minutes=15,
        cook_time_minutes=12,
        tags=["dessert", "vegetarian", "baking"],
        ingredients=[
            IngredientInput(ingredient_name="all-purpose flour", quantity=2.25, unit="cups"),
            IngredientInput(ingredient_name="unsalted butter", quantity=1, unit="cup", notes="softened"),
            IngredientInput(ingredient_name="granulated sugar", quantity=0.75, unit="cups"),
            IngredientInput(ingredient_name="brown sugar", quantity=0.75, unit="cups", notes="packed"),
            IngredientInput(ingredient_name="eggs", quantity=2, unit="large"),
            IngredientInput(ingredient_name="vanilla extract", quantity=2, unit="tsp"),
            IngredientInput(ingredient_name="baking soda", quantity=1, unit="tsp"),
            IngredientInput(ingredient_name="kosher salt", quantity=1, unit="tsp"),
            IngredientInput(ingredient_name="chocolate chips", quantity=2, unit="cups"),
        ],
        steps=[
            StepInput(order=1, instruction="Preheat oven to 375°F. Line baking sheets with parchment."),
            StepInput(order=2, instruction="Beat butter, granulated sugar, and brown sugar until light and fluffy, about 3 minutes."),
            StepInput(order=3, instruction="Add eggs and vanilla, beat until combined."),
            StepInput(order=4, instruction="Mix in flour, baking soda, and salt until just combined. Fold in chocolate chips."),
            StepInput(order=5, instruction="Drop rounded tablespoons onto prepared sheets, spacing 2 inches apart."),
            StepInput(order=6, instruction="Bake 9–12 minutes until golden at the edges. Cool on sheet for 5 minutes before transferring."),
        ],
    ),
    RecipeCreate(
        name="TEST_Spaghetti Carbonara",
        description="The real thing — no cream, just eggs, cheese, and pasta water.",
        servings=4,
        prep_time_minutes=10,
        cook_time_minutes=20,
        tags=["dinner", "italian", "pasta"],
        ingredients=[
            IngredientInput(ingredient_name="spaghetti", quantity=400, unit="g"),
            IngredientInput(ingredient_name="pancetta", quantity=200, unit="g", notes="or guanciale, diced"),
            IngredientInput(ingredient_name="eggs", quantity=4, unit="large"),
            IngredientInput(ingredient_name="parmesan", quantity=1, unit="cup", notes="finely grated, plus more to serve"),
            IngredientInput(ingredient_name="black pepper", quantity=2, unit="tsp", notes="freshly cracked"),
            IngredientInput(ingredient_name="kosher salt", quantity=1, unit="tbsp", notes="for pasta water"),
        ],
        steps=[
            StepInput(order=1, instruction="Bring a large pot of salted water to a boil. Cook spaghetti until just al dente, reserving 1 cup pasta water before draining."),
            StepInput(order=2, instruction="While pasta cooks, render pancetta in a large skillet over medium heat until crispy. Remove from heat."),
            StepInput(order=3, instruction="Whisk eggs and parmesan together in a bowl. Season generously with black pepper."),
            StepInput(order=4, instruction="Add drained pasta to the skillet with pancetta. Toss to coat in the fat."),
            StepInput(order=5, instruction="Off heat, pour egg mixture over pasta. Toss rapidly, adding pasta water a splash at a time until sauce is creamy and clings to the pasta. The residual heat cooks the eggs — do not put back on the burner or they will scramble."),
            StepInput(order=6, instruction="Serve immediately with extra parmesan and black pepper."),
        ],
    ),
]


if __name__ == "__main__":
    with Session(engine) as session:
        for recipe_data in RECIPES:
            recipe = create_recipe_from_schema(recipe_data, session)
            print(f"Created: {recipe.name} (id={recipe.id})")
    print("Done.")
