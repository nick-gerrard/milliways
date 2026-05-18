<script lang="ts">
    import RecipeCard from "$lib/components/RecipeCard.svelte";
    let { data } = $props();
</script>

<div class="w-full grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8 p-8">

    {#each data.recipes as recipe}
        <RecipeCard {recipe} />
    {/each}
</div>
