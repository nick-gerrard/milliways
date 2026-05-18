export interface User {
	id: number;
	name: string;
	email: string;
	google_id: string;
	created_at: string;
}

export interface Tag {
	id: number;
	name: string;
}

export interface RecipeIngredient {
	id: number;
	ingredient_id: number;
	quantity: number;
	unit: string;
	notes: string | null;
}

export interface RecipeStep {
	id: number;
	order: number;
	instruction: string;
}

export interface Recipe {
	id: number;
	name: string;
	description: string | null;
	servings: number;
	prep_time_minutes: number | null;
	cook_time_minutes: number | null;
	source_url: string | null;
	author: string | null;
	image_url: string | null;
	is_public: boolean;
	created_at: string;
	ingredients: RecipeIngredient[];
	steps: RecipeStep[];
	tags: Tag[];
}

export interface ShoppingListItem {
	ingredient_name: string;
	quantity: number;
	unit: string;
}
