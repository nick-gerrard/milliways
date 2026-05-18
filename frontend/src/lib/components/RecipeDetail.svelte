<script lang="ts">
    import type { RecipeDetail } from "$lib/types";
    let { recipe }: { recipe: RecipeDetail } = $props();
</script>

<div class="flex flex-col gap-4 text-white">
    <h1 class="text-center text-3xl font-bold">{recipe.name}</h1>
    {#if recipe.description}
        <p class="text-sm text-center text-white/70">{recipe.description}</p>
    {/if}
    {#if recipe.tags}
        <div class="flex justify-between gap-2 lg:gap-8 mx-auto">
            {#each recipe.tags as tag}
                <span class="px-4 py-2 rounded-full bg-green-500 text-white border-green-600">{tag.name}</span>
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
</div>
