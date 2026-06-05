<script lang="ts">
    import { invalidateAll } from "$app/navigation";
    import { PUBLIC_API_URL } from "$env/static/public";
    import RecipeCard from "$lib/components/RecipeCard.svelte";
    import RecipeDetail from "$lib/components/RecipeDetail.svelte";
    import Button from "$lib/components/Button.svelte";
    import type { Recipe, RecipeDetail as RecipeDetailType } from "$lib/types";

    let { data } = $props();
    let searchTerm = $state("");
    let selectedRecipe = $state<RecipeDetailType | null>(null);
    let totalRecipes = data.recipes.length;
    let sort = $state<"az" | "za" | "newest">("az");

    function handleDelete() {
        selectedRecipe = null;
        invalidateAll();
    }

    let filteredRecipes = $derived.by(() => {
        const filtered = data.recipes.filter((r: Recipe) =>
            r.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
            r.tags?.some((tag: { name: string }) => tag.name.toLowerCase().includes(searchTerm.toLowerCase())),
        );
        if (sort === "az") return filtered.sort((a: Recipe, b: Recipe) => a.name.localeCompare(b.name));
        if (sort === "za") return filtered.sort((a: Recipe, b: Recipe) => b.name.localeCompare(a.name));
        return filtered.sort((a: Recipe, b: Recipe) => b.id - a.id);
    });

    async function selectRecipe(id: number) {
        const res = await fetch(`${PUBLIC_API_URL}/recipes/${id}`);
        selectedRecipe = await res.json();
    }
</script>

<div class="flex h-[calc(100vh-4rem)] overflow-hidden min-h-0">
    <div class="flex flex-col w-full lg:w-1/3 min-h-0">
        <div class="p-8 pb-4 border-b border-zinc-800/40 flex flex-col gap-3">
            <div class="flex items-center gap-3">
                <input
                    class="flex-1 rounded-lg shadow-lg border border-white/30 bg-white/10 p-2 text-white"
                    bind:value={searchTerm}
                    placeholder="Search from {totalRecipes} recipes..."
                    type="text"
                />
                <Button variant="primary" href="/recipes/add">+ Add</Button>
            </div>
            <div class="flex gap-2">
                {#each [["az", "A–Z"], ["za", "Z–A"], ["newest", "Newest"]] as [val, label]}
                    <button
                        onclick={() => sort = val as typeof sort}
                        class="rounded-full px-3 py-1 text-xs transition-colors {sort === val ? 'bg-violet-600 text-white' : 'bg-white/10 text-white/50 hover:text-white'}"
                    >{label}</button>
                {/each}
            </div>
        </div>
        <div class="p-8 w-full flex flex-col gap-8 overflow-y-auto min-h-0">
            {#each filteredRecipes as recipe}
                <RecipeCard {recipe} onclick={() => selectRecipe(recipe.id)} />
            {/each}
        </div>
    </div>

    {#if selectedRecipe}
        <div class="hidden lg:flex lg:flex-col lg:w-2/3 px-8 pt-8 pb-16 overflow-y-auto border-l border-white/20 min-h-0">
            <RecipeDetail recipe={selectedRecipe} ondelete={handleDelete} />
        </div>
    {/if}
  <div class="lg:hidden fixed bottom-0 left-0 right-0 h-4/5 z-50 bg-slate-900/95 backdrop-blur-md border-t border-white/20 rounded-t-2xl p-6 overflow-y-auto transition-transform duration-300"
    class:translate-y-full={!selectedRecipe}
    class:translate-y-0={!!selectedRecipe}>
      {#if selectedRecipe}
          <Button variant="ghost" onclick={() => selectedRecipe = null} class="mb-4 mt-4">✕ Close</Button>
          <RecipeDetail recipe={selectedRecipe} ondelete={handleDelete} />
      {/if}
  </div>
</div>
