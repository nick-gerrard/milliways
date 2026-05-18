<script lang="ts">
  import GlassCard from "$lib/components/GlassCard.svelte";
</script>

<div class="flex flex-col items-center justify-center m-auto">
  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 p-8">
    <GlassCard>
      <h1 class="text-3xl font-bold text-white">Add a Recipe</h1>
    </GlassCard>
    <GlassCard>
      <h1 class="text-3xl font-bold text-white">Create a Shopping List</h1>
    </GlassCard>
    <GlassCard>
      <h1 class="text-3xl font-bold text-white">Become Gordon Ramsay</h1>
    </GlassCard>
  </div>
</div>
