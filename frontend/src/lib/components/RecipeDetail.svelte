<script lang="ts">
    import { fade } from "svelte/transition";
    import type { RecipeDetail, ShoppingItem, RecipeIngredient } from "$lib/types";
    import Button from "./Button.svelte";
    let { recipe }: { recipe: RecipeDetail } = $props();

    let toastVisible = $state(false);

    function addIngredients(list: Record<string, ShoppingItem>, ingredients: RecipeIngredient[]): Record<string, ShoppingItem> {
        for (const ing of ingredients) {
            const key = `${ing.unit}|${ing.ingredient.name}`;
            if (list[key]) {
                list[key].quantity += ing.quantity;
            } else {
                list[key] = {quantity: ing.quantity, name: ing.ingredient.name, unit: ing.unit};
            }
        }
        return list
    }

    function updateShoppingList() {
        const existing = JSON.parse(sessionStorage.getItem('shoppingList') ?? '{}');
        const updated = addIngredients(existing, recipe.ingredients);
        sessionStorage.setItem('shoppingList', JSON.stringify(updated));
        toastVisible = true;
        setTimeout(() => toastVisible = false, 2000);
    }

</script>

<div class="flex flex-col gap-4 text-white">
    <div class="flex items-start justify-between gap-4">
        <h1 class="text-2xl font-bold">{recipe.name}</h1>
        <div class="flex gap-2 shrink-0">
            <Button variant="ghost" href="/recipes/{recipe.id}/edit">Edit</Button>
            <Button variant="secondary" onclick={updateShoppingList}>+ Shopping List</Button>
        </div>
    </div>
    {#if recipe.description}
        <p class="text-sm text-white/70">{recipe.description}</p>
    {/if}

    <div class="flex flex-wrap gap-2">
        <span class="rounded-full bg-white/10 px-3 py-1 text-sm text-white">Serves {recipe.servings}</span>
        {#if recipe.prep_time_minutes}
            <span class="rounded-full bg-white/10 px-3 py-1 text-sm text-white">Prep: {recipe.prep_time_minutes} mins</span>
        {/if}
        {#if recipe.cook_time_minutes}
            <span class="rounded-full bg-white/10 px-3 py-1 text-sm text-white">Cook: {recipe.cook_time_minutes} mins</span>
        {/if}
    </div>

    {#if recipe.tags?.length}
        <div class="flex flex-wrap gap-2">
            {#each recipe.tags as tag}
                <span class="px-3 py-1 rounded-full bg-violet-600/40 text-sm text-white">{tag.name}</span>
            {/each}
        </div>
    {/if}
    <ul class="flex flex-col gap-1">
        {#each recipe.ingredients as ing}
        <li class="text-white italic">{ing.quantity} {ing.unit} {ing.ingredient.name}</li>
        {/each}
    </ul>
    <ol class="flex flex-col gap-2">
        {#each recipe.steps as step}
            <li class="flex gap-2">
                <span class="font-bold">{step.order}.</span>
                <span>{step.instruction}</span>
            </li>
        {/each}
    </ol>

    {#if recipe.author || recipe.source_url}
        <div class="mt-2 flex items-center gap-3 border-t border-white/10 pt-4 text-sm text-white/40">
            {#if recipe.author}<span>By {recipe.author}</span>{/if}
            {#if recipe.author && recipe.source_url}<span>·</span>{/if}
            {#if recipe.source_url}
                <a href={recipe.source_url} target="_blank" rel="noopener noreferrer" class="hover:text-white/70 underline">View original</a>
            {/if}
        </div>
    {/if}
</div>

{#if toastVisible}
    <div transition:fade={{ duration: 150 }} class="fixed bottom-6 right-6 rounded-full bg-violet-600 px-4 py-2 text-sm text-white shadow-lg">
        ✓ Added to shopping list
    </div>
{/if}
