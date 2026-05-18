<script lang="ts">
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { api } from '$lib/api';
	import type { Recipe } from '$lib/types';

	let recipe = $state<Recipe | null>(null);
	let loading = $state(true);
	let error = $state<string | null>(null);

	onMount(async () => {
		try {
			const id = parseInt($page.params.id ?? '');
			recipe = await api.recipes.get(id);
		} catch (e) {
			error = e instanceof Error ? e.message : 'Failed to load recipe';
		}
		loading = false;
	});
</script>

{#if loading}
	<p class="text-gray-400">Loading...</p>
{:else if error}
	<p class="text-red-500 text-sm">{error}</p>
{:else if recipe}
	<div class="flex flex-col gap-8">
		<!-- Header -->
		<header>
			<div class="flex items-start justify-between gap-4 mb-2">
				<h1 class="text-2xl font-bold leading-tight">{recipe.name}</h1>
				<a href="/recipes/{recipe.id}/edit" class="text-sm text-gray-400 hover:text-gray-700 mt-1 shrink-0">
					Edit
				</a>
			</div>

			{#if recipe.description}
				<p class="text-gray-500 mb-3">{recipe.description}</p>
			{/if}

			<div class="flex flex-wrap gap-4 text-sm text-gray-500 mb-3">
				{#if recipe.servings}
					<span>Serves {recipe.servings}</span>
				{/if}
				{#if recipe.prep_time_minutes}
					<span>Prep {recipe.prep_time_minutes}m</span>
				{/if}
				{#if recipe.cook_time_minutes}
					<span>Cook {recipe.cook_time_minutes}m</span>
				{/if}
				{#if recipe.author}
					<span>By {recipe.author}</span>
				{/if}
				{#if recipe.source_url}
					<a href={recipe.source_url} target="_blank" rel="noopener" class="underline">
						Source
					</a>
				{/if}
			</div>

			{#if recipe.tags.length > 0}
				<div class="flex flex-wrap gap-1.5">
					{#each recipe.tags as tag}
						<span class="text-xs px-2 py-0.5 bg-gray-100 text-gray-500 rounded-full">
							{tag.name}
						</span>
					{/each}
				</div>
			{/if}
		</header>

		<!-- Ingredients -->
		<section>
			<h2 class="text-lg font-semibold mb-3">Ingredients</h2>
			<ul class="flex flex-col gap-2">
				{#each recipe.ingredients as item}
					<li class="flex gap-3 text-sm">
						<span class="font-medium text-gray-900 w-24 shrink-0">
							{item.quantity} {item.unit}
						</span>
						{#if item.notes}
							<span class="text-gray-400">({item.notes})</span>
						{/if}
					</li>
				{/each}
			</ul>
		</section>

		<!-- Steps -->
		<section>
			<h2 class="text-lg font-semibold mb-3">Steps</h2>
			<ol class="flex flex-col gap-4">
				{#each recipe.steps.sort((a, b) => a.order - b.order) as step}
					<li class="flex gap-4 text-sm leading-relaxed">
						<span class="font-bold text-gray-300 w-5 shrink-0 pt-0.5">{step.order}</span>
						<span>{step.instruction}</span>
					</li>
				{/each}
			</ol>
		</section>
	</div>
{/if}
