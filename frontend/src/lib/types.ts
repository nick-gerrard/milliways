export interface Recipe {
  id: number;
  name: string;
  description?: string;
  imageUrl?: string;
  tags?: string[];
  prep_time_minutes: number;
  cook_time_minutes: number;
}

export interface RecipeStep {
  id: number;
  order: number;
  instruction: string;
}

export interface RecipeIngredient {
  id: number;
  quantity: number;
  unit: string;
  notes?: string;
  ingredient: { name: string };
}

export interface RecipeDetail {
  id: number;
  name: string;
  description?: string;
  servings: number;
  prep_time_minutes?: number;
  cook_time_minutes?: number;
  source_url?: string;
  author?: string;
  image_url?: string;
  ingredients: RecipeIngredient[];
  steps: RecipeStep[];
  tags: { id: number; name: string }[];
}
