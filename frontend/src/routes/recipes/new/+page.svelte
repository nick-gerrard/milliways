<script lang="ts">
	import { api } from '$lib/api';
	import { goto } from '$app/navigation';

	let name = $state('');
	let description = $state('');
	let servings = $state(2);
	let submitting = $state(false);
	let error = $state<string | null>(null);

	async function submit(e: SubmitEvent) {
		e.preventDefault();
		submitting = true;
		error = null;
		try {
			const recipe = await api.recipes.create({ name, description, servings, ingredients: [], steps: [], tags: [] });
			goto(`/recipes/${recipe.id}`);
		} catch (e) {
			error = e instanceof Error ? e.message : 'Failed to create recipe';
			submitting = false;
		}
	}
</script>

<h1 class="text-2xl font-bold mb-1">New Recipe</h1>
<p class="text-sm text-gray-400 mb-6">Full ingredient and step entry coming soon.</p>

{#if error}
	<p class="text-red-500 text-sm mb-4">{error}</p>
{/if}

<form onsubmit={submit} class="flex flex-col gap-5 max-w-md">
	<label class="flex flex-col gap-1.5">
		<span class="text-sm font-medium">Name</span>
		<input
			type="text"
			bind:value={name}
			required
			placeholder="e.g. Classic Margarita"
			class="px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-gray-900"
		/>
	</label>

	<label class="flex flex-col gap-1.5">
		<span class="text-sm font-medium">Description</span>
		<textarea
			bind:value={description}
			placeholder="Optional short description"
			rows="3"
			class="px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-gray-900 resize-none"
		></textarea>
	</label>

	<label class="flex flex-col gap-1.5">
		<span class="text-sm font-medium">Servings</span>
		<input
			type="number"
			bind:value={servings}
			min="1"
			required
			class="px-3 py-2 border border-gray-300 rounded-md text-sm w-24 focus:outline-none focus:ring-2 focus:ring-gray-900"
		/>
	</label>

	<button
		type="submit"
		disabled={submitting}
		class="self-start px-4 py-2 bg-gray-900 text-white text-sm rounded-md hover:bg-gray-700 disabled:opacity-40 disabled:cursor-not-allowed"
	>
		{submitting ? 'Creating...' : 'Create Recipe'}
	</button>
</form>
