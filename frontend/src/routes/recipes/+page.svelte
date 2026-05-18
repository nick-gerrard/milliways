<script lang="ts">
    import RecipeCard from "$lib/components/RecipeCard.svelte";
    import type { Recipe } from "$lib/types";
    let { data } = $props();
    let searchTerm = $state("");

    let filteredRecipes = $derived(
        data.recipes.filter((r: Recipe) =>
            r.name.toLowerCase().includes(searchTerm.toLowerCase()),
        ),
    );
</script>

<div>
    <input
        class="rounded-lg shadow-lg border border-white/30 bg-white/10 p-2 text-white"
        bind:value={searchTerm}
        placeholder="Search for recipes..."
        type="text"
    />
</div>
<div class="w-full grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8 p-8">
    {#each filteredRecipes as recipe}
        <RecipeCard {recipe} />
    {/each}
</div>
