<script lang="ts">
  import type { Recipe } from "$lib/types";
  import GlassCard from "$lib/components/GlassCard.svelte";
  let { recipe, onclick } = $props();

  function formatMinutes(mins: number): string {
    const hours = Math.floor(mins / 60);
    const minutes = mins % 60;
    if (hours > 0) {
      return `${hours} hours, ${minutes} mins`;
    } else {
      return `${minutes} mins`;
    }
  }
</script>

<button {onclick} class="w-full text-left">
  <GlassCard accent class="w-full shrink-0 transition-all duration-200 hover:scale-105">
    <h1 class="text-3xl font-bold text-white">{recipe.name}</h1>
    {#if recipe.description}
      <p class="text-sm text-white">{recipe.description}</p>
    {/if}
    <div class="mt-auto flex justify-center gap-4">
      {#if recipe.prep_time_minutes}
        <p class="rounded-full bg-white/10 px-4 py-2 text-white backdrop-blur-md">
          Prep: {formatMinutes(recipe.prep_time_minutes)}
        </p>
      {/if}
      {#if recipe.cook_time_minutes}
        <p class="rounded-full bg-white/10 px-4 py-2 text-white backdrop-blur-md">
          Cook: {formatMinutes(recipe.cook_time_minutes)}
        </p>
      {/if}
    </div>
  </GlassCard>
</button>
