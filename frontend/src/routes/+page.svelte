<script lang="ts">
  import GlassCard from "$lib/components/GlassCard.svelte";
  let { data } = $props();
  const firstName = data.user.name.split(" ")[0];
</script>

<div class="flex min-h-[calc(100vh-4rem)] flex-col items-center justify-center gap-8 px-4">
  <div class="text-center">
    <h1 class="text-4xl font-bold text-white">Welcome back, {firstName}.</h1>
    <p class="mt-2 text-white/50">What are we cooking today?</p>
  </div>

  <div class="grid w-full max-w-2xl grid-cols-1 gap-4 sm:grid-cols-3">
    <a href="/recipes" class="group">
      <GlassCard class="h-full transition-transform duration-200 group-hover:scale-105">
        <p class="text-xs font-semibold uppercase tracking-widest text-white/40">Browse</p>
        <h2 class="mt-1 text-lg font-semibold text-white">Recipes</h2>
        <p class="mt-1 text-sm text-white/50">Your full collection</p>
      </GlassCard>
    </a>
    <a href="/recipes/add" class="group">
      <GlassCard accent class="h-full transition-transform duration-200 group-hover:scale-105">
        <p class="text-xs font-semibold uppercase tracking-widest text-white/40">New</p>
        <h2 class="mt-1 text-lg font-semibold text-white">Add Recipe</h2>
        <p class="mt-1 text-sm text-white/50">Save something new</p>
      </GlassCard>
    </a>
    <a href="/shop" class="group">
      <GlassCard class="h-full transition-transform duration-200 group-hover:scale-105">
        <p class="text-xs font-semibold uppercase tracking-widest text-white/40">Plan</p>
        <h2 class="mt-1 text-lg font-semibold text-white">Shopping List</h2>
        <p class="mt-1 text-sm text-white/50">Plan your shop</p>
      </GlassCard>
    </a>
  </div>
</div>
