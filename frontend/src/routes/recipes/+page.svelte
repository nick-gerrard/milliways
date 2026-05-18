<script lang="ts">
    import { PUBLIC_API_URL } from "$env/static/public";
    import RecipeCard from "$lib/components/RecipeCard.svelte";
    import RecipeDetail from "$lib/components/RecipeDetail.svelte";
    import type { Recipe, RecipeDetail as RecipeDetailType } from "$lib/types";

    let { data } = $props();
    let searchTerm = $state("");
    let selectedRecipe = $state<RecipeDetailType | null>(null);

    let filteredRecipes = $derived(
        data.recipes.filter((r: Recipe) =>
            r.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
            r.tags?.some(tag => tag.name.toLowerCase().includes(searchTerm.toLowerCase())),
        ),
    );

    async function selectRecipe(id: number) {
        const res = await fetch(`${PUBLIC_API_URL}/recipes/${id}`);
        selectedRecipe = await res.json();
    }
</script>

<div class="flex h-screen overflow-hidden min-h-0">
    <div class="flex flex-col w-full lg:w-1/3">
        <div class="p-8 pb-0">
        <input
            class="w-full rounded-lg shadow-lg border border-white/30 bg-white/10 p-2 text-white"
            bind:value={searchTerm}
            placeholder="Search for recipes..."
            type="text"
        />

        </div>
        <div class="p-8 w-full flex flex-col gap-8 overflow-y-auto min-h-0">
            {#each filteredRecipes as recipe}
                <RecipeCard {recipe} onclick={() => selectRecipe(recipe.id)} />
            {/each}
        </div>
    </div>

    {#if selectedRecipe}
        <div class="hidden lg:block lg:w-2/3 p-8 overflow-y-auto border-l border-white/20">
            <RecipeDetail recipe={selectedRecipe} />
        </div>
    {/if}
  <div class="lg:hidden fixed bottom-0 left-0 right-0 h-4/5 z-50 bg-slate-900/95 backdrop-blur-md border-t border-white/20 rounded-t-2xl p-6 overflow-y-auto transition-transform duration-300"
    class:translate-y-full={!selectedRecipe}
    class:translate-y-0={!!selectedRecipe}>
      {#if selectedRecipe}
          <button onclick={() => selectedRecipe = null} class="mb-4 mt-4 text-white/50 text-xl">✕ Close</button>
          <RecipeDetail recipe={selectedRecipe} />
      {/if}
  </div>
</div>
