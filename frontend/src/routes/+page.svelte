<script lang="ts">
	import { onMount } from 'svelte';
	import { api } from '$lib/api';
	import type { Recipe } from '$lib/types';

	let recipes = $state<Recipe[]>([]);
	let loading = $state(true);
	let error = $state<string | null>(null);

	onMount(async () => {
		try {
			recipes = await api.recipes.list();
		} catch (e) {
			error = e instanceof Error ? e.message : 'Failed to load recipes';
		}
		loading = false;
	});
</script>

<div class="flex items-center justify-between mb-6">
	<h1 class="text-2xl font-bold">Recipes</h1>
	<a href="/recipes/new" class="text-sm bg-gray-900 text-white px-3 py-1.5 rounded-md hover:bg-gray-700">
		+ New
	</a>
</div>

{#if loading}
	<p class="text-gray-400">Loading...</p>
{:else if error}
	<p class="text-red-500 text-sm">{error}</p>
{:else if recipes.length === 0}
	<p class="text-gray-500">No recipes yet. <a href="/recipes/new" class="underline">Add one.</a></p>
{:else}
	<ul class="flex flex-col gap-2">
		{#each recipes as recipe}
			<li>
				<a
					href="/recipes/{recipe.id}"
					class="flex items-center gap-3 px-4 py-3 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
				>
					<span class="font-medium flex-1">{recipe.name}</span>
					{#if recipe.prep_time_minutes || recipe.cook_time_minutes}
						<span class="text-xs text-gray-400 hidden sm:inline">
							{(recipe.prep_time_minutes ?? 0) + (recipe.cook_time_minutes ?? 0)}m
						</span>
					{/if}
					{#if recipe.tags.length > 0}
						<div class="flex gap-1.5">
							{#each recipe.tags as tag}
								<span class="text-xs px-2 py-0.5 bg-gray-100 text-gray-500 rounded-full">
									{tag.name}
								</span>
							{/each}
						</div>
					{/if}
					<svg class="w-4 h-4 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
					</svg>
				</a>
			</li>
		{/each}
	</ul>
{/if}
