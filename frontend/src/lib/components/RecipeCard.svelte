<script lang="ts">
    import type { Recipe } from "$lib/types";
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

<button
    onclick={onclick}
    class="shrink-0 overflow-hidden w-full text-left border border-white/30 bg-white/10 backdrop-blur-md rounded-lg shadow-lg flex flex-col gap-4 p-8 hover:scale-105 transition-all duration-200"
>
  <div class="h-2 -mx-8 -mt-8 bg-gradient-to-r from-fuchsia-400 via-green-400 to-violet-400"></div>
    <h1 class="text-white text-3xl font-bold">{recipe.name}</h1>
    <p class="text-sm text-white">{recipe.description}</p>
    <div class="mt-auto flex justify-center gap-4">
        <p class="px-4 py-2 rounded-full bg-white/10 backdrop-blur-md text-white">
            Prep: {formatMinutes(recipe.prep_time_minutes)}
        </p>
        <p class="px-4 py-2 rounded-full bg-white/10 backdrop-blur-md text-white">
            Cook: {formatMinutes(recipe.cook_time_minutes)}
        </p>
    </div>
</button>
