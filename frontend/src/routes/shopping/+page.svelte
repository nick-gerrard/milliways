<script lang="ts">
	import { onMount } from 'svelte';
	import { api } from '$lib/api';
	import type { Recipe, ShoppingListItem } from '$lib/types';

	let recipes = $state<Recipe[]>([]);
	let selected = $state<Set<number>>(new Set());
	let list = $state<ShoppingListItem[]>([]);
	let loading = $state(true);
	let building = $state(false);

	onMount(async () => {
		try {
			recipes = await api.recipes.list();
		} catch {}
		loading = false;
	});

	function toggle(id: number) {
		const next = new Set(selected);
		next.has(id) ? next.delete(id) : next.add(id);
		selected = next;
		list = [];
	}

	async function build() {
		if (selected.size === 0) return;
		building = true;
		try {
			list = await api.shopping.build([...selected]);
		} catch {}
		building = false;
	}
</script>

<h1 class="text-2xl font-bold mb-6">Shopping List</h1>

<div class="grid grid-cols-1 sm:grid-cols-2 gap-8 items-start">
	<section>
		<h2 class="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-3">Select recipes</h2>
		{#if loading}
			<p class="text-gray-400 text-sm">Loading...</p>
		{:else if recipes.length === 0}
			<p class="text-gray-400 text-sm">No recipes yet.</p>
		{:else}
			<ul class="flex flex-col gap-2 mb-4">
				{#each recipes as recipe}
					<li>
						<label class="flex items-center gap-3 cursor-pointer group">
							<input
								type="checkbox"
								checked={selected.has(recipe.id)}
								onchange={() => toggle(recipe.id)}
								class="w-4 h-4 rounded border-gray-300 accent-gray-900"
							/>
							<span class="text-sm group-hover:text-gray-600">{recipe.name}</span>
						</label>
					</li>
				{/each}
			</ul>
			<button
				onclick={build}
				disabled={selected.size === 0 || building}
				class="px-4 py-2 bg-gray-900 text-white text-sm rounded-md hover:bg-gray-700 disabled:opacity-40 disabled:cursor-not-allowed"
			>
				{building ? 'Building...' : `Build list${selected.size > 0 ? ` (${selected.size})` : ''}`}
			</button>
		{/if}
	</section>

	{#if list.length > 0}
		<section>
			<h2 class="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-3">You'll need</h2>
			<ul class="flex flex-col gap-2">
				{#each list as item}
					<li class="flex gap-3 text-sm">
						<span class="font-semibold text-gray-900 w-20 shrink-0">
							{item.quantity} {item.unit}
						</span>
						<span class="text-gray-700">{item.ingredient_name}</span>
					</li>
				{/each}
			</ul>
		</section>
	{/if}
</div>
