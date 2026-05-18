<script lang="ts">
    interface Recipe {
        id: number;
        name: string;
        description?: string;
        imageUrl?: string;
        tags?: string[]
        prep_time_minutes: number;
        cook_time_minutes: number;
    }
    let { recipe } = $props();

function formatMinutes(mins: number): string {
        const hours = Math.floor(mins/60)
        const minutes = mins % 60
        if (hours > 0) {
            return `${hours} hours, ${minutes} mins`
        } else {
            return `${minutes} mins`
        }
    }

</script>

<div
    class="border border-white/30 bg-white/10 backdrop-blur-md rounded-lg shadow-lg flex flex-col gap-4 p-8 hover:scale-105 transition-all duration-200ms"
>
    <h1 class="text-white text-3xl font-bold">{recipe.name}</h1>
    <p class="text-sm text-white">{recipe.description}</p>
    <div class="mt-8 flex justify-center gap-4">
        <p class="px-4 py-2 rounded-full bg-violet-800 text-white">Prep Time: {formatMinutes(recipe.prep_time_minutes)}</p>
        <p class="px-4 py-2 rounded-full bg-violet-800 text-white">Cook Time: {formatMinutes(recipe.cook_time_minutes)}</p>
        
    </div>
</div>
