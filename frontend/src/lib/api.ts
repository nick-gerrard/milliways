import { PUBLIC_API_URL } from '$env/static/public';
import type { Recipe, ShoppingListItem, Tag, User } from './types';

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
	const res = await fetch(`${PUBLIC_API_URL}${path}`, {
		credentials: 'include',
		headers: { 'Content-Type': 'application/json' },
		...options
	});
	if (!res.ok) {
		const text = await res.text();
		throw new Error(text || `${res.status} ${res.statusText}`);
	}
	if (res.status === 204) return undefined as T;
	return res.json();
}

export const api = {
	auth: {
		me: () => request<User>('/auth/me'),
		logout: () => request<void>('/auth/logout', { method: 'POST' }),
		loginUrl: `${PUBLIC_API_URL}/auth/google`
	},

	recipes: {
		list: (tag?: string) =>
			request<Recipe[]>(`/recipes${tag ? `?tag=${encodeURIComponent(tag)}` : ''}`),
		get: (id: number) => request<Recipe>(`/recipes/${id}`),
		create: (data: unknown) =>
			request<Recipe>('/recipes', { method: 'POST', body: JSON.stringify(data) }),
		update: (id: number, data: unknown) =>
			request<Recipe>(`/recipes/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
		delete: (id: number) => request<void>(`/recipes/${id}`, { method: 'DELETE' }),
		save: (id: number) => request<void>(`/recipes/${id}/save`, { method: 'POST' }),
		unsave: (id: number) => request<void>(`/recipes/${id}/save`, { method: 'DELETE' })
	},

	tags: {
		list: () => request<Tag[]>('/tags')
	},

	shopping: {
		build: (recipeIds: number[]) =>
			request<ShoppingListItem[]>('/shopping-list', {
				method: 'POST',
				body: JSON.stringify({ recipe_ids: recipeIds })
			})
	}
};
